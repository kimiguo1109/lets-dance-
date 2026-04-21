from pathlib import Path
from textwrap import dedent

ROOT = Path('/home/ubuntu/lets-dance-mvp')

files = {
    'server/dance-data.ts': dedent('''
        export type ServerDanceGroup = {
          id: string;
          name: string;
          captainName: string;
          address: string;
          locationLabel: string;
          latitude: number;
          longitude: number;
          distanceMeters: number;
          memberCount: number;
          status: 'active' | 'sleeping';
          lastCheckInAt: string;
          createdAt: string;
          wechatLink?: string;
        };

        const now = new Date();
        const hoursAgo = (hours: number) => new Date(now.getTime() - hours * 60 * 60 * 1000).toISOString();
        const daysAgo = (days: number) => new Date(now.getTime() - days * 24 * 60 * 60 * 1000).toISOString();

        export const SEEDED_SERVER_GROUPS: ServerDanceGroup[] = [
          {
            id: 'group-binjiang',
            name: '滨江晚舞团',
            captainName: '张姐',
            address: '青年路地铁 B 口东侧空地',
            locationLabel: '青年路与滨江路交叉口广场',
            latitude: 31.2281,
            longitude: 121.4742,
            distanceMeters: 128,
            memberCount: 26,
            status: 'active',
            lastCheckInAt: hoursAgo(5),
            createdAt: daysAgo(20),
            wechatLink: 'https://weixin.qq.com/',
          },
          {
            id: 'group-metro',
            name: '地铁口晨练舞团',
            captainName: '李队',
            address: '和平公园南门健身广场',
            locationLabel: '和平路与中山路交叉口广场',
            latitude: 31.2298,
            longitude: 121.4711,
            distanceMeters: 186,
            memberCount: 18,
            status: 'active',
            lastCheckInAt: hoursAgo(12),
            createdAt: daysAgo(33),
            wechatLink: 'https://weixin.qq.com/',
          },
          {
            id: 'group-lotus',
            name: '莲花广场舞友会',
            captainName: '吴老师',
            address: '莲花路社区中心西侧空地',
            locationLabel: '莲花路社区中心广场',
            latitude: 31.2316,
            longitude: 121.4769,
            distanceMeters: 342,
            memberCount: 14,
            status: 'sleeping',
            lastCheckInAt: daysAgo(5),
            createdAt: daysAgo(49),
            wechatLink: 'https://weixin.qq.com/',
          },
        ];
    ''').strip() + '\n',
    'server/dance-memory.ts': dedent('''
        import { SEEDED_SERVER_GROUPS, type ServerDanceGroup } from './dance-data';

        let groups: ServerDanceGroup[] = [...SEEDED_SERVER_GROUPS];

        export function listMemoryGroups() {
          return [...groups].sort((a, b) => a.distanceMeters - b.distanceMeters);
        }

        export function getMemoryGroup(id: string) {
          return groups.find((group) => group.id === id);
        }

        export function createMemoryGroup(input: {
          captainName: string;
          address: string;
          locationLabel: string;
          latitude: number;
          longitude: number;
        }) {
          const createdAt = new Date().toISOString();
          const group: ServerDanceGroup = {
            id: `group-${Date.now()}`,
            name: `${input.locationLabel}舞团`,
            captainName: input.captainName,
            address: input.address,
            locationLabel: input.locationLabel,
            latitude: input.latitude,
            longitude: input.longitude,
            distanceMeters: 30,
            memberCount: 1,
            status: 'active',
            lastCheckInAt: createdAt,
            createdAt,
            wechatLink: 'https://weixin.qq.com/',
          };
          groups = [group, ...groups];
          return group;
        }

        export function joinMemoryGroup(id: string) {
          let updated: ServerDanceGroup | undefined;
          groups = groups.map((group) => {
            if (group.id !== id) return group;
            updated = {
              ...group,
              memberCount: group.memberCount + 1,
              lastCheckInAt: new Date().toISOString(),
              status: 'active',
            };
            return updated;
          });
          return updated;
        }

        export function wakeMemoryGroup(id: string) {
          let updated: ServerDanceGroup | undefined;
          groups = groups.map((group) => {
            if (group.id !== id) return group;
            updated = {
              ...group,
              status: 'active',
              lastCheckInAt: new Date().toISOString(),
            };
            return updated;
          });
          return updated;
        }
    ''').strip() + '\n',
    'server/routers.ts': dedent('''
        import { z } from 'zod';

        import { COOKIE_NAME } from '../shared/const.js';
        import { getSessionCookieOptions } from './_core/cookies';
        import { systemRouter } from './_core/systemRouter';
        import { publicProcedure, router } from './_core/trpc';
        import { createMemoryGroup, getMemoryGroup, joinMemoryGroup, listMemoryGroups, wakeMemoryGroup } from './dance-memory';

        export const appRouter = router({
          system: systemRouter,
          auth: router({
            me: publicProcedure.query((opts) => opts.ctx.user),
            logout: publicProcedure.mutation(({ ctx }) => {
              const cookieOptions = getSessionCookieOptions(ctx.req);
              ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
              return {
                success: true,
              } as const;
            }),
          }),
          dance: router({
            listNearby: publicProcedure
              .input(
                z
                  .object({
                    latitude: z.number().optional(),
                    longitude: z.number().optional(),
                    radiusMeters: z.number().min(50).max(5000).default(500),
                  })
                  .optional(),
              )
              .query(({ input }) => {
                const radiusMeters = input?.radiusMeters ?? 500;
                return listMemoryGroups().filter((group) => group.distanceMeters <= radiusMeters);
              }),
            detail: publicProcedure.input(z.object({ id: z.string().min(1) })).query(({ input }) => {
              return getMemoryGroup(input.id) ?? null;
            }),
            create: publicProcedure
              .input(
                z.object({
                  captainName: z.string().min(1),
                  address: z.string().min(1),
                  locationLabel: z.string().min(1),
                  latitude: z.number(),
                  longitude: z.number(),
                }),
              )
              .mutation(({ input }) => createMemoryGroup(input)),
            join: publicProcedure.input(z.object({ id: z.string().min(1) })).mutation(({ input }) => {
              return joinMemoryGroup(input.id) ?? null;
            }),
            wake: publicProcedure.input(z.object({ id: z.string().min(1) })).mutation(({ input }) => {
              return wakeMemoryGroup(input.id) ?? null;
            }),
          }),
        });

        export type AppRouter = typeof appRouter;
    ''').strip() + '\n',
}

for relative_path, content in files.items():
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print(f'Wrote {len(files)} backend files')

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

import { describe, expect, it } from 'vitest';

import type { TrpcContext } from '../server/_core/context';
import { appRouter } from '../server/routers';
import { buildMapUrl, createGroupName, formatDistance, getGroupStatus, searchGroups } from '../lib/dance-utils';
import { SEEDED_GROUPS } from '../lib/dance-data';
import { AppRoutes, getBackRoute } from '../lib/app-routes';

function createPublicContext(): TrpcContext {
  return {
    user: null,
    req: {
      protocol: 'https',
      headers: {},
    } as TrpcContext['req'],
    res: {
      clearCookie: () => undefined,
    } as unknown as TrpcContext['res'],
  };
}

describe('dance utils', () => {
  it('formats short and long distances in Chinese mobile-friendly text', () => {
    expect(formatDistance(128)).toBe('128 米');
    expect(formatDistance(1860)).toBe('1.9 公里');
  });

  it('creates a readable auto-generated group name', () => {
    expect(createGroupName('青年路与滨江路交叉口广场')).toBe('青年路与滨江路交叉口广场舞团');
  });

  it('marks groups as sleeping after 72 hours without check-in', () => {
    const recent = new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString();
    const old = new Date(Date.now() - 80 * 60 * 60 * 1000).toISOString();

    expect(getGroupStatus(recent)).toBe('active');
    expect(getGroupStatus(old)).toBe('sleeping');
  });

  it('supports fuzzy searching by name, captain, and address', () => {
    expect(searchGroups(SEEDED_GROUPS, '滨江')).toHaveLength(1);
    expect(searchGroups(SEEDED_GROUPS, '张姐')).toHaveLength(1);
    expect(searchGroups(SEEDED_GROUPS, '社区中心')).toHaveLength(1);
  });

  it('builds a valid map url for native navigation handoff', () => {
    const url = buildMapUrl({ latitude: 31.2281, longitude: 121.4742 }, '青年路广场');
    expect(url).toContain('maps.apple.com');
    expect(url).toContain('31.2281');
    expect(url).toContain('121.4742');
  });
});

describe('app routes', () => {
  it('builds typed group and share destinations with clear back targets', () => {
    expect(AppRoutes.group('group-1', 'groups')).toEqual({
      pathname: '/group/[id]',
      params: { id: 'group-1', from: 'groups' },
    });

    expect(AppRoutes.share('group-2', 'start')).toEqual({
      pathname: '/share-card',
      params: { groupId: 'group-2', from: 'start' },
    });

    expect(getBackRoute('voice')).toBe('/voice-search');
    expect(getBackRoute('groups')).toBe('/(tabs)/groups');
    expect(getBackRoute('unknown')).toBe('/(tabs)/groups');
  });
});

describe('dance router', () => {
  it('lists nearby groups within the requested radius', async () => {
    const caller = appRouter.createCaller(createPublicContext());
    const groups = await caller.dance.listNearby({ radiusMeters: 200 });

    expect(groups.length).toBeGreaterThan(0);
    expect(groups.every((group) => group.distanceMeters <= 200)).toBe(true);
  });

  it('creates, joins, and wakes a dance group through the public MVP API', async () => {
    const caller = appRouter.createCaller(createPublicContext());

    const created = await caller.dance.create({
      captainName: '王阿姨',
      address: '青年路与滨江路交叉口广场',
      locationLabel: '青年路与滨江路交叉口广场',
      latitude: 31.2286,
      longitude: 121.4737,
    });

    expect(created.name).toContain('舞团');
    expect(created.memberCount).toBe(1);

    const joined = await caller.dance.join({ id: created.id });
    expect(joined?.memberCount).toBe(2);

    const woken = await caller.dance.wake({ id: created.id });
    expect(woken?.status).toBe('active');

    const detail = await caller.dance.detail({ id: created.id });
    expect(detail?.id).toBe(created.id);
  });
});

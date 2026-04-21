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

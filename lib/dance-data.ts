import type { DanceGroup, UserProfile } from '@/lib/dance-types';

const now = new Date();
const hoursAgo = (hours: number) => new Date(now.getTime() - hours * 60 * 60 * 1000).toISOString();
const daysAgo = (days: number) => new Date(now.getTime() - days * 24 * 60 * 60 * 1000).toISOString();

export const DEFAULT_PROFILE: UserProfile = {
  id: 'local-user',
  nickname: '王阿姨',
  loginMethod: 'phone',
  updatedAt: now.toISOString(),
};

export const SEEDED_GROUPS: DanceGroup[] = [
  {
    id: 'group-binjiang',
    name: '滨江晚舞团',
    captainName: '张姐',
    address: '青年路地铁 B 口东侧空地',
    locationLabel: '青年路与滨江路交叉口广场',
    coordinates: { latitude: 31.2281, longitude: 121.4742 },
    distanceMeters: 128,
    memberCount: 26,
    members: [
      { id: 'm1', name: '张姐', joinedAt: daysAgo(15), isCaptain: true },
      { id: 'm2', name: '刘阿姨', joinedAt: daysAgo(10), isCaptain: false },
      { id: 'm3', name: '陈叔', joinedAt: daysAgo(6), isCaptain: false },
    ],
    status: 'active',
    lastCheckInAt: hoursAgo(5),
    createdAt: daysAgo(20),
    wechatLink: 'https://weixin.qq.com/',
    shareMessage: '我们在滨江晚舞团等你，一起跳舞更热闹。',
  },
  {
    id: 'group-metro',
    name: '地铁口晨练舞团',
    captainName: '李队',
    address: '和平公园南门健身广场',
    locationLabel: '和平路与中山路交叉口广场',
    coordinates: { latitude: 31.2298, longitude: 121.4711 },
    distanceMeters: 186,
    memberCount: 18,
    members: [
      { id: 'm4', name: '李队', joinedAt: daysAgo(28), isCaptain: true },
      { id: 'm5', name: '孙姨', joinedAt: daysAgo(11), isCaptain: false },
    ],
    status: 'active',
    lastCheckInAt: hoursAgo(12),
    createdAt: daysAgo(33),
    wechatLink: 'https://weixin.qq.com/',
    shareMessage: '地铁口晨练舞团欢迎你，到了就能开跳。',
  },
  {
    id: 'group-lotus',
    name: '莲花广场舞友会',
    captainName: '吴老师',
    address: '莲花路社区中心西侧空地',
    locationLabel: '莲花路社区中心广场',
    coordinates: { latitude: 31.2316, longitude: 121.4769 },
    distanceMeters: 342,
    memberCount: 14,
    members: [
      { id: 'm6', name: '吴老师', joinedAt: daysAgo(41), isCaptain: true },
    ],
    status: 'sleeping',
    lastCheckInAt: daysAgo(5),
    createdAt: daysAgo(49),
    wechatLink: 'https://weixin.qq.com/',
    shareMessage: '莲花广场舞友会等你来唤醒今晚的舞步。',
  },
];

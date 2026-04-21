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

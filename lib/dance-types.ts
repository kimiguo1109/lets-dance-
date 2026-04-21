export type AppLoginMethod = 'phone' | 'wechat' | 'douyin';
export type GroupStatus = 'active' | 'sleeping';

export interface UserProfile {
  id: string;
  nickname: string;
  avatarUri?: string;
  loginMethod: AppLoginMethod;
  updatedAt: string;
}

export interface Coordinates {
  latitude: number;
  longitude: number;
}

export interface GroupMember {
  id: string;
  name: string;
  joinedAt: string;
  isCaptain: boolean;
}

export interface DanceGroup {
  id: string;
  name: string;
  captainName: string;
  address: string;
  locationLabel: string;
  coordinates: Coordinates;
  distanceMeters: number;
  photoUri?: string;
  memberCount: number;
  members: GroupMember[];
  status: GroupStatus;
  lastCheckInAt: string;
  createdAt: string;
  wechatLink?: string;
  shareMessage: string;
}

export interface StartDancingResult {
  type: 'joined' | 'created';
  group: DanceGroup;
}

export interface VoiceSearchResult {
  transcript: string;
  matchedGroupIds: string[];
  directNavigationLabel?: string;
}

export interface AppStateShape {
  initialized: boolean;
  profile: UserProfile | null;
  groups: DanceGroup[];
  selectedGroupId: string | null;
  lastStartResult: StartDancingResult | null;
  lastVoiceResult: VoiceSearchResult | null;
}

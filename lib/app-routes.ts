import type { Href } from 'expo-router';

export type RouteSource = 'home' | 'groups' | 'messages' | 'me' | 'start' | 'voice';

export const AppRoutes = {
  home: '/(tabs)' as const,
  groups: '/(tabs)/groups' as const,
  messages: '/(tabs)/messages' as const,
  me: '/(tabs)/me' as const,
  start: '/start-dancing' as const,
  voice: '/voice-search' as const,
  group: (id: string, from: RouteSource = 'groups'): Href => ({
    pathname: '/group/[id]',
    params: { id, from },
  }),
  share: (groupId?: string, from: RouteSource = 'start'): Href => ({
    pathname: '/share-card',
    params: groupId ? { groupId, from } : { from },
  }),
} as const;

export function getBackRoute(from?: string) {
  switch (from) {
    case 'home':
      return AppRoutes.home;
    case 'messages':
      return AppRoutes.messages;
    case 'me':
      return AppRoutes.me;
    case 'voice':
      return AppRoutes.voice;
    case 'start':
      return AppRoutes.start;
    case 'groups':
    default:
      return AppRoutes.groups;
  }
}

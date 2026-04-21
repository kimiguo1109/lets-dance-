import type { Coordinates, DanceGroup, GroupStatus } from '@/lib/dance-types';

export function formatDistance(distanceMeters: number) {
  if (distanceMeters < 1000) return `${Math.round(distanceMeters)} 米`;
  return `${(distanceMeters / 1000).toFixed(1)} 公里`;
}

export function getGroupStatus(lastCheckInAt: string): GroupStatus {
  const hours = (Date.now() - new Date(lastCheckInAt).getTime()) / (1000 * 60 * 60);
  return hours > 72 ? 'sleeping' : 'active';
}

export function sortGroups(groups: DanceGroup[]) {
  return [...groups].sort((a, b) => a.distanceMeters - b.distanceMeters);
}

export function searchGroups(groups: DanceGroup[], keyword: string) {
  const normalized = keyword.trim().toLowerCase();
  if (!normalized) return sortGroups(groups);
  return sortGroups(
    groups.filter((group) =>
      [group.name, group.address, group.locationLabel, group.captainName]
        .join(' ')
        .toLowerCase()
        .includes(normalized),
    ),
  );
}

export function createGroupName(addressLabel: string) {
  return `${addressLabel}舞团`;
}

export function createShareMessage(group: DanceGroup) {
  return `${group.name}｜${group.locationLabel}｜当前 ${group.memberCount} 人，来一起跳舞吧。`;
}

export function buildMapUrl(
  coords: Coordinates,
  label: string,
  platformOS: 'ios' | 'android' | 'web' = 'ios',
) {
  const encoded = encodeURIComponent(label);
  if (platformOS === 'ios') {
    return `http://maps.apple.com/?ll=${coords.latitude},${coords.longitude}&q=${encoded}`;
  }
  return `https://uri.amap.com/navigation?to=${coords.longitude},${coords.latitude},${encoded}&mode=walk&src=lets-dance-mvp`;
}

export async function openNavigation(coords: Coordinates, label: string) {
  const [{ Platform }, Linking] = await Promise.all([import('react-native'), import('expo-linking')]);
  const url = buildMapUrl(
    coords,
    label,
    Platform.OS === 'ios' ? 'ios' : Platform.OS === 'android' ? 'android' : 'web',
  );
  await Linking.openURL(url);
}

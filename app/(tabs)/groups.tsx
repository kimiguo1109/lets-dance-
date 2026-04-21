import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';

import { ScreenContainer } from '@/components/screen-container';
import { useDanceApp } from '@/lib/dance-app-context';
import { formatDistance } from '@/lib/dance-utils';

export default function GroupsScreen() {
  const { visibleGroups } = useDanceApp();

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={styles.headerCard}>
          <Text style={styles.title}>附近舞团</Text>
          <Text style={styles.subtitle}>按距离从近到远排列，点一下就能查看详情。</Text>
        </View>

        <View style={styles.listWrap}>
          {visibleGroups.map((group) => (
            <Pressable key={group.id} onPress={() => router.push(`/group/${group.id}`)} style={({ pressed }) => [styles.groupCard, pressed && styles.pressed]}>
              <Text style={styles.groupName}>{group.name}</Text>
              <Text style={styles.groupMeta}>队长：{group.captainName}</Text>
              <Text style={styles.groupMeta}>{group.address}</Text>
              <View style={styles.bottomRow}>
                <Text style={styles.distance}>{formatDistance(group.distanceMeters)}</Text>
                <Text style={[styles.status, group.status === 'active' ? styles.active : styles.sleeping]}>{group.status === 'active' ? '活跃中' : '已休眠'}</Text>
              </View>
            </Pressable>
          ))}
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 14,
    paddingBottom: 144,
    gap: 18,
  },
  headerCard: {
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 22,
    paddingTop: 24,
    paddingBottom: 24,
    shadowColor: '#E9D8C7',
    shadowOpacity: 0.1,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 4 },
    elevation: 1,
  },
  title: {
    fontSize: 30,
    lineHeight: 36,
    fontWeight: '900',
    color: '#241F1A',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 19,
    lineHeight: 30,
    color: '#74685E',
  },
  listWrap: {
    gap: 14,
  },
  groupCard: {
    borderRadius: 28,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 22,
    paddingVertical: 22,
    shadowColor: '#D6451D',
    shadowOpacity: 0.06,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 6 },
    elevation: 2,
  },
  groupName: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
    marginBottom: 10,
  },
  groupMeta: {
    fontSize: 20,
    lineHeight: 30,
    color: '#5F564F',
  },
  bottomRow: {
    marginTop: 12,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  distance: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '800',
    color: '#D75A18',
  },
  status: {
    fontSize: 19,
    lineHeight: 24,
    fontWeight: '800',
  },
  active: {
    color: '#2E9E5B',
  },
  sleeping: {
    color: '#4EB7A5',
  },
  pressed: {
    opacity: 0.94,
    transform: [{ scale: 0.99 }],
  },
});

import { useEffect } from 'react';
import { router, useLocalSearchParams } from 'expo-router';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { Image } from 'expo-image';

import { Badge, PrimaryButton } from '@/components/dance-ui';
import { ScreenContainer } from '@/components/screen-container';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { AppRoutes, getBackRoute } from '@/lib/app-routes';
import { useDanceApp } from '@/lib/dance-app-context';
import { appHaptics } from '@/lib/haptics';
import { formatDistance, openNavigation } from '@/lib/dance-utils';

export default function GroupDetailScreen() {
  const params = useLocalSearchParams<{ id: string; from?: string }>();
  const { width } = useWindowDimensions();
  const { getGroupById, state, shareGroup, joinGroup, wakeGroup, setSelectedGroup } = useDanceApp();
  const group = getGroupById(params.id);
  const nickname = state.profile?.nickname ?? '舞友';
  const isCaptain = group?.captainName === nickname;
  const backRoute = getBackRoute(params.from);
  const imageHeight = Math.max(210, Math.min(290, width * 0.58));

  useEffect(() => {
    if (params.id) {
      setSelectedGroup(params.id);
    }
  }, [params.id, setSelectedGroup]);

  if (!group) {
    return (
      <ScreenContainer className="items-center justify-center px-6" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
        <Text style={styles.emptyTitle}>未找到舞团</Text>
        <Pressable onPress={() => router.replace(backRoute)} style={({ pressed }) => [styles.inlineBackButton, pressed && styles.pressed]}>
          <Text style={styles.inlineBackText}>返回上一页</Text>
        </Pressable>
      </ScreenContainer>
    );
  }

  const handleJoin = async () => {
    await joinGroup(group.id);
    Alert.alert('加入成功', `你已经加入 ${group.name}。`);
  };

  const handleNavigate = async () => {
    appHaptics.light();
    await openNavigation(group.coordinates, group.locationLabel);
  };

  const handleCaptainAction = async () => {
    if (isCaptain) {
      await wakeGroup(group.id);
      Alert.alert('舞团已唤醒', '舞团状态已更新为活跃。');
      return;
    }
    if (group.wechatLink) {
      router.push(AppRoutes.share(group.id, 'groups'));
    }
  };

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]" edges={['top', 'bottom', 'left', 'right']}>
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={styles.topBar}>
          <Pressable onPress={() => router.replace(backRoute)} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
            <IconSymbol name="chevron.right" size={28} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
          </Pressable>
          <Text style={styles.pageTitle}>舞团详情</Text>
          <Pressable onPress={() => router.replace(AppRoutes.groups)} style={({ pressed }) => [styles.sideButton, pressed && styles.pressed]}>
            <Text style={styles.sideButtonText}>舞队</Text>
          </Pressable>
        </View>

        {group.photoUri ? (
          <Image source={{ uri: group.photoUri }} style={{ width: '100%', height: imageHeight, borderRadius: 28 }} contentFit="cover" />
        ) : (
          <View style={[styles.placeholderImage, { height: imageHeight }]}> 
            <Text style={styles.placeholderText}>等待今晚的舞步照片</Text>
          </View>
        )}

        <View style={styles.card}>
          <Text style={styles.groupName}>{group.name}</Text>
          <Text style={styles.groupMeta}>队长：{group.captainName}｜当前 {group.memberCount} 人</Text>
          <Badge label={group.status === 'active' ? '活跃中' : '已休眠'} tone={group.status === 'active' ? 'active' : 'sleeping'} />
          <Text style={styles.address}>{group.address}</Text>
          <Text style={styles.distance}>距离你约 {formatDistance(group.distanceMeters)}</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.sectionTitle}>今晚安排</Text>
          <Text style={styles.infoText}>集合点：{group.locationLabel}</Text>
          <Text style={styles.infoText}>最近打卡：{new Date(group.lastCheckInAt).toLocaleString('zh-CN')}</Text>
          <Text style={styles.infoText}>分享话术：{group.shareMessage}</Text>
        </View>

        <View style={styles.actionWrap}>
          <PrimaryButton label="导航过去" icon="map.fill" onPress={handleNavigate} />
          <View style={styles.rowActions}>
            <View style={styles.flexOne}>
              <PrimaryButton label="发给好友" icon="arrow.triangle.turn.up.right.diamond.fill" tone="light" onPress={() => shareGroup(group.id)} />
            </View>
            <View style={styles.flexOne}>
              <PrimaryButton label={isCaptain ? '唤醒舞团' : '联系队长'} icon="phone.fill" tone="light" onPress={handleCaptainAction} />
            </View>
          </View>
          {!isCaptain ? <PrimaryButton label="加入舞团" icon="plus.circle.fill" tone="light" onPress={handleJoin} /> : null}
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 12,
    paddingBottom: 40,
    gap: 16,
  },
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingBottom: 6,
  },
  backButton: {
    width: 48,
    height: 48,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFFFFF',
  },
  sideButton: {
    minWidth: 56,
    height: 48,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFF8EF',
    paddingHorizontal: 12,
    borderWidth: 1,
    borderColor: '#EEDFCF',
  },
  sideButtonText: {
    fontSize: 16,
    lineHeight: 20,
    fontWeight: '800',
    color: '#241F1A',
  },
  pageTitle: {
    flex: 1,
    textAlign: 'center',
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
  },
  placeholderImage: {
    width: '100%',
    borderRadius: 28,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#EEDFCF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  placeholderText: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '800',
    color: '#7F756D',
  },
  card: {
    borderRadius: 28,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 20,
    gap: 10,
    borderWidth: 1,
    borderColor: '#EFE3D8',
  },
  groupName: {
    fontSize: 30,
    lineHeight: 36,
    fontWeight: '900',
    color: '#241F1A',
  },
  groupMeta: {
    fontSize: 18,
    lineHeight: 26,
    color: '#5F564F',
  },
  address: {
    fontSize: 18,
    lineHeight: 28,
    color: '#5F564F',
  },
  distance: {
    fontSize: 21,
    lineHeight: 26,
    fontWeight: '900',
    color: '#D75A18',
  },
  sectionTitle: {
    fontSize: 26,
    lineHeight: 32,
    fontWeight: '900',
    color: '#241F1A',
  },
  infoText: {
    fontSize: 18,
    lineHeight: 28,
    color: '#5F564F',
  },
  actionWrap: {
    gap: 12,
  },
  rowActions: {
    flexDirection: 'row',
    gap: 12,
  },
  flexOne: {
    flex: 1,
  },
  emptyTitle: {
    fontSize: 24,
    lineHeight: 30,
    fontWeight: '900',
    color: '#241F1A',
    marginBottom: 16,
  },
  inlineBackButton: {
    borderRadius: 22,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 14,
  },
  inlineBackText: {
    fontSize: 18,
    lineHeight: 24,
    fontWeight: '800',
    color: '#241F1A',
  },
  pressed: {
    opacity: 0.94,
    transform: [{ scale: 0.99 }],
  },
});

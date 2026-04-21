import { router, useLocalSearchParams } from 'expo-router';
import { Alert, ScrollView, Text, View } from 'react-native';
import { Image } from 'expo-image';

import { ScreenContainer } from '@/components/screen-container';
import { Badge, PrimaryButton, SectionTitle } from '@/components/dance-ui';
import { useDanceApp } from '@/lib/dance-app-context';
import { appHaptics } from '@/lib/haptics';
import { formatDistance, openNavigation } from '@/lib/dance-utils';

export default function GroupDetailScreen() {
  const params = useLocalSearchParams<{ id: string }>();
  const { getGroupById, state, shareGroup, joinGroup, wakeGroup } = useDanceApp();
  const group = getGroupById(params.id);
  const nickname = state.profile?.nickname ?? '舞友';
  const isCaptain = group?.captainName === nickname;

  if (!group) {
    return (
      <ScreenContainer className="items-center justify-center px-6">
        <Text className="text-[22px] font-bold text-foreground">未找到舞团</Text>
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
      appHaptics.light();
      router.push('/share-card');
    }
  };

  return (
    <ScreenContainer className="px-5 pb-6" edges={['top', 'bottom', 'left', 'right']}>
      <ScrollView contentContainerStyle={{ paddingBottom: 150, gap: 18 }} showsVerticalScrollIndicator={false}>
        {group.photoUri ? (
          <Image source={{ uri: group.photoUri }} style={{ width: '100%', height: 240, borderRadius: 28 }} contentFit="cover" />
        ) : (
          <View className="h-[240px] rounded-[28px] bg-surface items-center justify-center border border-border">
            <Text className="text-[22px] font-bold text-muted">等待今晚的舞步照片</Text>
          </View>
        )}
        <View className="gap-3 rounded-[30px] bg-surface px-5 py-6 border border-border">
          <SectionTitle title={group.name} subtitle={`队长：${group.captainName}｜当前 ${group.memberCount} 人`} />
          <Badge label={group.status === 'active' ? '活跃中' : '已休眠'} tone={group.status === 'active' ? 'active' : 'sleeping'} />
          <Text className="text-[18px] leading-7 text-muted">{group.address}</Text>
          <Text className="text-[18px] font-bold text-primary">距离你约 {formatDistance(group.distanceMeters)}</Text>
        </View>
        <View className="gap-3 rounded-[30px] bg-surface px-5 py-6 border border-border">
          <Text className="text-[22px] font-extrabold text-foreground">今晚安排</Text>
          <Text className="text-[18px] leading-7 text-muted">集合点：{group.locationLabel}</Text>
          <Text className="text-[18px] leading-7 text-muted">最近打卡：{new Date(group.lastCheckInAt).toLocaleString('zh-CN')}</Text>
          <Text className="text-[18px] leading-7 text-muted">分享话术：{group.shareMessage}</Text>
        </View>
      </ScrollView>
      <View className="absolute bottom-0 left-0 right-0 border-t border-border bg-background px-5 pb-6 pt-4">
        <View className="gap-3">
          <PrimaryButton label="导航过去" icon="map.fill" onPress={handleNavigate} />
          <View className="flex-row gap-3">
            <View className="flex-1">
              <PrimaryButton label="发给好友" icon="arrow.triangle.turn.up.right.diamond.fill" tone="light" onPress={() => shareGroup(group.id)} />
            </View>
            <View className="flex-1">
              <PrimaryButton label={isCaptain ? '唤醒舞团' : '联系队长'} icon="phone.fill" tone="light" onPress={handleCaptainAction} />
            </View>
          </View>
          {!isCaptain ? <PrimaryButton label="加入舞团" icon="plus.circle.fill" tone="light" onPress={handleJoin} /> : null}
        </View>
      </View>
    </ScreenContainer>
  );
}

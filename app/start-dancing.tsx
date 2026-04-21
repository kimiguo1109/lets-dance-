import { router } from 'expo-router';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { PrimaryButton } from '@/components/dance-ui';
import { ScreenContainer } from '@/components/screen-container';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { AppRoutes } from '@/lib/app-routes';
import { useDanceApp } from '@/lib/dance-app-context';
import { formatDistance } from '@/lib/dance-utils';

function StepRow({ index, label }: { index: number; label: string }) {
  return (
    <View style={styles.stepRow}>
      <View style={styles.stepBadge}>
        <Text style={styles.stepBadgeText}>{index}</Text>
      </View>
      <Text style={styles.stepText}>{label}</Text>
    </View>
  );
}

export default function StartDancingScreen() {
  const { nearbyGroups, startDancing, state } = useDanceApp();
  const result = state.lastStartResult;

  const handleStart = async (forceCreate = false) => {
    const nextResult = await startDancing({ createNew: forceCreate });
    if (!nextResult) return;
    Alert.alert(nextResult.type === 'created' ? '舞团创建成功' : '加入成功', `已进入 ${nextResult.group.name}`);
  };

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]" edges={['top', 'bottom', 'left', 'right']}>
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={styles.headerShell}>
          <View style={styles.topBar}>
            <Pressable onPress={() => router.replace(AppRoutes.home)} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
              <IconSymbol name="chevron.right" size={28} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
            </Pressable>
            <Text style={styles.pageTitle}>开始跳舞</Text>
            <Pressable onPress={() => router.push(AppRoutes.groups)} style={({ pressed }) => [styles.sideButton, pressed && styles.pressed]}>
              <Text style={styles.sideButtonText}>舞队</Text>
            </Pressable>
          </View>
        </View>

        <View style={styles.heroCard}>
          <Text style={styles.heroTitle}>四步完成</Text>
          <Text style={styles.heroSubtitle}>定位、拍照、判断附近舞团，再自动加入或创建，主路径保持尽量简单。</Text>
          <View style={styles.stepsWrap}>
            <StepRow index={1} label="获取当前位置" />
            <StepRow index={2} label="拍一张现场照片" />
            <StepRow index={3} label="优先加入 200 米内舞团" />
            <StepRow index={4} label="没有舞团时创建新舞团" />
          </View>
          <View style={styles.actionGap}>
            <PrimaryButton label="立即开始" icon="play.circle.fill" onPress={() => handleStart(false)} />
            <PrimaryButton label="直接创建新的舞团" icon="plus.circle.fill" tone="light" onPress={() => handleStart(true)} />
          </View>
        </View>

        <View style={styles.sectionCard}>
          <Text style={styles.sectionTitle}>附近可加入舞团</Text>
          <Text style={styles.sectionSubtitle}>如果你只想先看看，也可以点进去看详情。</Text>
          <View style={styles.groupList}>
            {nearbyGroups.slice(0, 3).map((group) => (
              <Pressable key={group.id} onPress={() => router.push(AppRoutes.group(group.id, 'start'))} style={({ pressed }) => [styles.groupRow, pressed && styles.pressed]}>
                <View style={styles.groupInfo}>
                  <Text style={styles.groupName}>{group.name}</Text>
                  <Text style={styles.groupMeta}>队长：{group.captainName}</Text>
                  <Text style={styles.groupMeta}>{group.address}</Text>
                  <Text style={styles.distance}>{formatDistance(group.distanceMeters)}</Text>
                </View>
                <View style={styles.groupRight}>
                  <Text style={[styles.groupStatus, group.status === 'active' ? styles.active : styles.sleeping]}>{group.status === 'active' ? '活跃中' : '已休眠'}</Text>
                  <Text style={styles.memberCount}>当前 {group.memberCount} 人</Text>
                </View>
              </Pressable>
            ))}
          </View>
        </View>

        {result ? (
          <View style={styles.resultCard}>
            <Text style={styles.resultTitle}>本次结果</Text>
            <Text style={styles.resultText}>你已{result.type === 'created' ? '创建' : '加入'}“{result.group.name}”。</Text>
            <View style={styles.actionGap}>
              <PrimaryButton label="查看舞团详情" icon="person.2.fill" onPress={() => router.push(AppRoutes.group(result.group.id, 'start'))} />
              <PrimaryButton label="分享卡片" icon="arrow.triangle.turn.up.right.diamond.fill" tone="light" onPress={() => router.push(AppRoutes.share(result.group.id, 'start'))} />
              <PrimaryButton label="回到首页" icon="house.fill" tone="light" onPress={() => router.replace(AppRoutes.home)} />
            </View>
          </View>
        ) : null}
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 4,
    paddingBottom: 40,
    gap: 18,
  },
  headerShell: {
    paddingTop: 10,
    paddingBottom: 8,
  },
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 24,
    backgroundColor: '#FFFDF9',
    borderWidth: 1,
    borderColor: '#EFE6DB',
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
    fontSize: 30,
    lineHeight: 36,
    fontWeight: '900',
    color: '#241F1A',
  },
  heroCard: {
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 22,
    gap: 16,
  },
  heroTitle: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
  },
  heroSubtitle: {
    fontSize: 18,
    lineHeight: 28,
    color: '#74685E',
  },
  stepsWrap: {
    gap: 12,
  },
  stepRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  stepBadge: {
    width: 34,
    height: 34,
    borderRadius: 17,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFEDD8',
  },
  stepBadgeText: {
    fontSize: 18,
    lineHeight: 22,
    fontWeight: '900',
    color: '#D75A18',
  },
  stepText: {
    flex: 1,
    fontSize: 20,
    lineHeight: 28,
    fontWeight: '800',
    color: '#D75A18',
  },
  actionGap: {
    gap: 12,
  },
  sectionCard: {
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 22,
    gap: 14,
  },
  sectionTitle: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
  },
  sectionSubtitle: {
    fontSize: 18,
    lineHeight: 28,
    color: '#74685E',
  },
  groupList: {
    gap: 14,
  },
  groupRow: {
    borderRadius: 24,
    backgroundColor: '#FFF8EF',
    borderWidth: 1,
    borderColor: '#EEDFCF',
    paddingHorizontal: 16,
    paddingVertical: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
  },
  groupInfo: {
    flex: 1,
  },
  groupRight: {
    alignItems: 'flex-end',
    gap: 10,
    paddingTop: 4,
  },
  groupName: {
    fontSize: 24,
    lineHeight: 30,
    fontWeight: '900',
    color: '#241F1A',
    marginBottom: 8,
  },
  groupMeta: {
    fontSize: 17,
    lineHeight: 24,
    color: '#5F564F',
  },
  distance: {
    marginTop: 10,
    fontSize: 20,
    lineHeight: 26,
    fontWeight: '900',
    color: '#D75A18',
  },
  groupStatus: {
    fontSize: 18,
    lineHeight: 22,
    fontWeight: '900',
  },
  active: {
    color: '#2E9E5B',
  },
  sleeping: {
    color: '#4EB7A5',
  },
  memberCount: {
    fontSize: 17,
    lineHeight: 22,
    fontWeight: '800',
    color: '#241F1A',
  },
  resultCard: {
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 22,
    gap: 10,
  },
  resultTitle: {
    fontSize: 26,
    lineHeight: 32,
    fontWeight: '900',
    color: '#241F1A',
  },
  resultText: {
    fontSize: 18,
    lineHeight: 28,
    color: '#5F564F',
  },
  pressed: {
    opacity: 0.94,
    transform: [{ scale: 0.99 }],
  },
});

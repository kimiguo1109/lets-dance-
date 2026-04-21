import { router } from 'expo-router';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { ScreenContainer } from '@/components/screen-container';
import { IconSymbol } from '@/components/ui/icon-symbol';
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
        <View style={styles.topBar}>
          <Pressable onPress={() => router.back()} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
            <IconSymbol name="chevron.right" size={30} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
          </Pressable>
          <Text style={styles.pageTitle}>开始跳舞</Text>
          <View style={styles.topPlaceholder} />
        </View>

        <View style={styles.heroCard}>
          <Text style={styles.heroSubtitle}>这条路径会依次完成定位、拍照、附近判断、创建或加入舞团。</Text>
          <View style={styles.stepsWrap}>
            <StepRow index={1} label="获取当前位置" />
            <StepRow index={2} label="拍一张现场照片" />
            <StepRow index={3} label="优先加入 200 米内舞团" />
            <StepRow index={4} label="没有舞团时创建新舞团" />
          </View>
          <Pressable onPress={() => handleStart(false)} style={({ pressed }) => [styles.primaryAction, pressed && styles.pressed]}>
            <IconSymbol name="play.circle.fill" size={34} color="#FFFFFF" />
            <Text style={styles.primaryActionText}>立即开始</Text>
          </Pressable>
          <Pressable onPress={() => handleStart(true)} style={({ pressed }) => [styles.secondaryAction, pressed && styles.pressed]}>
            <IconSymbol name="plus.circle.fill" size={30} color="#241F1A" />
            <Text style={styles.secondaryActionText}>附近有舞团也创建新的</Text>
          </Pressable>
        </View>

        <View style={styles.sectionCard}>
          <Text style={styles.sectionTitle}>附近可加入舞团</Text>
          <Text style={styles.sectionSubtitle}>如果你只想先看看，也可以直接进入详情。</Text>
          <View style={styles.groupList}>
            {nearbyGroups.slice(0, 2).map((group) => (
              <Pressable key={group.id} onPress={() => router.push(`/group/${group.id}`)} style={({ pressed }) => [styles.groupRow, pressed && styles.pressed]}>
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
            <View style={styles.resultActions}>
              <Pressable onPress={() => router.push(`/group/${result.group.id}`)} style={({ pressed }) => [styles.resultButton, pressed && styles.pressed]}>
                <Text style={styles.resultButtonText}>查看详情</Text>
              </Pressable>
              <Pressable onPress={() => router.push('/share-card')} style={({ pressed }) => [styles.resultButtonLight, pressed && styles.pressed]}>
                <Text style={styles.resultButtonLightText}>分享卡片</Text>
              </Pressable>
            </View>
          </View>
        ) : null}
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 10,
    paddingBottom: 40,
    gap: 18,
  },
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingBottom: 8,
  },
  backButton: {
    width: 52,
    height: 52,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFFFFF',
  },
  topPlaceholder: {
    width: 52,
    height: 52,
  },
  pageTitle: {
    flex: 1,
    textAlign: 'center',
    fontSize: 32,
    lineHeight: 38,
    fontWeight: '900',
    color: '#241F1A',
  },
  heroCard: {
    borderRadius: 32,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 22,
    paddingTop: 22,
    paddingBottom: 22,
    shadowColor: '#E9D8C7',
    shadowOpacity: 0.1,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 4 },
    elevation: 1,
  },
  heroSubtitle: {
    fontSize: 19,
    lineHeight: 30,
    color: '#74685E',
    marginBottom: 18,
  },
  stepsWrap: {
    gap: 14,
    marginBottom: 22,
  },
  stepRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 14,
  },
  stepBadge: {
    width: 38,
    height: 38,
    borderRadius: 19,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFEDD8',
  },
  stepBadgeText: {
    fontSize: 20,
    lineHeight: 24,
    fontWeight: '900',
    color: '#D75A18',
  },
  stepText: {
    flex: 1,
    fontSize: 22,
    lineHeight: 30,
    fontWeight: '800',
    color: '#D75A18',
  },
  primaryAction: {
    marginBottom: 14,
    minHeight: 68,
    borderRadius: 26,
    backgroundColor: '#D91E12',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
  primaryActionText: {
    fontSize: 24,
    lineHeight: 30,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  secondaryAction: {
    minHeight: 68,
    borderRadius: 26,
    backgroundColor: '#FFF8EF',
    borderWidth: 1,
    borderColor: '#F0E4D6',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
  secondaryActionText: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '900',
    color: '#241F1A',
  },
  sectionCard: {
    borderRadius: 32,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 22,
    paddingTop: 22,
    paddingBottom: 22,
  },
  sectionTitle: {
    fontSize: 30,
    lineHeight: 36,
    fontWeight: '900',
    color: '#241F1A',
  },
  sectionSubtitle: {
    marginTop: 8,
    fontSize: 19,
    lineHeight: 28,
    color: '#74685E',
  },
  groupList: {
    marginTop: 18,
    gap: 16,
  },
  groupRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: 16,
  },
  groupInfo: {
    flex: 1,
  },
  groupRight: {
    alignItems: 'flex-end',
    gap: 12,
    paddingTop: 4,
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
  distance: {
    marginTop: 10,
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '900',
    color: '#D75A18',
  },
  groupStatus: {
    fontSize: 19,
    lineHeight: 24,
    fontWeight: '900',
  },
  active: {
    color: '#2E9E5B',
  },
  sleeping: {
    color: '#4EB7A5',
  },
  memberCount: {
    fontSize: 20,
    lineHeight: 26,
    fontWeight: '800',
    color: '#241F1A',
  },
  resultCard: {
    borderRadius: 32,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 22,
    paddingTop: 22,
    paddingBottom: 22,
  },
  resultTitle: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
    marginBottom: 10,
  },
  resultText: {
    fontSize: 20,
    lineHeight: 30,
    color: '#5F564F',
  },
  resultActions: {
    marginTop: 18,
    gap: 12,
  },
  resultButton: {
    minHeight: 64,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#D91E12',
  },
  resultButtonText: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  resultButtonLight: {
    minHeight: 64,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#FFF8EF',
    borderWidth: 1,
    borderColor: '#F0E4D6',
  },
  resultButtonLightText: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '900',
    color: '#241F1A',
  },
  pressed: {
    opacity: 0.94,
    transform: [{ scale: 0.99 }],
  },
});

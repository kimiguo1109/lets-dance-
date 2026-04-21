import { router } from 'expo-router';
import { Alert, ScrollView, Text, View } from 'react-native';

import { ScreenContainer } from '@/components/screen-container';
import { Badge, GroupCard, PrimaryButton, SectionTitle } from '@/components/dance-ui';
import { useDanceApp } from '@/lib/dance-app-context';

export default function StartDancingScreen() {
  const { nearbyGroups, startDancing, state } = useDanceApp();
  const result = state.lastStartResult;

  const handleStart = async (forceCreate = false) => {
    const nextResult = await startDancing({ createNew: forceCreate });
    if (!nextResult) return;
    Alert.alert(nextResult.type === 'created' ? '舞团创建成功' : '加入成功', `已进入 ${nextResult.group.name}`);
  };

  return (
    <ScreenContainer className="px-5 pb-6" edges={['top', 'bottom', 'left', 'right']}>
      <ScrollView contentContainerStyle={{ paddingBottom: 24, gap: 18 }} showsVerticalScrollIndicator={false}>
        <View className="mt-2 rounded-[30px] bg-surface px-5 py-6 border border-border gap-4">
          <SectionTitle title="开始跳舞" subtitle="这条路径会依次完成定位、拍照、附近判断、创建或加入舞团。" />
          <View className="gap-3">
            <Badge label="步骤 1：获取当前位置" tone="warm" />
            <Badge label="步骤 2：拍一张现场照片" tone="warm" />
            <Badge label="步骤 3：优先加入 200 米内舞团" tone="warm" />
            <Badge label="步骤 4：没有舞团时创建新舞团" tone="warm" />
          </View>
          <PrimaryButton label="立即开始" icon="figure.dance" onPress={() => handleStart(false)} />
          <PrimaryButton label="附近有舞团也创建新的" icon="plus.circle.fill" tone="light" onPress={() => handleStart(true)} />
        </View>

        <View className="gap-4">
          <SectionTitle title="附近可加入舞团" subtitle="如果你只想先看看，也可以直接进入详情。" />
          {nearbyGroups.slice(0, 2).map((group) => (
            <GroupCard key={group.id} group={group} href={`/group/${group.id}`} />
          ))}
        </View>

        {result ? (
          <View className="rounded-[30px] bg-surface px-5 py-6 border border-border gap-3">
            <Text className="text-[24px] font-extrabold text-foreground">本次结果</Text>
            <Text className="text-[18px] leading-7 text-muted">你已{result.type === 'created' ? '创建' : '加入'}“{result.group.name}”。</Text>
            <View className="flex-row gap-3">
              <View className="flex-1">
                <PrimaryButton label="查看详情" icon="person.2.fill" tone="light" onPress={() => router.push(`/group/${result.group.id}`)} />
              </View>
              <View className="flex-1">
                <PrimaryButton label="分享卡片" icon="arrow.triangle.turn.up.right.diamond.fill" tone="light" onPress={() => router.push('/share-card')} />
              </View>
            </View>
          </View>
        ) : null}
      </ScrollView>
    </ScreenContainer>
  );
}

import { router } from 'expo-router';
import { ScrollView, Text, View } from 'react-native';

import { ScreenContainer } from '@/components/screen-container';
import { GroupCard, HeroCard, PrimaryButton, SectionTitle, TinyAction } from '@/components/dance-ui';
import { useDanceApp } from '@/lib/dance-app-context';

export default function HomeScreen() {
  const { state, nearbyGroups } = useDanceApp();
  const profileName = state.profile?.nickname ?? '舞友';
  const topGroup = nearbyGroups[0];

  return (
    <ScreenContainer className="px-5 pb-6">
      <ScrollView contentContainerStyle={{ paddingBottom: 24, gap: 22 }} showsVerticalScrollIndicator={false}>
        <View className="rounded-[32px] bg-surface px-5 py-6 border border-border gap-4 mt-2">
          <Text className="text-[18px] font-semibold text-muted">下午好，{profileName}</Text>
          <SectionTitle title="跳舞吧" subtitle="一键找人，一键开跳，一键导航到场。" />
          <View className="flex-row gap-3">
            <HeroCard title="附近活跃舞团" value={`${nearbyGroups.filter((item) => item.status === 'active').length}`} detail="200 米内优先推荐" />
            <HeroCard title="我的状态" value={state.lastStartResult ? '已加入' : '待出发'} detail={state.lastStartResult ? state.lastStartResult.group.name : '点击开始跳舞'} />
          </View>
        </View>

        <View className="items-center gap-4 py-2">
          <View className="w-full px-2">
            <PrimaryButton label="开始跳舞" icon="figure.dance" onPress={() => router.push('/start-dancing')} />
          </View>
          <Text className="text-[18px] leading-7 text-center text-muted">定位、拍照、判断附近舞团，完成后即可生成分享卡片。</Text>
        </View>

        <View className="flex-row gap-3">
          <TinyAction label="附近舞团" icon="person.2.fill" onPress={() => router.push('/(tabs)/groups')} />
          <TinyAction label="说话找地" icon="mic.fill" onPress={() => router.push('/voice-search')} />
        </View>

        {topGroup ? (
          <View className="gap-4">
            <SectionTitle title="离你最近" subtitle="先看看附近正在跳的舞团。" />
            <GroupCard group={topGroup} href={`/group/${topGroup.id}`} caption="支持直接导航、联系队长与发给好友。" />
          </View>
        ) : null}
      </ScrollView>
    </ScreenContainer>
  );
}

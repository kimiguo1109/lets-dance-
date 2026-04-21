import { router } from 'expo-router';
import { Modal, Pressable, Text, View } from 'react-native';

import { PrimaryButton } from '@/components/dance-ui';
import { useDanceApp } from '@/lib/dance-app-context';

export default function ShareCardScreen() {
  const { state, shareGroup } = useDanceApp();
  const group = state.lastStartResult?.group ?? state.groups[0];

  return (
    <Modal transparent animationType="slide">
      <View className="flex-1 justify-end bg-black/35 px-4 pb-6">
        <View className="rounded-[32px] bg-surface p-6 border border-border gap-5">
          <View className="gap-2">
            <Text className="text-[28px] font-extrabold text-foreground">分享卡片</Text>
            <Text className="text-[18px] leading-7 text-muted">把现场照片、舞团名称和当前人数发给微信好友。</Text>
          </View>
          <View className="rounded-[28px] bg-background px-5 py-6 gap-3">
            <Text className="text-[16px] font-semibold text-muted">跳舞吧邀请你</Text>
            <Text className="text-[28px] font-extrabold text-foreground">{group.name}</Text>
            <Text className="text-[18px] leading-7 text-muted">{group.locationLabel}</Text>
            <Text className="text-[20px] font-bold text-primary">当前 {group.memberCount} 人</Text>
            <Text className="text-[18px] leading-7 text-muted">{group.shareMessage}</Text>
          </View>
          <PrimaryButton label="发给好友" icon="arrow.triangle.turn.up.right.diamond.fill" onPress={() => shareGroup(group.id)} />
          <Pressable onPress={() => router.back()}>
            <Text className="text-center text-[18px] font-bold text-muted">稍后再说</Text>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
}

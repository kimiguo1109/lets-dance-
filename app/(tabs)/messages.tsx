import { ScrollView, Text, View } from 'react-native';

import { PrimaryButton, SectionTitle } from '@/components/dance-ui';
import { ScreenContainer } from '@/components/screen-container';

export default function MessagesScreen() {
  return (
    <ScreenContainer className="bg-[#FBF8F2] px-5" containerClassName="bg-[#FBF8F2]">
      <ScrollView contentContainerStyle={{ paddingBottom: 140, gap: 18 }} showsVerticalScrollIndicator={false}>
        <View className="mt-3 rounded-[30px] bg-white px-5 py-6">
          <SectionTitle title="消息" subtitle="这里保留最重要的提醒，避免信息太多。" />
        </View>
        <View className="rounded-[30px] bg-white px-5 py-6 gap-4">
          <Text className="text-[24px] font-extrabold text-foreground">当前 MVP 提醒</Text>
          <Text className="text-[20px] leading-8 text-muted">有人加入你的舞团、舞团休眠提醒、队长通知，后续都可以集中放在这里。</Text>
          <PrimaryButton label="稍后完善消息中心" icon="bell.fill" onPress={() => {}} tone="light" />
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

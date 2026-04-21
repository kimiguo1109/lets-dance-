import { useMemo, useState } from 'react';
import { Alert, ScrollView, Text, View } from 'react-native';

import { ScreenContainer } from '@/components/screen-container';
import { CardInput, GroupCard, PrimaryButton, SectionTitle } from '@/components/dance-ui';
import { useDanceApp } from '@/lib/dance-app-context';
import { appHaptics } from '@/lib/haptics';

const QUICK_PHRASES = ['青年路地铁口', '滨江晚舞团', '和平公园南门'];

export default function VoiceSearchScreen() {
  const { state, runVoiceSearch } = useDanceApp();
  const [transcript, setTranscript] = useState(state.lastVoiceResult?.transcript ?? '');

  const matchedGroups = useMemo(
    () => state.groups.filter((group) => state.lastVoiceResult?.matchedGroupIds.includes(group.id)),
    [state.groups, state.lastVoiceResult?.matchedGroupIds],
  );

  const handleSearch = async (value?: string) => {
    const next = (value ?? transcript).trim();
    if (!next) {
      Alert.alert('没听清', '请再说一次，或者直接输入地点。');
      return;
    }
    appHaptics.light();
    await runVoiceSearch(next);
    setTranscript(next);
  };

  return (
    <ScreenContainer className="px-5 pb-6" edges={['top', 'bottom', 'left', 'right']}>
      <ScrollView contentContainerStyle={{ paddingBottom: 24, gap: 18 }} showsVerticalScrollIndicator={false}>
        <View className="mt-2 rounded-[30px] bg-surface px-5 py-6 border border-border gap-4">
          <SectionTitle title="说话找地" subtitle="MVP 使用语音结果承接界面，你可以直接输入识别结果或点击常用短语模拟录音完成后的文本。" />
          <CardInput value={transcript} onChangeText={setTranscript} placeholder="例如：青年路地铁口东侧空地" />
          <PrimaryButton label="识别并搜索" icon="waveform" onPress={() => handleSearch()} />
          <View className="gap-3">
            <Text className="text-[18px] font-semibold text-muted">常用地点</Text>
            <View className="flex-row flex-wrap gap-3">
              {QUICK_PHRASES.map((item) => (
                <View key={item} className="w-full">
                  <PrimaryButton label={item} icon="mic.fill" tone="light" onPress={() => handleSearch(item)} />
                </View>
              ))}
            </View>
          </View>
        </View>

        <View className="gap-4">
          <SectionTitle title="搜索结果" subtitle="优先展示匹配舞团，没有匹配时提供直接导航提示。" />
          {matchedGroups.map((group) => (
            <GroupCard key={group.id} group={group} href={`/group/${group.id}`} />
          ))}
          {!matchedGroups.length && state.lastVoiceResult?.directNavigationLabel ? (
            <View className="rounded-[28px] bg-surface px-5 py-5 border border-border gap-3">
              <Text className="text-[22px] font-extrabold text-foreground">没有匹配舞团</Text>
              <Text className="text-[18px] leading-7 text-muted">可直接导航去“{state.lastVoiceResult.directNavigationLabel}”。</Text>
            </View>
          ) : null}
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

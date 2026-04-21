import { useMemo, useState } from 'react';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';

import { CardInput, GroupCard, PrimaryButton } from '@/components/dance-ui';
import { ScreenContainer } from '@/components/screen-container';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { AppRoutes } from '@/lib/app-routes';
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
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]" edges={['top', 'bottom', 'left', 'right']}>
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={styles.topBar}>
          <Pressable onPress={() => router.replace(AppRoutes.home)} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
            <IconSymbol name="chevron.right" size={28} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
          </Pressable>
          <Text style={styles.pageTitle}>说话找地</Text>
          <View style={styles.placeholder} />
        </View>

        <View style={styles.card}>
          <Text style={styles.title}>语音结果承接</Text>
          <Text style={styles.subtitle}>你可以直接输入识别出的地点，或者点常用短语快速模拟。</Text>
          <CardInput value={transcript} onChangeText={setTranscript} placeholder="例如：青年路地铁口东侧空地" />
          <PrimaryButton label="识别并搜索" icon="waveform" onPress={() => handleSearch()} />
          <View style={styles.quickWrap}>
            {QUICK_PHRASES.map((item) => (
              <PrimaryButton key={item} label={item} icon="mic.fill" tone="light" onPress={() => handleSearch(item)} />
            ))}
          </View>
        </View>

        <View style={styles.resultsWrap}>
          <Text style={styles.title}>搜索结果</Text>
          <Text style={styles.subtitle}>优先展示匹配舞团，没有匹配时给出直接导航提示。</Text>
          {matchedGroups.map((group) => (
            <GroupCard key={group.id} group={group} href={AppRoutes.group(group.id, 'voice')} />
          ))}
          {!matchedGroups.length && state.lastVoiceResult?.directNavigationLabel ? (
            <View style={styles.emptyCard}>
              <Text style={styles.emptyTitle}>没有匹配舞团</Text>
              <Text style={styles.emptyText}>可直接导航去“{state.lastVoiceResult.directNavigationLabel}”。</Text>
            </View>
          ) : null}
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
  placeholder: {
    width: 48,
    height: 48,
  },
  pageTitle: {
    flex: 1,
    textAlign: 'center',
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
  },
  card: {
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 22,
    gap: 12,
  },
  title: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
  },
  subtitle: {
    fontSize: 18,
    lineHeight: 28,
    color: '#74685E',
  },
  quickWrap: {
    gap: 10,
  },
  resultsWrap: {
    gap: 12,
  },
  emptyCard: {
    borderRadius: 28,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 20,
    borderWidth: 1,
    borderColor: '#EFE3D8',
  },
  emptyTitle: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '900',
    color: '#241F1A',
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 18,
    lineHeight: 28,
    color: '#5F564F',
  },
  pressed: {
    opacity: 0.94,
    transform: [{ scale: 0.99 }],
  },
});

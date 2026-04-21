import { router } from 'expo-router';
import { ScrollView, StyleSheet, Text, View } from 'react-native';

import { PrimaryButton, SectionTitle } from '@/components/dance-ui';
import { ScreenContainer } from '@/components/screen-container';
import { AppRoutes } from '@/lib/app-routes';
import { useDanceApp } from '@/lib/dance-app-context';

export default function MessagesScreen() {
  const { state } = useDanceApp();
  const recentGroup = state.lastStartResult?.group ?? state.groups[0];

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={styles.card}>
          <SectionTitle title="消息" subtitle="把最重要的提醒放在这里，方便老人直接看到下一步。" />
        </View>

        <View style={styles.noticeCard}>
          <Text style={styles.noticeTitle}>今晚提醒</Text>
          <Text style={styles.noticeText}>你最近查看的是“{recentGroup.name}”。如果现在就要出发，可以直接看详情或重新开始跳舞。</Text>
        </View>

        <View style={styles.actionsWrap}>
          <PrimaryButton label="查看最近舞团" icon="person.2.fill" onPress={() => router.push(AppRoutes.group(recentGroup.id, 'messages'))} />
          <PrimaryButton label="重新开始跳舞" icon="play.circle.fill" tone="light" onPress={() => router.push(AppRoutes.start)} />
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 16,
    paddingBottom: 156,
    gap: 16,
  },
  card: {
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 22,
  },
  noticeCard: {
    borderRadius: 28,
    backgroundColor: '#FFF8EF',
    borderWidth: 1,
    borderColor: '#EEDFCF',
    paddingHorizontal: 20,
    paddingVertical: 22,
    gap: 10,
  },
  noticeTitle: {
    fontSize: 26,
    lineHeight: 32,
    fontWeight: '900',
    color: '#241F1A',
  },
  noticeText: {
    fontSize: 19,
    lineHeight: 29,
    color: '#5F564F',
  },
  actionsWrap: {
    gap: 12,
  },
});

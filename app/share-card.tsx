import { router, useLocalSearchParams } from 'expo-router';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { PrimaryButton } from '@/components/dance-ui';
import { AppRoutes, getBackRoute } from '@/lib/app-routes';
import { useDanceApp } from '@/lib/dance-app-context';

export default function ShareCardScreen() {
  const params = useLocalSearchParams<{ groupId?: string; from?: string }>();
  const { state, shareGroup, getGroupById } = useDanceApp();
  const group = getGroupById(params.groupId) ?? state.lastStartResult?.group ?? state.groups[0];
  const backRoute = params.from === 'start' ? AppRoutes.start : getBackRoute(params.from);

  return (
    <View style={styles.overlay}>
      <View style={styles.sheet}>
        <View style={styles.titleWrap}>
          <Text style={styles.title}>分享卡片</Text>
          <Text style={styles.subtitle}>把现场照片、舞团名称和当前人数发给微信好友。</Text>
        </View>
        <View style={styles.card}>
          <Text style={styles.kicker}>跳舞吧邀请你</Text>
          <Text style={styles.groupName}>{group.name}</Text>
          <Text style={styles.meta}>{group.locationLabel}</Text>
          <Text style={styles.count}>当前 {group.memberCount} 人</Text>
          <Text style={styles.meta}>{group.shareMessage}</Text>
        </View>
        <View style={styles.actions}>
          <PrimaryButton label="发给好友" icon="arrow.triangle.turn.up.right.diamond.fill" onPress={() => shareGroup(group.id)} />
          <Pressable onPress={() => router.replace(backRoute)} style={({ pressed }) => [styles.backTextWrap, pressed && styles.pressed]}>
            <Text style={styles.backText}>返回上一页</Text>
          </Pressable>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    justifyContent: 'flex-end',
    backgroundColor: 'rgba(0,0,0,0.35)',
    paddingHorizontal: 16,
    paddingBottom: 16,
  },
  sheet: {
    borderRadius: 30,
    backgroundColor: '#FFF9F3',
    paddingHorizontal: 20,
    paddingTop: 20,
    paddingBottom: 24,
    gap: 16,
  },
  titleWrap: {
    gap: 8,
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
  card: {
    borderRadius: 26,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 18,
    paddingVertical: 20,
    gap: 10,
    borderWidth: 1,
    borderColor: '#EFE3D8',
  },
  kicker: {
    fontSize: 16,
    lineHeight: 20,
    fontWeight: '700',
    color: '#8A7C72',
  },
  groupName: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
  },
  meta: {
    fontSize: 18,
    lineHeight: 28,
    color: '#5F564F',
  },
  count: {
    fontSize: 20,
    lineHeight: 26,
    fontWeight: '900',
    color: '#D75A18',
  },
  actions: {
    gap: 12,
  },
  backTextWrap: {
    paddingVertical: 6,
  },
  backText: {
    textAlign: 'center',
    fontSize: 18,
    lineHeight: 24,
    fontWeight: '800',
    color: '#6B625B',
  },
  pressed: {
    opacity: 0.94,
    transform: [{ scale: 0.99 }],
  },
});

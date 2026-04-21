import { useState } from 'react';
import { Alert, Pressable, ScrollView, StyleSheet, Text, TextInput, View } from 'react-native';

import { ScreenContainer } from '@/components/screen-container';
import { ProfileAvatar } from '@/components/dance-ui';
import { useDanceApp } from '@/lib/dance-app-context';
import { IconSymbol } from '@/components/ui/icon-symbol';

export default function MeScreen() {
  const { state, pickAvatar, updateProfile } = useDanceApp();
  const [nickname, setNickname] = useState(state.profile?.nickname ?? '');
  const [avatarUri, setAvatarUri] = useState(state.profile?.avatarUri);

  const handleAvatar = async () => {
    const uri = await pickAvatar();
    if (uri) setAvatarUri(uri);
  };

  const handleSave = async () => {
    await updateProfile({
      nickname,
      avatarUri,
      loginMethod: state.profile?.loginMethod ?? 'phone',
    });
    Alert.alert('已保存', '你的资料已经更新。');
  };

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={styles.card}>
          <Text style={styles.title}>我的</Text>
          <Text style={styles.subtitle}>只保留常用设置，头像、昵称和登录方式一眼能看清。</Text>

          <View style={styles.avatarSection}>
            <ProfileAvatar uri={avatarUri} fallback={nickname || '舞'} />
            <Pressable onPress={handleAvatar} style={({ pressed }) => [styles.pickButton, pressed && styles.pressed]}>
              <IconSymbol name="camera.fill" size={24} color="#FFFFFF" />
              <Text style={styles.pickButtonText}>换头像</Text>
            </Pressable>
          </View>

          <View style={styles.fieldWrap}>
            <Text style={styles.fieldLabel}>昵称</Text>
            <TextInput
              value={nickname}
              onChangeText={setNickname}
              placeholder="请输入你的称呼"
              placeholderTextColor="#9C8D84"
              style={styles.input}
              returnKeyType="done"
            />
          </View>

          <View style={styles.infoCard}>
            <Text style={styles.infoTitle}>当前登录方式</Text>
            <Text style={styles.infoValue}>
              {state.profile?.loginMethod === 'wechat'
                ? '微信登录'
                : state.profile?.loginMethod === 'douyin'
                  ? '抖音登录'
                  : '手机号登录'}
            </Text>
          </View>

          <Pressable onPress={handleSave} style={({ pressed }) => [styles.saveButton, pressed && styles.pressed]}>
            <Text style={styles.saveButtonText}>保存资料</Text>
          </Pressable>
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingTop: 16,
    paddingBottom: 156,
  },
  card: {
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 20,
    paddingVertical: 22,
  },
  title: {
    fontSize: 30,
    lineHeight: 36,
    fontWeight: '900',
    color: '#241F1A',
  },
  subtitle: {
    marginTop: 8,
    fontSize: 19,
    lineHeight: 28,
    color: '#74685E',
  },
  avatarSection: {
    alignItems: 'center',
    paddingVertical: 26,
    gap: 16,
  },
  pickButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    paddingHorizontal: 22,
    paddingVertical: 15,
    borderRadius: 22,
    backgroundColor: '#FF7A12',
  },
  pickButtonText: {
    fontSize: 21,
    lineHeight: 27,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  fieldWrap: {
    gap: 10,
    marginBottom: 18,
  },
  fieldLabel: {
    fontSize: 21,
    lineHeight: 28,
    fontWeight: '800',
    color: '#241F1A',
  },
  input: {
    borderRadius: 22,
    backgroundColor: '#F6F1EA',
    paddingHorizontal: 18,
    paddingVertical: 16,
    fontSize: 20,
    lineHeight: 26,
    fontWeight: '700',
    color: '#241F1A',
  },
  infoCard: {
    borderRadius: 24,
    backgroundColor: '#FBF8F2',
    paddingHorizontal: 18,
    paddingVertical: 18,
    marginBottom: 20,
  },
  infoTitle: {
    fontSize: 20,
    lineHeight: 26,
    fontWeight: '800',
    color: '#241F1A',
    marginBottom: 8,
  },
  infoValue: {
    fontSize: 20,
    lineHeight: 26,
    color: '#74685E',
  },
  saveButton: {
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 24,
    backgroundColor: '#D91E12',
    paddingVertical: 17,
  },
  saveButtonText: {
    fontSize: 22,
    lineHeight: 28,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  pressed: {
    opacity: 0.93,
    transform: [{ scale: 0.985 }],
  },
});

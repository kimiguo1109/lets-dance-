import { useState } from 'react';
import { Alert, ScrollView, Text, View } from 'react-native';

import { ScreenContainer } from '@/components/screen-container';
import { CardInput, PrimaryButton, ProfileAvatar, SectionTitle } from '@/components/dance-ui';
import { useDanceApp } from '@/lib/dance-app-context';

export default function MeScreen() {
  const { state, pickAvatar, updateProfile } = useDanceApp();
  const [nickname, setNickname] = useState(state.profile?.nickname ?? '');
  const [avatarUri, setAvatarUri] = useState(state.profile?.avatarUri);

  const handleAvatar = async () => {
    const uri = await pickAvatar();
    if (uri) {
      setAvatarUri(uri);
    }
  };

  const handleSave = async () => {
    await updateProfile({
      nickname,
      avatarUri,
      loginMethod: state.profile?.loginMethod ?? 'phone',
    });
    Alert.alert('资料已更新', '你的头像和昵称已经保存。');
  };

  return (
    <ScreenContainer className="px-5 pb-6">
      <ScrollView contentContainerStyle={{ paddingBottom: 24, gap: 20 }} showsVerticalScrollIndicator={false}>
        <View className="mt-2 rounded-[32px] bg-surface px-5 py-6 border border-border gap-5">
          <SectionTitle title="我的资料" subtitle="MVP 阶段支持头像与昵称设置，保持操作尽量简单。" />
          <View className="items-center gap-4">
            <ProfileAvatar uri={avatarUri} fallback={nickname || '舞'} />
            <View className="w-full">
              <PrimaryButton label="从相册选择头像" icon="camera.fill" tone="light" onPress={handleAvatar} />
            </View>
          </View>
          <View className="gap-3">
            <Text className="text-[18px] font-semibold text-muted">昵称</Text>
            <CardInput value={nickname} onChangeText={setNickname} placeholder="请输入你的称呼，例如 王阿姨" />
          </View>
          <View className="gap-3 rounded-[24px] bg-background px-4 py-4">
            <Text className="text-[18px] font-bold text-foreground">当前登录方式</Text>
            <Text className="text-[18px] leading-7 text-muted">{state.profile?.loginMethod === 'wechat' ? '微信登录' : state.profile?.loginMethod === 'douyin' ? '抖音登录' : '手机号登录'}</Text>
          </View>
          <PrimaryButton label="保存资料" icon="star.fill" onPress={handleSave} />
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

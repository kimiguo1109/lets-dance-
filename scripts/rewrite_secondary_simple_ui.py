from pathlib import Path
from textwrap import dedent

ROOT = Path('/home/ubuntu/lets-dance-mvp')

files = {
    'app/(tabs)/groups.tsx': dedent('''
        import { ScrollView, StyleSheet, Text, View } from 'react-native';
        import { router } from 'expo-router';

        import { ScreenContainer } from '@/components/screen-container';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { formatDistance } from '@/lib/dance-utils';

        export default function GroupsScreen() {
          const { visibleGroups } = useDanceApp();

          return (
            <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
              <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
                <View style={styles.headerCard}>
                  <Text style={styles.title}>附近舞团</Text>
                  <Text style={styles.subtitle}>按距离从近到远排列，点一下就能查看详情。</Text>
                </View>

                <View style={styles.listWrap}>
                  {visibleGroups.map((group) => (
                    <View key={group.id} style={styles.groupCard}>
                      <Text onPress={() => router.push(`/group/${group.id}`)} style={styles.groupName}>
                        {group.name}
                      </Text>
                      <Text style={styles.groupMeta}>队长：{group.captainName}</Text>
                      <Text style={styles.groupMeta}>{group.address}</Text>
                      <View style={styles.bottomRow}>
                        <Text style={styles.distance}>{formatDistance(group.distanceMeters)}</Text>
                        <Text style={styles.status}>{group.status === 'active' ? '活跃中' : '已休眠'}</Text>
                      </View>
                    </View>
                  ))}
                </View>
              </ScrollView>
            </ScreenContainer>
          );
        }

        const styles = StyleSheet.create({
          container: {
            paddingTop: 12,
            paddingBottom: 144,
            gap: 18,
          },
          headerCard: {
            borderRadius: 30,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 22,
            paddingVertical: 24,
          },
          title: {
            fontSize: 30,
            lineHeight: 36,
            fontWeight: '900',
            color: '#241F1A',
            marginBottom: 8,
          },
          subtitle: {
            fontSize: 19,
            lineHeight: 28,
            color: '#74685E',
          },
          listWrap: {
            gap: 14,
          },
          groupCard: {
            borderRadius: 28,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 22,
            paddingVertical: 22,
            shadowColor: '#D6451D',
            shadowOpacity: 0.06,
            shadowRadius: 12,
            shadowOffset: { width: 0, height: 6 },
            elevation: 2,
          },
          groupName: {
            fontSize: 28,
            lineHeight: 34,
            fontWeight: '900',
            color: '#241F1A',
            marginBottom: 10,
          },
          groupMeta: {
            fontSize: 20,
            lineHeight: 30,
            color: '#5F564F',
          },
          bottomRow: {
            marginTop: 12,
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
          },
          distance: {
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '800',
            color: '#D75A18',
          },
          status: {
            fontSize: 19,
            lineHeight: 24,
            fontWeight: '800',
            color: '#2E9E5B',
          },
        });
    ''').strip() + '\n',
    'app/(tabs)/me.tsx': dedent('''
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
                  <Text style={styles.subtitle}>只保留老人最常用的头像和昵称设置。</Text>

                  <View style={styles.avatarSection}>
                    <ProfileAvatar uri={avatarUri} fallback={nickname || '舞'} />
                    <Pressable onPress={handleAvatar} style={({ pressed }) => [styles.pickButton, pressed && styles.pressed]}>
                      <IconSymbol name="camera.fill" size={26} color="#FFFFFF" />
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
            paddingTop: 12,
            paddingBottom: 144,
          },
          card: {
            borderRadius: 30,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 22,
            paddingVertical: 24,
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
            paddingVertical: 28,
            gap: 16,
          },
          pickButton: {
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 10,
            paddingHorizontal: 24,
            paddingVertical: 16,
            borderRadius: 24,
            backgroundColor: '#FF7A12',
          },
          pickButtonText: {
            fontSize: 22,
            lineHeight: 28,
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
            borderRadius: 24,
            backgroundColor: '#F6F1EA',
            paddingHorizontal: 18,
            paddingVertical: 18,
            fontSize: 22,
            lineHeight: 28,
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
            fontSize: 21,
            lineHeight: 28,
            color: '#74685E',
          },
          saveButton: {
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: 26,
            backgroundColor: '#D91E12',
            paddingVertical: 18,
          },
          saveButtonText: {
            fontSize: 24,
            lineHeight: 30,
            fontWeight: '900',
            color: '#FFFFFF',
          },
          pressed: {
            opacity: 0.93,
            transform: [{ scale: 0.98 }],
          },
        });
    ''').strip() + '\n',
}

for relative_path, content in files.items():
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print(f'rewrote {len(files)} files')

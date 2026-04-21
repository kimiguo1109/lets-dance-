from pathlib import Path
from textwrap import dedent

ROOT = Path('/home/ubuntu/lets-dance-mvp')

files = {
    'components/ui/icon-symbol.tsx': dedent('''
        import MaterialIcons from '@expo/vector-icons/MaterialIcons';
        import { SymbolWeight, SymbolViewProps } from 'expo-symbols';
        import { ComponentProps } from 'react';
        import { OpaqueColorValue, type StyleProp, type TextStyle } from 'react-native';

        type IconMapping = Record<SymbolViewProps['name'], ComponentProps<typeof MaterialIcons>['name']>;
        type IconSymbolName = keyof typeof MAPPING;

        const MAPPING = {
          'house.fill': 'home',
          'paperplane.fill': 'send',
          'chevron.left.forwardslash.chevron.right': 'code',
          'chevron.right': 'chevron-right',
          'figure.dance': 'play-circle-filled',
          'person.2.fill': 'groups',
          'person.crop.circle.fill': 'person',
          'location.fill': 'location-on',
          'mic.fill': 'mic',
          'camera.fill': 'photo-camera',
          'arrow.triangle.turn.up.right.diamond.fill': 'share',
          'map.fill': 'map',
          'phone.fill': 'phone',
          'plus.circle.fill': 'add-circle',
          'clock.fill': 'schedule',
          'star.fill': 'star',
          'waveform': 'graphic-eq',
          'bell.fill': 'notifications',
          'line.3.horizontal': 'menu',
          'play.circle.fill': 'play-circle-filled',
        } as IconMapping;

        export function IconSymbol({
          name,
          size = 24,
          color,
          style,
        }: {
          name: IconSymbolName;
          size?: number;
          color: string | OpaqueColorValue;
          style?: StyleProp<TextStyle>;
          weight?: SymbolWeight;
        }) {
          return <MaterialIcons color={color} size={size} name={MAPPING[name]} style={style} />;
        }
    ''').strip() + '\n',
    'app/(tabs)/_layout.tsx': dedent('''
        import { Tabs } from 'expo-router';
        import { Platform } from 'react-native';
        import { useSafeAreaInsets } from 'react-native-safe-area-context';

        import { HapticTab } from '@/components/haptic-tab';
        import { IconSymbol } from '@/components/ui/icon-symbol';
        import { useColors } from '@/hooks/use-colors';

        export default function TabLayout() {
          const colors = useColors();
          const insets = useSafeAreaInsets();
          const bottomPadding = Platform.OS === 'web' ? 14 : Math.max(insets.bottom, 10);
          const tabBarHeight = 88 + bottomPadding;

          return (
            <Tabs
              screenOptions={{
                headerShown: false,
                tabBarButton: HapticTab,
                tabBarActiveTintColor: '#FFFFFF',
                tabBarInactiveTintColor: '#8D8A86',
                tabBarStyle: {
                  position: 'absolute',
                  left: 12,
                  right: 12,
                  bottom: 8,
                  paddingTop: 10,
                  paddingBottom: bottomPadding,
                  height: tabBarHeight,
                  backgroundColor: '#FFF9F3',
                  borderTopWidth: 0,
                  borderRadius: 28,
                  shadowColor: '#D6451D',
                  shadowOpacity: 0.12,
                  shadowRadius: 18,
                  shadowOffset: { width: 0, height: 8 },
                  elevation: 4,
                },
                tabBarLabelStyle: {
                  fontSize: 15,
                  fontWeight: '800',
                  marginTop: 4,
                },
                tabBarItemStyle: {
                  marginHorizontal: 4,
                  marginTop: 4,
                  borderRadius: 22,
                },
                tabBarActiveBackgroundColor: colors.primary,
              }}
            >
              <Tabs.Screen
                name="index"
                options={{
                  title: '首页',
                  tabBarIcon: ({ color }) => <IconSymbol size={28} name="house.fill" color={color} />,
                }}
              />
              <Tabs.Screen
                name="groups"
                options={{
                  title: '舞队',
                  tabBarIcon: ({ color }) => <IconSymbol size={28} name="person.2.fill" color={color} />,
                }}
              />
              <Tabs.Screen
                name="messages"
                options={{
                  title: '消息',
                  tabBarIcon: ({ color }) => <IconSymbol size={28} name="bell.fill" color={color} />,
                }}
              />
              <Tabs.Screen
                name="me"
                options={{
                  title: '我的',
                  tabBarIcon: ({ color }) => <IconSymbol size={28} name="person.crop.circle.fill" color={color} />,
                }}
              />
            </Tabs>
          );
        }
    ''').strip() + '\n',
    'app/(tabs)/index.tsx': dedent('''
        import { router } from 'expo-router';
        import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

        import { ScreenContainer } from '@/components/screen-container';
        import { IconSymbol } from '@/components/ui/icon-symbol';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { appHaptics } from '@/lib/haptics';

        function TopIconButton({ icon, onPress }: { icon: React.ComponentProps<typeof IconSymbol>['name']; onPress: () => void }) {
          return (
            <Pressable onPress={onPress} style={({ pressed }) => [styles.iconButton, pressed && styles.pressed]}>
              <IconSymbol name={icon} size={30} color={icon === 'mic.fill' ? '#B42318' : '#1F1F1F'} />
            </Pressable>
          );
        }

        function ActionTile({
          label,
          icon,
          tone,
          badge,
          onPress,
        }: {
          label: string;
          icon: React.ComponentProps<typeof IconSymbol>['name'];
          tone: 'light' | 'orange';
          badge?: string;
          onPress: () => void;
        }) {
          return (
            <Pressable
              onPress={onPress}
              style={({ pressed }) => [styles.tile, pressed && styles.pressed]}
              className={tone === 'orange' ? 'bg-[#FF7A12]' : 'bg-[#F2EFEB]'}
            >
              {badge ? (
                <View className="absolute right-4 top-4 h-10 min-w-10 items-center justify-center rounded-full bg-[#C62828] px-3">
                  <Text className="text-[20px] font-extrabold text-white">{badge}</Text>
                </View>
              ) : null}
              <View className="mb-5 mt-2 items-center">
                <IconSymbol name={icon} size={52} color={tone === 'orange' ? '#40200A' : '#B42318'} />
              </View>
              <Text className="text-center text-[24px] font-extrabold text-[#241F1A]">{label}</Text>
            </Pressable>
          );
        }

        export default function HomeScreen() {
          const { nearbyGroups } = useDanceApp();
          const nearbyCount = nearbyGroups.filter((group) => group.distanceMeters <= 200).length;

          const openNearby = () => {
            appHaptics.light();
            router.push('/(tabs)/groups');
          };

          return (
            <ScreenContainer className="bg-[#FBF8F2] px-5" containerClassName="bg-[#FBF8F2]">
              <ScrollView contentContainerStyle={{ paddingBottom: 138 }} showsVerticalScrollIndicator={false}>
                <View className="flex-row items-center justify-between border-b border-[#F0E9DF] pb-5 pt-3">
                  <TopIconButton icon="line.3.horizontal" onPress={() => appHaptics.light()} />
                  <Text className="text-[34px] font-extrabold tracking-[1px] text-[#B42318]">跳舞吧</Text>
                  <TopIconButton icon="mic.fill" onPress={() => router.push('/voice-search')} />
                </View>

                <View className="items-center px-3 pb-10 pt-12">
                  <Pressable
                    onPress={() => router.push('/start-dancing')}
                    style={({ pressed }) => [styles.heroButton, pressed && styles.pressed]}
                    className="h-[360px] w-full max-w-[520px] items-center justify-center rounded-[54px] bg-[#D91E12]"
                  >
                    <View className="mb-8 h-28 w-28 items-center justify-center rounded-full bg-white">
                      <IconSymbol name="play.circle.fill" size={62} color="#D91E12" />
                    </View>
                    <Text className="text-[38px] font-extrabold text-white">开始跳舞</Text>
                  </Pressable>
                </View>

                <View className="flex-row gap-4 pb-4">
                  <ActionTile
                    label="附近舞团"
                    icon="location.fill"
                    badge={String(nearbyCount)}
                    tone="light"
                    onPress={openNearby}
                  />
                  <ActionTile
                    label="说话找地"
                    icon="mic.fill"
                    tone="orange"
                    onPress={() => router.push('/voice-search')}
                  />
                </View>
              </ScrollView>
            </ScreenContainer>
          );
        }

        const styles = StyleSheet.create({
          iconButton: {
            width: 54,
            height: 54,
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: 18,
          },
          heroButton: {
            shadowColor: '#E45C2F',
            shadowOpacity: 0.28,
            shadowRadius: 28,
            shadowOffset: { width: 0, height: 14 },
            elevation: 8,
          },
          tile: {
            flex: 1,
            minHeight: 210,
            borderRadius: 30,
            paddingHorizontal: 18,
            paddingVertical: 18,
            justifyContent: 'center',
            shadowColor: '#D6451D',
            shadowOpacity: 0.08,
            shadowRadius: 14,
            shadowOffset: { width: 0, height: 6 },
            elevation: 2,
          },
          pressed: {
            opacity: 0.93,
            transform: [{ scale: 0.98 }],
          },
        });
    ''').strip() + '\n',
    'app/(tabs)/messages.tsx': dedent('''
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
    ''').strip() + '\n',
}

for relative_path, content in files.items():
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print(f'rewrote {len(files)} files')

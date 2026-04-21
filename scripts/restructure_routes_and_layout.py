from pathlib import Path
from textwrap import dedent

ROOT = Path('/home/ubuntu/lets-dance-mvp')

files = {
    'lib/app-routes.ts': '''
        export type RouteSource = 'home' | 'groups' | 'messages' | 'me' | 'start' | 'voice';

        export const AppRoutes = {
          home: '/(tabs)',
          groups: '/(tabs)/groups',
          messages: '/(tabs)/messages',
          me: '/(tabs)/me',
          start: '/start-dancing',
          voice: '/voice-search',
          group: (id: string, from: RouteSource = 'groups') => `/group/${id}?from=${from}`,
          share: (groupId?: string, from: RouteSource = 'start') =>
            groupId ? `/share-card?groupId=${encodeURIComponent(groupId)}&from=${from}` : `/share-card?from=${from}`,
        } as const;

        export function getBackRoute(from?: string) {
          switch (from) {
            case 'home':
              return AppRoutes.home;
            case 'messages':
              return AppRoutes.messages;
            case 'me':
              return AppRoutes.me;
            case 'voice':
              return AppRoutes.voice;
            case 'start':
              return AppRoutes.start;
            case 'groups':
            default:
              return AppRoutes.groups;
          }
        }
    ''',
    'components/dance-ui.tsx': '''
        import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
        import { Image } from 'expo-image';
        import { Link } from 'expo-router';

        import { IconSymbol } from '@/components/ui/icon-symbol';
        import { formatDistance } from '@/lib/dance-utils';
        import type { DanceGroup } from '@/lib/dance-types';

        export function SectionTitle({ title, subtitle }: { title: string; subtitle?: string }) {
          return (
            <View style={styles.sectionTitleWrap}>
              <Text style={styles.sectionTitle}>{title}</Text>
              {subtitle ? <Text style={styles.sectionSubtitle}>{subtitle}</Text> : null}
            </View>
          );
        }

        export function PrimaryButton({
          label,
          onPress,
          icon,
          tone = 'primary',
        }: {
          label: string;
          onPress: () => void;
          icon?: React.ComponentProps<typeof IconSymbol>['name'];
          tone?: 'primary' | 'light';
        }) {
          const primary = tone === 'primary';
          return (
            <Pressable
              onPress={onPress}
              style={({ pressed }) => [styles.buttonBase, primary ? styles.buttonPrimary : styles.buttonLight, pressed && styles.pressed]}
            >
              {icon ? <IconSymbol name={icon} size={24} color={primary ? '#FFFFFF' : '#2C241E'} /> : null}
              <Text style={primary ? styles.buttonPrimaryText : styles.buttonLightText}>{label}</Text>
            </Pressable>
          );
        }

        export function TinyAction({
          label,
          icon,
          onPress,
        }: {
          label: string;
          icon: React.ComponentProps<typeof IconSymbol>['name'];
          onPress: () => void;
        }) {
          return (
            <Pressable onPress={onPress} style={({ pressed }) => [styles.tinyAction, pressed && styles.pressed]}>
              <IconSymbol name={icon} size={22} color="#D75A18" />
              <Text style={styles.tinyActionText}>{label}</Text>
            </Pressable>
          );
        }

        export function Badge({ label, tone = 'active' }: { label: string; tone?: 'active' | 'sleeping' | 'warm' }) {
          return <Text style={[styles.badge, tone === 'active' ? styles.badgeActive : tone === 'sleeping' ? styles.badgeSleeping : styles.badgeWarm]}>{label}</Text>;
        }

        export function GroupCard({ group, caption, href }: { group: DanceGroup; caption?: string; href: string }) {
          return (
            <Link href={href as never} asChild>
              <Pressable style={({ pressed }) => [styles.groupCard, pressed && styles.pressed]}>
                <View style={styles.groupCardTop}>
                  <View style={styles.groupCardInfo}>
                    <Text style={styles.groupCardName}>{group.name}</Text>
                    <Text style={styles.groupCardMeta}>队长：{group.captainName}</Text>
                    <Text style={styles.groupCardMeta}>{group.address}</Text>
                  </View>
                  <Badge label={group.status === 'active' ? '活跃中' : '已休眠'} tone={group.status === 'active' ? 'active' : 'sleeping'} />
                </View>
                <View style={styles.groupCardBottom}>
                  <Text style={styles.groupCardDistance}>{formatDistance(group.distanceMeters)}</Text>
                  <Text style={styles.groupCardCount}>当前 {group.memberCount} 人</Text>
                </View>
                {caption ? <Text style={styles.groupCardCaption}>{caption}</Text> : null}
              </Pressable>
            </Link>
          );
        }

        export function HeroCard({ title, value, detail }: { title: string; value: string; detail: string }) {
          return (
            <View style={styles.heroCard}>
              <Text style={styles.heroLabel}>{title}</Text>
              <Text style={styles.heroValue}>{value}</Text>
              <Text style={styles.heroDetail}>{detail}</Text>
            </View>
          );
        }

        export function ProfileAvatar({ uri, fallback }: { uri?: string; fallback: string }) {
          if (uri) {
            return <Image source={{ uri }} style={styles.avatar} contentFit="cover" />;
          }
          return (
            <View style={[styles.avatar, styles.avatarFallback]}>
              <Text style={styles.avatarText}>{fallback.slice(0, 1)}</Text>
            </View>
          );
        }

        export function CardInput({ value, onChangeText, placeholder }: { value: string; onChangeText: (text: string) => void; placeholder: string }) {
          return (
            <TextInput
              value={value}
              onChangeText={onChangeText}
              placeholder={placeholder}
              placeholderTextColor="#9C8D84"
              style={styles.cardInput}
              returnKeyType="done"
            />
          );
        }

        const styles = StyleSheet.create({
          sectionTitleWrap: {
            gap: 4,
          },
          sectionTitle: {
            fontSize: 28,
            lineHeight: 34,
            fontWeight: '900',
            color: '#241F1A',
          },
          sectionSubtitle: {
            fontSize: 18,
            lineHeight: 28,
            color: '#6B625B',
          },
          buttonBase: {
            minHeight: 60,
            borderRadius: 24,
            paddingHorizontal: 20,
            paddingVertical: 16,
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 10,
            shadowColor: '#D95C2C',
            shadowOpacity: 0.08,
            shadowRadius: 14,
            shadowOffset: { width: 0, height: 6 },
            elevation: 2,
          },
          buttonPrimary: {
            backgroundColor: '#D91E12',
          },
          buttonLight: {
            backgroundColor: '#FFF8EF',
            borderWidth: 1,
            borderColor: '#EEDFCF',
          },
          buttonPrimaryText: {
            fontSize: 20,
            lineHeight: 26,
            fontWeight: '900',
            color: '#FFFFFF',
          },
          buttonLightText: {
            fontSize: 20,
            lineHeight: 26,
            fontWeight: '900',
            color: '#2C241E',
          },
          tinyAction: {
            minHeight: 56,
            borderRadius: 22,
            paddingHorizontal: 14,
            paddingVertical: 14,
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 8,
            backgroundColor: '#FFF8EF',
            borderWidth: 1,
            borderColor: '#EEDFCF',
          },
          tinyActionText: {
            fontSize: 17,
            lineHeight: 22,
            fontWeight: '800',
            color: '#241F1A',
          },
          badge: {
            alignSelf: 'flex-start',
            borderRadius: 999,
            paddingHorizontal: 12,
            paddingVertical: 8,
            fontSize: 15,
            lineHeight: 18,
            fontWeight: '800',
          },
          badgeActive: {
            backgroundColor: '#E9F8EF',
            color: '#2E9E5B',
          },
          badgeSleeping: {
            backgroundColor: '#E8F3F0',
            color: '#4EB7A5',
          },
          badgeWarm: {
            backgroundColor: '#FFF1DD',
            color: '#D75A18',
          },
          groupCard: {
            borderRadius: 28,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 18,
            paddingVertical: 18,
            gap: 14,
            shadowColor: '#D6451D',
            shadowOpacity: 0.06,
            shadowRadius: 12,
            shadowOffset: { width: 0, height: 6 },
            elevation: 2,
          },
          groupCardTop: {
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            gap: 12,
          },
          groupCardInfo: {
            flex: 1,
            gap: 6,
          },
          groupCardName: {
            fontSize: 26,
            lineHeight: 32,
            fontWeight: '900',
            color: '#241F1A',
          },
          groupCardMeta: {
            fontSize: 18,
            lineHeight: 26,
            color: '#5F564F',
          },
          groupCardBottom: {
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
            gap: 12,
            flexWrap: 'wrap',
          },
          groupCardDistance: {
            fontSize: 21,
            lineHeight: 26,
            fontWeight: '900',
            color: '#D75A18',
          },
          groupCardCount: {
            fontSize: 18,
            lineHeight: 24,
            fontWeight: '800',
            color: '#241F1A',
          },
          groupCardCaption: {
            fontSize: 17,
            lineHeight: 25,
            color: '#6B625B',
          },
          heroCard: {
            flex: 1,
            borderRadius: 24,
            paddingHorizontal: 16,
            paddingVertical: 16,
            gap: 6,
            backgroundColor: '#FFFFFF',
            borderWidth: 1,
            borderColor: '#EFE3D8',
          },
          heroLabel: {
            fontSize: 15,
            lineHeight: 20,
            fontWeight: '700',
            color: '#8A7C72',
          },
          heroValue: {
            fontSize: 26,
            lineHeight: 32,
            fontWeight: '900',
            color: '#241F1A',
          },
          heroDetail: {
            fontSize: 16,
            lineHeight: 22,
            color: '#6B625B',
          },
          avatar: {
            width: 86,
            height: 86,
            borderRadius: 43,
          },
          avatarFallback: {
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#D91E12',
          },
          avatarText: {
            fontSize: 28,
            lineHeight: 34,
            fontWeight: '900',
            color: '#FFFFFF',
          },
          cardInput: {
            borderRadius: 22,
            borderWidth: 1,
            borderColor: '#E9D9C8',
            backgroundColor: '#FFFDF9',
            paddingHorizontal: 18,
            paddingVertical: 16,
            fontSize: 18,
            lineHeight: 24,
            fontWeight: '700',
            color: '#241F1A',
          },
          pressed: {
            opacity: 0.92,
            transform: [{ scale: 0.985 }],
          },
        });
    ''',
    'app/_layout.tsx': '''
        import '@/global.css';
        import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
        import { Stack } from 'expo-router';
        import { StatusBar } from 'expo-status-bar';
        import { useCallback, useEffect, useMemo, useState } from 'react';
        import { GestureHandlerRootView } from 'react-native-gesture-handler';
        import 'react-native-reanimated';
        import { Platform } from 'react-native';
        import '@/lib/_core/nativewind-pressable';
        import { ThemeProvider } from '@/lib/theme-provider';
        import {
          SafeAreaFrameContext,
          SafeAreaInsetsContext,
          SafeAreaProvider,
          initialWindowMetrics,
        } from 'react-native-safe-area-context';
        import type { EdgeInsets, Metrics, Rect } from 'react-native-safe-area-context';

        import { trpc, createTRPCClient } from '@/lib/trpc';
        import { initManusRuntime, subscribeSafeAreaInsets } from '@/lib/_core/manus-runtime';
        import { DanceAppProvider } from '@/lib/dance-app-context';

        const DEFAULT_WEB_INSETS: EdgeInsets = { top: 0, right: 0, bottom: 0, left: 0 };
        const DEFAULT_WEB_FRAME: Rect = { x: 0, y: 0, width: 0, height: 0 };

        export const unstable_settings = {
          anchor: '(tabs)',
        };

        export default function RootLayout() {
          const initialInsets = initialWindowMetrics?.insets ?? DEFAULT_WEB_INSETS;
          const initialFrame = initialWindowMetrics?.frame ?? DEFAULT_WEB_FRAME;

          const [insets, setInsets] = useState<EdgeInsets>(initialInsets);
          const [frame, setFrame] = useState<Rect>(initialFrame);

          useEffect(() => {
            initManusRuntime();
          }, []);

          const handleSafeAreaUpdate = useCallback((metrics: Metrics) => {
            setInsets(metrics.insets);
            setFrame(metrics.frame);
          }, []);

          useEffect(() => {
            if (Platform.OS !== 'web') return;
            const unsubscribe = subscribeSafeAreaInsets(handleSafeAreaUpdate);
            return () => unsubscribe();
          }, [handleSafeAreaUpdate]);

          const [queryClient] = useState(
            () =>
              new QueryClient({
                defaultOptions: {
                  queries: {
                    refetchOnWindowFocus: false,
                    retry: 1,
                  },
                },
              }),
          );
          const [trpcClient] = useState(() => createTRPCClient());

          const providerInitialMetrics = useMemo(() => {
            const metrics = initialWindowMetrics ?? { insets: initialInsets, frame: initialFrame };
            return {
              ...metrics,
              insets: {
                ...metrics.insets,
                top: Math.max(metrics.insets.top, 18),
                bottom: Math.max(metrics.insets.bottom, 12),
              },
            };
          }, [initialInsets, initialFrame]);

          const content = (
            <GestureHandlerRootView style={{ flex: 1 }}>
              <trpc.Provider client={trpcClient} queryClient={queryClient}>
                <QueryClientProvider client={queryClient}>
                  <DanceAppProvider>
                    <Stack screenOptions={{ headerShown: false, contentStyle: { backgroundColor: '#FBF8F2' } }}>
                      <Stack.Screen name="(tabs)" />
                      <Stack.Screen name="oauth/callback" />
                      <Stack.Screen name="group/[id]" />
                      <Stack.Screen name="voice-search" />
                      <Stack.Screen name="start-dancing" />
                      <Stack.Screen name="share-card" options={{ presentation: 'transparentModal' }} />
                    </Stack>
                    <StatusBar style="dark" />
                  </DanceAppProvider>
                </QueryClientProvider>
              </trpc.Provider>
            </GestureHandlerRootView>
          );

          if (Platform.OS === 'web') {
            return (
              <ThemeProvider>
                <SafeAreaProvider initialMetrics={providerInitialMetrics}>
                  <SafeAreaFrameContext.Provider value={frame}>
                    <SafeAreaInsetsContext.Provider value={insets}>{content}</SafeAreaInsetsContext.Provider>
                  </SafeAreaFrameContext.Provider>
                </SafeAreaProvider>
              </ThemeProvider>
            );
          }

          return (
            <ThemeProvider>
              <SafeAreaProvider initialMetrics={providerInitialMetrics}>{content}</SafeAreaProvider>
            </ThemeProvider>
          );
        }
    ''',
    'app/(tabs)/_layout.tsx': '''
        import { Tabs } from 'expo-router';
        import { Platform } from 'react-native';
        import { useSafeAreaInsets } from 'react-native-safe-area-context';

        import { HapticTab } from '@/components/haptic-tab';
        import { IconSymbol } from '@/components/ui/icon-symbol';

        export default function TabLayout() {
          const insets = useSafeAreaInsets();
          const bottomPadding = Platform.OS === 'web' ? 12 : Math.max(insets.bottom, 10);
          const tabBarHeight = 72 + bottomPadding;

          return (
            <Tabs
              screenOptions={{
                headerShown: false,
                tabBarButton: HapticTab,
                tabBarActiveTintColor: '#FFFFFF',
                tabBarInactiveTintColor: '#8D8A86',
                tabBarStyle: {
                  position: 'absolute',
                  left: 14,
                  right: 14,
                  bottom: 10,
                  height: tabBarHeight,
                  paddingTop: 8,
                  paddingBottom: bottomPadding,
                  backgroundColor: '#FFF9F3',
                  borderTopWidth: 0,
                  borderRadius: 26,
                  shadowColor: '#D6451D',
                  shadowOpacity: 0.12,
                  shadowRadius: 18,
                  shadowOffset: { width: 0, height: 8 },
                  elevation: 4,
                },
                tabBarLabelStyle: {
                  fontSize: 14,
                  fontWeight: '800',
                  marginTop: 2,
                },
                tabBarItemStyle: {
                  marginHorizontal: 2,
                  marginVertical: 4,
                  borderRadius: 18,
                },
                tabBarActiveBackgroundColor: '#FF6A2A',
              }}
            >
              <Tabs.Screen
                name="index"
                options={{
                  title: '首页',
                  tabBarIcon: ({ color }) => <IconSymbol size={26} name="house.fill" color={color} />,
                }}
              />
              <Tabs.Screen
                name="groups"
                options={{
                  title: '舞队',
                  tabBarIcon: ({ color }) => <IconSymbol size={26} name="person.2.fill" color={color} />,
                }}
              />
              <Tabs.Screen
                name="messages"
                options={{
                  title: '消息',
                  tabBarIcon: ({ color }) => <IconSymbol size={26} name="bell.fill" color={color} />,
                }}
              />
              <Tabs.Screen
                name="me"
                options={{
                  title: '我的',
                  tabBarIcon: ({ color }) => <IconSymbol size={26} name="person.crop.circle.fill" color={color} />,
                }}
              />
            </Tabs>
          );
        }
    ''',
    'app/(tabs)/index.tsx': '''
        import { router } from 'expo-router';
        import { Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from 'react-native';

        import { ScreenContainer } from '@/components/screen-container';
        import { IconSymbol } from '@/components/ui/icon-symbol';
        import { AppRoutes } from '@/lib/app-routes';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { appHaptics } from '@/lib/haptics';

        function TopIconButton({ icon, onPress }: { icon: React.ComponentProps<typeof IconSymbol>['name']; onPress: () => void }) {
          return (
            <Pressable onPress={onPress} style={({ pressed }) => [styles.topIconButton, pressed && styles.pressed]}>
              <IconSymbol name={icon} size={30} color={icon === 'mic.fill' ? '#B42318' : '#1F1F1F'} />
            </Pressable>
          );
        }

        function ActionTile({
          label,
          icon,
          backgroundColor,
          iconColor,
          badge,
          height,
          onPress,
        }: {
          label: string;
          icon: React.ComponentProps<typeof IconSymbol>['name'];
          backgroundColor: string;
          iconColor: string;
          badge?: string;
          height: number;
          onPress: () => void;
        }) {
          return (
            <Pressable onPress={onPress} style={({ pressed }) => [styles.tile, { backgroundColor, minHeight: height }, pressed && styles.pressed]}>
              {badge ? (
                <View style={styles.badge}>
                  <Text style={styles.badgeText}>{badge}</Text>
                </View>
              ) : null}
              <View style={styles.tileIconWrap}>
                <IconSymbol name={icon} size={46} color={iconColor} />
              </View>
              <Text style={styles.tileLabel}>{label}</Text>
            </Pressable>
          );
        }

        export default function HomeScreen() {
          const { nearbyGroups } = useDanceApp();
          const { width } = useWindowDimensions();
          const nearbyCount = nearbyGroups.filter((group) => group.distanceMeters <= 200).length;
          const heroHeight = Math.max(280, Math.min(390, width * 0.78));
          const tileHeight = Math.max(170, Math.min(230, width * 0.45));

          const openNearby = () => {
            appHaptics.light();
            router.push(AppRoutes.groups);
          };

          return (
            <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
              <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
                <View style={styles.headerWrap}>
                  <View style={styles.header}>
                    <TopIconButton icon="line.3.horizontal" onPress={() => router.push(AppRoutes.me)} />
                    <Text style={styles.brand}>跳舞吧</Text>
                    <TopIconButton icon="mic.fill" onPress={() => router.push(AppRoutes.voice)} />
                  </View>
                </View>

                <View style={styles.heroWrap}>
                  <Pressable onPress={() => router.push(AppRoutes.start)} style={({ pressed }) => [styles.heroButton, { minHeight: heroHeight }, pressed && styles.pressed]}>
                    <View style={styles.heroIconCircle}>
                      <IconSymbol name="play.circle.fill" size={64} color="#D91E12" />
                    </View>
                    <Text style={styles.heroText}>开始跳舞</Text>
                  </Pressable>
                </View>

                <View style={styles.tilesRow}>
                  <ActionTile
                    label="附近舞团"
                    icon="location.fill"
                    badge={String(nearbyCount)}
                    backgroundColor="#F1EEEA"
                    iconColor="#B42318"
                    height={tileHeight}
                    onPress={openNearby}
                  />
                  <ActionTile
                    label="说话找地"
                    icon="mic.fill"
                    backgroundColor="#FF7A12"
                    iconColor="#40200A"
                    height={tileHeight}
                    onPress={() => router.push(AppRoutes.voice)}
                  />
                </View>
              </ScrollView>
            </ScreenContainer>
          );
        }

        const styles = StyleSheet.create({
          container: {
            paddingTop: 12,
            paddingBottom: 156,
            backgroundColor: '#FBF8F2',
          },
          headerWrap: {
            paddingTop: 10,
            paddingBottom: 8,
          },
          header: {
            minHeight: 60,
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between',
            paddingBottom: 16,
            borderBottomWidth: 1,
            borderBottomColor: '#EEE6DD',
          },
          topIconButton: {
            width: 50,
            height: 50,
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: 18,
          },
          brand: {
            fontSize: 30,
            lineHeight: 36,
            fontWeight: '900',
            color: '#B42318',
            letterSpacing: 1,
          },
          heroWrap: {
            paddingTop: 24,
            paddingBottom: 28,
            alignItems: 'center',
          },
          heroButton: {
            width: '100%',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: 44,
            backgroundColor: '#D91E12',
            shadowColor: '#E45C2F',
            shadowOpacity: 0.22,
            shadowRadius: 24,
            shadowOffset: { width: 0, height: 12 },
            elevation: 6,
          },
          heroIconCircle: {
            width: 104,
            height: 104,
            borderRadius: 52,
            backgroundColor: '#FFFFFF',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: 24,
          },
          heroText: {
            fontSize: 34,
            lineHeight: 40,
            fontWeight: '900',
            color: '#FFFFFF',
          },
          tilesRow: {
            flexDirection: 'row',
            gap: 16,
            alignItems: 'stretch',
          },
          tile: {
            flex: 1,
            borderRadius: 30,
            paddingHorizontal: 16,
            paddingVertical: 18,
            justifyContent: 'center',
            shadowColor: '#D6451D',
            shadowOpacity: 0.08,
            shadowRadius: 14,
            shadowOffset: { width: 0, height: 6 },
            elevation: 2,
          },
          tileIconWrap: {
            alignItems: 'center',
            marginBottom: 18,
            marginTop: 10,
          },
          tileLabel: {
            textAlign: 'center',
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '900',
            color: '#241F1A',
          },
          badge: {
            position: 'absolute',
            top: 12,
            right: 12,
            minWidth: 38,
            height: 38,
            borderRadius: 19,
            backgroundColor: '#C62828',
            alignItems: 'center',
            justifyContent: 'center',
            paddingHorizontal: 8,
          },
          badgeText: {
            color: '#FFFFFF',
            fontSize: 20,
            lineHeight: 24,
            fontWeight: '900',
          },
          pressed: {
            opacity: 0.93,
            transform: [{ scale: 0.985 }],
          },
        });
    ''',
    'app/(tabs)/groups.tsx': '''
        import { FlatList, Pressable, StyleSheet, Text, View } from 'react-native';
        import { router } from 'expo-router';

        import { ScreenContainer } from '@/components/screen-container';
        import { AppRoutes } from '@/lib/app-routes';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { formatDistance } from '@/lib/dance-utils';

        export default function GroupsScreen() {
          const { visibleGroups } = useDanceApp();

          return (
            <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
              <FlatList
                data={visibleGroups}
                keyExtractor={(item) => item.id}
                showsVerticalScrollIndicator={false}
                contentContainerStyle={styles.container}
                ListHeaderComponent={
                  <View style={styles.headerCard}>
                    <Text style={styles.title}>附近舞团</Text>
                    <Text style={styles.subtitle}>按距离从近到远排列，点一下就能查看详情。</Text>
                  </View>
                }
                renderItem={({ item: group }) => (
                  <Pressable onPress={() => router.push(AppRoutes.group(group.id, 'groups'))} style={({ pressed }) => [styles.groupCard, pressed && styles.pressed]}>
                    <Text style={styles.groupName}>{group.name}</Text>
                    <Text style={styles.groupMeta}>队长：{group.captainName}</Text>
                    <Text style={styles.groupMeta}>{group.address}</Text>
                    <View style={styles.bottomRow}>
                      <Text style={styles.distance}>{formatDistance(group.distanceMeters)}</Text>
                      <Text style={[styles.status, group.status === 'active' ? styles.active : styles.sleeping]}>{group.status === 'active' ? '活跃中' : '已休眠'}</Text>
                    </View>
                  </Pressable>
                )}
                ItemSeparatorComponent={() => <View style={styles.separator} />}
              />
            </ScreenContainer>
          );
        }

        const styles = StyleSheet.create({
          container: {
            paddingTop: 16,
            paddingBottom: 160,
          },
          headerCard: {
            borderRadius: 30,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 20,
            paddingTop: 22,
            paddingBottom: 22,
            shadowColor: '#E9D8C7',
            shadowOpacity: 0.1,
            shadowRadius: 12,
            shadowOffset: { width: 0, height: 4 },
            elevation: 1,
            marginBottom: 16,
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
          separator: {
            height: 14,
          },
          groupCard: {
            borderRadius: 28,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 20,
            paddingVertical: 20,
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
            lineHeight: 29,
            color: '#5F564F',
          },
          bottomRow: {
            marginTop: 14,
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
            gap: 12,
            flexWrap: 'wrap',
          },
          distance: {
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '900',
            color: '#D75A18',
          },
          status: {
            fontSize: 19,
            lineHeight: 24,
            fontWeight: '900',
          },
          active: {
            color: '#2E9E5B',
          },
          sleeping: {
            color: '#4EB7A5',
          },
          pressed: {
            opacity: 0.94,
            transform: [{ scale: 0.99 }],
          },
        });
    ''',
    'app/(tabs)/messages.tsx': '''
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
    ''',
    'app/(tabs)/me.tsx': '''
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
    ''',
    'app/start-dancing.tsx': '''
        import { router } from 'expo-router';
        import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

        import { PrimaryButton } from '@/components/dance-ui';
        import { ScreenContainer } from '@/components/screen-container';
        import { IconSymbol } from '@/components/ui/icon-symbol';
        import { AppRoutes } from '@/lib/app-routes';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { formatDistance } from '@/lib/dance-utils';

        function StepRow({ index, label }: { index: number; label: string }) {
          return (
            <View style={styles.stepRow}>
              <View style={styles.stepBadge}>
                <Text style={styles.stepBadgeText}>{index}</Text>
              </View>
              <Text style={styles.stepText}>{label}</Text>
            </View>
          );
        }

        export default function StartDancingScreen() {
          const { nearbyGroups, startDancing, state } = useDanceApp();
          const result = state.lastStartResult;

          const handleStart = async (forceCreate = false) => {
            const nextResult = await startDancing({ createNew: forceCreate });
            if (!nextResult) return;
            Alert.alert(nextResult.type === 'created' ? '舞团创建成功' : '加入成功', `已进入 ${nextResult.group.name}`);
          };

          return (
            <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]" edges={['top', 'bottom', 'left', 'right']}>
              <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
                <View style={styles.topBar}>
                  <Pressable onPress={() => router.replace(AppRoutes.home)} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
                    <IconSymbol name="chevron.right" size={28} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
                  </Pressable>
                  <Text style={styles.pageTitle}>开始跳舞</Text>
                  <Pressable onPress={() => router.push(AppRoutes.groups)} style={({ pressed }) => [styles.sideButton, pressed && styles.pressed]}>
                    <Text style={styles.sideButtonText}>舞队</Text>
                  </Pressable>
                </View>

                <View style={styles.heroCard}>
                  <Text style={styles.heroTitle}>四步完成</Text>
                  <Text style={styles.heroSubtitle}>定位、拍照、判断附近舞团，再自动加入或创建，主路径保持尽量简单。</Text>
                  <View style={styles.stepsWrap}>
                    <StepRow index={1} label="获取当前位置" />
                    <StepRow index={2} label="拍一张现场照片" />
                    <StepRow index={3} label="优先加入 200 米内舞团" />
                    <StepRow index={4} label="没有舞团时创建新舞团" />
                  </View>
                  <View style={styles.actionGap}>
                    <PrimaryButton label="立即开始" icon="play.circle.fill" onPress={() => handleStart(false)} />
                    <PrimaryButton label="直接创建新的舞团" icon="plus.circle.fill" tone="light" onPress={() => handleStart(true)} />
                  </View>
                </View>

                <View style={styles.sectionCard}>
                  <Text style={styles.sectionTitle}>附近可加入舞团</Text>
                  <Text style={styles.sectionSubtitle}>如果你只想先看看，也可以点进去看详情。</Text>
                  <View style={styles.groupList}>
                    {nearbyGroups.slice(0, 3).map((group) => (
                      <Pressable key={group.id} onPress={() => router.push(AppRoutes.group(group.id, 'start'))} style={({ pressed }) => [styles.groupRow, pressed && styles.pressed]}>
                        <View style={styles.groupInfo}>
                          <Text style={styles.groupName}>{group.name}</Text>
                          <Text style={styles.groupMeta}>队长：{group.captainName}</Text>
                          <Text style={styles.groupMeta}>{group.address}</Text>
                          <Text style={styles.distance}>{formatDistance(group.distanceMeters)}</Text>
                        </View>
                        <View style={styles.groupRight}>
                          <Text style={[styles.groupStatus, group.status === 'active' ? styles.active : styles.sleeping]}>{group.status === 'active' ? '活跃中' : '已休眠'}</Text>
                          <Text style={styles.memberCount}>当前 {group.memberCount} 人</Text>
                        </View>
                      </Pressable>
                    ))}
                  </View>
                </View>

                {result ? (
                  <View style={styles.resultCard}>
                    <Text style={styles.resultTitle}>本次结果</Text>
                    <Text style={styles.resultText}>你已{result.type === 'created' ? '创建' : '加入'}“{result.group.name}”。</Text>
                    <View style={styles.actionGap}>
                      <PrimaryButton label="查看舞团详情" icon="person.2.fill" onPress={() => router.push(AppRoutes.group(result.group.id, 'start'))} />
                      <PrimaryButton label="分享卡片" icon="arrow.triangle.turn.up.right.diamond.fill" tone="light" onPress={() => router.push(AppRoutes.share(result.group.id, 'start'))} />
                      <PrimaryButton label="回到首页" icon="house.fill" tone="light" onPress={() => router.replace(AppRoutes.home)} />
                    </View>
                  </View>
                ) : null}
              </ScrollView>
            </ScreenContainer>
          );
        }

        const styles = StyleSheet.create({
          container: {
            paddingTop: 12,
            paddingBottom: 40,
            gap: 18,
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
          sideButton: {
            minWidth: 56,
            height: 48,
            borderRadius: 16,
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#FFF8EF',
            paddingHorizontal: 12,
            borderWidth: 1,
            borderColor: '#EEDFCF',
          },
          sideButtonText: {
            fontSize: 16,
            lineHeight: 20,
            fontWeight: '800',
            color: '#241F1A',
          },
          pageTitle: {
            flex: 1,
            textAlign: 'center',
            fontSize: 30,
            lineHeight: 36,
            fontWeight: '900',
            color: '#241F1A',
          },
          heroCard: {
            borderRadius: 30,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 20,
            paddingVertical: 22,
            gap: 16,
          },
          heroTitle: {
            fontSize: 28,
            lineHeight: 34,
            fontWeight: '900',
            color: '#241F1A',
          },
          heroSubtitle: {
            fontSize: 18,
            lineHeight: 28,
            color: '#74685E',
          },
          stepsWrap: {
            gap: 12,
          },
          stepRow: {
            flexDirection: 'row',
            alignItems: 'center',
            gap: 12,
          },
          stepBadge: {
            width: 34,
            height: 34,
            borderRadius: 17,
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#FFEDD8',
          },
          stepBadgeText: {
            fontSize: 18,
            lineHeight: 22,
            fontWeight: '900',
            color: '#D75A18',
          },
          stepText: {
            flex: 1,
            fontSize: 20,
            lineHeight: 28,
            fontWeight: '800',
            color: '#D75A18',
          },
          actionGap: {
            gap: 12,
          },
          sectionCard: {
            borderRadius: 30,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 20,
            paddingVertical: 22,
            gap: 14,
          },
          sectionTitle: {
            fontSize: 28,
            lineHeight: 34,
            fontWeight: '900',
            color: '#241F1A',
          },
          sectionSubtitle: {
            fontSize: 18,
            lineHeight: 28,
            color: '#74685E',
          },
          groupList: {
            gap: 14,
          },
          groupRow: {
            borderRadius: 24,
            backgroundColor: '#FFF8EF',
            borderWidth: 1,
            borderColor: '#EEDFCF',
            paddingHorizontal: 16,
            paddingVertical: 16,
            flexDirection: 'row',
            justifyContent: 'space-between',
            gap: 12,
          },
          groupInfo: {
            flex: 1,
          },
          groupRight: {
            alignItems: 'flex-end',
            gap: 10,
            paddingTop: 4,
          },
          groupName: {
            fontSize: 24,
            lineHeight: 30,
            fontWeight: '900',
            color: '#241F1A',
            marginBottom: 8,
          },
          groupMeta: {
            fontSize: 17,
            lineHeight: 24,
            color: '#5F564F',
          },
          distance: {
            marginTop: 10,
            fontSize: 20,
            lineHeight: 26,
            fontWeight: '900',
            color: '#D75A18',
          },
          groupStatus: {
            fontSize: 18,
            lineHeight: 22,
            fontWeight: '900',
          },
          active: {
            color: '#2E9E5B',
          },
          sleeping: {
            color: '#4EB7A5',
          },
          memberCount: {
            fontSize: 17,
            lineHeight: 22,
            fontWeight: '800',
            color: '#241F1A',
          },
          resultCard: {
            borderRadius: 30,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 20,
            paddingVertical: 22,
            gap: 10,
          },
          resultTitle: {
            fontSize: 26,
            lineHeight: 32,
            fontWeight: '900',
            color: '#241F1A',
          },
          resultText: {
            fontSize: 18,
            lineHeight: 28,
            color: '#5F564F',
          },
          pressed: {
            opacity: 0.94,
            transform: [{ scale: 0.99 }],
          },
        });
    ''',
    'app/group/[id].tsx': '''
        import { useEffect } from 'react';
        import { router, useLocalSearchParams } from 'expo-router';
        import { Alert, Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
        import { Image } from 'expo-image';

        import { Badge, PrimaryButton } from '@/components/dance-ui';
        import { ScreenContainer } from '@/components/screen-container';
        import { IconSymbol } from '@/components/ui/icon-symbol';
        import { AppRoutes, getBackRoute } from '@/lib/app-routes';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { appHaptics } from '@/lib/haptics';
        import { formatDistance, openNavigation } from '@/lib/dance-utils';

        export default function GroupDetailScreen() {
          const params = useLocalSearchParams<{ id: string; from?: string }>();
          const { width } = useWindowDimensions();
          const { getGroupById, state, shareGroup, joinGroup, wakeGroup, setSelectedGroup } = useDanceApp();
          const group = getGroupById(params.id);
          const nickname = state.profile?.nickname ?? '舞友';
          const isCaptain = group?.captainName === nickname;
          const backRoute = getBackRoute(params.from);
          const imageHeight = Math.max(210, Math.min(290, width * 0.58));

          useEffect(() => {
            if (params.id) {
              setSelectedGroup(params.id);
            }
          }, [params.id, setSelectedGroup]);

          if (!group) {
            return (
              <ScreenContainer className="items-center justify-center px-6" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
                <Text style={styles.emptyTitle}>未找到舞团</Text>
                <Pressable onPress={() => router.replace(backRoute)} style={({ pressed }) => [styles.inlineBackButton, pressed && styles.pressed]}>
                  <Text style={styles.inlineBackText}>返回上一页</Text>
                </Pressable>
              </ScreenContainer>
            );
          }

          const handleJoin = async () => {
            await joinGroup(group.id);
            Alert.alert('加入成功', `你已经加入 ${group.name}。`);
          };

          const handleNavigate = async () => {
            appHaptics.light();
            await openNavigation(group.coordinates, group.locationLabel);
          };

          const handleCaptainAction = async () => {
            if (isCaptain) {
              await wakeGroup(group.id);
              Alert.alert('舞团已唤醒', '舞团状态已更新为活跃。');
              return;
            }
            if (group.wechatLink) {
              router.push(AppRoutes.share(group.id, 'groups'));
            }
          };

          return (
            <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]" edges={['top', 'bottom', 'left', 'right']}>
              <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
                <View style={styles.topBar}>
                  <Pressable onPress={() => router.replace(backRoute)} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
                    <IconSymbol name="chevron.right" size={28} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
                  </Pressable>
                  <Text style={styles.pageTitle}>舞团详情</Text>
                  <Pressable onPress={() => router.replace(AppRoutes.groups)} style={({ pressed }) => [styles.sideButton, pressed && styles.pressed]}>
                    <Text style={styles.sideButtonText}>舞队</Text>
                  </Pressable>
                </View>

                {group.photoUri ? (
                  <Image source={{ uri: group.photoUri }} style={{ width: '100%', height: imageHeight, borderRadius: 28 }} contentFit="cover" />
                ) : (
                  <View style={[styles.placeholderImage, { height: imageHeight }]}> 
                    <Text style={styles.placeholderText}>等待今晚的舞步照片</Text>
                  </View>
                )}

                <View style={styles.card}>
                  <Text style={styles.groupName}>{group.name}</Text>
                  <Text style={styles.groupMeta}>队长：{group.captainName}｜当前 {group.memberCount} 人</Text>
                  <Badge label={group.status === 'active' ? '活跃中' : '已休眠'} tone={group.status === 'active' ? 'active' : 'sleeping'} />
                  <Text style={styles.address}>{group.address}</Text>
                  <Text style={styles.distance}>距离你约 {formatDistance(group.distanceMeters)}</Text>
                </View>

                <View style={styles.card}>
                  <Text style={styles.sectionTitle}>今晚安排</Text>
                  <Text style={styles.infoText}>集合点：{group.locationLabel}</Text>
                  <Text style={styles.infoText}>最近打卡：{new Date(group.lastCheckInAt).toLocaleString('zh-CN')}</Text>
                  <Text style={styles.infoText}>分享话术：{group.shareMessage}</Text>
                </View>

                <View style={styles.actionWrap}>
                  <PrimaryButton label="导航过去" icon="map.fill" onPress={handleNavigate} />
                  <View style={styles.rowActions}>
                    <View style={styles.flexOne}>
                      <PrimaryButton label="发给好友" icon="arrow.triangle.turn.up.right.diamond.fill" tone="light" onPress={() => shareGroup(group.id)} />
                    </View>
                    <View style={styles.flexOne}>
                      <PrimaryButton label={isCaptain ? '唤醒舞团' : '联系队长'} icon="phone.fill" tone="light" onPress={handleCaptainAction} />
                    </View>
                  </View>
                  {!isCaptain ? <PrimaryButton label="加入舞团" icon="plus.circle.fill" tone="light" onPress={handleJoin} /> : null}
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
          sideButton: {
            minWidth: 56,
            height: 48,
            borderRadius: 16,
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#FFF8EF',
            paddingHorizontal: 12,
            borderWidth: 1,
            borderColor: '#EEDFCF',
          },
          sideButtonText: {
            fontSize: 16,
            lineHeight: 20,
            fontWeight: '800',
            color: '#241F1A',
          },
          pageTitle: {
            flex: 1,
            textAlign: 'center',
            fontSize: 28,
            lineHeight: 34,
            fontWeight: '900',
            color: '#241F1A',
          },
          placeholderImage: {
            width: '100%',
            borderRadius: 28,
            backgroundColor: '#FFFFFF',
            borderWidth: 1,
            borderColor: '#EEDFCF',
            alignItems: 'center',
            justifyContent: 'center',
          },
          placeholderText: {
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '800',
            color: '#7F756D',
          },
          card: {
            borderRadius: 28,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 20,
            paddingVertical: 20,
            gap: 10,
            borderWidth: 1,
            borderColor: '#EFE3D8',
          },
          groupName: {
            fontSize: 30,
            lineHeight: 36,
            fontWeight: '900',
            color: '#241F1A',
          },
          groupMeta: {
            fontSize: 18,
            lineHeight: 26,
            color: '#5F564F',
          },
          address: {
            fontSize: 18,
            lineHeight: 28,
            color: '#5F564F',
          },
          distance: {
            fontSize: 21,
            lineHeight: 26,
            fontWeight: '900',
            color: '#D75A18',
          },
          sectionTitle: {
            fontSize: 26,
            lineHeight: 32,
            fontWeight: '900',
            color: '#241F1A',
          },
          infoText: {
            fontSize: 18,
            lineHeight: 28,
            color: '#5F564F',
          },
          actionWrap: {
            gap: 12,
          },
          rowActions: {
            flexDirection: 'row',
            gap: 12,
          },
          flexOne: {
            flex: 1,
          },
          emptyTitle: {
            fontSize: 24,
            lineHeight: 30,
            fontWeight: '900',
            color: '#241F1A',
            marginBottom: 16,
          },
          inlineBackButton: {
            borderRadius: 22,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 20,
            paddingVertical: 14,
          },
          inlineBackText: {
            fontSize: 18,
            lineHeight: 24,
            fontWeight: '800',
            color: '#241F1A',
          },
          pressed: {
            opacity: 0.94,
            transform: [{ scale: 0.99 }],
          },
        });
    ''',
    'app/voice-search.tsx': '''
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
    ''',
    'app/share-card.tsx': '''
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
    ''',
}

for relative_path, content in files.items():
    target = ROOT / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dedent(content).lstrip('\n'), encoding='utf-8')

print(f'Updated {len(files)} files.')

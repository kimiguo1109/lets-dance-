from pathlib import Path
from textwrap import dedent

ROOT = Path('/home/ubuntu/lets-dance-mvp')

files = {
    'components/screen-container.tsx': '''
        import { View, type ViewProps } from "react-native";
        import { SafeAreaView, type Edge } from "react-native-safe-area-context";

        import { cn } from "@/lib/utils";

        export interface ScreenContainerProps extends ViewProps {
          edges?: Edge[];
          className?: string;
          containerClassName?: string;
          safeAreaClassName?: string;
        }

        export function ScreenContainer({
          children,
          edges = ["top", "left", "right"],
          className,
          containerClassName,
          safeAreaClassName,
          style,
          ...props
        }: ScreenContainerProps) {
          return (
            <View className={cn("flex-1", "bg-background", containerClassName)} {...props}>
              <SafeAreaView edges={edges} className={cn("flex-1", safeAreaClassName)} style={style}>
                <View className={cn("flex-1 pt-2", className)}>{children}</View>
              </SafeAreaView>
            </View>
          );
        }
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
                top: Math.max(metrics.insets.top, 28),
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
                  <View style={styles.headerShell}>
                    <View style={styles.headerCard}>
                      <Text style={styles.title}>附近舞团</Text>
                      <Text style={styles.subtitle}>按距离从近到远排列，点一下就能查看详情。</Text>
                    </View>
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
            paddingTop: 8,
            paddingBottom: 160,
          },
          headerShell: {
            paddingTop: 10,
            paddingBottom: 18,
          },
          headerCard: {
            borderRadius: 30,
            backgroundColor: '#FFFDF9',
            paddingHorizontal: 20,
            paddingTop: 24,
            paddingBottom: 22,
            borderWidth: 1,
            borderColor: '#EFE6DB',
            shadowColor: '#E9D8C7',
            shadowOpacity: 0.1,
            shadowRadius: 12,
            shadowOffset: { width: 0, height: 4 },
            elevation: 1,
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
                <View style={styles.headerShell}>
                  <View style={styles.topBar}>
                    <Pressable onPress={() => router.replace(backRoute)} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
                      <IconSymbol name="chevron.right" size={28} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
                    </Pressable>
                    <Text style={styles.pageTitle}>舞团详情</Text>
                    <Pressable onPress={() => router.replace(AppRoutes.groups)} style={({ pressed }) => [styles.sideButton, pressed && styles.pressed]}>
                      <Text style={styles.sideButtonText}>舞队</Text>
                    </Pressable>
                  </View>
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
            paddingTop: 4,
            paddingBottom: 40,
            gap: 16,
          },
          headerShell: {
            paddingTop: 10,
            paddingBottom: 8,
          },
          topBar: {
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between',
            paddingHorizontal: 12,
            paddingVertical: 10,
            borderRadius: 24,
            backgroundColor: '#FFFDF9',
            borderWidth: 1,
            borderColor: '#EFE6DB',
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
                <View style={styles.headerShell}>
                  <View style={styles.topBar}>
                    <Pressable onPress={() => router.replace(AppRoutes.home)} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
                      <IconSymbol name="chevron.right" size={28} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
                    </Pressable>
                    <Text style={styles.pageTitle}>开始跳舞</Text>
                    <Pressable onPress={() => router.push(AppRoutes.groups)} style={({ pressed }) => [styles.sideButton, pressed && styles.pressed]}>
                      <Text style={styles.sideButtonText}>舞队</Text>
                    </Pressable>
                  </View>
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
            paddingTop: 4,
            paddingBottom: 40,
            gap: 18,
          },
          headerShell: {
            paddingTop: 10,
            paddingBottom: 8,
          },
          topBar: {
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between',
            paddingHorizontal: 12,
            paddingVertical: 10,
            borderRadius: 24,
            backgroundColor: '#FFFDF9',
            borderWidth: 1,
            borderColor: '#EFE6DB',
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
    '''
}

for relative_path, content in files.items():
    target = ROOT / relative_path
    target.write_text(dedent(content).lstrip('\n'), encoding='utf-8')

print(f'Updated {len(files)} files.')

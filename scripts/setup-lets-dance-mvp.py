from pathlib import Path
from textwrap import dedent

ROOT = Path('/home/ubuntu/lets-dance-mvp')

files = {
    'theme.config.js': dedent('''
        /** @type {const} */
        const themeColors = {
          primary: { light: '#F05A28', dark: '#F56E42' },
          background: { light: '#FFF7F1', dark: '#1E1814' },
          surface: { light: '#FFFFFF', dark: '#2A221D' },
          foreground: { light: '#2A241F', dark: '#FFF3EB' },
          muted: { light: '#7A6B62', dark: '#C8B9B0' },
          border: { light: '#F1D9CC', dark: '#4A3B34' },
          success: { light: '#2E9E5B', dark: '#49C774' },
          warning: { light: '#C96A1A', dark: '#E78F3F' },
          error: { light: '#C94A3D', dark: '#FF7D70' },
        };

        module.exports = { themeColors };
    ''').strip() + '\n',
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
          'figure.dance': 'directions-run',
          'person.2.fill': 'groups',
          'person.crop.circle.fill': 'account-circle',
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
          const bottomPadding = Platform.OS === 'web' ? 12 : Math.max(insets.bottom, 10);
          const tabBarHeight = 62 + bottomPadding;

          return (
            <Tabs
              screenOptions={{
                headerShown: false,
                tabBarButton: HapticTab,
                tabBarActiveTintColor: colors.primary,
                tabBarInactiveTintColor: colors.muted,
                tabBarStyle: {
                  paddingTop: 8,
                  paddingBottom: bottomPadding,
                  height: tabBarHeight,
                  backgroundColor: colors.surface,
                  borderTopColor: colors.border,
                  borderTopWidth: 1,
                },
                tabBarLabelStyle: {
                  fontSize: 14,
                  fontWeight: '700',
                },
              }}
            >
              <Tabs.Screen
                name="index"
                options={{
                  title: '开始跳舞',
                  tabBarIcon: ({ color }) => <IconSymbol size={28} name="figure.dance" color={color} />,
                }}
              />
              <Tabs.Screen
                name="groups"
                options={{
                  title: '附近舞团',
                  tabBarIcon: ({ color }) => <IconSymbol size={28} name="person.2.fill" color={color} />,
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
    'app/_layout.tsx': dedent('''
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
                top: Math.max(metrics.insets.top, 16),
                bottom: Math.max(metrics.insets.bottom, 12),
              },
            };
          }, [initialInsets, initialFrame]);

          const content = (
            <GestureHandlerRootView style={{ flex: 1 }}>
              <trpc.Provider client={trpcClient} queryClient={queryClient}>
                <QueryClientProvider client={queryClient}>
                  <DanceAppProvider>
                    <Stack screenOptions={{ headerShown: false }}>
                      <Stack.Screen name="(tabs)" />
                      <Stack.Screen name="oauth/callback" />
                      <Stack.Screen name="group/[id]" />
                      <Stack.Screen name="voice-search" />
                      <Stack.Screen name="start-dancing" />
                      <Stack.Screen name="share-card" options={{ presentation: 'modal' }} />
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
    ''').strip() + '\n',
    'lib/haptics.ts': dedent('''
        import { Platform } from 'react-native';
        import * as Haptics from 'expo-haptics';

        export const appHaptics = {
          light() {
            if (Platform.OS !== 'web') {
              void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
            }
          },
          medium() {
            if (Platform.OS !== 'web') {
              void Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
            }
          },
          success() {
            if (Platform.OS !== 'web') {
              void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
            }
          },
          error() {
            if (Platform.OS !== 'web') {
              void Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
            }
          },
        };
    ''').strip() + '\n',
    'lib/dance-types.ts': dedent('''
        export type AppLoginMethod = 'phone' | 'wechat' | 'douyin';
        export type GroupStatus = 'active' | 'sleeping';

        export interface UserProfile {
          id: string;
          nickname: string;
          avatarUri?: string;
          loginMethod: AppLoginMethod;
          updatedAt: string;
        }

        export interface Coordinates {
          latitude: number;
          longitude: number;
        }

        export interface GroupMember {
          id: string;
          name: string;
          joinedAt: string;
          isCaptain: boolean;
        }

        export interface DanceGroup {
          id: string;
          name: string;
          captainName: string;
          address: string;
          locationLabel: string;
          coordinates: Coordinates;
          distanceMeters: number;
          photoUri?: string;
          memberCount: number;
          members: GroupMember[];
          status: GroupStatus;
          lastCheckInAt: string;
          createdAt: string;
          wechatLink?: string;
          shareMessage: string;
        }

        export interface StartDancingResult {
          type: 'joined' | 'created';
          group: DanceGroup;
        }

        export interface VoiceSearchResult {
          transcript: string;
          matchedGroupIds: string[];
          directNavigationLabel?: string;
        }

        export interface AppStateShape {
          initialized: boolean;
          profile: UserProfile | null;
          groups: DanceGroup[];
          selectedGroupId: string | null;
          lastStartResult: StartDancingResult | null;
          lastVoiceResult: VoiceSearchResult | null;
        }
    ''').strip() + '\n',
    'lib/dance-data.ts': dedent('''
        import type { DanceGroup, UserProfile } from '@/lib/dance-types';

        const now = new Date();
        const hoursAgo = (hours: number) => new Date(now.getTime() - hours * 60 * 60 * 1000).toISOString();
        const daysAgo = (days: number) => new Date(now.getTime() - days * 24 * 60 * 60 * 1000).toISOString();

        export const DEFAULT_PROFILE: UserProfile = {
          id: 'local-user',
          nickname: '王阿姨',
          loginMethod: 'phone',
          updatedAt: now.toISOString(),
        };

        export const SEEDED_GROUPS: DanceGroup[] = [
          {
            id: 'group-binjiang',
            name: '滨江晚舞团',
            captainName: '张姐',
            address: '青年路地铁 B 口东侧空地',
            locationLabel: '青年路与滨江路交叉口广场',
            coordinates: { latitude: 31.2281, longitude: 121.4742 },
            distanceMeters: 128,
            memberCount: 26,
            members: [
              { id: 'm1', name: '张姐', joinedAt: daysAgo(15), isCaptain: true },
              { id: 'm2', name: '刘阿姨', joinedAt: daysAgo(10), isCaptain: false },
              { id: 'm3', name: '陈叔', joinedAt: daysAgo(6), isCaptain: false },
            ],
            status: 'active',
            lastCheckInAt: hoursAgo(5),
            createdAt: daysAgo(20),
            wechatLink: 'https://weixin.qq.com/',
            shareMessage: '我们在滨江晚舞团等你，一起跳舞更热闹。',
          },
          {
            id: 'group-metro',
            name: '地铁口晨练舞团',
            captainName: '李队',
            address: '和平公园南门健身广场',
            locationLabel: '和平路与中山路交叉口广场',
            coordinates: { latitude: 31.2298, longitude: 121.4711 },
            distanceMeters: 186,
            memberCount: 18,
            members: [
              { id: 'm4', name: '李队', joinedAt: daysAgo(28), isCaptain: true },
              { id: 'm5', name: '孙姨', joinedAt: daysAgo(11), isCaptain: false },
            ],
            status: 'active',
            lastCheckInAt: hoursAgo(12),
            createdAt: daysAgo(33),
            wechatLink: 'https://weixin.qq.com/',
            shareMessage: '地铁口晨练舞团欢迎你，到了就能开跳。',
          },
          {
            id: 'group-lotus',
            name: '莲花广场舞友会',
            captainName: '吴老师',
            address: '莲花路社区中心西侧空地',
            locationLabel: '莲花路社区中心广场',
            coordinates: { latitude: 31.2316, longitude: 121.4769 },
            distanceMeters: 342,
            memberCount: 14,
            members: [
              { id: 'm6', name: '吴老师', joinedAt: daysAgo(41), isCaptain: true },
            ],
            status: 'sleeping',
            lastCheckInAt: daysAgo(5),
            createdAt: daysAgo(49),
            wechatLink: 'https://weixin.qq.com/',
            shareMessage: '莲花广场舞友会等你来唤醒今晚的舞步。',
          },
        ];
    ''').strip() + '\n',
    'lib/dance-storage.ts': dedent('''
        import AsyncStorage from '@react-native-async-storage/async-storage';

        import { DEFAULT_PROFILE, SEEDED_GROUPS } from '@/lib/dance-data';
        import type { AppStateShape } from '@/lib/dance-types';

        const STORAGE_KEY = 'lets-dance-mvp-state-v1';

        export const defaultAppState: AppStateShape = {
          initialized: true,
          profile: DEFAULT_PROFILE,
          groups: SEEDED_GROUPS,
          selectedGroupId: SEEDED_GROUPS[0]?.id ?? null,
          lastStartResult: null,
          lastVoiceResult: null,
        };

        export async function loadAppState() {
          const raw = await AsyncStorage.getItem(STORAGE_KEY);
          if (!raw) {
            await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(defaultAppState));
            return defaultAppState;
          }
          return JSON.parse(raw) as AppStateShape;
        }

        export async function persistAppState(state: AppStateShape) {
          await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        }
    ''').strip() + '\n',
    'lib/dance-utils.ts': dedent('''
        import * as Linking from 'expo-linking';
        import { Platform } from 'react-native';

        import type { Coordinates, DanceGroup, GroupStatus } from '@/lib/dance-types';

        export function formatDistance(distanceMeters: number) {
          if (distanceMeters < 1000) return `${Math.round(distanceMeters)} 米`;
          return `${(distanceMeters / 1000).toFixed(1)} 公里`;
        }

        export function getGroupStatus(lastCheckInAt: string): GroupStatus {
          const hours = (Date.now() - new Date(lastCheckInAt).getTime()) / (1000 * 60 * 60);
          return hours > 72 ? 'sleeping' : 'active';
        }

        export function sortGroups(groups: DanceGroup[]) {
          return [...groups].sort((a, b) => a.distanceMeters - b.distanceMeters);
        }

        export function searchGroups(groups: DanceGroup[], keyword: string) {
          const normalized = keyword.trim().toLowerCase();
          if (!normalized) return sortGroups(groups);
          return sortGroups(
            groups.filter((group) =>
              [group.name, group.address, group.locationLabel, group.captainName]
                .join(' ')
                .toLowerCase()
                .includes(normalized),
            ),
          );
        }

        export function createGroupName(addressLabel: string) {
          return `${addressLabel}舞团`;
        }

        export function createShareMessage(group: DanceGroup) {
          return `${group.name}｜${group.locationLabel}｜当前 ${group.memberCount} 人，来一起跳舞吧。`;
        }

        export function buildMapUrl(coords: Coordinates, label: string) {
          const encoded = encodeURIComponent(label);
          if (Platform.OS === 'ios') {
            return `http://maps.apple.com/?ll=${coords.latitude},${coords.longitude}&q=${encoded}`;
          }
          return `https://uri.amap.com/navigation?to=${coords.longitude},${coords.latitude},${encoded}&mode=walk&src=lets-dance-mvp`; 
        }

        export async function openNavigation(coords: Coordinates, label: string) {
          const url = buildMapUrl(coords, label);
          await Linking.openURL(url);
        }
    ''').strip() + '\n',
    'lib/dance-app-context.tsx': dedent('''
        import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
        import { Alert } from 'react-native';
        import * as ImagePicker from 'expo-image-picker';
        import * as Location from 'expo-location';
        import * as Sharing from 'expo-sharing';

        import { defaultAppState, loadAppState, persistAppState } from '@/lib/dance-storage';
        import { appHaptics } from '@/lib/haptics';
        import { createGroupName, createShareMessage, getGroupStatus, searchGroups, sortGroups } from '@/lib/dance-utils';
        import type { AppLoginMethod, AppStateShape, DanceGroup, StartDancingResult, UserProfile, VoiceSearchResult } from '@/lib/dance-types';

        interface StartFlowOptions {
          createNew?: boolean;
        }

        interface DanceAppContextValue {
          state: AppStateShape;
          loading: boolean;
          nearbyGroups: DanceGroup[];
          visibleGroups: DanceGroup[];
          setSelectedGroup: (id: string) => void;
          updateProfile: (payload: { nickname: string; loginMethod: AppLoginMethod; avatarUri?: string }) => Promise<void>;
          pickAvatar: () => Promise<string | undefined>;
          startDancing: (options?: StartFlowOptions) => Promise<StartDancingResult | null>;
          joinGroup: (groupId: string) => Promise<void>;
          wakeGroup: (groupId: string) => Promise<void>;
          runVoiceSearch: (transcript: string) => Promise<VoiceSearchResult>;
          shareGroup: (groupId: string) => Promise<void>;
          getGroupById: (id?: string | null) => DanceGroup | undefined;
        }

        const DanceAppContext = createContext<DanceAppContextValue | null>(null);

        const FAKE_LOCATION = {
          latitude: 31.2286,
          longitude: 121.4737,
        };

        export function DanceAppProvider({ children }: { children: React.ReactNode }) {
          const [state, setState] = useState<AppStateShape>(defaultAppState);
          const [loading, setLoading] = useState(true);

          useEffect(() => {
            loadAppState()
              .then((saved) => setState(saved))
              .finally(() => setLoading(false));
          }, []);

          useEffect(() => {
            if (!loading) {
              void persistAppState(state);
            }
          }, [loading, state]);

          const updateState = useCallback((updater: (current: AppStateShape) => AppStateShape) => {
            setState((current) => updater(current));
          }, []);

          const nearbyGroups = useMemo(() => sortGroups(state.groups.filter((group) => group.distanceMeters <= 500)), [state.groups]);
          const visibleGroups = useMemo(
            () => sortGroups(state.groups.map((group) => ({ ...group, status: getGroupStatus(group.lastCheckInAt) }))),
            [state.groups],
          );

          const setSelectedGroup = useCallback((id: string) => {
            updateState((current) => ({ ...current, selectedGroupId: id }));
          }, [updateState]);

          const updateProfile = useCallback(async (payload: { nickname: string; loginMethod: AppLoginMethod; avatarUri?: string }) => {
            const profile: UserProfile = {
              id: state.profile?.id ?? 'local-user',
              nickname: payload.nickname.trim() || '舞友',
              loginMethod: payload.loginMethod,
              avatarUri: payload.avatarUri,
              updatedAt: new Date().toISOString(),
            };
            updateState((current) => ({ ...current, profile }));
            appHaptics.success();
          }, [state.profile?.id, updateState]);

          const pickAvatar = useCallback(async () => {
            const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
            if (permission.status !== 'granted') {
              Alert.alert('无法访问相册', '请允许访问相册后再设置头像。');
              return undefined;
            }
            const result = await ImagePicker.launchImageLibraryAsync({
              allowsEditing: true,
              aspect: [1, 1],
              quality: 0.8,
              mediaTypes: ImagePicker.MediaTypeOptions.Images,
            });
            if (result.canceled) return undefined;
            appHaptics.light();
            return result.assets[0]?.uri;
          }, []);

          const requestLocation = useCallback(async () => {
            const servicesEnabled = await Location.hasServicesEnabledAsync();
            if (!servicesEnabled) {
              throw new Error('定位服务未开启');
            }
            const permission = await Location.requestForegroundPermissionsAsync();
            if (permission.status !== 'granted') {
              throw new Error('定位权限未授权');
            }
            const location = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced });
            return location.coords;
          }, []);

          const joinGroup = useCallback(async (groupId: string) => {
            updateState((current) => {
              const nickname = current.profile?.nickname ?? '新舞友';
              const groups = current.groups.map((group) => {
                if (group.id !== groupId) return group;
                const alreadyJoined = group.members.some((member) => member.name === nickname);
                const members = alreadyJoined
                  ? group.members
                  : [
                      ...group.members,
                      {
                        id: `member-${Date.now()}`,
                        name: nickname,
                        joinedAt: new Date().toISOString(),
                        isCaptain: false,
                      },
                    ];
                return {
                  ...group,
                  members,
                  memberCount: members.length,
                  lastCheckInAt: new Date().toISOString(),
                };
              });
              const group = groups.find((item) => item.id == groupId) ?? current.groups[0];
              return {
                ...current,
                groups,
                selectedGroupId: groupId,
                lastStartResult: group ? { type: 'joined', group: { ...group, memberCount: group.memberCount } } : current.lastStartResult,
              };
            });
            appHaptics.success();
          }, [updateState]);

          const startDancing = useCallback(async (options?: StartFlowOptions) => {
            try {
              let coords = FAKE_LOCATION;
              try {
                const real = await requestLocation();
                coords = { latitude: real.latitude, longitude: real.longitude };
              } catch {
                // MVP fallback uses seeded location when native location is unavailable.
              }

              const cameraPermission = await ImagePicker.requestCameraPermissionsAsync();
              if (cameraPermission.status !== 'granted') {
                Alert.alert('无法拍照', '请允许相机权限后再开始跳舞。');
                return null;
              }

              const cameraResult = await ImagePicker.launchCameraAsync({
                allowsEditing: true,
                aspect: [4, 3],
                quality: 0.7,
                cameraType: ImagePicker.CameraType.front,
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
              });
              if (cameraResult.canceled) return null;

              const currentNearby = sortGroups(
                state.groups.filter((group) => group.distanceMeters <= 200).map((group) => ({ ...group, status: getGroupStatus(group.lastCheckInAt) })),
              );

              if (currentNearby.length > 0 && !options?.createNew) {
                const targetGroup = currentNearby[0];
                await joinGroup(targetGroup.id);
                const result: StartDancingResult = {
                  type: 'joined',
                  group: {
                    ...targetGroup,
                    photoUri: cameraResult.assets[0]?.uri,
                    shareMessage: createShareMessage(targetGroup),
                  },
                };
                updateState((current) => ({ ...current, lastStartResult: result, selectedGroupId: targetGroup.id }));
                return result;
              }

              const nickname = state.profile?.nickname ?? '新队长';
              const createdAt = new Date().toISOString();
              const label = '青年路与滨江路交叉口广场';
              const newGroup: DanceGroup = {
                id: `group-${Date.now()}`,
                name: createGroupName(label),
                captainName: nickname,
                address: label,
                locationLabel: label,
                coordinates: coords,
                distanceMeters: 36,
                photoUri: cameraResult.assets[0]?.uri,
                memberCount: 1,
                members: [{ id: `member-captain-${Date.now()}`, name: nickname, joinedAt: createdAt, isCaptain: true }],
                status: 'active',
                lastCheckInAt: createdAt,
                createdAt,
                wechatLink: 'https://weixin.qq.com/',
                shareMessage: '我刚创建了一个新的舞团，来一起跳舞吧。',
              };
              const result: StartDancingResult = { type: 'created', group: newGroup };
              updateState((current) => ({
                ...current,
                groups: sortGroups([newGroup, ...current.groups]),
                selectedGroupId: newGroup.id,
                lastStartResult: result,
              }));
              appHaptics.success();
              return result;
            } catch (error) {
              const message = error instanceof Error ? error.message : '开始跳舞失败';
              Alert.alert('操作未完成', message);
              appHaptics.error();
              return null;
            }
          }, [joinGroup, requestLocation, state.groups, state.profile?.nickname, updateState]);

          const wakeGroup = useCallback(async (groupId: string) => {
            updateState((current) => ({
              ...current,
              groups: current.groups.map((group) =>
                group.id === groupId
                  ? { ...group, status: 'active', lastCheckInAt: new Date().toISOString() }
                  : group,
              ),
            }));
            appHaptics.success();
          }, [updateState]);

          const runVoiceSearch = useCallback(async (transcript: string) => {
            const trimmed = transcript.trim();
            const results = searchGroups(state.groups, trimmed);
            const voiceResult: VoiceSearchResult = {
              transcript: trimmed,
              matchedGroupIds: results.map((group) => group.id),
              directNavigationLabel: results.length === 0 && trimmed ? trimmed : undefined,
            };
            updateState((current) => ({ ...current, lastVoiceResult: voiceResult }));
            return voiceResult;
          }, [state.groups, updateState]);

          const shareGroup = useCallback(async (groupId: string) => {
            const group = state.groups.find((item) => item.id === groupId);
            if (!group) return;
            const message = createShareMessage(group);
            try {
              if (await Sharing.isAvailableAsync()) {
                Alert.alert('系统分享已就绪', message);
              } else {
                Alert.alert('分享提示', message);
              }
              appHaptics.light();
            } catch {
              Alert.alert('暂时无法分享', '请稍后再试。');
            }
          }, [state.groups]);

          const getGroupById = useCallback((id?: string | null) => state.groups.find((group) => group.id === id), [state.groups]);

          const value = useMemo<DanceAppContextValue>(() => ({
            state,
            loading,
            nearbyGroups,
            visibleGroups,
            setSelectedGroup,
            updateProfile,
            pickAvatar,
            startDancing,
            joinGroup,
            wakeGroup,
            runVoiceSearch,
            shareGroup,
            getGroupById,
          }), [
            state,
            loading,
            nearbyGroups,
            visibleGroups,
            setSelectedGroup,
            updateProfile,
            pickAvatar,
            startDancing,
            joinGroup,
            wakeGroup,
            runVoiceSearch,
            shareGroup,
            getGroupById,
          ]);

          return <DanceAppContext.Provider value={value}>{children}</DanceAppContext.Provider>;
        }

        export function useDanceApp() {
          const context = useContext(DanceAppContext);
          if (!context) {
            throw new Error('useDanceApp must be used within DanceAppProvider');
          }
          return context;
        }
    ''').strip() + '\n',
    'components/dance-ui.tsx': dedent('''
        import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
        import { Image } from 'expo-image';
        import { Link } from 'expo-router';

        import { IconSymbol } from '@/components/ui/icon-symbol';
        import { cn } from '@/lib/utils';
        import { formatDistance } from '@/lib/dance-utils';
        import type { DanceGroup } from '@/lib/dance-types';

        export function SectionTitle({ title, subtitle }: { title: string; subtitle?: string }) {
          return (
            <View className="gap-1">
              <Text className="text-[28px] font-extrabold text-foreground">{title}</Text>
              {subtitle ? <Text className="text-[18px] leading-7 text-muted">{subtitle}</Text> : null}
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
          const isPrimary = tone === 'primary';
          return (
            <Pressable
              onPress={onPress}
              style={({ pressed }) => [styles.pressable, pressed && styles.pressed]}
              className={cn(
                'flex-row items-center justify-center gap-3 rounded-[28px] px-6 py-5',
                isPrimary ? 'bg-primary' : 'bg-surface border border-border',
              )}
            >
              {icon ? <IconSymbol name={icon} size={24} color={isPrimary ? '#FFF7F1' : '#2A241F'} /> : null}
              <Text className={cn('text-[20px] font-extrabold', isPrimary ? 'text-background' : 'text-foreground')}>{label}</Text>
            </Pressable>
          );
        }

        export function TinyAction({ label, icon, onPress }: { label: string; icon: React.ComponentProps<typeof IconSymbol>['name']; onPress: () => void }) {
          return (
            <Pressable
              onPress={onPress}
              style={({ pressed }) => [styles.pressable, pressed && styles.pressed]}
              className="flex-1 rounded-[22px] bg-surface px-4 py-4 border border-border"
            >
              <View className="flex-row items-center justify-center gap-2">
                <IconSymbol name={icon} size={22} color="#F05A28" />
                <Text className="text-[18px] font-bold text-foreground">{label}</Text>
              </View>
            </Pressable>
          );
        }

        export function Badge({ label, tone = 'active' }: { label: string; tone?: 'active' | 'sleeping' | 'warm' }) {
          const className = tone === 'active'
            ? 'bg-success/15 text-success'
            : tone === 'sleeping'
              ? 'bg-border text-muted'
              : 'bg-warning/15 text-warning';
          return <Text className={cn('self-start rounded-full px-3 py-2 text-[15px] font-bold', className)}>{label}</Text>;
        }

        export function GroupCard({ group, caption, href }: { group: DanceGroup; caption?: string; href: string }) {
          return (
            <Link href={href as never} asChild>
              <Pressable style={({ pressed }) => [styles.pressable, pressed && styles.pressed]} className="rounded-[28px] bg-surface p-5 border border-border gap-4">
                <View className="flex-row items-start justify-between gap-4">
                  <View className="flex-1 gap-2">
                    <Text className="text-[22px] font-extrabold text-foreground">{group.name}</Text>
                    <Text className="text-[18px] leading-7 text-muted">队长：{group.captainName}</Text>
                    <Text className="text-[18px] leading-7 text-muted">{group.address}</Text>
                  </View>
                  <Badge label={group.status === 'active' ? '活跃中' : '已休眠'} tone={group.status === 'active' ? 'active' : 'sleeping'} />
                </View>
                <View className="flex-row items-center justify-between">
                  <Text className="text-[18px] font-bold text-primary">{formatDistance(group.distanceMeters)}</Text>
                  <Text className="text-[18px] font-semibold text-foreground">当前 {group.memberCount} 人</Text>
                </View>
                {caption ? <Text className="text-[17px] leading-7 text-muted">{caption}</Text> : null}
              </Pressable>
            </Link>
          );
        }

        export function HeroCard({ title, value, detail }: { title: string; value: string; detail: string }) {
          return (
            <View className="flex-1 rounded-[24px] bg-surface p-4 border border-border gap-2">
              <Text className="text-[16px] font-semibold text-muted">{title}</Text>
              <Text className="text-[28px] font-extrabold text-foreground">{value}</Text>
              <Text className="text-[16px] leading-6 text-muted">{detail}</Text>
            </View>
          );
        }

        export function ProfileAvatar({ uri, fallback }: { uri?: string; fallback: string }) {
          if (uri) {
            return <Image source={{ uri }} style={styles.avatar} contentFit="cover" />;
          }
          return (
            <View style={styles.avatar} className="items-center justify-center bg-primary">
              <Text className="text-[28px] font-extrabold text-background">{fallback.slice(0, 1)}</Text>
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
              className="rounded-[22px] border border-border bg-surface px-5 py-4 text-[19px] font-semibold text-foreground"
              returnKeyType="done"
            />
          );
        }

        const styles = StyleSheet.create({
          pressable: {
            shadowColor: '#D95C2C',
            shadowOpacity: 0.08,
            shadowRadius: 16,
            shadowOffset: { width: 0, height: 6 },
            elevation: 2,
          },
          pressed: {
            opacity: 0.92,
            transform: [{ scale: 0.98 }],
          },
          avatar: {
            width: 86,
            height: 86,
            borderRadius: 43,
          },
        });
    ''').strip() + '\n',
    'app/(tabs)/index.tsx': dedent('''
        import { router } from 'expo-router';
        import { ScrollView, Text, View } from 'react-native';

        import { ScreenContainer } from '@/components/screen-container';
        import { GroupCard, HeroCard, PrimaryButton, SectionTitle, TinyAction } from '@/components/dance-ui';
        import { useDanceApp } from '@/lib/dance-app-context';

        export default function HomeScreen() {
          const { state, nearbyGroups } = useDanceApp();
          const profileName = state.profile?.nickname ?? '舞友';
          const topGroup = nearbyGroups[0];

          return (
            <ScreenContainer className="px-5 pb-6">
              <ScrollView contentContainerStyle={{ paddingBottom: 24, gap: 22 }} showsVerticalScrollIndicator={false}>
                <View className="rounded-[32px] bg-surface px-5 py-6 border border-border gap-4 mt-2">
                  <Text className="text-[18px] font-semibold text-muted">下午好，{profileName}</Text>
                  <SectionTitle title="跳舞吧" subtitle="一键找人，一键开跳，一键导航到场。" />
                  <View className="flex-row gap-3">
                    <HeroCard title="附近活跃舞团" value={`${nearbyGroups.filter((item) => item.status === 'active').length}`} detail="200 米内优先推荐" />
                    <HeroCard title="我的状态" value={state.lastStartResult ? '已加入' : '待出发'} detail={state.lastStartResult ? state.lastStartResult.group.name : '点击开始跳舞'} />
                  </View>
                </View>

                <View className="items-center gap-4 py-2">
                  <View className="w-full px-2">
                    <PrimaryButton label="开始跳舞" icon="figure.dance" onPress={() => router.push('/start-dancing')} />
                  </View>
                  <Text className="text-[18px] leading-7 text-center text-muted">定位、拍照、判断附近舞团，完成后即可生成分享卡片。</Text>
                </View>

                <View className="flex-row gap-3">
                  <TinyAction label="附近舞团" icon="person.2.fill" onPress={() => router.push('/(tabs)/groups')} />
                  <TinyAction label="说话找地" icon="mic.fill" onPress={() => router.push('/voice-search')} />
                </View>

                {topGroup ? (
                  <View className="gap-4">
                    <SectionTitle title="离你最近" subtitle="先看看附近正在跳的舞团。" />
                    <GroupCard group={topGroup} href={`/group/${topGroup.id}`} caption="支持直接导航、联系队长与发给好友。" />
                  </View>
                ) : null}
              </ScrollView>
            </ScreenContainer>
          );
        }
    ''').strip() + '\n',
    'app/(tabs)/groups.tsx': dedent('''
        import { useMemo, useState } from 'react';
        import { ScrollView, Text, View } from 'react-native';

        import { ScreenContainer } from '@/components/screen-container';
        import { CardInput, GroupCard, SectionTitle } from '@/components/dance-ui';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { searchGroups } from '@/lib/dance-utils';

        export default function GroupsScreen() {
          const { visibleGroups } = useDanceApp();
          const [keyword, setKeyword] = useState('');
          const groups = useMemo(() => searchGroups(visibleGroups, keyword), [visibleGroups, keyword]);

          return (
            <ScreenContainer className="px-5 pb-6">
              <ScrollView contentContainerStyle={{ paddingBottom: 24, gap: 18 }} showsVerticalScrollIndicator={false}>
                <View className="mt-2 gap-3">
                  <SectionTitle title="附近舞团" subtitle="按距离排序，休眠舞团会自动下沉显示。" />
                  <CardInput value={keyword} onChangeText={setKeyword} placeholder="搜索舞团名、地址或队长称呼" />
                </View>
                <View className="gap-4">
                  {groups.map((group) => (
                    <GroupCard key={group.id} group={group} href={`/group/${group.id}`} />
                  ))}
                  {groups.length === 0 ? <Text className="text-[18px] leading-7 text-muted">没有找到匹配舞团，可以试试语音找地或直接开始跳舞。</Text> : null}
                </View>
              </ScrollView>
            </ScreenContainer>
          );
        }
    ''').strip() + '\n',
    'app/(tabs)/me.tsx': dedent('''
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
    ''').strip() + '\n',
    'app/group/[id].tsx': dedent('''
        import { router, useLocalSearchParams } from 'expo-router';
        import { Alert, ScrollView, Text, View } from 'react-native';
        import { Image } from 'expo-image';

        import { ScreenContainer } from '@/components/screen-container';
        import { Badge, PrimaryButton, SectionTitle } from '@/components/dance-ui';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { appHaptics } from '@/lib/haptics';
        import { formatDistance, openNavigation } from '@/lib/dance-utils';

        export default function GroupDetailScreen() {
          const params = useLocalSearchParams<{ id: string }>();
          const { getGroupById, state, shareGroup, joinGroup, wakeGroup } = useDanceApp();
          const group = getGroupById(params.id);
          const nickname = state.profile?.nickname ?? '舞友';
          const isCaptain = group?.captainName === nickname;

          if (!group) {
            return (
              <ScreenContainer className="items-center justify-center px-6">
                <Text className="text-[22px] font-bold text-foreground">未找到舞团</Text>
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
              appHaptics.light();
              router.push('/share-card');
            }
          };

          return (
            <ScreenContainer className="px-5 pb-6" edges={['top', 'bottom', 'left', 'right']}>
              <ScrollView contentContainerStyle={{ paddingBottom: 150, gap: 18 }} showsVerticalScrollIndicator={false}>
                {group.photoUri ? (
                  <Image source={{ uri: group.photoUri }} style={{ width: '100%', height: 240, borderRadius: 28 }} contentFit="cover" />
                ) : (
                  <View className="h-[240px] rounded-[28px] bg-surface items-center justify-center border border-border">
                    <Text className="text-[22px] font-bold text-muted">等待今晚的舞步照片</Text>
                  </View>
                )}
                <View className="gap-3 rounded-[30px] bg-surface px-5 py-6 border border-border">
                  <SectionTitle title={group.name} subtitle={`队长：${group.captainName}｜当前 ${group.memberCount} 人`} />
                  <Badge label={group.status === 'active' ? '活跃中' : '已休眠'} tone={group.status === 'active' ? 'active' : 'sleeping'} />
                  <Text className="text-[18px] leading-7 text-muted">{group.address}</Text>
                  <Text className="text-[18px] font-bold text-primary">距离你约 {formatDistance(group.distanceMeters)}</Text>
                </View>
                <View className="gap-3 rounded-[30px] bg-surface px-5 py-6 border border-border">
                  <Text className="text-[22px] font-extrabold text-foreground">今晚安排</Text>
                  <Text className="text-[18px] leading-7 text-muted">集合点：{group.locationLabel}</Text>
                  <Text className="text-[18px] leading-7 text-muted">最近打卡：{new Date(group.lastCheckInAt).toLocaleString('zh-CN')}</Text>
                  <Text className="text-[18px] leading-7 text-muted">分享话术：{group.shareMessage}</Text>
                </View>
              </ScrollView>
              <View className="absolute bottom-0 left-0 right-0 border-t border-border bg-background px-5 pb-6 pt-4">
                <View className="gap-3">
                  <PrimaryButton label="导航过去" icon="map.fill" onPress={handleNavigate} />
                  <View className="flex-row gap-3">
                    <View className="flex-1">
                      <PrimaryButton label="发给好友" icon="arrow.triangle.turn.up.right.diamond.fill" tone="light" onPress={() => shareGroup(group.id)} />
                    </View>
                    <View className="flex-1">
                      <PrimaryButton label={isCaptain ? '唤醒舞团' : '联系队长'} icon="phone.fill" tone="light" onPress={handleCaptainAction} />
                    </View>
                  </View>
                  {!isCaptain ? <PrimaryButton label="加入舞团" icon="plus.circle.fill" tone="light" onPress={handleJoin} /> : null}
                </View>
              </View>
            </ScreenContainer>
          );
        }
    ''').strip() + '\n',
    'app/start-dancing.tsx': dedent('''
        import { router } from 'expo-router';
        import { Alert, ScrollView, Text, View } from 'react-native';

        import { ScreenContainer } from '@/components/screen-container';
        import { Badge, GroupCard, PrimaryButton, SectionTitle } from '@/components/dance-ui';
        import { useDanceApp } from '@/lib/dance-app-context';

        export default function StartDancingScreen() {
          const { nearbyGroups, startDancing, state } = useDanceApp();
          const result = state.lastStartResult;

          const handleStart = async (forceCreate = false) => {
            const nextResult = await startDancing({ createNew: forceCreate });
            if (!nextResult) return;
            Alert.alert(nextResult.type === 'created' ? '舞团创建成功' : '加入成功', `已进入 ${nextResult.group.name}`);
          };

          return (
            <ScreenContainer className="px-5 pb-6" edges={['top', 'bottom', 'left', 'right']}>
              <ScrollView contentContainerStyle={{ paddingBottom: 24, gap: 18 }} showsVerticalScrollIndicator={false}>
                <View className="mt-2 rounded-[30px] bg-surface px-5 py-6 border border-border gap-4">
                  <SectionTitle title="开始跳舞" subtitle="这条路径会依次完成定位、拍照、附近判断、创建或加入舞团。" />
                  <View className="gap-3">
                    <Badge label="步骤 1：获取当前位置" tone="warm" />
                    <Badge label="步骤 2：拍一张现场照片" tone="warm" />
                    <Badge label="步骤 3：优先加入 200 米内舞团" tone="warm" />
                    <Badge label="步骤 4：没有舞团时创建新舞团" tone="warm" />
                  </View>
                  <PrimaryButton label="立即开始" icon="figure.dance" onPress={() => handleStart(false)} />
                  <PrimaryButton label="附近有舞团也创建新的" icon="plus.circle.fill" tone="light" onPress={() => handleStart(true)} />
                </View>

                <View className="gap-4">
                  <SectionTitle title="附近可加入舞团" subtitle="如果你只想先看看，也可以直接进入详情。" />
                  {nearbyGroups.slice(0, 2).map((group) => (
                    <GroupCard key={group.id} group={group} href={`/group/${group.id}`} />
                  ))}
                </View>

                {result ? (
                  <View className="rounded-[30px] bg-surface px-5 py-6 border border-border gap-3">
                    <Text className="text-[24px] font-extrabold text-foreground">本次结果</Text>
                    <Text className="text-[18px] leading-7 text-muted">你已{result.type === 'created' ? '创建' : '加入'}“{result.group.name}”。</Text>
                    <View className="flex-row gap-3">
                      <View className="flex-1">
                        <PrimaryButton label="查看详情" icon="person.2.fill" tone="light" onPress={() => router.push(`/group/${result.group.id}`)} />
                      </View>
                      <View className="flex-1">
                        <PrimaryButton label="分享卡片" icon="arrow.triangle.turn.up.right.diamond.fill" tone="light" onPress={() => router.push('/share-card')} />
                      </View>
                    </View>
                  </View>
                ) : null}
              </ScrollView>
            </ScreenContainer>
          );
        }
    ''').strip() + '\n',
    'app/share-card.tsx': dedent('''
        import { router } from 'expo-router';
        import { Modal, Pressable, Text, View } from 'react-native';

        import { PrimaryButton } from '@/components/dance-ui';
        import { useDanceApp } from '@/lib/dance-app-context';

        export default function ShareCardScreen() {
          const { state, shareGroup } = useDanceApp();
          const group = state.lastStartResult?.group ?? state.groups[0];

          return (
            <Modal transparent animationType="slide">
              <View className="flex-1 justify-end bg-black/35 px-4 pb-6">
                <View className="rounded-[32px] bg-surface p-6 border border-border gap-5">
                  <View className="gap-2">
                    <Text className="text-[28px] font-extrabold text-foreground">分享卡片</Text>
                    <Text className="text-[18px] leading-7 text-muted">把现场照片、舞团名称和当前人数发给微信好友。</Text>
                  </View>
                  <View className="rounded-[28px] bg-background px-5 py-6 gap-3">
                    <Text className="text-[16px] font-semibold text-muted">跳舞吧邀请你</Text>
                    <Text className="text-[28px] font-extrabold text-foreground">{group.name}</Text>
                    <Text className="text-[18px] leading-7 text-muted">{group.locationLabel}</Text>
                    <Text className="text-[20px] font-bold text-primary">当前 {group.memberCount} 人</Text>
                    <Text className="text-[18px] leading-7 text-muted">{group.shareMessage}</Text>
                  </View>
                  <PrimaryButton label="发给好友" icon="arrow.triangle.turn.up.right.diamond.fill" onPress={() => shareGroup(group.id)} />
                  <Pressable onPress={() => router.back()}>
                    <Text className="text-center text-[18px] font-bold text-muted">稍后再说</Text>
                  </Pressable>
                </View>
              </View>
            </Modal>
          );
        }
    ''').strip() + '\n',
    'app/voice-search.tsx': dedent('''
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
    ''').strip() + '\n',
}

for relative_path, content in files.items():
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

print(f'Wrote {len(files)} files')

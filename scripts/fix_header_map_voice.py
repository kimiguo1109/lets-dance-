from pathlib import Path
import textwrap

ROOT = Path('/home/ubuntu/lets-dance-mvp')

FILES = {
    ROOT / 'components/screen-container.tsx': '''import { StyleSheet, View, type ViewProps } from 'react-native';
import { SafeAreaView, useSafeAreaInsets, type Edge } from 'react-native-safe-area-context';

import { cn } from '@/lib/utils';

export interface ScreenContainerProps extends ViewProps {
  /**
   * SafeArea edges to apply. Defaults to ["top", "left", "right"].
   * Bottom is typically handled by Tab Bar.
   */
  edges?: Edge[];
  /**
   * Tailwind className for the content area.
   */
  className?: string;
  /**
   * Additional className for the outer container (background layer).
   */
  containerClassName?: string;
  /**
   * Additional className for the SafeAreaView (content layer).
   */
  safeAreaClassName?: string;
}

/**
 * A container component that properly handles SafeArea and background colors.
 *
 * The outer View extends to full screen (including status bar area) with the background color,
 * while the inner SafeAreaView ensures content is within safe bounds.
 */
export function ScreenContainer({
  children,
  edges = ['top', 'left', 'right'],
  className,
  containerClassName,
  safeAreaClassName,
  style,
  ...props
}: ScreenContainerProps) {
  const insets = useSafeAreaInsets();
  const topComfortSpacing = edges.includes('top') ? Math.max(10, Math.min(18, insets.top * 0.25)) : 0;

  return (
    <View className={cn('flex-1', 'bg-background', containerClassName)} {...props}>
      <SafeAreaView edges={edges} className={cn('flex-1', safeAreaClassName)} style={style}>
        <View className={cn('flex-1', className)} style={[styles.content, topComfortSpacing > 0 ? { paddingTop: topComfortSpacing } : null]}>
          {children}
        </View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  content: {
    flex: 1,
  },
});
''',
    ROOT / 'lib/app-routes.ts': '''import type { Href } from 'expo-router';

export type RouteSource = 'home' | 'groups' | 'messages' | 'me' | 'start' | 'voice' | 'map';

export const AppRoutes = {
  home: '/(tabs)' as const,
  groups: '/(tabs)/groups' as const,
  messages: '/(tabs)/messages' as const,
  me: '/(tabs)/me' as const,
  start: '/start-dancing' as const,
  startFromVoice: (voiceLabel: string): Href => ({
    pathname: '/start-dancing',
    params: { voiceLabel },
  }),
  voice: '/voice-search' as const,
  group: (id: string, from: RouteSource = 'groups'): Href => ({
    pathname: '/group/[id]',
    params: { id, from },
  }),
  map: (id: string, from: RouteSource = 'groups'): Href => ({
    pathname: '/map/[id]',
    params: { id, from },
  }),
  share: (groupId?: string, from: RouteSource = 'start'): Href => ({
    pathname: '/share-card',
    params: groupId ? { groupId, from } : { from },
  }),
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
    ROOT / 'lib/dance-app-context.tsx': '''import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
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
  labelOverride?: string;
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
      const label = options?.labelOverride?.trim() || '青年路与滨江路交叉口广场';
      const groupName = label.includes('舞团') ? label : createGroupName(label);
      const newGroup: DanceGroup = {
        id: `group-${Date.now()}`,
        name: groupName,
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
        shareMessage: `我刚在${label}建了一个新的舞团，来一起跳舞吧。`,
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
''',
    ROOT / 'app/_layout.tsx': '''import '@/global.css';
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
              <Stack.Screen name="map/[id]" />
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
    ROOT / 'app/(tabs)/index.tsx': '''import { router } from 'expo-router';
import { useEffect, useRef, useState } from 'react';
import {
  Alert,
  KeyboardAvoidingView,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
  useWindowDimensions,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { ScreenContainer } from '@/components/screen-container';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { AppRoutes } from '@/lib/app-routes';
import { useDanceApp } from '@/lib/dance-app-context';
import { appHaptics } from '@/lib/haptics';

const QUICK_PHRASES = ['青年路广场', '人民公园', '滨江路口', '东方广场'];

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
  const { nearbyGroups, runVoiceSearch, getGroupById } = useDanceApp();
  const { width } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const inputRef = useRef<TextInput>(null);
  const [voiceModalVisible, setVoiceModalVisible] = useState(false);
  const [voiceDraft, setVoiceDraft] = useState('');
  const [voiceListening, setVoiceListening] = useState(false);
  const nearbyCount = nearbyGroups.filter((group) => group.distanceMeters <= 200).length;
  const heroHeight = Math.max(280, Math.min(390, width * 0.78));
  const tileHeight = Math.max(170, Math.min(230, width * 0.45));
  const headerTopPadding = Math.max(8, Math.min(16, insets.top * 0.18));

  useEffect(() => {
    if (!voiceModalVisible) return;
    setVoiceListening(true);
    const timer = setTimeout(() => {
      setVoiceListening(false);
      inputRef.current?.focus();
    }, 900);
    return () => clearTimeout(timer);
  }, [voiceModalVisible]);

  const openNearby = () => {
    appHaptics.light();
    router.push(AppRoutes.groups);
  };

  const openVoiceModal = () => {
    appHaptics.light();
    setVoiceDraft('');
    setVoiceModalVisible(true);
  };

  const closeVoiceModal = () => {
    setVoiceModalVisible(false);
    setVoiceListening(false);
  };

  const handleVoiceSearch = async (value?: string) => {
    const transcript = (value ?? voiceDraft).trim();
    if (!transcript) {
      Alert.alert('还没听清地点', '请直接说出广场、地铁口或舞团名。');
      return;
    }
    const result = await runVoiceSearch(transcript);
    closeVoiceModal();
    const matchedId = result.matchedGroupIds[0];
    if (matchedId) {
      const matchedGroup = getGroupById(matchedId);
      if (matchedGroup) {
        appHaptics.success();
        router.push(AppRoutes.group(matchedGroup.id, 'home'));
        return;
      }
    }
    Alert.alert('先帮你新建舞团', `没有找到现成舞团，我先把“${result.directNavigationLabel ?? transcript}”带到开始跳舞流程。`);
    router.push(AppRoutes.startFromVoice(result.directNavigationLabel ?? transcript));
  };

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={[styles.headerWrap, { paddingTop: headerTopPadding }]}>
          <View style={styles.headerCard}>
            <View style={styles.header}>
              <TopIconButton icon="line.3.horizontal" onPress={() => router.push(AppRoutes.me)} />
              <Text style={styles.brand}>跳舞吧</Text>
              <TopIconButton icon="mic.fill" onPress={openVoiceModal} />
            </View>
            <Text style={styles.headerHint}>今天想去哪儿跳？点一下就能开始。</Text>
          </View>
        </View>

        <View style={styles.heroWrap}>
          <Pressable onPress={() => router.push(AppRoutes.start)} style={({ pressed }) => [styles.heroButton, { minHeight: heroHeight }, pressed && styles.pressed]}>
            <View style={styles.heroIconCircle}>
              <IconSymbol name="play.circle.fill" size={64} color="#D91E12" />
            </View>
            <Text style={styles.heroText}>开始跳舞</Text>
            <Text style={styles.heroSubtext}>拍一张现场照片，附近舞团会自动帮你判断。</Text>
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
            onPress={openVoiceModal}
          />
        </View>
      </ScrollView>

      <Modal animationType="fade" transparent visible={voiceModalVisible} onRequestClose={closeVoiceModal}>
        <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.modalRoot}>
          <Pressable style={styles.modalBackdrop} onPress={closeVoiceModal} />
          <View style={styles.modalCard}>
            <View style={styles.modalMicHalo}>
              <View style={[styles.modalMicCore, voiceListening && styles.modalMicCoreListening]}>
                <IconSymbol name="waveform" size={42} color="#B42318" />
              </View>
            </View>
            <Text style={styles.modalTitle}>{voiceListening ? '正在听你说话…' : '直接说地点，也可以顺手改字'}</Text>
            <Text style={styles.modalSubtitle}>例如：青年路广场、人民公园南门、滨江路口。</Text>
            <TextInput
              ref={inputRef}
              value={voiceDraft}
              onChangeText={setVoiceDraft}
              placeholder="我想去哪里跳舞"
              placeholderTextColor="#9C9187"
              style={styles.voiceInput}
              returnKeyType="done"
              onSubmitEditing={() => void handleVoiceSearch()}
            />
            <View style={styles.quickPhraseWrap}>
              {QUICK_PHRASES.map((phrase) => (
                <Pressable key={phrase} onPress={() => setVoiceDraft(phrase)} style={({ pressed }) => [styles.quickPhraseChip, pressed && styles.pressed]}>
                  <Text style={styles.quickPhraseText}>{phrase}</Text>
                </Pressable>
              ))}
            </View>
            <View style={styles.modalActions}>
              <Pressable onPress={closeVoiceModal} style={({ pressed }) => [styles.secondaryAction, pressed && styles.pressed]}>
                <Text style={styles.secondaryActionText}>取消</Text>
              </Pressable>
              <Pressable onPress={() => void handleVoiceSearch()} style={({ pressed }) => [styles.primaryAction, pressed && styles.pressed]}>
                <Text style={styles.primaryActionText}>马上找舞团</Text>
              </Pressable>
            </View>
          </View>
        </KeyboardAvoidingView>
      </Modal>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingBottom: 156,
    backgroundColor: '#FBF8F2',
  },
  headerWrap: {
    paddingBottom: 10,
  },
  headerCard: {
    borderRadius: 30,
    backgroundColor: '#FFFDF9',
    paddingHorizontal: 18,
    paddingTop: 16,
    paddingBottom: 18,
    borderWidth: 1,
    borderColor: '#EFE6DB',
    shadowColor: '#E9D8C7',
    shadowOpacity: 0.12,
    shadowRadius: 14,
    shadowOffset: { width: 0, height: 6 },
    elevation: 2,
  },
  header: {
    minHeight: 62,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingBottom: 14,
    borderBottomWidth: 1,
    borderBottomColor: '#EEE6DD',
  },
  headerHint: {
    marginTop: 12,
    fontSize: 18,
    lineHeight: 26,
    color: '#74685E',
    textAlign: 'center',
  },
  topIconButton: {
    width: 52,
    height: 52,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 18,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#F0E3D8',
  },
  brand: {
    fontSize: 32,
    lineHeight: 38,
    fontWeight: '900',
    color: '#B42318',
    letterSpacing: 1,
  },
  heroWrap: {
    paddingTop: 22,
    paddingBottom: 28,
    alignItems: 'center',
  },
  heroButton: {
    width: '100%',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 44,
    backgroundColor: '#D91E12',
    paddingHorizontal: 22,
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
  heroSubtext: {
    marginTop: 12,
    fontSize: 19,
    lineHeight: 28,
    color: '#FFF2EA',
    textAlign: 'center',
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
  modalRoot: {
    flex: 1,
    justifyContent: 'flex-end',
  },
  modalBackdrop: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(36, 31, 26, 0.34)',
  },
  modalCard: {
    borderTopLeftRadius: 34,
    borderTopRightRadius: 34,
    backgroundColor: '#FFFDF9',
    paddingHorizontal: 22,
    paddingTop: 28,
    paddingBottom: 28,
    gap: 16,
  },
  modalMicHalo: {
    alignItems: 'center',
  },
  modalMicCore: {
    width: 102,
    height: 102,
    borderRadius: 51,
    backgroundColor: '#FFF1E5',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#F4D0B1',
  },
  modalMicCoreListening: {
    backgroundColor: '#FFE4D0',
    transform: [{ scale: 1.02 }],
  },
  modalTitle: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
    textAlign: 'center',
  },
  modalSubtitle: {
    fontSize: 18,
    lineHeight: 27,
    color: '#74685E',
    textAlign: 'center',
  },
  voiceInput: {
    borderRadius: 24,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#EEDFCF',
    paddingHorizontal: 18,
    paddingVertical: 18,
    fontSize: 22,
    lineHeight: 30,
    color: '#241F1A',
  },
  quickPhraseWrap: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
  },
  quickPhraseChip: {
    borderRadius: 18,
    backgroundColor: '#FFF4E8',
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  quickPhraseText: {
    fontSize: 17,
    lineHeight: 22,
    fontWeight: '800',
    color: '#B54C13',
  },
  modalActions: {
    flexDirection: 'row',
    gap: 12,
  },
  secondaryAction: {
    flex: 1,
    minHeight: 58,
    borderRadius: 22,
    backgroundColor: '#F4EDE3',
    alignItems: 'center',
    justifyContent: 'center',
  },
  primaryAction: {
    flex: 1.4,
    minHeight: 58,
    borderRadius: 22,
    backgroundColor: '#D91E12',
    alignItems: 'center',
    justifyContent: 'center',
  },
  secondaryActionText: {
    fontSize: 20,
    lineHeight: 24,
    fontWeight: '900',
    color: '#241F1A',
  },
  primaryActionText: {
    fontSize: 20,
    lineHeight: 24,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  pressed: {
    opacity: 0.93,
    transform: [{ scale: 0.985 }],
  },
});
''',
    ROOT / 'app/(tabs)/groups.tsx': '''import { FlatList, Pressable, StyleSheet, Text, View } from 'react-native';
import { router } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { ScreenContainer } from '@/components/screen-container';
import { AppRoutes } from '@/lib/app-routes';
import { useDanceApp } from '@/lib/dance-app-context';
import { formatDistance } from '@/lib/dance-utils';

export default function GroupsScreen() {
  const { visibleGroups } = useDanceApp();
  const insets = useSafeAreaInsets();
  const headerTopPadding = Math.max(8, Math.min(16, insets.top * 0.18));

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
      <FlatList
        data={visibleGroups}
        keyExtractor={(item) => item.id}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.container}
        ListHeaderComponent={
          <View style={[styles.headerShell, { paddingTop: headerTopPadding }]}>
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
    paddingBottom: 160,
  },
  headerShell: {
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
    shadowOpacity: 0.12,
    shadowRadius: 14,
    shadowOffset: { width: 0, height: 6 },
    elevation: 2,
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
    ROOT / 'app/start-dancing.tsx': '''import { router, useLocalSearchParams } from 'expo-router';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

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
  const params = useLocalSearchParams<{ voiceLabel?: string }>();
  const insets = useSafeAreaInsets();
  const { nearbyGroups, startDancing, state } = useDanceApp();
  const result = state.lastStartResult;
  const voiceLabel = typeof params.voiceLabel === 'string' ? params.voiceLabel.trim() : '';
  const shortVoiceLabel = voiceLabel.length > 8 ? `${voiceLabel.slice(0, 8)}…` : voiceLabel;
  const headerTopPadding = Math.max(8, Math.min(16, insets.top * 0.18));

  const handleStart = async (forceCreate = false) => {
    const nextResult = await startDancing({ createNew: forceCreate, labelOverride: voiceLabel || undefined });
    if (!nextResult) return;
    Alert.alert(nextResult.type === 'created' ? '舞团创建成功' : '加入成功', `已进入 ${nextResult.group.name}`);
  };

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]" edges={['top', 'bottom', 'left', 'right']}>
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={[styles.headerShell, { paddingTop: headerTopPadding }]}>
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
          {voiceLabel ? (
            <View style={styles.voiceHintCard}>
              <Text style={styles.voiceHintLabel}>我听到你说</Text>
              <Text style={styles.voiceHintText}>{voiceLabel}</Text>
              <Text style={styles.voiceHintSubtext}>如果附近没有同名舞团，可以直接按这个地点创建新的舞团。</Text>
            </View>
          ) : null}
          <View style={styles.stepsWrap}>
            <StepRow index={1} label="获取当前位置" />
            <StepRow index={2} label="拍一张现场照片" />
            <StepRow index={3} label="优先加入 200 米内舞团" />
            <StepRow index={4} label={voiceLabel ? `没有结果时按“${shortVoiceLabel || '当前位置'}”创建` : '没有舞团时创建新舞团'} />
          </View>
          <View style={styles.actionGap}>
            {voiceLabel ? (
              <>
                <PrimaryButton label={`按“${shortVoiceLabel}”创建舞团`} icon="mic.fill" onPress={() => handleStart(true)} />
                <PrimaryButton label="先看附近现成舞团" icon="person.2.fill" tone="light" onPress={() => router.push(AppRoutes.groups)} />
              </>
            ) : (
              <>
                <PrimaryButton label="立即开始" icon="play.circle.fill" onPress={() => handleStart(false)} />
                <PrimaryButton label="直接创建新的舞团" icon="plus.circle.fill" tone="light" onPress={() => handleStart(true)} />
              </>
            )}
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
    paddingBottom: 40,
    gap: 18,
  },
  headerShell: {
    paddingBottom: 8,
  },
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderRadius: 24,
    backgroundColor: '#FFFDF9',
    borderWidth: 1,
    borderColor: '#EFE6DB',
    shadowColor: '#E9D8C7',
    shadowOpacity: 0.12,
    shadowRadius: 14,
    shadowOffset: { width: 0, height: 6 },
    elevation: 2,
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
  voiceHintCard: {
    borderRadius: 24,
    backgroundColor: '#FFF5EA',
    borderWidth: 1,
    borderColor: '#F3D7BC',
    paddingHorizontal: 16,
    paddingVertical: 16,
    gap: 6,
  },
  voiceHintLabel: {
    fontSize: 16,
    lineHeight: 20,
    fontWeight: '800',
    color: '#B85A17',
  },
  voiceHintText: {
    fontSize: 24,
    lineHeight: 30,
    fontWeight: '900',
    color: '#241F1A',
  },
  voiceHintSubtext: {
    fontSize: 17,
    lineHeight: 25,
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
    ROOT / 'app/group/[id].tsx': '''import { useEffect } from 'react';
import { router, useLocalSearchParams } from 'expo-router';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from 'react-native';
import { Image } from 'expo-image';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { Badge, PrimaryButton } from '@/components/dance-ui';
import { ScreenContainer } from '@/components/screen-container';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { AppRoutes, type RouteSource, getBackRoute } from '@/lib/app-routes';
import { useDanceApp } from '@/lib/dance-app-context';
import { appHaptics } from '@/lib/haptics';
import { formatDistance } from '@/lib/dance-utils';

export default function GroupDetailScreen() {
  const params = useLocalSearchParams<{ id: string; from?: string }>();
  const { width } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const { getGroupById, state, shareGroup, joinGroup, wakeGroup, setSelectedGroup } = useDanceApp();
  const group = getGroupById(params.id);
  const nickname = state.profile?.nickname ?? '舞友';
  const isCaptain = group?.captainName === nickname;
  const routeSource = (params.from as RouteSource | undefined) ?? 'groups';
  const backRoute = getBackRoute(routeSource);
  const imageHeight = Math.max(210, Math.min(290, width * 0.58));
  const headerTopPadding = Math.max(8, Math.min(16, insets.top * 0.18));

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

  const handleNavigate = () => {
    appHaptics.light();
    router.push(AppRoutes.map(group.id, routeSource));
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
        <View style={[styles.headerShell, { paddingTop: headerTopPadding }]}>
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
          <Text style={styles.tipText}>导航入口现在会先留在应用内，让你随时可以返回这一页。</Text>
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
    paddingBottom: 40,
    gap: 16,
  },
  headerShell: {
    paddingBottom: 8,
  },
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderRadius: 24,
    backgroundColor: '#FFFDF9',
    borderWidth: 1,
    borderColor: '#EFE6DB',
    shadowColor: '#E9D8C7',
    shadowOpacity: 0.12,
    shadowRadius: 14,
    shadowOffset: { width: 0, height: 6 },
    elevation: 2,
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
  tipText: {
    fontSize: 17,
    lineHeight: 26,
    color: '#B85A17',
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
    ROOT / 'app/map/[id].tsx': '''import { router, useLocalSearchParams } from 'expo-router';
import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { PrimaryButton } from '@/components/dance-ui';
import { ScreenContainer } from '@/components/screen-container';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { AppRoutes, type RouteSource } from '@/lib/app-routes';
import { useDanceApp } from '@/lib/dance-app-context';
import { formatDistance, openNavigation } from '@/lib/dance-utils';

export default function MapPreviewScreen() {
  const params = useLocalSearchParams<{ id: string; from?: string }>();
  const insets = useSafeAreaInsets();
  const { getGroupById } = useDanceApp();
  const group = getGroupById(params.id);
  const routeSource = (params.from as RouteSource | undefined) ?? 'groups';
  const headerTopPadding = Math.max(8, Math.min(16, insets.top * 0.18));

  if (!group) {
    return (
      <ScreenContainer className="items-center justify-center px-6" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
        <Text style={styles.emptyTitle}>地图信息暂时不可用</Text>
        <Pressable onPress={() => router.replace(AppRoutes.groups)} style={({ pressed }) => [styles.inlineBackButton, pressed && styles.pressed]}>
          <Text style={styles.inlineBackText}>回到舞队列表</Text>
        </Pressable>
      </ScreenContainer>
    );
  }

  const handleOpenSystemMap = () => {
    Alert.alert('打开手机地图', '将跳转到手机地图继续导航；完成后请再回到“跳舞吧”。', [
      { text: '取消', style: 'cancel' },
      {
        text: '打开',
        onPress: () => {
          void openNavigation(group.coordinates, group.locationLabel);
        },
      },
    ]);
  };

  return (
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]" edges={['top', 'bottom', 'left', 'right']}>
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={[styles.headerShell, { paddingTop: headerTopPadding }]}>
          <View style={styles.topBar}>
            <Pressable onPress={() => router.replace(AppRoutes.group(group.id, routeSource))} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
              <IconSymbol name="chevron.right" size={28} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
            </Pressable>
            <Text style={styles.pageTitle}>去舞团的路</Text>
            <Pressable onPress={() => router.replace(AppRoutes.group(group.id, routeSource))} style={({ pressed }) => [styles.sideButton, pressed && styles.pressed]}>
              <Text style={styles.sideButtonText}>详情</Text>
            </Pressable>
          </View>
        </View>

        <View style={styles.mapCard}>
          <View style={styles.mapTopRow}>
            <View style={styles.mapBadge}>
              <IconSymbol name="map.fill" size={34} color="#B42318" />
            </View>
            <View style={styles.mapSummary}>
              <Text style={styles.mapTitle}>先在应用里确认路线，再决定是否打开手机地图。</Text>
              <Text style={styles.mapSubtitle}>这样看完以后，随时都能直接返回上一层。</Text>
            </View>
          </View>
          <View style={styles.fakeMap}>
            <View style={styles.fakeMapRoute} />
            <View style={[styles.mapDot, styles.mapDotStart]} />
            <View style={[styles.mapDot, styles.mapDotEnd]} />
            <Text style={styles.fakeMapLabelTop}>你现在的位置</Text>
            <Text style={styles.fakeMapLabelBottom}>{group.locationLabel}</Text>
          </View>
        </View>

        <View style={styles.infoCard}>
          <Text style={styles.sectionTitle}>{group.name}</Text>
          <Text style={styles.infoText}>集合点：{group.locationLabel}</Text>
          <Text style={styles.infoText}>地址：{group.address}</Text>
          <Text style={styles.infoText}>大约距离：{formatDistance(group.distanceMeters)}</Text>
          <Text style={styles.infoText}>坐标：{group.coordinates.latitude.toFixed(4)}，{group.coordinates.longitude.toFixed(4)}</Text>
        </View>

        <View style={styles.tipCard}>
          <Text style={styles.tipTitle}>退出方式更清楚了</Text>
          <Text style={styles.tipBody}>你现在看到的是应用内导航页。点左上角返回，或点下面的“回到舞团详情”，都能直接回去；只有在你确认后，才会再打开手机地图。</Text>
        </View>

        <View style={styles.actionWrap}>
          <PrimaryButton label="打开手机地图" icon="arrow.triangle.turn.up.right.diamond.fill" onPress={handleOpenSystemMap} />
          <PrimaryButton label="回到舞团详情" icon="person.2.fill" tone="light" onPress={() => router.replace(AppRoutes.group(group.id, routeSource))} />
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingBottom: 40,
    gap: 16,
  },
  headerShell: {
    paddingBottom: 8,
  },
  topBar: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderRadius: 24,
    backgroundColor: '#FFFDF9',
    borderWidth: 1,
    borderColor: '#EFE6DB',
    shadowColor: '#E9D8C7',
    shadowOpacity: 0.12,
    shadowRadius: 14,
    shadowOffset: { width: 0, height: 6 },
    elevation: 2,
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
  mapCard: {
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#EFE3D8',
    paddingHorizontal: 20,
    paddingVertical: 20,
    gap: 18,
  },
  mapTopRow: {
    flexDirection: 'row',
    gap: 14,
    alignItems: 'center',
  },
  mapBadge: {
    width: 68,
    height: 68,
    borderRadius: 34,
    backgroundColor: '#FFF1E5',
    alignItems: 'center',
    justifyContent: 'center',
  },
  mapSummary: {
    flex: 1,
    gap: 4,
  },
  mapTitle: {
    fontSize: 24,
    lineHeight: 30,
    fontWeight: '900',
    color: '#241F1A',
  },
  mapSubtitle: {
    fontSize: 17,
    lineHeight: 25,
    color: '#74685E',
  },
  fakeMap: {
    height: 240,
    borderRadius: 28,
    backgroundColor: '#F5EEE2',
    position: 'relative',
    overflow: 'hidden',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  fakeMapRoute: {
    position: 'absolute',
    left: '22%',
    top: '18%',
    width: '52%',
    height: '56%',
    borderWidth: 10,
    borderColor: '#FFB06E',
    borderRadius: 80,
    transform: [{ rotate: '12deg' }],
  },
  mapDot: {
    position: 'absolute',
    width: 22,
    height: 22,
    borderRadius: 11,
  },
  mapDotStart: {
    left: '18%',
    top: '24%',
    backgroundColor: '#2E9E5B',
  },
  mapDotEnd: {
    right: '18%',
    bottom: '20%',
    backgroundColor: '#D91E12',
  },
  fakeMapLabelTop: {
    position: 'absolute',
    top: 26,
    left: 22,
    fontSize: 18,
    lineHeight: 24,
    fontWeight: '800',
    color: '#2A6B45',
  },
  fakeMapLabelBottom: {
    position: 'absolute',
    right: 22,
    bottom: 24,
    fontSize: 18,
    lineHeight: 24,
    fontWeight: '800',
    color: '#9F2D17',
    maxWidth: '52%',
    textAlign: 'right',
  },
  infoCard: {
    borderRadius: 28,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#EFE3D8',
    paddingHorizontal: 20,
    paddingVertical: 20,
    gap: 8,
  },
  sectionTitle: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#241F1A',
    marginBottom: 4,
  },
  infoText: {
    fontSize: 18,
    lineHeight: 28,
    color: '#5F564F',
  },
  tipCard: {
    borderRadius: 28,
    backgroundColor: '#FFF8EF',
    borderWidth: 1,
    borderColor: '#EEDFCF',
    paddingHorizontal: 20,
    paddingVertical: 18,
    gap: 8,
  },
  tipTitle: {
    fontSize: 24,
    lineHeight: 30,
    fontWeight: '900',
    color: '#241F1A',
  },
  tipBody: {
    fontSize: 18,
    lineHeight: 28,
    color: '#74685E',
  },
  actionWrap: {
    gap: 12,
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
}

for path, content in FILES.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).rstrip() + '\n', encoding='utf-8')

print('patched', len(FILES), 'files')

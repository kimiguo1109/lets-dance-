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

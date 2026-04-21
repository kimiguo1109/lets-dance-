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

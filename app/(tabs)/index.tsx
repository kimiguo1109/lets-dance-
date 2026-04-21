import { router } from 'expo-router';
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

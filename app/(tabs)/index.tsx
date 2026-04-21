import { router } from 'expo-router';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { ScreenContainer } from '@/components/screen-container';
import { IconSymbol } from '@/components/ui/icon-symbol';
import { useDanceApp } from '@/lib/dance-app-context';
import { appHaptics } from '@/lib/haptics';

function TopIconButton({ icon, onPress }: { icon: React.ComponentProps<typeof IconSymbol>['name']; onPress: () => void }) {
  return (
    <Pressable onPress={onPress} style={({ pressed }) => [styles.topIconButton, pressed && styles.pressed]}>
      <IconSymbol name={icon} size={32} color={icon === 'mic.fill' ? '#B42318' : '#1F1F1F'} />
    </Pressable>
  );
}

function ActionTile({
  label,
  icon,
  backgroundColor,
  iconColor,
  badge,
  onPress,
}: {
  label: string;
  icon: React.ComponentProps<typeof IconSymbol>['name'];
  backgroundColor: string;
  iconColor: string;
  badge?: string;
  onPress: () => void;
}) {
  return (
    <Pressable onPress={onPress} style={({ pressed }) => [styles.tile, { backgroundColor }, pressed && styles.pressed]}>
      {badge ? (
        <View style={styles.badge}>
          <Text style={styles.badgeText}>{badge}</Text>
        </View>
      ) : null}
      <View style={styles.tileIconWrap}>
        <IconSymbol name={icon} size={54} color={iconColor} />
      </View>
      <Text style={styles.tileLabel}>{label}</Text>
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
    <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
      <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <TopIconButton icon="line.3.horizontal" onPress={() => appHaptics.light()} />
          <Text style={styles.brand}>跳舞吧</Text>
          <TopIconButton icon="mic.fill" onPress={() => router.push('/voice-search')} />
        </View>

        <View style={styles.heroWrap}>
          <Pressable
            onPress={() => router.push('/start-dancing')}
            style={({ pressed }) => [styles.heroButton, pressed && styles.pressed]}
          >
            <View style={styles.heroIconCircle}>
              <IconSymbol name="play.circle.fill" size={66} color="#D91E12" />
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
            onPress={openNearby}
          />
          <ActionTile
            label="说话找地"
            icon="mic.fill"
            backgroundColor="#FF7A12"
            iconColor="#40200A"
            onPress={() => router.push('/voice-search')}
          />
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingBottom: 144,
    backgroundColor: '#FBF8F2',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: 8,
    paddingBottom: 18,
    borderBottomWidth: 1,
    borderBottomColor: '#EEE6DD',
  },
  topIconButton: {
    width: 54,
    height: 54,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 18,
  },
  brand: {
    fontSize: 34,
    lineHeight: 40,
    fontWeight: '900',
    color: '#B42318',
    letterSpacing: 1,
  },
  heroWrap: {
    paddingTop: 44,
    paddingBottom: 44,
    alignItems: 'center',
  },
  heroButton: {
    width: '88%',
    maxWidth: 520,
    minHeight: 360,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 54,
    backgroundColor: '#D91E12',
    shadowColor: '#E45C2F',
    shadowOpacity: 0.28,
    shadowRadius: 28,
    shadowOffset: { width: 0, height: 14 },
    elevation: 8,
  },
  heroIconCircle: {
    width: 108,
    height: 108,
    borderRadius: 54,
    backgroundColor: '#FFFFFF',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 28,
  },
  heroText: {
    fontSize: 36,
    lineHeight: 42,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  tilesRow: {
    flexDirection: 'row',
    gap: 16,
    paddingBottom: 16,
  },
  tile: {
    flex: 1,
    minHeight: 208,
    borderRadius: 32,
    paddingHorizontal: 18,
    paddingVertical: 20,
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
    marginTop: 8,
  },
  tileLabel: {
    textAlign: 'center',
    fontSize: 24,
    lineHeight: 30,
    fontWeight: '900',
    color: '#241F1A',
  },
  badge: {
    position: 'absolute',
    top: 14,
    right: 14,
    minWidth: 42,
    height: 42,
    borderRadius: 21,
    backgroundColor: '#C62828',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 10,
  },
  badgeText: {
    color: '#FFFFFF',
    fontSize: 22,
    lineHeight: 26,
    fontWeight: '900',
  },
  pressed: {
    opacity: 0.93,
    transform: [{ scale: 0.98 }],
  },
});

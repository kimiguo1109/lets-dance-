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

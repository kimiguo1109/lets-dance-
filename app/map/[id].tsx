import { router, useLocalSearchParams } from 'expo-router';
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

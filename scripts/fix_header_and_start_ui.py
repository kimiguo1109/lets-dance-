from pathlib import Path
from textwrap import dedent

ROOT = Path('/home/ubuntu/lets-dance-mvp')

files = {
    'app/(tabs)/index.tsx': dedent('''
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
                <View style={styles.headerWrap}>
                  <View style={styles.header}>
                    <TopIconButton icon="line.3.horizontal" onPress={() => appHaptics.light()} />
                    <Text style={styles.brand}>跳舞吧</Text>
                    <TopIconButton icon="mic.fill" onPress={() => router.push('/voice-search')} />
                  </View>
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
            paddingTop: 10,
            paddingBottom: 144,
            backgroundColor: '#FBF8F2',
          },
          headerWrap: {
            paddingTop: 6,
            paddingBottom: 10,
          },
          header: {
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between',
            paddingTop: 4,
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
            paddingTop: 34,
            paddingBottom: 40,
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
    ''').strip() + '\n',
    'app/(tabs)/groups.tsx': dedent('''
        import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';
        import { router } from 'expo-router';

        import { ScreenContainer } from '@/components/screen-container';
        import { useDanceApp } from '@/lib/dance-app-context';
        import { formatDistance } from '@/lib/dance-utils';

        export default function GroupsScreen() {
          const { visibleGroups } = useDanceApp();

          return (
            <ScreenContainer className="px-5" containerClassName="bg-[#FBF8F2]" safeAreaClassName="bg-[#FBF8F2]">
              <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
                <View style={styles.headerCard}>
                  <Text style={styles.title}>附近舞团</Text>
                  <Text style={styles.subtitle}>按距离从近到远排列，点一下就能查看详情。</Text>
                </View>

                <View style={styles.listWrap}>
                  {visibleGroups.map((group) => (
                    <Pressable key={group.id} onPress={() => router.push(`/group/${group.id}`)} style={({ pressed }) => [styles.groupCard, pressed && styles.pressed]}>
                      <Text style={styles.groupName}>{group.name}</Text>
                      <Text style={styles.groupMeta}>队长：{group.captainName}</Text>
                      <Text style={styles.groupMeta}>{group.address}</Text>
                      <View style={styles.bottomRow}>
                        <Text style={styles.distance}>{formatDistance(group.distanceMeters)}</Text>
                        <Text style={[styles.status, group.status === 'active' ? styles.active : styles.sleeping]}>{group.status === 'active' ? '活跃中' : '已休眠'}</Text>
                      </View>
                    </Pressable>
                  ))}
                </View>
              </ScrollView>
            </ScreenContainer>
          );
        }

        const styles = StyleSheet.create({
          container: {
            paddingTop: 14,
            paddingBottom: 144,
            gap: 18,
          },
          headerCard: {
            borderRadius: 30,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 22,
            paddingTop: 24,
            paddingBottom: 24,
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
            lineHeight: 30,
            color: '#74685E',
          },
          listWrap: {
            gap: 14,
          },
          groupCard: {
            borderRadius: 28,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 22,
            paddingVertical: 22,
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
            lineHeight: 30,
            color: '#5F564F',
          },
          bottomRow: {
            marginTop: 12,
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
          },
          distance: {
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '800',
            color: '#D75A18',
          },
          status: {
            fontSize: 19,
            lineHeight: 24,
            fontWeight: '800',
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
    ''').strip() + '\n',
    'app/start-dancing.tsx': dedent('''
        import { router } from 'expo-router';
        import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

        import { ScreenContainer } from '@/components/screen-container';
        import { IconSymbol } from '@/components/ui/icon-symbol';
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
                  <Pressable onPress={() => router.back()} style={({ pressed }) => [styles.backButton, pressed && styles.pressed]}>
                    <IconSymbol name="chevron.right" size={30} color="#241F1A" style={{ transform: [{ rotate: '180deg' }] }} />
                  </Pressable>
                  <Text style={styles.pageTitle}>开始跳舞</Text>
                  <View style={styles.topPlaceholder} />
                </View>

                <View style={styles.heroCard}>
                  <Text style={styles.heroSubtitle}>这条路径会依次完成定位、拍照、附近判断、创建或加入舞团。</Text>
                  <View style={styles.stepsWrap}>
                    <StepRow index={1} label="获取当前位置" />
                    <StepRow index={2} label="拍一张现场照片" />
                    <StepRow index={3} label="优先加入 200 米内舞团" />
                    <StepRow index={4} label="没有舞团时创建新舞团" />
                  </View>
                  <Pressable onPress={() => handleStart(false)} style={({ pressed }) => [styles.primaryAction, pressed && styles.pressed]}>
                    <IconSymbol name="play.circle.fill" size={34} color="#FFFFFF" />
                    <Text style={styles.primaryActionText}>立即开始</Text>
                  </Pressable>
                  <Pressable onPress={() => handleStart(true)} style={({ pressed }) => [styles.secondaryAction, pressed && styles.pressed]}>
                    <IconSymbol name="plus.circle.fill" size={30} color="#241F1A" />
                    <Text style={styles.secondaryActionText}>附近有舞团也创建新的</Text>
                  </Pressable>
                </View>

                <View style={styles.sectionCard}>
                  <Text style={styles.sectionTitle}>附近可加入舞团</Text>
                  <Text style={styles.sectionSubtitle}>如果你只想先看看，也可以直接进入详情。</Text>
                  <View style={styles.groupList}>
                    {nearbyGroups.slice(0, 2).map((group) => (
                      <Pressable key={group.id} onPress={() => router.push(`/group/${group.id}`)} style={({ pressed }) => [styles.groupRow, pressed && styles.pressed]}>
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
                    <View style={styles.resultActions}>
                      <Pressable onPress={() => router.push(`/group/${result.group.id}`)} style={({ pressed }) => [styles.resultButton, pressed && styles.pressed]}>
                        <Text style={styles.resultButtonText}>查看详情</Text>
                      </Pressable>
                      <Pressable onPress={() => router.push('/share-card')} style={({ pressed }) => [styles.resultButtonLight, pressed && styles.pressed]}>
                        <Text style={styles.resultButtonLightText}>分享卡片</Text>
                      </Pressable>
                    </View>
                  </View>
                ) : null}
              </ScrollView>
            </ScreenContainer>
          );
        }

        const styles = StyleSheet.create({
          container: {
            paddingTop: 10,
            paddingBottom: 40,
            gap: 18,
          },
          topBar: {
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between',
            paddingBottom: 8,
          },
          backButton: {
            width: 52,
            height: 52,
            borderRadius: 18,
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#FFFFFF',
          },
          topPlaceholder: {
            width: 52,
            height: 52,
          },
          pageTitle: {
            flex: 1,
            textAlign: 'center',
            fontSize: 32,
            lineHeight: 38,
            fontWeight: '900',
            color: '#241F1A',
          },
          heroCard: {
            borderRadius: 32,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 22,
            paddingTop: 22,
            paddingBottom: 22,
            shadowColor: '#E9D8C7',
            shadowOpacity: 0.1,
            shadowRadius: 12,
            shadowOffset: { width: 0, height: 4 },
            elevation: 1,
          },
          heroSubtitle: {
            fontSize: 19,
            lineHeight: 30,
            color: '#74685E',
            marginBottom: 18,
          },
          stepsWrap: {
            gap: 14,
            marginBottom: 22,
          },
          stepRow: {
            flexDirection: 'row',
            alignItems: 'center',
            gap: 14,
          },
          stepBadge: {
            width: 38,
            height: 38,
            borderRadius: 19,
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#FFEDD8',
          },
          stepBadgeText: {
            fontSize: 20,
            lineHeight: 24,
            fontWeight: '900',
            color: '#D75A18',
          },
          stepText: {
            flex: 1,
            fontSize: 22,
            lineHeight: 30,
            fontWeight: '800',
            color: '#D75A18',
          },
          primaryAction: {
            marginBottom: 14,
            minHeight: 68,
            borderRadius: 26,
            backgroundColor: '#D91E12',
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 12,
          },
          primaryActionText: {
            fontSize: 24,
            lineHeight: 30,
            fontWeight: '900',
            color: '#FFFFFF',
          },
          secondaryAction: {
            minHeight: 68,
            borderRadius: 26,
            backgroundColor: '#FFF8EF',
            borderWidth: 1,
            borderColor: '#F0E4D6',
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 12,
          },
          secondaryActionText: {
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '900',
            color: '#241F1A',
          },
          sectionCard: {
            borderRadius: 32,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 22,
            paddingTop: 22,
            paddingBottom: 22,
          },
          sectionTitle: {
            fontSize: 30,
            lineHeight: 36,
            fontWeight: '900',
            color: '#241F1A',
          },
          sectionSubtitle: {
            marginTop: 8,
            fontSize: 19,
            lineHeight: 28,
            color: '#74685E',
          },
          groupList: {
            marginTop: 18,
            gap: 16,
          },
          groupRow: {
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            gap: 16,
          },
          groupInfo: {
            flex: 1,
          },
          groupRight: {
            alignItems: 'flex-end',
            gap: 12,
            paddingTop: 4,
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
            lineHeight: 30,
            color: '#5F564F',
          },
          distance: {
            marginTop: 10,
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '900',
            color: '#D75A18',
          },
          groupStatus: {
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
          memberCount: {
            fontSize: 20,
            lineHeight: 26,
            fontWeight: '800',
            color: '#241F1A',
          },
          resultCard: {
            borderRadius: 32,
            backgroundColor: '#FFFFFF',
            paddingHorizontal: 22,
            paddingTop: 22,
            paddingBottom: 22,
          },
          resultTitle: {
            fontSize: 28,
            lineHeight: 34,
            fontWeight: '900',
            color: '#241F1A',
            marginBottom: 10,
          },
          resultText: {
            fontSize: 20,
            lineHeight: 30,
            color: '#5F564F',
          },
          resultActions: {
            marginTop: 18,
            gap: 12,
          },
          resultButton: {
            minHeight: 64,
            borderRadius: 24,
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#D91E12',
          },
          resultButtonText: {
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '900',
            color: '#FFFFFF',
          },
          resultButtonLight: {
            minHeight: 64,
            borderRadius: 24,
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#FFF8EF',
            borderWidth: 1,
            borderColor: '#F0E4D6',
          },
          resultButtonLightText: {
            fontSize: 22,
            lineHeight: 28,
            fontWeight: '900',
            color: '#241F1A',
          },
          pressed: {
            opacity: 0.94,
            transform: [{ scale: 0.99 }],
          },
        });
    ''').strip() + '\n',
}

for relative_path, content in files.items():
    path = ROOT / relative_path
    path.write_text(content, encoding='utf-8')

print(f'patched {len(files)} files')

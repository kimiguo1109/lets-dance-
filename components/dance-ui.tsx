import { Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { Image } from 'expo-image';
import { Link, type Href } from 'expo-router';

import { IconSymbol } from '@/components/ui/icon-symbol';
import { formatDistance } from '@/lib/dance-utils';
import type { DanceGroup } from '@/lib/dance-types';

export function SectionTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <View style={styles.sectionTitleWrap}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {subtitle ? <Text style={styles.sectionSubtitle}>{subtitle}</Text> : null}
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
  const primary = tone === 'primary';
  return (
    <Pressable
      onPress={onPress}
      style={({ pressed }) => [styles.buttonBase, primary ? styles.buttonPrimary : styles.buttonLight, pressed && styles.pressed]}
    >
      {icon ? <IconSymbol name={icon} size={24} color={primary ? '#FFFFFF' : '#2C241E'} /> : null}
      <Text style={primary ? styles.buttonPrimaryText : styles.buttonLightText}>{label}</Text>
    </Pressable>
  );
}

export function TinyAction({
  label,
  icon,
  onPress,
}: {
  label: string;
  icon: React.ComponentProps<typeof IconSymbol>['name'];
  onPress: () => void;
}) {
  return (
    <Pressable onPress={onPress} style={({ pressed }) => [styles.tinyAction, pressed && styles.pressed]}>
      <IconSymbol name={icon} size={22} color="#D75A18" />
      <Text style={styles.tinyActionText}>{label}</Text>
    </Pressable>
  );
}

export function Badge({ label, tone = 'active' }: { label: string; tone?: 'active' | 'sleeping' | 'warm' }) {
  return <Text style={[styles.badge, tone === 'active' ? styles.badgeActive : tone === 'sleeping' ? styles.badgeSleeping : styles.badgeWarm]}>{label}</Text>;
}

export function GroupCard({ group, caption, href }: { group: DanceGroup; caption?: string; href: Href }) {
  return (
            <Link href={href} asChild>

      <Pressable style={({ pressed }) => [styles.groupCard, pressed && styles.pressed]}>
        <View style={styles.groupCardTop}>
          <View style={styles.groupCardInfo}>
            <Text style={styles.groupCardName}>{group.name}</Text>
            <Text style={styles.groupCardMeta}>队长：{group.captainName}</Text>
            <Text style={styles.groupCardMeta}>{group.address}</Text>
          </View>
          <Badge label={group.status === 'active' ? '活跃中' : '已休眠'} tone={group.status === 'active' ? 'active' : 'sleeping'} />
        </View>
        <View style={styles.groupCardBottom}>
          <Text style={styles.groupCardDistance}>{formatDistance(group.distanceMeters)}</Text>
          <Text style={styles.groupCardCount}>当前 {group.memberCount} 人</Text>
        </View>
        {caption ? <Text style={styles.groupCardCaption}>{caption}</Text> : null}
      </Pressable>
    </Link>
  );
}

export function HeroCard({ title, value, detail }: { title: string; value: string; detail: string }) {
  return (
    <View style={styles.heroCard}>
      <Text style={styles.heroLabel}>{title}</Text>
      <Text style={styles.heroValue}>{value}</Text>
      <Text style={styles.heroDetail}>{detail}</Text>
    </View>
  );
}

export function ProfileAvatar({ uri, fallback }: { uri?: string; fallback: string }) {
  if (uri) {
    return <Image source={{ uri }} style={styles.avatar} contentFit="cover" />;
  }
  return (
    <View style={[styles.avatar, styles.avatarFallback]}>
      <Text style={styles.avatarText}>{fallback.slice(0, 1)}</Text>
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
      style={styles.cardInput}
      returnKeyType="done"
    />
  );
}

const styles = StyleSheet.create({
  sectionTitleWrap: {
    gap: 4,
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
    color: '#6B625B',
  },
  buttonBase: {
    minHeight: 60,
    borderRadius: 24,
    paddingHorizontal: 20,
    paddingVertical: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 10,
    shadowColor: '#D95C2C',
    shadowOpacity: 0.08,
    shadowRadius: 14,
    shadowOffset: { width: 0, height: 6 },
    elevation: 2,
  },
  buttonPrimary: {
    backgroundColor: '#D91E12',
  },
  buttonLight: {
    backgroundColor: '#FFF8EF',
    borderWidth: 1,
    borderColor: '#EEDFCF',
  },
  buttonPrimaryText: {
    fontSize: 20,
    lineHeight: 26,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  buttonLightText: {
    fontSize: 20,
    lineHeight: 26,
    fontWeight: '900',
    color: '#2C241E',
  },
  tinyAction: {
    minHeight: 56,
    borderRadius: 22,
    paddingHorizontal: 14,
    paddingVertical: 14,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#FFF8EF',
    borderWidth: 1,
    borderColor: '#EEDFCF',
  },
  tinyActionText: {
    fontSize: 17,
    lineHeight: 22,
    fontWeight: '800',
    color: '#241F1A',
  },
  badge: {
    alignSelf: 'flex-start',
    borderRadius: 999,
    paddingHorizontal: 12,
    paddingVertical: 8,
    fontSize: 15,
    lineHeight: 18,
    fontWeight: '800',
  },
  badgeActive: {
    backgroundColor: '#E9F8EF',
    color: '#2E9E5B',
  },
  badgeSleeping: {
    backgroundColor: '#E8F3F0',
    color: '#4EB7A5',
  },
  badgeWarm: {
    backgroundColor: '#FFF1DD',
    color: '#D75A18',
  },
  groupCard: {
    borderRadius: 28,
    backgroundColor: '#FFFFFF',
    paddingHorizontal: 18,
    paddingVertical: 18,
    gap: 14,
    shadowColor: '#D6451D',
    shadowOpacity: 0.06,
    shadowRadius: 12,
    shadowOffset: { width: 0, height: 6 },
    elevation: 2,
  },
  groupCardTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: 12,
  },
  groupCardInfo: {
    flex: 1,
    gap: 6,
  },
  groupCardName: {
    fontSize: 26,
    lineHeight: 32,
    fontWeight: '900',
    color: '#241F1A',
  },
  groupCardMeta: {
    fontSize: 18,
    lineHeight: 26,
    color: '#5F564F',
  },
  groupCardBottom: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 12,
    flexWrap: 'wrap',
  },
  groupCardDistance: {
    fontSize: 21,
    lineHeight: 26,
    fontWeight: '900',
    color: '#D75A18',
  },
  groupCardCount: {
    fontSize: 18,
    lineHeight: 24,
    fontWeight: '800',
    color: '#241F1A',
  },
  groupCardCaption: {
    fontSize: 17,
    lineHeight: 25,
    color: '#6B625B',
  },
  heroCard: {
    flex: 1,
    borderRadius: 24,
    paddingHorizontal: 16,
    paddingVertical: 16,
    gap: 6,
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#EFE3D8',
  },
  heroLabel: {
    fontSize: 15,
    lineHeight: 20,
    fontWeight: '700',
    color: '#8A7C72',
  },
  heroValue: {
    fontSize: 26,
    lineHeight: 32,
    fontWeight: '900',
    color: '#241F1A',
  },
  heroDetail: {
    fontSize: 16,
    lineHeight: 22,
    color: '#6B625B',
  },
  avatar: {
    width: 86,
    height: 86,
    borderRadius: 43,
  },
  avatarFallback: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#D91E12',
  },
  avatarText: {
    fontSize: 28,
    lineHeight: 34,
    fontWeight: '900',
    color: '#FFFFFF',
  },
  cardInput: {
    borderRadius: 22,
    borderWidth: 1,
    borderColor: '#E9D9C8',
    backgroundColor: '#FFFDF9',
    paddingHorizontal: 18,
    paddingVertical: 16,
    fontSize: 18,
    lineHeight: 24,
    fontWeight: '700',
    color: '#241F1A',
  },
  pressed: {
    opacity: 0.92,
    transform: [{ scale: 0.985 }],
  },
});

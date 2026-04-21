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

import { StyleSheet, View, type ViewProps } from 'react-native';
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

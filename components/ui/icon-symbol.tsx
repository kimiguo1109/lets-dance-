import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import { SymbolWeight, SymbolViewProps } from 'expo-symbols';
import { ComponentProps } from 'react';
import { OpaqueColorValue, type StyleProp, type TextStyle } from 'react-native';

type IconMapping = Record<SymbolViewProps['name'], ComponentProps<typeof MaterialIcons>['name']>;
type IconSymbolName = keyof typeof MAPPING;

const MAPPING = {
  'house.fill': 'home',
  'paperplane.fill': 'send',
  'chevron.left.forwardslash.chevron.right': 'code',
  'chevron.right': 'chevron-right',
  'figure.dance': 'directions-run',
  'person.2.fill': 'groups',
  'person.crop.circle.fill': 'account-circle',
  'location.fill': 'location-on',
  'mic.fill': 'mic',
  'camera.fill': 'photo-camera',
  'arrow.triangle.turn.up.right.diamond.fill': 'share',
  'map.fill': 'map',
  'phone.fill': 'phone',
  'plus.circle.fill': 'add-circle',
  'clock.fill': 'schedule',
  'star.fill': 'star',
  'waveform': 'graphic-eq',
} as IconMapping;

export function IconSymbol({
  name,
  size = 24,
  color,
  style,
}: {
  name: IconSymbolName;
  size?: number;
  color: string | OpaqueColorValue;
  style?: StyleProp<TextStyle>;
  weight?: SymbolWeight;
}) {
  return <MaterialIcons color={color} size={size} name={MAPPING[name]} style={style} />;
}

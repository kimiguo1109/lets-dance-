import { Tabs } from 'expo-router';
import { Platform } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { HapticTab } from '@/components/haptic-tab';
import { IconSymbol } from '@/components/ui/icon-symbol';

export default function TabLayout() {
  const insets = useSafeAreaInsets();
  const bottomPadding = Platform.OS === 'web' ? 12 : Math.max(insets.bottom, 10);
  const tabBarHeight = 72 + bottomPadding;

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarButton: HapticTab,
        tabBarActiveTintColor: '#FFFFFF',
        tabBarInactiveTintColor: '#8D8A86',
        tabBarStyle: {
          position: 'absolute',
          left: 14,
          right: 14,
          bottom: 10,
          height: tabBarHeight,
          paddingTop: 8,
          paddingBottom: bottomPadding,
          backgroundColor: '#FFF9F3',
          borderTopWidth: 0,
          borderRadius: 26,
          shadowColor: '#D6451D',
          shadowOpacity: 0.12,
          shadowRadius: 18,
          shadowOffset: { width: 0, height: 8 },
          elevation: 4,
        },
        tabBarLabelStyle: {
          fontSize: 14,
          fontWeight: '800',
          marginTop: 2,
        },
        tabBarItemStyle: {
          marginHorizontal: 2,
          marginVertical: 4,
          borderRadius: 18,
        },
        tabBarActiveBackgroundColor: '#FF6A2A',
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: '首页',
          tabBarIcon: ({ color }) => <IconSymbol size={26} name="house.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="groups"
        options={{
          title: '舞队',
          tabBarIcon: ({ color }) => <IconSymbol size={26} name="person.2.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="messages"
        options={{
          title: '消息',
          tabBarIcon: ({ color }) => <IconSymbol size={26} name="bell.fill" color={color} />,
        }}
      />
      <Tabs.Screen
        name="me"
        options={{
          title: '我的',
          tabBarIcon: ({ color }) => <IconSymbol size={26} name="person.crop.circle.fill" color={color} />,
        }}
      />
    </Tabs>
  );
}

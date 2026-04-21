import { useMemo, useState } from 'react';
import { ScrollView, Text, View } from 'react-native';

import { ScreenContainer } from '@/components/screen-container';
import { CardInput, GroupCard, SectionTitle } from '@/components/dance-ui';
import { useDanceApp } from '@/lib/dance-app-context';
import { searchGroups } from '@/lib/dance-utils';

export default function GroupsScreen() {
  const { visibleGroups } = useDanceApp();
  const [keyword, setKeyword] = useState('');
  const groups = useMemo(() => searchGroups(visibleGroups, keyword), [visibleGroups, keyword]);

  return (
    <ScreenContainer className="px-5 pb-6">
      <ScrollView contentContainerStyle={{ paddingBottom: 24, gap: 18 }} showsVerticalScrollIndicator={false}>
        <View className="mt-2 gap-3">
          <SectionTitle title="附近舞团" subtitle="按距离排序，休眠舞团会自动下沉显示。" />
          <CardInput value={keyword} onChangeText={setKeyword} placeholder="搜索舞团名、地址或队长称呼" />
        </View>
        <View className="gap-4">
          {groups.map((group) => (
            <GroupCard key={group.id} group={group} href={`/group/${group.id}`} />
          ))}
          {groups.length === 0 ? <Text className="text-[18px] leading-7 text-muted">没有找到匹配舞团，可以试试语音找地或直接开始跳舞。</Text> : null}
        </View>
      </ScrollView>
    </ScreenContainer>
  );
}

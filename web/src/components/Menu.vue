<template>
    <n-layout-sider bordered collapse-mode="width" :collapsed-width="64" :width="240" :collapsed="collapsed"
        show-trigger @collapse="collapsed = true" @expand="collapsed = false">
        <n-menu :collapsed="collapsed" :collapsed-width="64" :collapsed-icon-size="22" :options="menuOptions"
            :expand-icon="expandIcon" :value="value()" :default-expanded-keys="['anime-view']" />
    </n-layout-sider>
</template>

<script setup>
import { NMenu, NIcon, NLayoutSider, NBadge } from 'naive-ui'
import { ref, h, computed, inject } from 'vue'
import { CaretDownOutline, LayersOutline, SettingsOutline, HomeOutline, CaretForwardCircleOutline, ArrowDownCircleOutline } from '@vicons/ionicons5'

import { RouterLink, useRoute } from 'vue-router'
import { animeState } from '@/common_state.js'

const route = useRoute()
const animations = inject('animations')

function createItem(to, v, icon) {
    return {
        label: () => h(RouterLink, { to: to }, v),
        key: to,
        icon: () => h(NIcon, null, { default: () => h(icon) })
    }
}

function createAnimeItem(item) {
    return {
        label: () => h(RouterLink, { to: "/anime-view/" + item.animation_id }, item.name),
        key: "/anime-view/" + item.animation_id,
        icon: () => h(NBadge, { value: item.total_episode - item.watched_episode }, h(NIcon, null, { default: () => h(CaretForwardCircleOutline) }))
    }
}

const menuOptions = computed(() => [
    createItem('/wdy', () => '动画列表', HomeOutline),
    createItem('/add-anime', '添加动画', SettingsOutline),
    createItem('/download', '下载进度', ArrowDownCircleOutline),
    {
        label: '动画',
        key: 'anime-view',
        icon: () => h(NIcon, null, { default: () => h(LayersOutline) }),
        children: animations.value.map(createAnimeItem)
    }
])
const collapsed = ref(false)
function expandIcon() {
    return h(NIcon, null, { default: () => h(CaretDownOutline) })
}
function value() {
    return route.path
}
// https://lain.bgm.tv/r/400/pic/cover/l/7f/1c/526973_zE0vy.jpg
</script>

<style scoped></style>

<template>
    <n-space vertical>
        <VideoPlayer v-if="episodes.length > 0" :url="episodes[episode_idx]?.url ?? ''"
            v-model:current_time="current_time" :time="time" @pause="onPause" @done="onDone" />
    </n-space>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import VideoPlayer from './VideoPlayer.vue';
import { NButton, NSpace, useMessage } from 'naive-ui';
import axios from 'axios';
import { useRoute } from 'vue-router';

const route = useRoute()
const message = useMessage()

const episodes = ref([])
const episode_idx = ref(0)
const time = ref(0)
const current_time = ref(0)

let latest_update_time = 0

function updateWatched(idx, time) {
    axios.post('/api/set_watched_time', {
        animation_id: route.params.animation_id,
        watched_episode: idx,
        watched_episode_time: time
    }).catch(err => {
        message.error("更新观看时间失败: " + err.message)
    })
}

watch(() => current_time.value, (newTime) => {
    if (Math.abs(newTime - latest_update_time) > 5) {
        updateWatched(episode_idx.value, newTime)
        latest_update_time = newTime
    }
})

function onPause() {
    updateWatched(episode_idx.value, current_time.value)
}

function onDone() {
    latest_update_time = -100
    episode_idx.value++
    time.value = -1
    updateWatched(episode_idx.value, 0)
}

function reload(animation_id) {
    axios.post('/api/get_animation_info', {
        animation_id: animation_id
    }).catch(err => {
        message.error("获取动画信息失败: " + err.message)
    }).then(res => {
        episodes.value = res.data.episodes
        episode_idx.value = res.data.watched_episode
        time.value = res.data.watched_episode_time
    })
}

watch(() => route.params.animation_id, (newId) => {
    reload(newId)
})

onMounted(() => {
    reload(route.params.animation_id)
})

</script>

<style scoped></style>
<template>
    <VideoPlayer url="https://vjs.zencdn.net/v/oceans.mp4" />
    <n-button @click="changeAnime">切换动画</n-button>
</template>

<script setup>
import VideoPlayer from './VideoPlayer.vue';
import { animeState } from '@/common_state.js'
import { NButton } from 'naive-ui';

function changeAnime() {
    animeState.anime.push(animeState.anime[0]);

}


let player = null;
</script>

<style scoped></style>
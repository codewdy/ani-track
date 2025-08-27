<template>
    <div :style="`width: 100%; max-width: ${width}px; margin: 0 auto; border: 1px solid black;`">
        <div ref="videoRef"></div>
    </div>
</template>

<script setup>
import XGPlayer from 'xgplayer';
import 'xgplayer/dist/index.min.css';
import { watch, onMounted, ref, defineProps } from 'vue';

const { url = '', width = 800 } = defineProps(['url', 'width'])


let player = null;
const videoRef = ref();

watch(() => url, (newUrl) => {
    if (player) {
        player.src = newUrl
    }
})

onMounted(() => {
    console.log(videoRef)
    player = new XGPlayer({
        el: videoRef.value,
        url: url,
        fluid: true,
    });
})
</script>

<style scoped></style>
<template>
    <div :style="`width: 100%; max-width: ${width}px; margin: 0 auto; border: 1px solid black;`">
        <div :id="dynamicId"></div>
    </div>
</template>

<script setup>
import Player from 'xgplayer';
import 'xgplayer/dist/index.min.css';
import { watch, onMounted, ref, defineProps } from 'vue';
import { getRandomInt } from '@/lib/Random';

const { url = '', width = 800 } = defineProps(['url', 'width'])


let player = null;
const dynamicId = ref('player-' + getRandomInt(0, 1000000));

watch(() => url, (newUrl) => {
    if (player) {
        player.src = newUrl
    }
})

onMounted(() => {
    player = new Player({
        id: dynamicId.value,
        url: url,
        fluid: true,
    });
})
</script>

<style scoped></style>
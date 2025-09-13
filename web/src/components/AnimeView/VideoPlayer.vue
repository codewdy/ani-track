<template>
    <p v-if="url === ''"> 看完了！ </p>
    <p v-if="url !== ''"> 当前视频源: {{ url }} </p>
    <div :style="`width: 100%; max-width: ${width}px; margin: 0 auto; border: 1px solid black; float: left;`">
        <div ref="videoRef"></div>
    </div>
</template>

<script setup>
import XGPlayer, { Events } from 'xgplayer';
import 'xgplayer/dist/index.min.css';
import { watch, onMounted, ref, defineProps, defineEmits, defineModel } from 'vue';

const { url = '', width = 800, time = 0 } = defineProps(['url', 'width', 'time'])
const current_time = defineModel('current_time', { default: 0 })
const emit = defineEmits(['done', 'pause'])

let player = null;
const videoRef = ref();

watch(() => [url, time], ([newUrl, newTime]) => {
    if (player) {
        let autoplay = false;
        if (newTime < 0) {
            newTime = 0
            autoplay = true
        }
        player.src = newUrl || "http://"
        player.currentTime = newTime
        if (autoplay && newUrl !== '') {
            player.play()
        }
    }
})

onMounted(() => {
    player = new XGPlayer({
        el: videoRef.value,
        url: url,
        fluid: true,
        startTime: time,
    });
    player.on(Events.TIME_UPDATE, () => {
        current_time.value = player.currentTime
    })
    player.on(Events.PAUSE, () => {
        if (url !== '') {
            emit('pause')
        }
    })
    player.on(Events.ENDED, () => {
        if (url !== '') {
            emit('done')
        }
    })
})
</script>

<style scoped></style>
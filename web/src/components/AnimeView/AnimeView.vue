<template>
    <n-space vertical>
        <VideoPlayer v-if="url" :url="url" />
    </n-space>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import VideoPlayer from './VideoPlayer.vue';
import { NButton, NSpace } from 'naive-ui';
import axios from 'axios';
import { useRoute } from 'vue-router';

const url = ref("")
const route = useRoute()

onMounted(() => {
    axios.post('/api/get_animation_info', {
        animation_id: route.params.id
    }).then(res => {
        console.log(res.data)
        url.value = res.data.episodes[0].url
    })
})

</script>

<style scoped></style>
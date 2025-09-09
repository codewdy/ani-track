<template>
    <slot></slot>
</template>

<script setup>
import { onMounted, onUnmounted, ref, provide } from 'vue'
import { useMessage } from 'naive-ui'
import axios from 'axios';

const animations = ref([])
const message = useMessage()
let timer = null
let version = ""

function reload() {
    axios.post('/api/get_animations', { version: version }).catch(err => {
        message.error("获取动画列表失败: " + err.message)
    }).then((response) => {
        let data = response.data
        if (data.is_new) {
            version = data.version
            animations.value = data.animations
        }
    })
}

onMounted(() => {
    reload()
    timer = setInterval(() => {
        reload()
    }, 60000)
})

onUnmounted(() => {
    clearInterval(timer)
})

provide('animations', animations)
provide('reload_animations', reload)

</script>

<style scoped></style>

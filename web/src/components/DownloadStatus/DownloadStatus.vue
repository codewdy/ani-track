<template>
    <n-list>
        <n-list-item v-for="download in downloads">
            <DownloadUnit :download="download" />
        </n-list-item>
    </n-list>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { NList, NListItem, useMessage } from 'naive-ui'
import DownloadUnit from './DownloadUnit.vue'
import axios from 'axios';
const message = useMessage()

const downloads = ref([])
let timer = null

function get_download() {
    axios.post('/api/get_download_manager_status', {}).catch(err => {
        message.error("获取下载状态失败: " + err.message)
    }).then((response) => {
        downloads.value = response.data.downloading.concat(response.data.pending)
    })
}

onMounted(() => {
    get_download()
    timer = setInterval(() => {
        get_download()
    }, 1000)
})

onUnmounted(() => {
    clearInterval(timer)
})

</script>

<style scoped></style>
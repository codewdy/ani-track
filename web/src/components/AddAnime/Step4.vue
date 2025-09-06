<template>
    <n-space vertical>
        <p>动画名称：{{ animation }}</p>
        <a :href="'https://bgm.tv/subject/' + bangumi?.id" target="_blank">番剧名称：{{ bangumi?.name }}</a>
        <a :href="channel?.url" target="_blank">渠道名称：{{ channel?.name }}</a>
        <n-space>
            <n-tag v-for="item in channel?.episodes" :key="item.name">
                <a :href="item.url" target="_blank">{{ item.name }}</a>
            </n-tag>
        </n-space>
        <n-button @click="submit">提交</n-button>
    </n-space>
</template>

<script setup>
import { NSpace, NButton, NTag } from 'naive-ui'
const emit = defineEmits(["submit"])
const { animation, bangumi, channel } = defineProps(["animation", "bangumi", "channel"])
const submit = () => {
    emit("submit")
}
</script>

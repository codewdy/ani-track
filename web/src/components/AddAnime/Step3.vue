<template>
    <n-space vertical>
        <p>搜索资源:</p>
        <n-input v-model:value="search" @keyup.enter="search_channel" type="text" placeholder="碧蓝之海"
            style="max-width: 800px;" />
        <n-button @click="search_channel" :disabled="search.length === 0">搜索</n-button>
        <n-select :loading="loading" v-model:value="selected_value" :options="search_result" placeholder="请选择"
            style="max-width: 800px;">
        </n-select>
        <n-space vertical v-if="selected_value">
            <a :href="selected_value.url" target="_blank">{{ selected_value.name }}</a>
            <n-space>
                <n-tag v-for="item in selected_value.episodes" :key="item.name">
                    <a :href="item.url" target="_blank">{{ item.name }}</a>
                </n-tag>
            </n-space>
        </n-space>
        <n-button @click="submit" :disabled="selected_value === null">下一步</n-button>
    </n-space>
</template>

<script setup>
import { NSpace, NInput, NButton, NSelect, NTag, useMessage } from 'naive-ui'
import { ref } from 'vue'
import axios from 'axios'
const message = useMessage()
const search = defineModel("search", { default: "" })
const emit = defineEmits(["submit"])
const search_result = ref([])
const selected_value = ref(null)
const loading = ref(false)

function search_channel() {
    const messageReactive = message.loading("搜索中(大概需要一分钟)", {
        duration: 0
    });
    search_result.value = []
    selected_value.value = null
    loading.value = true
    axios.post("/api/search_channel", {
        keyword: search.value
    }).catch(err => {
        loading.value = false
        messageReactive.destroy()
        message.error("搜索失败: " + err.message)
    }).then(res => {
        search_result.value = res.data.channels.map((item) => {
            return {
                label: item.name,
                value: item
            }
        })
        loading.value = false
        messageReactive.destroy()
        message.success("搜索完成")
    })
}

const submit = () => {
    emit("submit", selected_value.value)
}
</script>

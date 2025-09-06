<template>
    <n-space vertical>
        <p>搜索Bangumi:</p>
        <n-input v-model:value="search" @keyup.enter="search_bangumi" type="text" placeholder="三月的狮子"
            style="max-width: 800px;" />
        <n-button @click="search_bangumi" :disabled="search.length === 0">搜索</n-button>
        <n-select :loading="loading" v-model:value="selected_value" :options="search_result" placeholder="请选择"
            style="max-width: 800px;">
        </n-select>
        <n-space v-show="selected_value">
            <img :src="selected_value?.image" alt="" style="max-width: 200px;" />
            <n-space vertical>
                <p>名称: {{ selected_value?.name }}</p>
                <a :href="'https://bgm.tv/subject/' + selected_value?.id">ID: {{ selected_value?.id }}</a>
            </n-space>
        </n-space>
        <n-button @click="submit" :disabled="selected_value === null">下一步</n-button>
    </n-space>
</template>

<script setup>
import { NSpace, NInput, NButton, NSelect, useMessage } from 'naive-ui'
import { ref } from 'vue'
import axios from 'axios'
const message = useMessage()
const search = defineModel("search", { default: "" })
const emit = defineEmits(["submit"])
const search_result = ref([])
const selected_value = ref(null)
const loading = ref(false)

function search_bangumi() {
    const messageReactive = message.loading("搜索中", {
        duration: 0
    });
    search_result.value = []
    selected_value.value = null
    loading.value = true
    axios.post("/api/search_bangumi", {
        keyword: search.value
    }).catch(err => {
        loading.value = false
        messageReactive.destroy()
        message.error("搜索失败: " + err.message)
    }).then(res => {
        search_result.value = res.data.animations.map((item) => {
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

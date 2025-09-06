<template>
    <n-space vertical>
        <p>搜索Bangumi:</p>
        <n-input v-model:value="search" @keyup.enter="search_bangumi" type="text" placeholder="三月的狮子"
            style="max-width: 500px;" />
        <n-button @click="search_bangumi" :disabled="search.length === 0">搜索</n-button>
        <n-radio-group v-model:value="selected_value" size="large">
            <n-space>
                <n-radio-button v-for="item in search_result" :key="item.name" :value="item" :label="item.name" />
            </n-space>
        </n-radio-group>
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
import { NSpace, NInput, NButton, NRadioGroup, NRadioButton } from 'naive-ui'
import { ref } from 'vue'
import axios from 'axios'
const search = defineModel("search", { default: "" })
const emit = defineEmits(["submit"])
const search_result = ref([])
const selected_value = ref(null)

function search_bangumi() {
    axios.post("/api/search_bangumi", {
        keyword: search.value
    }).then(res => {
        selected_value.value = null
        search_result.value = res.data.animations.map(item => ({
            name: item.name,
            id: item.id,
            image: item.image
        }))
    })
}

const submit = () => {
    emit("submit", selected_value.value)
}
</script>

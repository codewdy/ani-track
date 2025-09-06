<template>
    <n-space vertical>
        <p>动画名称:</p>
        <n-input v-model:value="name" @keyup.enter="submit" type="text" placeholder="三月的狮子" style="max-width: 500px;" />
        <n-button @click="submit" :disabled="name.length === 0">下一步</n-button>
    </n-space>
</template>

<script setup>
import { NSpace, NInput, NButton } from 'naive-ui'
const name = defineModel("name", { default: "" })
const emit = defineEmits(["submit"])
const submit = () => {
    emit("submit", name.value)
}
</script>

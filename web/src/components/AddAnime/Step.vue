<template>
    <n-space vertical>
        <n-steps v-model:current="step" :status="status">
            <n-step title="动画名称" :description="step1" :disabled="maxStep < 1" />
            <n-step title="Bangumi搜索" :description="step2" :disabled="maxStep < 2" />
            <n-step title="动画源搜索" :description="step3" :disabled="maxStep < 3" />
            <n-step title="确认" :description="step4" :disabled="maxStep < 4" />
        </n-steps>
    </n-space>
</template>

<script setup>
import { defineComponent, ref } from "vue";
import { NSteps, NStep, NSpace } from 'naive-ui'
const status = ref("process");
const step = defineModel("step", { default: 1 })
const maxStep = defineModel("maxStep", { default: 1 })
const { step1, step2, step3, step4 } = defineProps(["step1", "step2", "step3", "step4"])
</script>
<template>
    <n-space vertical>
        <Step :max-step="max_step" v-model:step="step" :step1="step1" :step2="step2" :step3="step3" :step4="step4" />
        <n-divider />
        <Step1 v-show="step === 1" @submit="step1_submit" />
        <Step2 v-show="step === 2" @submit="step2_submit" v-model:search="search" />
    </n-space>
</template>

<script setup>
import { ref } from 'vue'
import Step from './Step.vue'
import { NSpace, NDivider } from 'naive-ui'
import Step1 from './Step1.vue';
import Step2 from './Step2.vue';

const step = ref(1)
const step1 = ref("")
const step2 = ref("")
const step3 = ref("")
const step4 = ref("")
const max_step = ref(1)
const search = ref("")

function step1_submit(name) {
    if (max_step.value === 1) {
        search.value = name
    }
    step1.value = name
    max_step.value = Math.max(max_step.value, 2)
    step.value = 2
}

function step2_submit(search) {
    step2.value = search.name
    max_step.value = Math.max(max_step.value, 3)
    step.value = 3
}

</script>

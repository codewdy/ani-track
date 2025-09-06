<template>
    <n-space vertical>
        <Step :max-step="max_step" v-model:step="step" :step1="step1" :step2="step2" :step3="step3" :step4="step4" />
        <n-divider />
        <Step1 v-show="step === 1" @submit="step1_submit" />
        <Step2 v-show="step === 2" @submit="step2_submit" v-model:search="search_1" />
        <Step3 v-show="step === 3" @submit="step3_submit" v-model:search="search_2" />
    </n-space>
</template>

<script setup>
import { ref } from 'vue'
import Step from './Step.vue'
import { NSpace, NDivider } from 'naive-ui'
import Step1 from './Step1.vue';
import Step2 from './Step2.vue';
import Step3 from './Step3.vue';

const step = ref(1)
const step1 = ref("")
const step2 = ref("")
const step3 = ref("")
const step4 = ref("")
const max_step = ref(1)
const search_1 = ref("")
const search_2 = ref("")
const animation = ref("")
const bangumi = ref(null)
const channel = ref(null)

function step1_submit(name) {
    if (max_step.value === 1) {
        search_1.value = name
        search_2.value = name
    }
    step1.value = name
    max_step.value = Math.max(max_step.value, 2)
    step.value = 2
    animation.value = name
}

function step2_submit(search) {
    step2.value = search.name
    max_step.value = Math.max(max_step.value, 3)
    step.value = 3
    bangumi.value = search
}

function step3_submit(search) {
    step3.value = search.name
    max_step.value = Math.max(max_step.value, 4)
    step.value = 4
    channel.value = search
}

</script>

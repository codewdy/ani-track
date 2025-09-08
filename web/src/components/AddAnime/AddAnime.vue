<template>
    <n-space vertical>
        <Step :max-step="max_step" v-model:step="step" :step1="step1" :step2="step2" :step3="step3" :step4="step4" />
        <n-divider />
        <Step1 v-show="step === 1" @submit="step1_submit" />
        <Step2 v-show="step === 2" @submit="step2_submit" v-model:search="search_1" />
        <Step3 v-show="step === 3" @submit="step3_submit" v-model:search="search_2" />
        <Step4 v-show="step === 4" @submit="step4_submit" :animation="animation" :bangumi="bangumi"
            :channel="channel" />
    </n-space>
</template>

<script setup>
import { ref } from 'vue'
import Step from './Step.vue'
import { NSpace, NDivider, useMessage } from 'naive-ui'
import axios from 'axios'
import Step1 from './Step1.vue';
import Step2 from './Step2.vue';
import Step3 from './Step3.vue';
import Step4 from './Step4.vue';
const message = useMessage()

const emit = defineEmits(["done"])
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

function step4_submit() {
    const messageReactive = message.loading("提交中", {
        duration: 0
    });
    axios.post("/api/add_animation", {
        name: animation.value,
        bangumi_id: bangumi.value.id,
        icon_url: bangumi.value.image,
        status: "wanted",
        channel_name: channel.value.name,
        channel_search_name: channel.value.search_name,
        channel_url: channel.value.url,
        channel_source_key: channel.value.source_key,
    }).catch(err => {
        messageReactive.destroy()
        message.error("提交失败: " + err.message)
    }).then(res => {
        messageReactive.destroy()
        message.success("提交成功")
        emit("done")
    })
}

</script>

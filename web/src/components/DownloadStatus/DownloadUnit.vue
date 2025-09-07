<template>
    <n-thing>
        <template #header>
            {{ download.resource_name }}
        </template>
        {{ download.status }}
    </n-thing>
</template>

<script setup>
import { defineProps } from 'vue'
import { NThing } from 'naive-ui'
const { download } = defineProps(["download"])


</script>

<style scoped></style>
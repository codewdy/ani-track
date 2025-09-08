<template>
    <AddAnime :key="key" @done="reset" />
</template>

<script setup>
import AddAnime from './AddAnime.vue';
import { ref } from 'vue';
const key = ref(0);

function reset() {
    key.value += 1;
}

</script>

<style scoped></style>

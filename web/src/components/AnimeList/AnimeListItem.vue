<template>
  <n-card>
    <template #cover>
      <img :src="item.cover" class="card-cover">
    </template>
    <n-h2 class="card-name"> {{ item.name }}</n-h2>
    <n-h3 class="card-fullname"> {{ item.fullname }} </n-h3>

    <p class="card-watch"> 观看： {{ item.watched }} / {{ item.downloaded }} / {{ item.total }}</p>
  <n-dropdown trigger="hover" :options="options" @select="handleSelect">
    <n-button>在看</n-button>
  </n-dropdown>
</n-card>
</template>

<script setup>
import { ref } from 'vue'
import { NH2, NH3, NCard, NDropdown, NButton } from 'naive-ui'


const item = ref({
    name: "动画名称",
    fullname: "动画全名",
    cover: "https://07akioni.oss-cn-beijing.aliyuncs.com/07akioni.jpeg",
    watched: 10, downloaded: 20, total: 30,
    status: "在看",
});


const options = [
{
    label: '想看',
    key: 'atlantis nahamas, nassau'
},
{
    label: '在看',
    key: 'marina bay sands',
},
{
    label: '看过',
    key: 'brown\'s hotel, london'
},
{
    label: '搁置',
    key: 'the beverly hills hotel, los angeles'
}
];

</script>


<style scoped>
.n-card {
  max-width: 200px;
}
.card-name {
    margin:10px 0px 0px 0px;
}
.card-fullname {
    margin:0px 0px 0px 0px;
}
.card-watch {
    margin:0px 0px 10px 0px;
}
.card-cover {
width: 100%; aspect-ratio: 3 / 4; object-fit: cover;
}
</style>

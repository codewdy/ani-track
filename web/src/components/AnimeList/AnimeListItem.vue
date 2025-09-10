<template>
  <n-space>
    <n-card v-for="item in animations">
      <template #cover>
        <img :src="item.icon_url" class="card-cover">
      </template>
      <n-h2 class="card-name">
        <a :href="'/anime-view/' + item.animation_id">{{ item.name }}</a>
      </n-h2>

      <p class="card-watch"> 观看： {{ item.watched_episode }} / {{ item.total_episode }}</p>
      <n-dropdown trigger="hover" :options="options" @select="(status) => set_status(item.animation_id, status)">
        <n-button>{{ watch_status[item.status] }}</n-button>
      </n-dropdown>
    </n-card>
  </n-space>
</template>

<script setup>
import { ref, inject } from 'vue'
import { NH2, NCard, NDropdown, NButton, NSpace } from 'naive-ui'
import { watch_status, all_watch_status } from '@/lib/schema'

const animations = inject('animations')

const options = all_watch_status.map(status => ({
  label: watch_status[status],
  key: status
}));

function set_status(animation_id, status) {
  // TODO: Send request to server
  animations.value.forEach(item => {
    if (item.animation_id == animation_id) {
      item.status = status
    }
  })
}

</script>


<style scoped>
.n-card {
  max-width: 200px;
}

.card-name {
  margin: 10px 0px 0px 0px;
}

.card-fullname {
  margin: 0px 0px 0px 0px;
}

.card-watch {
  margin: 0px 0px 10px 0px;
}

.card-cover {
  width: 100%;
  aspect-ratio: 3 / 4;
  object-fit: cover;
}
</style>

import { reactive } from 'vue';

export const animeState = reactive({
  anime: [
    { id: 1, name: '银魂', watched: 10, downloaded: 20, total: 30 },
    { id: 2, name: '银魂2', watched: 10, downloaded: 20, total: 30 },
  ]
});

import { createRouter, createWebHistory } from 'vue-router';
import NotFound from '@/components/NotFound.vue';
import AnimeList from '@/components/AnimeList/AnimeList.vue';
import AddAnimeContainer from '@/components/AddAnime/AddAnimeContainer.vue';
import DownloadStatus from '@/components/DownloadStatus/DownloadStatus.vue';
import AnimeView from './components/AnimeView/AnimeView.vue';

const routes = [
  {
    path: '/',
    redirect: '/wdy',
  },
  {
    path: '/wdy',
    name: 'wdy',
    component: AnimeList,
  },
  {
    path: '/download',
    name: 'download',
    component: DownloadStatus,
  },
  {
    path: '/anime-view/:animation_id',
    name: 'anime-view',
    component: AnimeView,
  },
  {
    path: '/add-anime',
    name: 'add-anime',
    component: AddAnimeContainer,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
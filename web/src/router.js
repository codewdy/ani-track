import { createRouter, createWebHistory } from 'vue-router';
import AnimeView from '@/components/AnimeView/AnimeView.vue';
import NotFound from '@/components/NotFound.vue';
import AnimeList from '@/components/AnimeList/AnimeList.vue';

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
    path: '/anime-view/:id',
    name: 'anime-view',
    component: AnimeView,
  },
  {
    path: '/config',
    name: 'config',
    component: AnimeView,
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
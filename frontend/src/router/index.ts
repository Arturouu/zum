import { createRouter, createWebHistory } from 'vue-router'
import BienvenidaView from '../views/BienvenidaView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'bienvenida', component: BienvenidaView },
    { path: '/inicio', name: 'inicio', component: () => import('../views/PuntoDePartidaView.vue') },
    // MapLibre pesa bastante: el mapa se carga recién al entrar a /mapa
    { path: '/mapa', name: 'mapa', component: () => import('../views/MapView.vue') },
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

export default router

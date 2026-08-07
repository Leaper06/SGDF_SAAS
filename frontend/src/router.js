import { createRouter, createWebHistory } from 'vue-router'
import { userToken } from './stores/authStore.js'

const routes = [
  { path: '/login', name: 'login', component: () => import('./components/LoginView.vue') },
  { path: '/unite', name: 'unite', component: () => import('./components/UniteView.vue') },
  { path: '/camps', name: 'camps', component: () => import('./components/CalendarView.vue') },
  { path: '/planning', name: 'planning', component: () => import('./components/PlanningView.vue') },
  { path: '/activity', name: 'activity', component: () => import('./components/ActivityDetail.vue') },
  { path: '/menu', name: 'menu', component: () => import('./components/MenuBuilder.vue') },
  { path: '/recipes', name: 'recipes', component: () => import('./components/RecipeCatalog.vue') },
  { path: '/recipe-builder', name: 'recipe_builder', component: () => import('./components/RecipeBuilder.vue') },
  { path: '/logistique', name: 'logistique', component: () => import('./components/LogistiqueView.vue') },
  { path: '/profile', name: 'profile', component: () => import('./components/ProfileView.vue') },
  { path: '/mentions-legales', name: 'MentionsLegales', component: () => import('./components/MentionsLegales.vue') },
  { path: '/:pathMatch(.*)*', redirect: '/camps' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// --- SÉCURITÉ (Navigation Guard) ---
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!userToken.value

  if (to.name !== 'login' && to.name !== 'MentionsLegales' && !isAuthenticated) {
    next({ name: 'login' })
  } else if (to.name === 'login' && isAuthenticated) {
    next({ name: 'unite' })
  } else {
    next()
  }
})

export default router
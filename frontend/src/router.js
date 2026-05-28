import { createRouter, createWebHistory } from 'vue-router'
import { userToken } from './stores/authStore.js'

// Import de tous tes composants
import LoginView from './components/LoginView.vue'
import UniteView from './components/UniteView.vue'
import CalendarView from './components/CalendarView.vue'
import PlanningView from './components/PlanningView.vue'
import ActivityDetail from './components/ActivityDetail.vue'
import MenuBuilder from './components/MenuBuilder.vue'
import RecipeCatalog from './components/RecipeCatalog.vue'
import RecipeBuilder from './components/RecipeBuilder.vue'
import logitique from './components/LogistiqueView.vue'
import ProfileView from './components/ProfileView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView },
  { path: '/unite', name: 'unite', component: UniteView },
  { path: '/camps', name: 'camps', component: CalendarView },
  { path: '/planning', name: 'planning', component: PlanningView },
  { path: '/activity', name: 'activity', component: ActivityDetail },
  { path: '/menu', name: 'menu', component: MenuBuilder },
  { path: '/recipes', name: 'recipes', component: RecipeCatalog },
  { path: '/recipe-builder', name: 'recipe_builder', component: RecipeBuilder },
  { path: '/logistique', name: 'logistique', component: logitique },
  { path: '/profile', name: 'profile', component: ProfileView },
  // Si l'utilisateur tape une URL qui n'existe pas, on le renvoie vers ses camps
  { path: '/:pathMatch(.*)*', redirect: '/camps' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// --- SÉCURITÉ (Navigation Guard) ---
// On empêche un visiteur non connecté d'accéder aux pages
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!userToken.value

  if (to.name !== 'login' && !isAuthenticated) {
    next({ name: 'login' }) // Retour à la connexion
  } else if (to.name === 'login' && isAuthenticated) {
    next({ name: 'unite' }) // S'il est déjà connecté, on l'envoie sur l'accueil
  } else {
    next() // On laisse passer
  }
})

export default router
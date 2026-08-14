<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-gray-50 dark:bg-gray-900 overflow-hidden transition-colors duration-300">
    
    <!-- NavBar : En bas sur mobile (fixed), À GAUCHE sur ordi (md:order-first) -->
    <NavBar class="order-last md:order-first shrink-0 z-40" />

    <!-- Zone principale (qui contiendra l'Unité, la Logistique, etc.) avec padding-bottom pour la navbar mobile -->
    <main class="flex-1 relative min-w-0 overflow-hidden flex flex-col pb-16 md:pb-0">
      <!-- Bannière de Statut réseau / Hors-Ligne -->
      <NetworkStatusBanner />
      <router-view />
      <!-- Pop-up Call to Action d'installation PWA -->
      <PwaInstallPrompt />
    </main>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// --- Imports de base ---
import NavBar from './components/NavBar.vue'
import NetworkStatusBanner from './components/NetworkStatusBanner.vue'
import PwaInstallPrompt from './components/PwaInstallPrompt.vue'
import { userToken, loginToSGDF, isLoggingIn, loginError, logout } from './stores/authStore.js'

// --- Imports Camps ---
import { 
  selectedCamp, campsList, loading, currentDate, showCampMenu,
  showAddModal, newEvent, showEditCampModal, editCampForm,
  moisActuelTexte, campsDuMois, joursDuCalendrier, joursDuCamp,
  changerMois, selectionnerDate, fermerModal, fetchCamps, 
  soumettreEvenement, modifierCamp, fermerEditCampModal, 
  soumettreModificationCamp, supprimerCamp 
} from './stores/campsStore.js'

// --- Imports Intendance ---
import { 
  searchQuery, selectedFilter, recipesList, currentMeal, currentMealRecipes, newRecipe, 
  shoppingList, showShoppingModal, rabEnabled, currentShoppingMealId, filteredRecipes, 
  groupedShoppingList, chargerCatalogueRecettes, ouvrirEditeurRecette, ajouterIngredientRecette, 
  supprimerIngredientRecette, partagerRecette, ouvrirMenuRepas, retirerRecette, ajouterRecetteAuMenu, 
  fermerMenuRepas, genererBordereau, genererBordereauGlobal, fermerBordereau, exporterBordereauPDF 
} from './stores/intendanceStore.js'

// --- Logique d'expiration de session ---
const router = useRouter()
const route = useRoute()
const showExpiredAlert = ref(false)

const handleSessionExpiration = () => {
    if (route.name === 'login') return 
    showExpiredAlert.value = true
}

const forcerDeconnexion = () => {
    showExpiredAlert.value = false
    localStorage.setItem('sgdf_redirect_after_login', route.fullPath)
    logout()
}

onMounted(() => {
  window.addEventListener('session-expired', handleSessionExpiration)
  fetchCamps()
  chargerCatalogueRecettes()
})

onUnmounted(() => {
  window.removeEventListener('session-expired', handleSessionExpiration)
})
</script>
<template>
  <div class="flex flex-col md:flex-row h-screen w-full bg-gray-50 dark:bg-gray-900 overflow-hidden transition-colors duration-300">
    
    <!-- NavBar : En bas sur mobile (order-last), À GAUCHE sur ordi (md:order-first) -->
    <NavBar class="order-last md:order-first shrink-0 z-40 relative" />

    <!-- Zone principale (qui contiendra l'Unité, la Logistique, etc.) -->
    <main class="flex-1 relative min-w-0 overflow-hidden flex flex-col">
      <router-view />
    </main>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// --- Imports de base ---
import NavBar from './components/NavBar.vue' // La fameuse NavBar !
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
    // Si on est déjà sur la page login, on ignore
    if (route.name === 'login') return 
    showExpiredAlert.value = true
}

const forcerDeconnexion = () => {
    showExpiredAlert.value = false
    // On mémorise la page où on se trouve pour y revenir plus tard
    localStorage.setItem('sgdf_redirect_after_login', route.fullPath)
    logout() // On vide le token et on va vers /login
}

onMounted(() => {
  // On écoute le signal d'alarme global
  window.addEventListener('session-expired', handleSessionExpiration)
  
  // Chargement des données initiales
  fetchCamps()
  chargerCatalogueRecettes()
})

onUnmounted(() => {
  
  window.removeEventListener('session-expired', handleSessionExpiration)
})
</script>
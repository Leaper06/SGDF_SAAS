<template>
  <div class="w-[390px] h-[844px] bg-gray-50 relative overflow-hidden shadow-2xl flex flex-col mx-auto my-8 border border-gray-200 rounded-[2rem]">
    
    <router-view class="flex-1 min-h-0 flex flex-col relative" />

    <NavBar v-if="userToken" />

    <div v-if="showExpiredAlert" class="absolute inset-0 z-[100] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-white p-6 rounded-3xl shadow-2xl text-center max-w-sm w-full animate-fade-in-up">
        
        <div class="w-16 h-16 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        
        <h3 class="text-xl font-black text-gray-900 mb-2">Session expirée</h3>
        <p class="text-sm text-gray-600 mb-6 leading-relaxed">
          Pour des raisons de sécurité, vous avez été déconnecté. 
          <br><br>
          <span class="font-bold text-[#004267]">Pas d'inquiétude :</span> les données que vous étiez en train de saisir sont conservées en mémoire.
        </p>
        
        <button @click="forcerDeconnexion" class="w-full bg-[#004267] hover:bg-[#003B5C] text-white font-bold py-3.5 rounded-xl transition-colors flex justify-center items-center gap-2">
          Se reconnecter
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
        </button>
      </div>
    </div>

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
  // Nettoyage de l'écouteur
  window.removeEventListener('session-expired', handleSessionExpiration)
})
</script>
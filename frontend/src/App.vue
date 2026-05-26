<template>
  <div class="w-[390px] h-[844px] bg-gray-50 relative overflow-hidden shadow-2xl flex flex-col mx-auto my-8 border border-gray-200 rounded-[2rem]">
    
    <router-view class="flex-1 min-h-0 flex flex-col relative" />

    <NavBar v-if="userToken" />

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { userToken, loginToSGDF, isLoggingIn, loginError } from './stores/authStore.js'
import { 
  selectedCamp, campsList, loading, currentDate, showCampMenu,
  showAddModal, newEvent, showEditCampModal, editCampForm,
  moisActuelTexte, campsDuMois, joursDuCalendrier, joursDuCamp,
  changerMois, selectionnerDate, fermerModal, fetchCamps, 
  soumettreEvenement, modifierCamp, fermerEditCampModal, 
  soumettreModificationCamp, supprimerCamp 
} from './stores/campsStore.js'
import { 
  searchQuery, selectedFilter, recipesList, currentMeal, currentMealRecipes, newRecipe, 
  shoppingList, showShoppingModal, rabEnabled, currentShoppingMealId, filteredRecipes, 
  groupedShoppingList, chargerCatalogueRecettes, ouvrirEditeurRecette, ajouterIngredientRecette, 
  supprimerIngredientRecette, partagerRecette, ouvrirMenuRepas, retirerRecette, ajouterRecetteAuMenu, 
  fermerMenuRepas, genererBordereau, genererBordereauGlobal, fermerBordereau, exporterBordereauPDF 
} from './stores/intendanceStore.js'

import NavBar from './components/NavBar.vue'

onMounted(() => {
  fetchCamps()
  chargerCatalogueRecettes()
})
</script>
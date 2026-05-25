<template>
  <div class="w-[390px] h-[844px] bg-gray-50 relative overflow-hidden shadow-2xl flex flex-col mx-auto my-8 border border-gray-200 rounded-[2rem]">
    
    <router-view class="flex-1 min-h-0 flex flex-col relative" />

    <NavBar v-if="userToken" />

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { chargerCatalogueRecettes } from './store.js'
import { userToken, loginToSGDF, isLoggingIn, loginError } from './stores/authStore.js'
import { 
  selectedCamp, campsList, loading, currentDate, showCampMenu,
  showAddModal, newEvent, showEditCampModal, editCampForm,
  moisActuelTexte, campsDuMois, joursDuCalendrier, joursDuCamp,
  changerMois, selectionnerDate, fermerModal, fetchCamps, 
  soumettreEvenement, modifierCamp, fermerEditCampModal, 
  soumettreModificationCamp, supprimerCamp 
} from './stores/campsStore.js'

// Plus besoin d'importer LoginView, UniteView, etc. Le routeur s'en occupe !
import NavBar from './components/NavBar.vue'

onMounted(() => {
  fetchCamps()
  chargerCatalogueRecettes()
})
</script>
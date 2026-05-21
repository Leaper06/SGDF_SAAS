<template>
  <div class="w-[390px] h-[844px] bg-gray-50 relative overflow-hidden shadow-2xl flex flex-col mx-auto my-8 border border-gray-200 rounded-[2rem]">
    
    <div v-if="!userToken" class="flex-1 flex flex-col min-h-0">
      <LoginView />
    </div>

    <div v-else class="flex-1 flex flex-col min-h-0 relative">
      
      <CalendarView v-if="currentView === 'calendar'" />
      <PlanningView v-else-if="currentView === 'planning'" />
      <ActivityDetail v-else-if="currentView === 'activity_detail' && selectedSlot" />
      <MenuBuilder v-else-if="currentView === 'menu_builder' && selectedSlot" />
      <RecipeCatalog v-else-if="currentView === 'recipe_catalog'" />
      <RecipeBuilder v-else-if="currentView === 'recipe_builder'" />
      <UniteView v-else-if="currentView === 'unite'" />
      
      <NavBar />
    </div>

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { currentView, selectedSlot, fetchCamps, chargerCatalogueRecettes, userToken } from './store.js'

// Importation de tous les composants
import CalendarView from './components/CalendarView.vue'
import PlanningView from './components/PlanningView.vue'
import ActivityDetail from './components/ActivityDetail.vue'
import MenuBuilder from './components/MenuBuilder.vue'
import RecipeCatalog from './components/RecipeCatalog.vue'
import RecipeBuilder from './components/RecipeBuilder.vue'
import LoginView from './components/LoginView.vue'
import UniteView from './components/UniteView.vue' // <-- Nouveau composant cible
import NavBar from './components/NavBar.vue'

onMounted(() => {
  fetchCamps()
  chargerCatalogueRecettes()
})
</script>
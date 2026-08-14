<template>
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-x-full" enter-to-class="opacity-100 translate-x-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-x-0" leave-to-class="opacity-0 translate-x-full">
    <div v-if="showRecipeDrawer" class="fixed inset-0 z-50 flex justify-end">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="closeDrawer"></div>

      <!-- Drawer Panel -->
      <div class="relative bg-white dark:bg-gray-800 w-full max-w-md h-full shadow-2xl flex flex-col z-10 transition-colors">
        
        <!-- Header -->
        <div class="bg-[#5b2b82] dark:bg-purple-900 text-white p-5 flex justify-between items-center shrink-0 shadow-md">
          <div>
            <h2 class="text-lg font-black tracking-wide">Ajouter au menu</h2>
            <p class="text-xs text-purple-200 mt-0.5">Recettes & Produits libres</p>
          </div>
          <button @click="closeDrawer" class="p-2 text-white/80 hover:text-white hover:bg-white/10 rounded-full transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Mode Selector (Tabs) -->
        <div class="flex border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 p-1.5 gap-1 shrink-0">
          <button 
            @click="activeTab = 'catalog'"
            :class="['flex-1 py-2 text-xs font-bold rounded-lg transition-colors flex items-center justify-center gap-1.5', activeTab === 'catalog' ? 'bg-white dark:bg-gray-800 text-[#5b2b82] dark:text-purple-300 shadow-sm' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <span>Catalogue Recettes</span>
          </button>
          <button 
            @click="activeTab = 'custom'"
            :class="['flex-1 py-2 text-xs font-bold rounded-lg transition-colors flex items-center justify-center gap-1.5', activeTab === 'custom' ? 'bg-white dark:bg-gray-800 text-[#5b2b82] dark:text-purple-300 shadow-sm' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700']"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
            </svg>
            <span>Ajout Libre (Aliment)</span>
          </button>
        </div>

        <!-- TAB 1: CATALOGUE -->
        <div v-if="activeTab === 'catalog'" class="flex-1 flex flex-col overflow-hidden">
          <!-- Search & Filters -->
          <div class="p-4 border-b border-gray-100 dark:border-gray-700 space-y-3 bg-white dark:bg-gray-800 shrink-0">
            <div class="relative">
              <input 
                v-model="drawerSearchQuery" 
                type="text" 
                placeholder="Rechercher une recette (ex: Carbonara, Salade...)"
                class="w-full pl-10 pr-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-medium text-gray-900 dark:text-white focus:outline-none focus:border-[#5b2b82] dark:focus:border-purple-500 transition-colors"
              >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 absolute left-3.5 top-3.5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>

            <!-- Filter Chips -->
            <div class="flex gap-1.5 overflow-x-auto scrollbar-hide py-1">
              <button 
                v-for="filter in ['Tous', 'Entrée', 'Plat principal', 'Dessert', 'Végétarien', 'Sans frigo', 'Feu de bois']" 
                :key="filter"
                @click="drawerFilter = filter"
                :class="['px-3 py-1 rounded-full text-xs font-bold shrink-0 transition-colors', drawerFilter === filter ? 'bg-[#5b2b82] text-white dark:bg-purple-600' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200']"
              >
                {{ filter }}
              </button>
            </div>
          </div>

          <!-- Recipe List -->
          <div class="flex-1 overflow-y-auto p-4 space-y-3">
            <div v-if="filteredDrawerRecipes.length === 0" class="py-12 text-center text-gray-400 dark:text-gray-500 text-sm font-medium">
              Aucune recette ne correspond à votre recherche.
            </div>

            <div 
              v-for="recipe in filteredDrawerRecipes" 
              :key="recipe.id"
              class="p-3 border border-gray-100 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900/40 flex items-center justify-between transition-all hover:border-purple-200 dark:hover:border-purple-800"
            >
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-purple-100 dark:bg-purple-900/40 text-[#5b2b82] dark:text-purple-300 flex items-center justify-center shrink-0">
                  <!-- SVG Dish Type Icon -->
                  <svg v-if="recipe.dish_type === 'Entrée'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                  <svg v-else-if="recipe.dish_type === 'Dessert'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M3 21h18M3 10h18M3 7l9-4 9 4v3H3V7z" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
                  </svg>
                </div>
                <div>
                  <p class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider">{{ recipe.dish_type || 'Plat' }}</p>
                  <h4 class="text-sm font-bold text-gray-900 dark:text-white">{{ recipe.name }}</h4>
                </div>
              </div>

              <button 
                @click="toggleRecipe(recipe)"
                :class="['px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1 transition-all', isAdded(recipe.id) ? 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300' : 'bg-[#5b2b82] text-white hover:bg-purple-900 dark:bg-purple-600 dark:hover:bg-purple-700']"
              >
                <svg v-if="isAdded(recipe.id)" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                </svg>
                <span>{{ isAdded(recipe.id) ? 'Ajouté' : 'Ajouter' }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- TAB 2: SAISIE LIBRE -->
        <div v-else class="p-5 space-y-5 flex-1 overflow-y-auto">
          <div class="bg-purple-50 dark:bg-purple-900/20 border border-purple-100 dark:border-purple-900/40 p-4 rounded-xl text-xs text-purple-900 dark:text-purple-300 space-y-1">
            <p class="font-bold">💡 Ajout d'aliments hors-catalogue</p>
            <p class="text-purple-700 dark:text-purple-400">Ajoute directement un produit au menu (ex: *Baguette de pain*, *Melon*, *Chips*) sans créer de recette.</p>
          </div>

          <form @submit.prevent="submitCustomItem" class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-1">Nom de l'aliment ou produit</label>
              <input 
                v-model="customName" 
                type="text" 
                required
                placeholder="Ex: Baguettes de pain, Melon, Chips..."
                class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-medium text-gray-900 dark:text-white focus:outline-none focus:border-[#5b2b82] dark:focus:border-purple-500 transition-colors"
              >
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-1">Quantité (ex: 4 kilos, 2 L, 6 pièces...)</label>
              <input 
                v-model="customQuantity" 
                type="text" 
                placeholder="Ex: 4 kilos, 2 L, 6 pièces (optionnel)"
                class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-medium text-gray-900 dark:text-white focus:outline-none focus:border-[#5b2b82] dark:focus:border-purple-500 transition-colors"
              >
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-1">Catégorie de repas</label>
              <select 
                v-model="customType"
                class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-medium text-gray-900 dark:text-white focus:outline-none focus:border-[#5b2b82] dark:focus:border-purple-500 transition-colors"
              >
                <option value="Entrée">Entrée</option>
                <option value="Plat principal">Plat principal</option>
                <option value="Dessert">Dessert</option>
                <option value="Accompagnement">Accompagnement / Pain / Boisson</option>
              </select>
            </div>

            <button type="submit" class="w-full py-3.5 bg-[#5b2b82] text-white rounded-xl font-bold text-sm hover:bg-purple-900 dark:bg-purple-600 dark:hover:bg-purple-700 transition-colors flex items-center justify-center gap-2 shadow-md">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
              </svg>
              <span>Ajouter au menu</span>
            </button>
          </form>
        </div>

      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  showRecipeDrawer, recipesList, currentMealRecipes, 
  chargerCatalogueRecettes, ajouterRecetteInline, retirerRecette, ajouterItemLibre 
} from '../stores/intendanceStore.js'

const activeTab = ref('catalog')
const drawerSearchQuery = ref('')
const drawerFilter = ref('Tous')
const customName = ref('')
const customQuantity = ref('')
const customType = ref('Accompagnement')

onMounted(() => {
  if (recipesList.value.length === 0) {
    chargerCatalogueRecettes()
  }
})

const closeDrawer = () => {
  showRecipeDrawer.value = false
}

const filteredDrawerRecipes = computed(() => {
  let list = recipesList.value
  if (drawerSearchQuery.value) {
    const q = drawerSearchQuery.value.toLowerCase()
    list = list.filter(r => r.name.toLowerCase().includes(q))
  }
  if (drawerFilter.value === 'Entrée') list = list.filter(r => (r.dish_type || '').toLowerCase().includes('entrée'))
  else if (drawerFilter.value === 'Plat principal') list = list.filter(r => (r.dish_type || '').toLowerCase().includes('plat'))
  else if (drawerFilter.value === 'Dessert') list = list.filter(r => (r.dish_type || '').toLowerCase().includes('dessert'))
  else if (drawerFilter.value === 'Végétarien') list = list.filter(r => r.is_vegetarian)
  else if (drawerFilter.value === 'Sans frigo') list = list.filter(r => r.is_fridge_free)
  else if (drawerFilter.value === 'Feu de bois') list = list.filter(r => r.is_wood_fire)
  return list
})

const isAdded = (recipeId) => {
  return currentMealRecipes.value.some(r => r.id === recipeId)
}

const toggleRecipe = (recipe) => {
  const index = currentMealRecipes.value.findIndex(r => r.id === recipe.id)
  if (index !== -1) {
    retirerRecette(index, recipe.id)
  } else {
    ajouterRecetteInline(recipe)
  }
}

const submitCustomItem = () => {
  if (!customName.value) return
  ajouterItemLibre(customName.value, customQuantity.value, customType.value)
  customName.value = ''
  customQuantity.value = ''
  showRecipeDrawer.value = false
}
</script>

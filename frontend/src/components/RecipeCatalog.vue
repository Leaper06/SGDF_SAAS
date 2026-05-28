<template>
    <div class="flex flex-col h-full bg-bgLight dark:bg-gray-900 transition-colors duration-300">
        
        <!-- HEADER -->
        <div class="bg-[#004267] dark:bg-gray-800 text-white pt-5 pb-6 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative transition-colors">
            <div class="flex justify-center items-center mb-1">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
            </div>
            <p class="text-center text-blue-100 dark:text-gray-300 text-sm font-medium mt-1 transition-colors">Catalogue de recettes</p>
        </div>

        <!-- BARRE D'OUTILS STICKY -->
        <div class="bg-white dark:bg-gray-800 px-4 pt-6 pb-3 shadow-sm z-20 sticky top-0 border-b border-gray-100 dark:border-gray-700 -mt-4 transition-colors">
            <div class="flex justify-between items-center mb-4">
                <button @click="$router.push('/planning')" class="text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 flex items-center gap-1 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                    <span class="text-sm font-medium">Planning</span>
                </button>
                <h2 class="text-sm font-extrabold text-gray-900 dark:text-white transition-colors">Ajouter un plat</h2>
                <div class="w-10">
                  <button @click="ouvrirEditeurRecette" class="w-8 h-8 rounded-full bg-violet-50 dark:bg-purple-900/30 text-[#5b2b82] dark:text-purple-400 flex items-center justify-center hover:bg-[#5b2b82] dark:hover:bg-purple-600 hover:text-white dark:hover:text-white transition-colors">
                    <span class="font-bold text-xl leading-none mb-1">+</span>
                  </button>
                </div> 
            </div>
            
            <!-- BARRE DE RECHERCHE -->
            <div class="relative mb-3">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-4 w-4 text-gray-400 dark:text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                </div>
                <input v-model="searchQuery" type="text" placeholder="Rechercher par nom..." class="w-full bg-gray-100 dark:bg-gray-900 border-none rounded-xl pl-9 pr-4 py-2.5 text-sm text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#5b2b82] dark:focus:ring-purple-500 transition-all">
            </div>

            <!-- FILTRES -->
            <div class="flex gap-2 overflow-x-auto scrollbar-hide pb-1">
                <button @click="selectedFilter = 'Tous'" :class="['whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold shadow-sm transition-colors', selectedFilter === 'Tous' ? 'bg-[#5b2b82] dark:bg-purple-600 text-white' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300']">Tous</button>
                <button @click="selectedFilter = 'Végétarien'" :class="['whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium border transition-colors', selectedFilter === 'Végétarien' ? 'bg-green-50 dark:bg-green-900/30 text-[#16a34a] dark:text-green-400 border-green-200 dark:border-green-800' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700']">✓ Végétarien</button>
                <button @click="selectedFilter = 'Sans frigo'" :class="['whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium border transition-colors', selectedFilter === 'Sans frigo' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700']">+ Sans frigo</button>
                <button @click="selectedFilter = 'Feu de bois'" :class="['whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium border transition-colors', selectedFilter === 'Feu de bois' ? 'bg-orange-50 dark:bg-orange-900/30 text-[#e45a27] dark:text-orange-400 border-orange-200 dark:border-orange-800' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700']">+ Feu de bois</button>
            </div>
        </div>

        <!-- LISTE DES RECETTES -->
        <div class="flex-1 overflow-y-auto p-4">
                    <h3 class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider ml-1 mb-4 transition-colors">Base de données ({{ filteredRecipes.length }} résultats)</h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                        <div v-for="recipe in filteredRecipes" :key="recipe.id" class="bg-white dark:bg-gray-800 p-3 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 flex justify-between items-center group transition-colors hover:shadow-md hover:border-purple-200 dark:hover:border-purple-800">
                            <div class="flex-1">
                                <h4 class="text-sm font-bold text-gray-900 dark:text-white transition-colors">{{ recipe.name }}</h4>
                                <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 transition-colors">{{ recipe.type }}</p>
                                <div class="flex gap-1.5 mt-2">
                                    <span v-if="recipe.is_vegetarian" class="text-[9px] bg-green-50 dark:bg-green-900/30 text-[#16a34a] dark:text-green-400 px-1.5 py-0.5 rounded font-bold uppercase tracking-wide transition-colors">Végé</span>
                                    <span v-if="recipe.is_pork_free && !recipe.is_vegetarian" class="text-[9px] bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 px-1.5 py-0.5 rounded font-bold uppercase tracking-wide transition-colors">Sans frigo</span>
                                    <span v-if="recipe.is_eco" class="text-[9px] bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-1.5 py-0.5 rounded font-bold uppercase tracking-wide transition-colors">Éco</span>
                                </div>
                            </div>
                            <button @click="ajouterRecetteAuMenu(recipe)" class="w-8 h-8 rounded-full bg-violet-50 dark:bg-purple-900/30 text-[#5b2b82] dark:text-purple-400 flex items-center justify-center hover:bg-[#5b2b82] dark:hover:bg-purple-600 hover:text-white dark:hover:text-white transition-colors shrink-0 ml-2">
                            <span class="font-bold text-xl leading-none mb-1">+</span>
                            </button>
                        </div>
                    </div>
                    <div v-if="filteredRecipes.length === 0" class="text-center p-8 text-gray-400 dark:text-gray-500 text-sm transition-colors mt-4">
                    Aucune recette ne correspond à ta recherche.
                    </div>
                </div>
    </div>
</template>

<script setup>
import { 
  searchQuery, selectedFilter, recipesList, currentMeal, currentMealRecipes, newRecipe, 
  shoppingList, showShoppingModal, rabEnabled, currentShoppingMealId, filteredRecipes, 
  groupedShoppingList, chargerCatalogueRecettes, ouvrirEditeurRecette, ajouterIngredientRecette, 
  supprimerIngredientRecette, partagerRecette, ouvrirMenuRepas, retirerRecette, ajouterRecetteAuMenu, 
  fermerMenuRepas, genererBordereau, genererBordereauGlobal, fermerBordereau, exporterBordereauPDF 
} from '../stores/intendanceStore.js'


import { getTheme, formatHeure, formatTypeLabel, formatCourt } from '../utils/helpers.js'
import { userToken, loginToSGDF, isLoggingIn, loginError } from '../stores/authStore.js'
</script>
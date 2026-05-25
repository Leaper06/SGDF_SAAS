<template>
    <div class="flex flex-col h-full bg-bgLight pb-20">
        <div class="bg-[#004267] text-white pt-5 pb-6 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative">
            <div class="flex justify-center items-center mb-1">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
            </div>
            <p class="text-center text-blue-100 text-sm font-medium mt-1">Catalogue de recettes</p>
        </div>

        <div class="bg-white px-4 pt-6 pb-3 shadow-sm z-20 sticky top-0 border-b border-gray-100 -mt-4">
            <div class="flex justify-between items-center mb-4">
                <button @click="$router.push('/planning')" class="text-gray-500 hover:text-gray-800 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                    <span class="text-sm font-medium">Planning</span>
                </button>
                <h2 class="text-sm font-extrabold text-gray-900">Ajouter un plat</h2>
                <div class="w-10">
                  <button @click="ouvrirEditeurRecette" class="w-8 h-8 rounded-full bg-violet-50 text-[#5b2b82] flex items-center justify-center hover:bg-[#5b2b82] hover:text-white transition-colors">
                    <span class="font-bold text-xl leading-none mb-1">+</span>
                  </button>
                </div> 
            </div>
            
            <div class="relative mb-3">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg class="h-4 w-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                </div>
                <input v-model="searchQuery" type="text" placeholder="Rechercher par nom..." class="w-full bg-gray-100 border-none rounded-xl pl-9 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#5b2b82] transition-shadow">
            </div>

            <div class="flex gap-2 overflow-x-auto scrollbar-hide pb-1">
                <button @click="selectedFilter = 'Tous'" :class="['whitespace-nowrap px-4 py-1.5 rounded-full text-xs font-bold shadow-sm', selectedFilter === 'Tous' ? 'bg-[#5b2b82] text-white' : 'bg-gray-100 text-gray-600']">Tous</button>
                <button @click="selectedFilter = 'Végétarien'" :class="['whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium border', selectedFilter === 'Végétarien' ? 'bg-green-50 text-[#16a34a] border-green-200' : 'bg-white text-gray-600 border-gray-200']">✓ Végétarien</button>
                <button @click="selectedFilter = 'Sans frigo'" :class="['whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium border', selectedFilter === 'Sans frigo' ? 'bg-blue-50 text-blue-600 border-blue-200' : 'bg-white text-gray-600 border-gray-200']">+ Sans frigo</button>
                <button @click="selectedFilter = 'Feu de bois'" :class="['whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium border', selectedFilter === 'Feu de bois' ? 'bg-orange-50 text-[#e45a27] border-orange-200' : 'bg-white text-gray-600 border-gray-200']">+ Feu de bois</button>
            </div>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-3">
            <h3 class="text-[10px] font-bold text-gray-400 uppercase tracking-wider ml-1 mb-2">Base de données ({{ filteredRecipes.length }} résultats)</h3>
            
            <div v-for="recipe in filteredRecipes" :key="recipe.id" class="bg-white p-3 rounded-xl shadow-sm border border-gray-100 flex justify-between items-center group">
                <div class="flex-1">
                    <h4 class="text-sm font-bold text-gray-900">{{ recipe.name }}</h4>
                    <p class="text-xs text-gray-500 mt-0.5">{{ recipe.type }}</p>
                    <div class="flex gap-1.5 mt-2">
                        <span v-if="recipe.is_vegetarian" class="text-[9px] bg-green-50 text-[#16a34a] px-1.5 py-0.5 rounded font-bold uppercase tracking-wide">Végé</span>
                        <span v-if="recipe.is_pork_free && !recipe.is_vegetarian" class="text-[9px] bg-blue-50 text-blue-600 px-1.5 py-0.5 rounded font-bold uppercase tracking-wide">Sans frigo</span>
                        <span v-if="recipe.is_eco" class="text-[9px] bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded font-bold uppercase tracking-wide">Éco</span>
                    </div>
                </div>
                <button @click="ajouterRecetteAuMenu(recipe)" class="w-8 h-8 rounded-full bg-violet-50 text-[#5b2b82] flex items-center justify-center hover:bg-[#5b2b82] hover:text-white transition-colors">
                  <span class="font-bold text-xl leading-none mb-1">+</span>
                </button>
            </div>
            
            <div v-if="filteredRecipes.length === 0" class="text-center p-8 text-gray-400 text-sm">
              Aucune recette ne correspond à ta recherche.
            </div>
        </div>
    </div>
</template>

<script setup>
import { 
  ouvrirEditeurRecette, searchQuery, 
  selectedFilter, filteredRecipes, ajouterRecetteAuMenu 
} from '../store.js'

import { getTheme, formatHeure, formatTypeLabel, formatCourt } from '../utils/helpers.js'
import { userToken, loginToSGDF, isLoggingIn, loginError } from '../stores/authStore.js'
</script>
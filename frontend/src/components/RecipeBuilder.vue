<template>
    <div class="flex flex-col h-full bg-gray-50 dark:bg-gray-900 pb-20 md:pb-0 transition-colors duration-300">
        
        <div class="bg-[#004267] dark:bg-gray-800 text-white pt-5 pb-6 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative shrink-0 transition-colors">
            <div class="flex justify-center items-center mb-1">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
            </div>
            <p class="text-center text-blue-100 dark:text-gray-300 text-sm font-medium mt-1 transition-colors">Éditeur de recette</p>
        </div>

        <div class="bg-white dark:bg-gray-800 px-4 py-4 shadow-sm z-20 flex justify-center items-center sticky top-0 border-b border-gray-100 dark:border-gray-700 -mt-4 pt-8 transition-colors">
            <div class="max-w-4xl mx-auto w-full flex justify-between items-center">
                <button @click="$router.push('/recipes')" class="text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 text-sm font-medium transition-colors">Annuler</button>
                <div class="text-center">
                    <h2 class="text-sm font-extrabold text-gray-900 dark:text-white transition-colors">Nouvelle recette</h2>
                    <p class="text-[9px] text-gray-400 dark:text-gray-500 uppercase tracking-wider transition-colors">Catalogue collectif</p>
                </div>
                <button @click="partagerRecette" class="text-[#5b2b82] dark:text-purple-400 hover:text-purple-900 dark:hover:text-purple-300 font-bold text-sm transition-colors">Partager</button>
            </div>
        </div>

        <div class="flex-1 overflow-y-auto p-4 md:p-8 pb-28 md:pb-8 scrollbar-hide">
            
            <div class="max-w-4xl mx-auto w-full">
                <div class="grid grid-cols-1 md:grid-cols-12 gap-6 md:gap-8">
                    
                    <div class="md:col-span-5 space-y-6">
                        
                        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 space-y-4 transition-colors">
                            <div>
                                <label class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wide mb-1 transition-colors">Nom du plat</label>
                                <input v-model="newRecipe.name" type="text" placeholder="Ex: Chili con Carne scout..." class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-[#5b2b82] dark:focus:border-purple-500 shadow-sm transition-colors placeholder-gray-400 dark:placeholder-gray-600">
                            </div>
                            <div>
                                <label class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wide mb-2 transition-colors">Type de plat</label>
                                <div class="grid grid-cols-3 gap-2">
                                    <button @click="newRecipe.type = 'Entrée'" :class="['py-2.5 text-xs font-semibold rounded-xl transition-colors', newRecipe.type === 'Entrée' ? 'bg-violet-50 dark:bg-purple-900/30 border border-[#5b2b82] dark:border-purple-500 text-[#5b2b82] dark:text-purple-300 shadow-sm' : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400']">Entrée</button>
                                    <button @click="newRecipe.type = 'Plat chaud'" :class="['py-2.5 text-xs font-semibold rounded-xl transition-colors', newRecipe.type === 'Plat chaud' ? 'bg-violet-50 dark:bg-purple-900/30 border border-[#5b2b82] dark:border-purple-500 text-[#5b2b82] dark:text-purple-300 shadow-sm' : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400']">Plat</button>
                                    <button @click="newRecipe.type = 'Dessert'" :class="['py-2.5 text-xs font-semibold rounded-xl transition-colors', newRecipe.type === 'Dessert' ? 'bg-violet-50 dark:bg-purple-900/30 border border-[#5b2b82] dark:border-purple-500 text-[#5b2b82] dark:text-purple-300 shadow-sm' : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400']">Dessert</button>
                                </div>
                            </div>
                        </div>

                        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 transition-colors">
                            <label class="block text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wide mb-3 transition-colors">Spécificités (Régimes & Matériel)</label>
                            <div class="flex flex-wrap gap-2">
                                <button @click="newRecipe.is_vegetarian = !newRecipe.is_vegetarian" :class="['px-3 py-1.5 rounded-full text-xs font-medium transition-colors border', newRecipe.is_vegetarian ? 'bg-green-50 dark:bg-green-900/30 text-[#16a34a] dark:text-green-400 border-green-200 dark:border-green-800 shadow-sm' : 'bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700']">
                                    {{ newRecipe.is_vegetarian ? '✓' : '+' }} Végétarien
                                </button>
                                <button @click="newRecipe.is_wood_fire = !newRecipe.is_wood_fire" :class="['px-3 py-1.5 rounded-full text-xs font-medium transition-colors border', newRecipe.is_wood_fire ? 'bg-orange-50 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 border-orange-200 dark:border-orange-800 shadow-sm' : 'bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700']">
                                    {{ newRecipe.is_wood_fire ? '✓' : '+' }} Feu de bois
                                </button>
                                <button @click="newRecipe.is_fridge_free = !newRecipe.is_fridge_free" :class="['px-3 py-1.5 rounded-full text-xs font-medium transition-colors border', newRecipe.is_fridge_free ? 'bg-purple-50 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 border-purple-200 dark:border-purple-800 shadow-sm' : 'bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700']">
                                    {{ newRecipe.is_fridge_free ? '✓' : '+' }} Sans frigo
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="md:col-span-7">
                        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 space-y-4 transition-colors h-full flex flex-col">
                            
                            <div class="border-b border-gray-50 dark:border-gray-700 pb-3 mb-2 transition-colors flex justify-between items-end">
                                <div>
                                    <h3 class="font-bold text-gray-800 dark:text-white transition-colors">Ingrédients & Grammages</h3>
                                    <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5 transition-colors">Portions individuelles (pour 1 personne).</p>
                                </div>
                                <button @click="ajouterIngredientRecette" class="text-xs font-bold text-white bg-[#5b2b82] dark:bg-purple-600 px-3 py-1.5 rounded-lg shadow-sm hover:bg-purple-900 dark:hover:bg-purple-500 transition-colors flex items-center gap-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                                    Ajouter
                                </button>
                            </div>

                            <div class="flex-1 space-y-3">
                                <div v-for="(ing, index) in newRecipe.ingredients" :key="ing.id" class="bg-gray-50 dark:bg-gray-900/50 border border-gray-100 dark:border-gray-700 rounded-xl p-4 relative group transition-colors">
                                    
                                    <button v-if="newRecipe.ingredients.length > 1" @click="supprimerIngredientRecette(index)" class="absolute top-4 right-4 text-gray-300 dark:text-gray-600 hover:text-red-500 dark:hover:text-red-400 transition-colors p-1 bg-white dark:bg-gray-800 rounded-md shadow-sm border border-gray-100 dark:border-gray-700 opacity-100 md:opacity-0 md:group-hover:opacity-100">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                    </button>
                                    
                                    <input v-model="ing.name" type="text" class="w-[85%] bg-transparent text-sm font-bold text-gray-800 dark:text-white focus:outline-none focus:border-b focus:border-[#5b2b82] dark:focus:border-purple-500 mb-4 pb-1 transition-colors placeholder-gray-400 dark:placeholder-gray-600" placeholder="Ex: Pâtes (Coquillettes)">
                                    
                                    <div class="flex gap-4">
                                        <div class="flex-1">
                                            <label class="block text-[10px] text-gray-500 dark:text-gray-400 font-bold uppercase mb-1.5 transition-colors">Enfant</label>
                                            <div class="relative">
                                                <input v-model="ing.qty_child" type="number" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg pl-3 pr-8 py-2.5 text-sm font-bold text-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#5b2b82]/30 dark:focus:ring-purple-500/30 transition-colors">
                                                <span class="absolute right-3 top-2.5 text-[11px] text-gray-400 dark:text-gray-500 font-black transition-colors">g</span>
                                            </div>
                                        </div>
                                        <div class="flex-1">
                                            <label class="block text-[10px] text-gray-500 dark:text-gray-400 font-bold uppercase mb-1.5 transition-colors">Ado / Adulte</label>
                                            <div class="relative">
                                                <input v-model="ing.qty_adult" type="number" class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg pl-3 pr-8 py-2.5 text-sm font-bold text-gray-700 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#5b2b82]/30 dark:focus:ring-purple-500/30 transition-colors">
                                                <span class="absolute right-3 top-2.5 text-[11px] text-gray-400 dark:text-gray-500 font-black transition-colors">g</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                </div>
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
import { userToken, loginToSGDF, isLoggingIn, loginError } from '../stores/authStore.js'
import { getTheme, formatHeure, formatTypeLabel, formatCourt } from '../utils/helpers.js'
</script>
<template>
    <div class="flex flex-col h-full bg-bgLight pb-20">
        <div class="bg-[#004267] text-white pt-5 pb-6 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative">
            <div class="flex justify-center items-center mb-1">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
            </div>
            <p class="text-center text-blue-100 text-sm font-medium mt-1">Éditeur de recette</p>
        </div>

        <div class="bg-white px-4 py-4 shadow-sm z-20 flex justify-between items-center sticky top-0 border-b border-gray-100 -mt-4 pt-6">
            <button @click="currentView = 'recipe_catalog'" class="text-gray-500 hover:text-gray-800 text-sm font-medium">Annuler</button>
            <div class="text-center">
                <h2 class="text-sm font-extrabold text-gray-900">Nouvelle recette</h2>
                <p class="text-[9px] text-gray-400 uppercase tracking-wider">Catalogue collectif</p>
            </div>
            <button @click="partagerRecette" class="text-[#5b2b82] font-bold text-sm">Partager</button>
        </div>

        <div class="flex-1 overflow-y-auto p-5 space-y-5 pb-28">
            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-1">Nom du plat</label>
                    <input v-model="newRecipe.name" type="text" placeholder="Ex: Chili con Carne scout..." class="w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-[#5b2b82] shadow-sm">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-2">Type de plat</label>
                    <div class="grid grid-cols-3 gap-2">
                        <button @click="newRecipe.type = 'Entrée'" :class="['py-2.5 text-xs font-semibold rounded-xl transition-colors', newRecipe.type === 'Entrée' ? 'bg-violet-50 border border-[#5b2b82] text-[#5b2b82] shadow-sm' : 'bg-white border border-gray-200 text-gray-600']">Entrée</button>
                        <button @click="newRecipe.type = 'Plat chaud'" :class="['py-2.5 text-xs font-semibold rounded-xl transition-colors', newRecipe.type === 'Plat chaud' ? 'bg-violet-50 border border-[#5b2b82] text-[#5b2b82] shadow-sm' : 'bg-white border border-gray-200 text-gray-600']">Plat</button>
                        <button @click="newRecipe.type = 'Dessert'" :class="['py-2.5 text-xs font-semibold rounded-xl transition-colors', newRecipe.type === 'Dessert' ? 'bg-violet-50 border border-[#5b2b82] text-[#5b2b82] shadow-sm' : 'bg-white border border-gray-200 text-gray-600']">Dessert</button>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 space-y-4">
                <div class="border-b border-gray-50 pb-2 mb-2">
                    <h3 class="font-bold text-gray-800 text-sm">Ingrédients & Grammages</h3>
                    <p class="text-[11px] text-gray-400 mt-0.5">Pour 1 personne.</p>
                </div>

                <div v-for="(ing, index) in newRecipe.ingredients" :key="ing.id" class="bg-gray-50 border border-gray-100 rounded-xl p-3 relative group">
                    <button v-if="newRecipe.ingredients.length > 1" @click="supprimerIngredientRecette(index)" class="absolute top-3 right-3 text-gray-300 hover:text-red-500">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                    <input v-model="ing.name" type="text" class="w-10/12 bg-transparent text-sm font-bold text-gray-800 focus:outline-none focus:border-b focus:border-[#5b2b82] mb-3 pb-1" placeholder="Ex: Pâtes (Coquillettes)">
                    
                    <div class="flex gap-3">
                        <div class="flex-1">
                            <label class="block text-[9px] text-gray-500 font-bold uppercase mb-1">Enfant (-11 ans)</label>
                            <div class="relative">
                                <input v-model="ing.qty_child" type="number" class="w-full bg-white border border-gray-200 rounded-lg pl-3 pr-6 py-2 text-xs font-bold text-gray-700 focus:outline-none focus:border-[#5b2b82]">
                                <span class="absolute right-2 top-2 text-[10px] text-gray-400 font-bold">g</span>
                            </div>
                        </div>
                        <div class="flex-1">
                            <label class="block text-[9px] text-gray-500 font-bold uppercase mb-1">Adulte / Pio</label>
                            <div class="relative">
                                <input v-model="ing.qty_adult" type="number" class="w-full bg-white border border-gray-200 rounded-lg pl-3 pr-6 py-2 text-xs font-bold text-gray-700 focus:outline-none focus:border-[#5b2b82]">
                                <span class="absolute right-2 top-2 text-[10px] text-gray-400 font-bold">g</span>
                            </div>
                        </div>
                    </div>
                </div>

                <button @click="ajouterIngredientRecette" class="text-xs font-semibold text-[#5b2b82] flex items-center gap-1 pt-1 hover:underline">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                    Ajouter un ingrédient
                </button>
            </div>

            <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-2">Spécificités</label>
                <div class="flex flex-wrap gap-2">
                    <button @click="newRecipe.is_vegetarian = !newRecipe.is_vegetarian" :class="['px-3 py-1.5 rounded-full text-xs font-medium transition-colors border', newRecipe.is_vegetarian ? 'bg-green-50 text-[#16a34a] border-green-200' : 'bg-white text-gray-500 border-gray-200']">
                        {{ newRecipe.is_vegetarian ? '✓' : '+' }} Végétarien
                    </button>
                    <button @click="newRecipe.is_wood_fire = !newRecipe.is_wood_fire" :class="['px-3 py-1.5 rounded-full text-xs font-medium transition-colors border', newRecipe.is_wood_fire ? 'bg-orange-50 text-orange-600 border-orange-200' : 'bg-white text-gray-500 border-gray-200']">
                        {{ newRecipe.is_wood_fire ? '✓' : '+' }} Feu de bois
                    </button>
                    <button @click="newRecipe.is_fridge_free = !newRecipe.is_fridge_free" :class="['px-3 py-1.5 rounded-full text-xs font-medium transition-colors border', newRecipe.is_fridge_free ? 'bg-purple-50 text-purple-600 border-purple-200' : 'bg-white text-gray-500 border-gray-200']">
                        {{ newRecipe.is_fridge_free ? '✓' : '+' }} Sans frigo
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { 
  currentView, partagerRecette, newRecipe, 
  supprimerIngredientRecette, ajouterIngredientRecette 
} from '../store.js'
</script>
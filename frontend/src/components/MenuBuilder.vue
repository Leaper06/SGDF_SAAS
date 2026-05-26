<template>
    <div class="flex flex-col h-full bg-gray-50 pb-20">
        <div class="bg-scoutBlue text-white pt-5 pb-6 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative no-print">
            <div class="flex justify-center items-center mb-1">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
            </div>
            <p class="text-center text-blue-100 text-sm font-medium mt-1">Gestion des menus</p>
        </div>

        <div class="bg-white px-4 py-4 shadow-sm z-20 flex justify-between items-center sticky top-0 -mt-4 pt-6 no-print">
            <button @click="fermerMenuRepas" class="text-gray-500 hover:text-gray-800 flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                <span class="text-sm font-medium">Planning</span>
            </button>
            <div class="text-center">
                <h2 class="text-sm font-extrabold text-gray-900">{{ selectedSlot?.title }}</h2>
            </div>
            <button @click="fermerMenuRepas" class="text-scoutViolet font-bold text-sm">OK</button>
        </div>

        <div class="flex-1 overflow-y-auto p-5 space-y-5 pb-28 no-print">
            <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <div class="flex items-center justify-between mb-4 border-b border-gray-50 pb-3">
                    <h3 class="font-bold text-gray-800">Composition du menu</h3>
                </div>

                <div v-for="(recipe, index) in currentMealRecipes" :key="recipe.id || index" class="flex items-center justify-between py-2 border-b border-gray-50">
                    <div class="flex items-center gap-3">
                        <div :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm', getRecipeIcon(recipe.dish_type).bg, getRecipeIcon(recipe.dish_type).text]">
                            {{ getRecipeIcon(recipe.dish_type).emoji }}
                        </div>
                        <div>
                            <p class="text-xs text-gray-400 font-bold uppercase">{{ recipe.dish_type }}</p>
                            <p class="text-sm font-medium text-gray-900">{{ recipe.name }}</p>
                        </div>
                    </div>
                    <button @click="retirerRecette(index, recipe.id)" class="text-gray-300 hover:text-red-500 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                </div>

                <div v-if="currentMealRecipes.length === 0" class="py-6 text-center">
                    <p class="text-sm text-gray-400 italic font-medium">Ce menu est vide. Ajoute un plat !</p>
                </div>

                <button @click="$router.push('/recipes')" class="w-full mt-4 border-2 border-dashed border-gray-200 rounded-lg py-3 text-sm font-medium text-gray-500 hover:border-scoutViolet hover:text-scoutViolet transition-colors flex justify-center items-center gap-2">
                    <span class="text-lg leading-none">+</span> Ajouter un plat / Recette
                </button>
            </div>
            
            <button @click="genererBordereau" class="w-full bg-[#5b2b82] text-white font-bold py-3.5 rounded-xl shadow-md transition-transform active:scale-95 text-sm flex justify-center items-center gap-2">
               Afficher la liste de courses
            </button>
        </div>

        <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-full">
            <div v-if="showShoppingModal" class="fixed inset-0 z-50 flex flex-col justify-end printable-modal">
                <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity no-print" @click="fermerBordereau"></div>
                
                <div class="relative bg-gray-50 w-full h-[90%] rounded-t-3xl shadow-2xl flex flex-col z-10 overflow-hidden printable-content">
                    
                    <div class="bg-[#004267] text-white pt-5 pb-6 px-6 shrink-0 text-center rounded-t-3xl border-b-4 border-[#003B5C]">
                        <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
                        <p class="text-sm font-medium text-blue-100 mt-0.5">Bordereau d'achats</p>
                    </div>

                    <div class="bg-gray-50 px-4 py-3 flex justify-between items-center shrink-0 shadow-sm border-b border-gray-100 z-10">
                        <button @click="fermerBordereau" class="p-2 text-gray-500 hover:text-gray-800 no-print">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" /></svg>
                        </button>
                        <div class="text-center">
                            <h2 class="text-[15px] font-extrabold text-gray-900">Courses du Week-end</h2>
                            <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-0.5">3 REPAS • 17 PERSONNES</p>
                        </div>
                        <button @click="exporterBordereauPDF" class="p-2 text-[#5b2b82] hover:bg-violet-50 rounded-full transition-colors no-print">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" /></svg>
                        </button>
                    </div>

                    <div class="flex-1 overflow-y-auto p-4 pb-20">
                        
                        <div class="bg-[#5b2b82] text-white rounded-xl p-4 mb-6 shadow-md flex justify-between items-center no-print">
                            <div>
                                <h3 class="font-bold">Marge de sécurité (Rab)</h3>
                                <p class="text-xs text-violet-200 mt-0.5">Quantités augmentées de +10%</p>
                            </div>
                            <div @click="rabEnabled = !rabEnabled" :class="['w-12 h-6 rounded-full p-1 cursor-pointer transition-colors duration-300 ease-in-out', rabEnabled ? 'bg-violet-400' : 'bg-violet-900']">
                                <div :class="['w-4 h-4 bg-white rounded-full shadow-sm transform transition-transform duration-300 ease-in-out', rabEnabled ? 'translate-x-6' : 'translate-x-0']"></div>
                            </div>
                        </div>

                        <div v-for="(items, category) in groupedShoppingList" :key="category" class="mb-6">
                            <h3 class="flex items-center gap-2 text-xs font-bold text-gray-400 uppercase tracking-wider mb-3 ml-1">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                                {{ category }}
                            </h3>

                            <div class="space-y-2">
                                <label v-for="(item, index) in items" :key="index" class="bg-white rounded-xl p-3 shadow-sm border flex items-center justify-between cursor-pointer transition-all hover:border-violet-200 group" :class="item.isChecked ? 'border-violet-200 bg-violet-50/30 opacity-75' : 'border-gray-100'">
                                    
                                    <div class="flex items-center gap-3">
                                        <div :class="['w-5 h-5 rounded border flex items-center justify-center transition-colors', item.isChecked ? 'bg-[#5b2b82] border-[#5b2b82]' : 'border-gray-300 bg-white group-hover:border-[#5b2b82]']">
                                            <input type="checkbox" v-model="item.isChecked" class="hidden">
                                            <svg v-if="item.isChecked" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
                                        </div>
                                        
                                        <span :class="['text-[15px] font-bold transition-colors', item.isChecked ? 'text-gray-500 line-through' : 'text-[#001D2D]']">
                                            {{ item.name }}
                                        </span>
                                    </div>

                                    <div class="font-black text-[#5b2b82] bg-violet-50 px-3 py-1.5 rounded-lg text-sm border border-violet-100">
                                        {{ item.displayQty }} <span class="text-xs font-bold">{{ item.displayUnit }}</span>
                                    </div>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { userToken, loginToSGDF, isLoggingIn, loginError } from '../stores/authStore.js'
import { getTheme, formatHeure, formatTypeLabel, formatCourt, getRecipeIcon } from '../utils/helpers.js'
import { 
  selectedSlot, slotsList, showEditSlotModal, slotToEditId, editSlot, joursOuverts, 
  showAddSlotModal, newSlot, currentActivity, isEditingImaginaire, newMaterialName, 
  isAddingStep, editingStepIndex, newStep, showResponsiblesModal, activityResponsibles, 
  presentChefs, showInviteModal, inviteAdherentId, slotsParJour, selectedResponsiblesDetails, 
  ouvrirPlanning, fetchSlots, exporterPlanning, ouvrirAjoutSlot, fermerSlotModal, soumettreSlot, 
  modifierSlot, fermerEditSlotModal, soumettreModificationSlot, supprimerSlot, ouvrirFicheActivite, 
  sauvegarderFicheActivite, fermerFicheActivite, ajouterMateriel, toggleMateriel, calculerHeureEtape, 
  ouvrirAjoutEtape, modifierEtape, supprimerEtape, ajouterEtape, ouvrirGestionResponsables, 
  toggleResponsible, sauvegarderResponsables, chargerResponsablesActivite, ouvrirInviteModal, 
  fermerInviteModal, soumettreInvitation
} from '../stores/planningStore.js'

import { 
  searchQuery, selectedFilter, recipesList, currentMeal, currentMealRecipes, newRecipe, 
  shoppingList, showShoppingModal, rabEnabled, currentShoppingMealId, filteredRecipes, 
  groupedShoppingList, chargerCatalogueRecettes, ouvrirEditeurRecette, ajouterIngredientRecette, 
  supprimerIngredientRecette, partagerRecette, ouvrirMenuRepas, retirerRecette, ajouterRecetteAuMenu, 
  fermerMenuRepas, genererBordereau, genererBordereauGlobal, fermerBordereau, exporterBordereauPDF 
} from '../stores/intendanceStore.js'
</script>

<style>
@media print {
    /* 1. On cache absolument TOUT le site/application par défaut */
    body * {
        visibility: hidden !important;
        overflow: visible !important;
    }
    
    /* 2. On cible la modale et tout son contenu pour les rendre visibles */
    .printable-modal, .printable-modal * {
        visibility: visible !important;
    }
    
    /* 3. On force la modale à prendre tout l'espace naturel du papier A4 */
    .printable-modal {
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        height: auto !important;
        min-height: 100% !important;
        background-color: #f9fafb !important; /* bg-gray-50 */
        display: block !important;
    }
    
    /* 4. On détruit les limites de hauteur et de scroll du conteneur de la liste */
    .printable-content {
        position: relative !important;
        display: block !important;
        width: 100% !important;
        height: auto !important;
        min-height: 100% !important;
        overflow: visible !important;
        overflow-y: visible !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }

    /* 5. On s'assure que la zone interne défilante s'étire sur toute sa vraie longueur */
    .printable-content .flex-1.overflow-y-auto {
        overflow: visible !important;
        height: auto !important;
        max-height: none !important;
        display: block !important;
        padding-bottom: 0 !important;
    }

    /* 6. On masque les éléments d'interface inutiles sur papier (boutons, toggles) */
    .no-print {
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* 7. Astuce : Évite qu'une ligne d'ingrédient soit coupée en deux à cheval sur deux pages */
    label.bg-white {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }
}
</style>
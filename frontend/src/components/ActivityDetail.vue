<template>
    <div class="flex flex-col h-full bg-gray-50 pb-20">
      <div class="bg-scoutBlue text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center transition-all">
        <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
        <p class="text-sm font-light text-blue-100 mt-1">Fiche d'activité</p>
      </div>
      <div class="bg-white px-4 py-3 shadow-sm z-10 flex justify-between items-center shrink-0">
        <button @click="fermerFicheActivite" class="flex items-center text-gray-500 hover:text-[#003B5C] transition-colors font-medium">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Planning
        </button>

        <div class="flex gap-2">
          <span class="text-[10px] font-bold px-2.5 py-1 rounded-md uppercase tracking-wider bg-orange-100 text-[#e85d22]">
            {{ formatTypeLabel(selectedSlot?.slot_type) }}
          </span>
          <span class="text-[10px] font-bold px-2.5 py-1 rounded-md uppercase tracking-wider bg-gray-100 text-gray-600">
            2H30
          </span>
        </div>

        <button @click="sauvegarderFicheActivite" class="text-[#432C7A] font-bold text-sm hover:text-purple-800 transition-colors">
          Enregistrer
        </button>
      </div>

      <div class="flex-1 overflow-y-auto px-4 pt-6 pb-28 space-y-6">
        <div class="flex flex-wrap items-center gap-2 mt-3 text-sm text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          <span>Resp :</span>
          
          <span v-if="selectedResponsiblesDetails.length === 0" class="text-xs italic text-gray-400">Aucun</span>
          
          <span v-for="chef in selectedResponsiblesDetails" :key="chef.id" class="bg-gray-100 text-[#432C7A] px-2.5 py-0.5 rounded-full font-bold text-xs border border-purple-100">
            {{ chef.prenom }}
          </span>
          
          <button @click="ouvrirGestionResponsables" class="w-6 h-6 rounded-full bg-gray-100 text-gray-400 hover:text-[#432C7A] hover:bg-purple-50 border border-transparent hover:border-purple-200 flex items-center justify-center transition-all shadow-sm">
            <span class="text-sm font-bold leading-none mb-0.5">+</span>
          </button>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-gray-100 relative group">
          <div class="flex justify-between items-center mb-3">
            <div class="flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#432C7A]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <h3 class="font-bold text-[#001D2D] text-lg">Imaginaire & Objectifs</h3>
            </div>
            <button v-if="!isEditingImaginaire" @click="isEditingImaginaire = true" class="text-[#432C7A] bg-purple-50 p-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
            </button>
            <button v-else @click="isEditingImaginaire = false" class="text-green-600 bg-green-50 px-3 py-1 text-xs font-bold rounded-lg">OK</button>
          </div>
          <p v-if="!isEditingImaginaire" class="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap cursor-pointer" @click="isEditingImaginaire = true">
            {{ currentActivity.imaginary_and_objectives || "Cliquez ici pour ajouter l'imaginaire et les objectifs pédagogiques de l'activité..." }}
          </p>
          <textarea v-else v-model="currentActivity.imaginary_and_objectives" rows="4" class="w-full bg-gray-50 border border-gray-200 rounded-xl p-3 text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#432C7A]/50 transition-all" placeholder="Rédigez l'imaginaire ici..." autofocus></textarea>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-gray-100">
          <div class="flex items-center gap-2 mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#e85d22]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="font-bold text-[#001D2D] text-lg">Le Déroulé</h3>
          </div>
          
          <div class="relative pl-2.5">
            <div class="absolute left-[15px] top-2 bottom-4 w-0.5 bg-[#e85d22]/30"></div>

            <div v-for="(step, index) in currentActivity.steps" :key="step.id" class="relative mb-6 pl-7 group">
              <div class="absolute left-0 top-1.5 w-2.5 h-2.5 bg-[#e85d22] rounded-full border-2 border-white box-content shadow-sm"></div>
              <div class="flex justify-between items-start gap-2">
                <div class="flex-1">
                  <div class="flex items-baseline gap-2">
                    <span class="font-extrabold text-gray-900 text-[15px]">{{ calculerHeureEtape(index) }}</span>
                    <span class="text-xs text-gray-400 font-semibold tracking-wide">({{ step.duration_minutes }} min)</span>
                  </div>
                  <h4 class="text-[15px] font-bold text-[#003B5C] mt-1">{{ step.title }}</h4>
                  <p v-if="step.description" class="text-sm text-gray-500 mt-1 leading-snug">{{ step.description }}</p>
                </div>
                <div class="flex gap-1 pt-1 opacity-100">
                  <button @click="modifierEtape(index)" class="p-1.5 text-gray-400 hover:text-[#e85d22] hover:bg-orange-50 rounded-lg transition-colors" title="Modifier">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                  </button>
                  <button @click="supprimerEtape(index)" class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors" title="Supprimer">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                  </button>
                </div>
              </div>
            </div>

            <div v-if="isAddingStep" class="relative pl-7 mt-4">
              <div class="absolute left-0 top-1.5 w-2.5 h-2.5 bg-gray-300 rounded-full border-2 border-white box-content"></div>
              <div class="bg-orange-50/50 rounded-xl p-4 border border-orange-100">
                <input v-model="newStep.title" type="text" placeholder="Titre de l'étape (ex: Lancement)" class="w-full bg-white border border-gray-200 rounded-lg px-3 py-2 text-sm font-bold text-[#003B5C] mb-3 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50">
                <textarea v-model="newStep.description" placeholder="Description courte (optionnelle)" rows="2" class="w-full bg-white border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-700 mb-3 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50"></textarea>
                <div class="flex items-center gap-3 mb-4">
                  <label class="text-xs font-bold text-gray-500 uppercase tracking-wider">Durée :</label>
                  <div class="flex items-center bg-white border border-gray-200 rounded-lg overflow-hidden focus-within:ring-2 focus-within:ring-[#e85d22]/50">
                    <input v-model="newStep.duration_minutes" type="number" min="1" class="w-16 px-2 py-1.5 text-sm font-bold text-center focus:outline-none">
                    <span class="text-xs text-gray-500 pr-3 font-medium bg-gray-50 h-full flex items-center">min</span>
                  </div>
                </div>
                <div class="flex gap-2">
                  <button @click="ajouterEtape" class="flex-1 bg-[#e85d22] text-white text-sm font-bold py-2.5 rounded-lg hover:bg-orange-600 transition-colors shadow-sm">Valider</button>
                  <button @click="isAddingStep = false" class="flex-1 bg-white border border-gray-200 text-gray-600 text-sm font-bold py-2.5 rounded-lg hover:bg-gray-50 transition-colors">Annuler</button>
                </div>
              </div>
            </div>

            <div v-else class="relative pl-7 mt-2">
              <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-white border-2 border-gray-300 rounded-full box-content"></div>
              <button @click="ouvrirAjoutEtape" class="bg-orange-50 text-[#e85d22] border border-orange-100 font-semibold text-sm px-4 py-2 rounded-xl hover:bg-orange-100 transition-colors flex items-center gap-1.5">
                <span class="text-lg leading-none mb-0.5">+</span> Ajouter une étape
              </button>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-2xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] border border-gray-100">
          <div class="flex items-center gap-2 mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
            </svg>
            <h3 class="font-bold text-[#001D2D] text-lg">Matériel</h3>
          </div>

          <div class="space-y-3 mb-4">
            <div v-for="mat in currentActivity.materials" :key="mat.id" class="flex items-center gap-3 cursor-pointer group" @click="toggleMateriel(mat)">
              <div :class="['w-5 h-5 rounded border flex justify-center items-center transition-colors', mat.is_checked ? 'bg-[#003B5C] border-[#003B5C]' : 'border-gray-300 group-hover:border-[#003B5C]']">
                <svg v-if="mat.is_checked" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span :class="['text-sm font-medium transition-all', mat.is_checked ? 'text-gray-400 line-through' : 'text-gray-700']">
                {{ mat.item_name }}
              </span>
            </div>
            <p v-if="currentActivity.materials.length === 0" class="text-xs text-gray-400 italic">Aucun matériel listé pour le moment.</p>
          </div>

          <div class="flex gap-2">
            <input v-model="newMaterialName" @keyup.enter="ajouterMateriel" type="text" placeholder="Ajouter un objet..." class="flex-1 bg-gray-50 border border-gray-100 text-gray-700 text-sm font-medium rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#003B5C]/30 transition-all">
            <button @click="ajouterMateriel" class="w-12 bg-gray-100 hover:bg-gray-200 text-gray-600 font-bold text-xl rounded-xl transition-colors flex justify-center items-center">+</button>
          </div>
        </div>
      </div>
    </div>
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-full">
  <div v-if="showResponsiblesModal" class="fixed inset-0 z-50 flex flex-col justify-end">
    <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="showResponsiblesModal = false"></div>
    
    <div class="relative bg-white w-full h-[60vh] rounded-t-3xl shadow-2xl flex flex-col z-10 overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
        <div>
          <h3 class="font-extrabold text-lg text-[#001D2D]">Responsables</h3>
          <p class="text-xs text-gray-500 font-medium">Chefs présents au week-end</p>
        </div>
        <button @click="showResponsiblesModal = false" class="p-2 bg-gray-200 hover:bg-gray-300 rounded-full text-gray-600 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
        </button>
      </div>
      
      <div class="flex-1 overflow-y-auto p-6 space-y-2 bg-gray-50/30">
        <div v-if="presentChefs.length === 0" class="text-center text-gray-500 text-sm mt-4">
          Aucun chef n'est marqué comme présent pour ce camp.
        </div>
        <div v-for="chef in presentChefs" :key="chef.id" @click="toggleResponsible(chef.id)" 
             :class="['border rounded-2xl p-3 flex justify-between items-center cursor-pointer transition-all', activityResponsibles.includes(String(chef.id)) ? 'border-[#432C7A] bg-purple-50' : 'border-gray-200 bg-white hover:border-purple-200']">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-gray-200 overflow-hidden flex items-center justify-center shrink-0">
              <img v-if="chef.photo" :src="chef.photo" class="w-full h-full object-cover">
              <span v-else class="text-xs font-bold text-gray-500">{{ chef.prenom.charAt(0) }}{{ chef.nom.charAt(0) }}</span>
            </div>
            <span class="font-bold text-gray-900 text-sm">{{ chef.prenom }} {{ chef.nom }}</span>
          </div>
          <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center', activityResponsibles.includes(String(chef.id)) ? 'bg-[#432C7A] border-[#432C7A] text-white' : 'border-gray-300']">
            <svg v-if="activityResponsibles.includes(String(chef.id))" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
          </div>
        </div>
      </div>
      
      <div class="p-6 border-t border-gray-100 bg-white shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <button @click="sauvegarderResponsables" class="w-full bg-[#432C7A] hover:bg-purple-900 text-white font-bold py-3.5 rounded-xl transition-transform active:scale-95 shadow-md">
          Valider les responsables
        </button>
      </div>
    </div>
  </div>
</transition>
</template>


<script setup>

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
import { formatTypeLabel, formatHeure, getTheme, formatCourt } from '../utils/helpers.js'
import { 
  selectedCamp, campsList, loading, currentDate, showCampMenu,
  showAddModal, newEvent, showEditCampModal, editCampForm,
  moisActuelTexte, campsDuMois, joursDuCalendrier, joursDuCamp,
  changerMois, selectionnerDate, fermerModal, fetchCamps, 
  soumettreEvenement, modifierCamp, fermerEditCampModal, 
  soumettreModificationCamp, supprimerCamp 
} from '../stores/campsStore.js'

import { onMounted } from 'vue'

onMounted(() => {
    chargerResponsablesActivite()
})

import { userToken, loginToSGDF, isLoggingIn, loginError } from '../stores/authStore.js'
</script>
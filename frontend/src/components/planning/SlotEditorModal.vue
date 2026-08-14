<template>
  <!-- MODALE AJOUT DE SLOT -->
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
    <div v-if="showAddModal" class="absolute inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
      <div class="absolute inset-0 bg-gray-900/40 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="$emit('closeAdd')"></div>
      <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-xl rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col pb-8 md:pb-6 z-10 transition-colors max-h-[90vh]">
        <div class="w-full flex justify-center py-4 md:hidden cursor-pointer" @click="$emit('closeAdd')"><div class="w-12 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full transition-colors"></div></div>
        <div class="px-6 md:pt-6 overflow-y-auto scrollbar-hide space-y-5">
          <div class="flex justify-between items-center mb-2">
            <h2 class="text-xl font-extrabold text-gray-900 dark:text-white transition-colors">Ajouter une activité</h2>
            <button @click="$emit('closeAdd')" class="hidden md:block text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
          </div>

          <!-- Presets Rapides -->
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Presets rapides en 1 clic</label>
            <div class="flex gap-2 overflow-x-auto pb-1 scrollbar-hide">
              <button type="button" @click="applyPreset(newSlot, 'repas')" class="px-3 py-2 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-bold rounded-lg border border-blue-200 dark:border-blue-800 shrink-0 hover:bg-blue-100 transition-colors flex items-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
                <span>Repas</span>
              </button>
              <button type="button" @click="applyPreset(newSlot, 'grand_jeu')" class="px-3 py-2 bg-orange-50 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 text-xs font-bold rounded-lg border border-orange-200 dark:border-orange-800 shrink-0 hover:bg-orange-100 transition-colors flex items-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" /></svg>
                <span>Grand Jeu</span>
              </button>
              <button type="button" @click="applyPreset(newSlot, 'veillee')" class="px-3 py-2 bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs font-bold rounded-lg border border-purple-200 dark:border-purple-800 shrink-0 hover:bg-purple-100 transition-colors flex items-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
                <span>Veillée</span>
              </button>
              <button type="button" @click="applyPreset(newSlot, 'rassemblement')" class="px-3 py-2 bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 text-xs font-bold rounded-lg border border-emerald-200 dark:border-emerald-800 shrink-0 hover:bg-emerald-100 transition-colors flex items-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                <span>Rassemblement</span>
              </button>
              <button type="button" @click="applyPreset(newSlot, 'coucher')" class="px-3 py-2 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 text-xs font-bold rounded-lg border border-indigo-200 dark:border-indigo-800 shrink-0 hover:bg-indigo-100 transition-colors flex items-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
                <span>Coucher</span>
              </button>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 transition-colors">Type</label>
            <div class="grid grid-cols-2 gap-2">
              <button @click="newSlot.slot_type = 'jeu'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', newSlot.slot_type === 'jeu' ? 'border-[#e85d22] bg-orange-50 dark:bg-orange-900/20 text-[#e85d22] dark:text-orange-400' : 'border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500']">Jeu / Anim</button>
              <button @click="newSlot.slot_type = 'repas'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', newSlot.slot_type === 'repas' ? 'border-scoutBlue dark:border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-scoutBlue dark:text-blue-400' : 'border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500']">Repas / Intendance</button>
              <button @click="newSlot.slot_type = 'service'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', newSlot.slot_type === 'service' ? 'border-amber-500 bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400' : 'border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500']">Service / Rangement</button>
              <button @click="newSlot.slot_type = 'autre'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', newSlot.slot_type === 'autre' ? 'border-gray-500 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300' : 'border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500']">Autre</button>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Titre</label>
            <input v-model="newSlot.title" type="text" placeholder="Ex: Grand Jeu de piste" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 dark:focus:ring-orange-500/50 transition-all">
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 transition-colors">Chefs responsables (Sélection multiple)</label>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="chef in chefs" 
                :key="chef.id" 
                type="button" 
                @click="toggleChef(newSlot, chef)"
                :class="['px-3 py-2 rounded-xl text-xs font-bold transition-all border flex items-center gap-1.5 cursor-pointer', isChefSelected(newSlot, chef) ? 'bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 border-purple-300 dark:border-purple-700 shadow-xs ring-2 ring-purple-400/20' : 'bg-gray-50 dark:bg-gray-900 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800']"
              >
                <svg v-if="isChefSelected(newSlot, chef)" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-purple-600 dark:text-purple-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
                <span>{{ chef.prenom }} {{ chef.nom }}</span>
              </button>
            </div>
            <p v-if="newSlot.responsible_name" class="text-xs text-purple-600 dark:text-purple-400 font-semibold mt-1.5">
              Sélectionné(s) : {{ newSlot.responsible_name }}
            </p>
          </div>

          <div v-if="joursDuCamp.length > 1">
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 transition-colors">Jour de l'activité</label>
            <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
              <button v-for="(jour, index) in joursDuCamp" :key="index" @click="newSlot.selected_day = jour" :class="['whitespace-nowrap px-5 py-3 text-sm font-bold rounded-xl transition-colors border-2 capitalize', newSlot.selected_day?.getTime() === jour.getTime() ? 'border-[#e85d22] dark:border-orange-500 bg-orange-50 dark:bg-orange-900/20 text-[#e85d22] dark:text-orange-400' : 'border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700']">{{ formatCourt(jour) }}</button>
            </div>
          </div>
          <div class="flex gap-4">
            <div class="flex-1">
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Heure de début</label>
              <div class="relative"><input v-model="newSlot.start_hour" type="time" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 dark:focus:ring-orange-500/50 text-lg appearance-none transition-colors"></div>
            </div>
            <div class="flex-1">
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Heure de fin</label>
              <input v-model="newSlot.end_hour" type="time" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 dark:focus:ring-orange-500/50 text-lg appearance-none transition-colors">
            </div>
          </div>
          <button @click="$emit('submitAdd')" class="w-full mt-4 bg-[#e85d22] dark:bg-orange-600 hover:bg-orange-600 dark:hover:bg-orange-500 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">Ajouter au planning</button>
        </div>
      </div>
    </div>
  </transition>

  <!-- MODALE MODIFICATION DE SLOT -->
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
    <div v-if="showEditModal" class="absolute inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
      <div class="absolute inset-0 bg-gray-900/40 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="$emit('closeEdit')"></div>
      <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-xl rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col pb-8 md:pb-6 z-10 transition-colors max-h-[90vh]">
        <div class="w-full flex justify-center py-4 md:hidden cursor-pointer" @click="$emit('closeEdit')"><div class="w-12 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full transition-colors"></div></div>
        <div class="px-6 md:pt-6 overflow-y-auto scrollbar-hide space-y-5">
          <div class="flex justify-between items-center mb-2">
            <h2 class="text-xl font-extrabold text-gray-900 dark:text-white transition-colors">Modifier l'activité</h2>
            <button @click="$emit('closeEdit')" class="hidden md:block text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 transition-colors">Type</label>
            <div class="grid grid-cols-2 gap-2">
              <button @click="editSlot.slot_type = 'jeu'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', editSlot.slot_type === 'jeu' ? 'border-[#e85d22] bg-orange-50 dark:bg-orange-900/20 text-[#e85d22] dark:text-orange-400' : 'border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500']">Jeu / Anim</button>
              <button @click="editSlot.slot_type = 'repas'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', editSlot.slot_type === 'repas' ? 'border-scoutBlue bg-blue-50 dark:bg-blue-900/20 text-scoutBlue dark:text-blue-400' : 'border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500']">Repas / Intendance</button>
              <button @click="editSlot.slot_type = 'service'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', editSlot.slot_type === 'service' ? 'border-amber-500 bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400' : 'border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500']">Service / Rangement</button>
              <button @click="editSlot.slot_type = 'autre'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', editSlot.slot_type === 'autre' ? 'border-gray-500 bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300' : 'border-gray-100 dark:border-gray-700 text-gray-400 dark:text-gray-500']">Autre</button>
            </div>
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Titre</label>
            <input v-model="editSlot.title" type="text" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 dark:focus:ring-orange-500/50 transition-all">
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 transition-colors">Chefs responsables (Sélection multiple)</label>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="chef in chefs" 
                :key="chef.id" 
                type="button" 
                @click="toggleChef(editSlot, chef)"
                :class="['px-3 py-2 rounded-xl text-xs font-bold transition-all border flex items-center gap-1.5 cursor-pointer', isChefSelected(editSlot, chef) ? 'bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 border-purple-300 dark:border-purple-700 shadow-xs ring-2 ring-purple-400/20' : 'bg-gray-50 dark:bg-gray-900 text-gray-600 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-800']"
              >
                <svg v-if="isChefSelected(editSlot, chef)" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-purple-600 dark:text-purple-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-gray-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
                <span>{{ chef.prenom }} {{ chef.nom }}</span>
              </button>
            </div>
            <p v-if="editSlot.responsible_name" class="text-xs text-purple-600 dark:text-purple-400 font-semibold mt-1.5">
              Sélectionné(s) : {{ editSlot.responsible_name }}
            </p>
          </div>

          <div v-if="joursDuCamp.length > 1">
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 transition-colors">Jour de l'activité</label>
            <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
              <button v-for="(jour, index) in joursDuCamp" :key="index" @click="editSlot.selected_day = jour" :class="['whitespace-nowrap px-5 py-3 text-sm font-bold rounded-xl transition-colors border-2 capitalize', editSlot.selected_day?.getTime() === jour.getTime() ? 'border-[#e85d22] dark:border-orange-500 bg-orange-50 dark:bg-orange-900/20 text-[#e85d22] dark:text-orange-400' : 'border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700']">{{ formatCourt(jour) }}</button>
            </div>
          </div>
          <div class="flex gap-4">
            <div class="flex-1">
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Heure de début</label>
              <div class="relative"><input v-model="editSlot.start_hour" type="time" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 dark:focus:ring-orange-500/50 text-lg appearance-none transition-colors"></div>
            </div>
            <div class="flex-1">
              <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Heure de fin</label>
              <input v-model="editSlot.end_hour" type="time" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 dark:focus:ring-orange-500/50 text-lg appearance-none transition-colors">
            </div>
          </div>
          <button @click="$emit('submitEdit')" class="w-full mt-4 bg-[#e85d22] dark:bg-orange-600 hover:bg-orange-600 dark:hover:bg-orange-500 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">Enregistrer les modifications</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { formatCourt } from '../../utils/helpers.js'
import { chefs } from '../../stores/adherentsStore.js'

defineProps({
  showAddModal: Boolean,
  showEditModal: Boolean,
  newSlot: { type: Object, default: () => ({}) },
  editSlot: { type: Object, default: () => ({}) },
  joursDuCamp: { type: Array, default: () => [] }
})

defineEmits(['closeAdd', 'closeEdit', 'submitAdd', 'submitEdit'])

const applyPreset = (targetSlot, presetType) => {
  if (presetType === 'repas') {
    targetSlot.title = 'Déjeuner / Intendance'
    targetSlot.slot_type = 'repas'
    targetSlot.start_hour = '12:00'
    targetSlot.end_hour = '13:30'
  } else if (presetType === 'veillee') {
    targetSlot.title = 'Veillée autour du feu'
    targetSlot.slot_type = 'veillée'
    targetSlot.start_hour = '21:00'
    targetSlot.end_hour = '22:30'
  } else if (presetType === 'grand_jeu') {
    targetSlot.title = 'Grand Jeu d\'Imaginaire'
    targetSlot.slot_type = 'jeu'
    targetSlot.start_hour = '14:30'
    targetSlot.end_hour = '17:00'
  } else if (presetType === 'rassemblement') {
    targetSlot.title = 'Rassemblement & Appel'
    targetSlot.slot_type = 'rassemblement'
    targetSlot.start_hour = '14:00'
    targetSlot.end_hour = '14:30'
  } else if (presetType === 'coucher') {
    targetSlot.title = 'Extinction des feux & Coucher'
    targetSlot.slot_type = 'nuit'
    targetSlot.start_hour = '22:30'
    targetSlot.end_hour = '08:00'
  }
}

const isChefSelected = (targetSlot, chef) => {
  if (!targetSlot || !targetSlot.responsible_name) return false
  const name = chef.prenom + ' ' + chef.nom
  const currentNames = targetSlot.responsible_name.split(',').map(n => n.trim())
  return currentNames.includes(name)
}

const toggleChef = (targetSlot, chef) => {
  if (!targetSlot) return
  const name = chef.prenom + ' ' + chef.nom
  let currentNames = targetSlot.responsible_name ? targetSlot.responsible_name.split(',').map(n => n.trim()).filter(Boolean) : []
  if (currentNames.includes(name)) {
    currentNames = currentNames.filter(n => n !== name)
  } else {
    currentNames.push(name)
  }
  targetSlot.responsible_name = currentNames.join(', ')
}
</script>

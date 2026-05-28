<template>
    <div class="flex-1 flex flex-col min-h-0 relative bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      
      <!-- EN-TÊTE FIXE EN HAUT -->
      <div :class="[branchStyles.bg, 'text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center shrink-0 transition-colors']">
        <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
        <p class="text-sm font-light text-blue-100 dark:text-gray-200 mt-1 transition-colors">Calendrier des Camps</p>
      </div>
      
      <!-- ZONE DE SCROLL GLOBALE (Calendrier + Cartes défilent ensemble !) -->
      <main class="flex-1 overflow-y-auto p-4 md:p-8 pb-24 md:pb-8 scrollbar-hide">
        
        <!-- COLONNE CENTRALE POUR LES GRANDS ÉCRANS -->
        <div class="max-w-5xl mx-auto w-full flex flex-col items-center">
            
            <!-- WIDGET CALENDRIER (Transformé en une jolie carte centrée) -->
            <div class="w-full max-w-2xl bg-white dark:bg-gray-800 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 mb-10 overflow-hidden transition-colors">
                
                <!-- Navigation du mois -->
                <div class="px-6 py-4 flex justify-between items-center border-b border-gray-50 dark:border-gray-700/50 transition-colors">
                  <button @click="changerMois(-1)" class="flex items-center text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 text-sm font-medium p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
                    </svg>
                  </button>
                  <h2 class="text-base font-bold text-gray-900 dark:text-white capitalize transition-colors">{{ moisActuelTexte }}</h2>
                  <button @click="changerMois(1)" class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>

                <!-- Grille du calendrier -->
                <div class="p-6">
                  <div class="grid grid-cols-7 mb-4 text-center text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider transition-colors">
                    <div>L</div><div>M</div><div>M</div><div>J</div><div>V</div><div>S</div><div>D</div>
                  </div>
                  <div class="grid grid-cols-7 gap-y-4 text-center text-sm items-center">
                    <div v-for="(jour, index) in joursDuCalendrier" :key="index" @click="gererClicJour(jour)" :class="[ 
                      'relative flex flex-col items-center justify-center py-2 transition-colors', 
                      jour.isCurrentMonth && jour.etatCamp === 'aucun' ? 'cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full' : '', 
                      !jour.isCurrentMonth ? 'text-gray-300 dark:text-gray-600' : 'font-medium', 
                      jour.etatCamp === 'debut' ? `${branchStyles.bg} text-white rounded-l-full cursor-pointer` : '', 
                      jour.etatCamp === 'fin' ? `${branchStyles.bg} text-white rounded-r-full cursor-pointer` : '', 
                      jour.etatCamp === 'milieu' ? `${branchStyles.bg} text-white cursor-pointer` : '', 
                      jour.etatCamp === 'aucun' && jour.isCurrentMonth ? 'text-gray-700 dark:text-gray-200' : ''
                    ]">
                      <span>{{ jour.dayNumber }}</span>
                      <div v-if="jour.etatCamp === 'journee'" :class="[branchStyles.bg, 'w-1.5 h-1.5 rounded-full absolute bottom-0.5']"></div>
                    </div>
                  </div>
                </div>
            </div>

            <!-- SECTION DES CARTES DE CAMPS -->
            <div class="w-full">
              <div class="flex justify-between items-center mb-4 px-2">
                <h3 class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider transition-colors">À venir ce mois-ci</h3>
              </div>
              
              <div v-if="loading" class="text-center p-8 text-sm text-gray-500 dark:text-gray-400 transition-colors">Chargement...</div>
              <div v-if="!loading && campsDuMois.length === 0" class="text-center p-8 text-sm text-gray-400 dark:text-gray-500 transition-colors">Aucun week-end prévu en {{ moisActuelTexte }}.</div>
              
              <!-- GRILLE RESPONSIVE ET CENTRÉE -->
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 w-full">
                <div v-for="camp in campsDuMois" :key="camp.id" :class="['bg-white dark:bg-gray-800 rounded-2xl shadow-sm border-l-4 p-5 flex flex-col justify-between hover:shadow-md transition-all', branchStyles.borderLeft]">
                  <div class="flex gap-4 items-center mb-5">
                    <div :class="['rounded-xl px-3 py-2 text-center min-w-[4rem] transition-colors', branchStyles.lightBg]">
                      <span :class="['block text-[10px] font-bold uppercase transition-colors', branchStyles.text]">{{ formatWeekday(camp.start_date) }}</span>
                      <span :class="['block text-xl font-black tracking-tight transition-colors', branchStyles.text]">{{ formatDay(camp.start_date) }}</span>
                    </div>
                    <div class="flex-1 min-w-0">
                      <h4 class="font-bold text-gray-900 dark:text-white text-lg truncate transition-colors">{{ camp.name }}</h4>
                      <p v-if="camp.location" class="text-xs text-gray-500 dark:text-gray-400 mt-1 truncate transition-colors">Lieu : {{ camp.location }}</p>
                    </div>
                  </div>
                  <button @click="ouvrirPlanning(camp)" :class="['w-full text-sm font-semibold py-3 rounded-xl flex justify-center items-center gap-2 transition-colors mt-auto', branchStyles.btnSolid]">
                    Gérer l'activité
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
                  </button>
                </div>
              </div>
            </div>

        </div>
      </main>

      <!-- BOUTON FLOTTANT + -->
      <button @click="selectionnerDate(new Date())" :class="[branchStyles.bg, 'absolute bottom-24 md:bottom-8 right-6 w-14 h-14 text-white rounded-full shadow-lg flex items-center justify-center hover:scale-105 transition-transform active:scale-95 z-30']">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
      </button>
      
      <!-- MODALE DE CRÉATION (Avec comportement PC Pop-up au centre) -->
      <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
        <div v-if="showAddModal" class="absolute inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
          <div class="absolute inset-0 bg-gray-900/40 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="fermerModal"></div>
          
          <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-xl rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col pb-8 md:pb-6 z-10 transition-colors">
            <div class="w-full flex justify-center py-4 md:hidden cursor-pointer" @click="fermerModal"><div class="w-12 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full"></div></div>
            
            <div class="px-6 md:pt-6 overflow-y-auto scrollbar-hide">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-xl font-extrabold text-gray-900 dark:text-white transition-colors">Planifier un événement</h2>
                <button @click="fermerModal" class="hidden md:block text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </div>
              
              <!-- Tabs Journée / Week-end -->
              <div class="flex p-1 bg-gray-100 dark:bg-gray-900 rounded-xl mb-6 transition-colors">
                <button @click="newEvent.type = 'journee'" :class="['flex-1 py-2 text-sm font-bold rounded-lg transition-all', newEvent.type === 'journee' ? `bg-white dark:bg-gray-800 shadow-sm ${branchStyles.text}` : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300']">Journée</button>
                <button @click="newEvent.type = 'weekend'" :class="['flex-1 py-2 text-sm font-bold rounded-lg transition-all', newEvent.type === 'weekend' ? `bg-white dark:bg-gray-800 shadow-sm ${branchStyles.text}` : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300']">Week-end</button>
              </div>

              <!-- Formulaire -->
              <div class="space-y-4">
                <div>
                  <label class="block text-xs font-bold text-gray-400 dark:text-gray-400 uppercase tracking-wider mb-1 transition-colors">Titre de l'événement</label>
                  <input v-model="newEvent.name" type="text" placeholder="Ex: WE d'équipage" :class="['w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:bg-white dark:focus:bg-gray-800 transition-all', branchStyles.ring]">
                </div>
                <div class="flex gap-4">
                  <div class="flex-1">
                    <label class="block text-xs font-bold text-gray-400 dark:text-gray-400 uppercase tracking-wider mb-1 transition-colors">Début</label>
                    <input v-model="newEvent.startDate" type="date" :class="['w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:bg-white dark:focus:bg-gray-800 transition-all', branchStyles.ring]">
                  </div>
                  <div v-if="newEvent.type === 'weekend'" class="flex-1">
                    <label class="block text-xs font-bold text-gray-400 dark:text-gray-400 uppercase tracking-wider mb-1 transition-colors">Fin</label>
                    <input v-model="newEvent.endDate" type="date" :class="['w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:bg-white dark:focus:bg-gray-800 transition-all', branchStyles.ring]">
                  </div>
                </div>
                <div>
                  <label class="block text-xs font-bold text-gray-400 dark:text-gray-400 uppercase tracking-wider mb-1 transition-colors">Lieu</label>
                  <input v-model="newEvent.location" type="text" placeholder="Ex: Base de la Guiche" :class="['w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:bg-white dark:focus:bg-gray-800 transition-all', branchStyles.ring]">
                </div>
              </div>

              <!-- Bouton Valider -->
              <button @click="soumettreEvenement" :class="['w-full mt-8 text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2 font-bold', branchStyles.btnSolid]">
                Créer l'événement
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>
</template>

<script setup>
import { formatWeekday, formatDay } from '../utils/helpers.js'
import { computed, onMounted } from 'vue'
import { userToken, loginToSGDF, isLoggingIn, loginError, chefBranch } from '../stores/authStore.js'
import { 
  selectedCamp, campsList, loading, currentDate, showCampMenu,
  showAddModal, newEvent, showEditCampModal, editCampForm,
  moisActuelTexte, campsDuMois, joursDuCalendrier, joursDuCamp,
  changerMois, selectionnerDate, fermerModal, fetchCamps, 
  soumettreEvenement, modifierCamp, fermerEditCampModal, 
  soumettreModificationCamp, supprimerCamp 
} from '../stores/campsStore.js'
import { ouvrirPlanning } from '../stores/planningStore.js'

// CALCUL DYNAMIQUE DES COULEURS AVEC LE DARK MODE INCLUS
const branchStyles = computed(() => {
  if (chefBranch.value === 'Louja') {
    return {
      bg: 'bg-[#e85d22]',
      text: 'text-[#e85d22] dark:text-orange-400',
      borderLeft: 'border-l-[#e85d22]',
      btnSolid: 'bg-[#e85d22] hover:bg-orange-700 text-black', 
      lightBg: 'bg-orange-50 dark:bg-orange-900/30',
      ring: 'focus:ring-[#e85d22]/50 dark:focus:ring-orange-500/50'
    }
  }
  if (chefBranch.value === 'Piok') {
    return {
      bg: 'bg-[#da291c]',
      text: 'text-[#da291c] dark:text-red-400',
      borderLeft: 'border-l-[#da291c]',
      btnSolid: 'bg-[#da291c] hover:bg-red-800 text-black', 
      lightBg: 'bg-red-50 dark:bg-red-900/30',
      ring: 'focus:ring-[#da291c]/50 dark:focus:ring-red-500/50'
    }
  }
  // Par défaut : Scout-Guide / Mousses (Bleu)
  return {
    bg: 'bg-[#004267]',
    text: 'text-[#004267] dark:text-blue-300',
    borderLeft: 'border-l-[#004267]',
    btnSolid: 'bg-[#004267] hover:bg-blue-900 text-white', 
    lightBg: 'bg-blue-50 dark:bg-[#004267]/40',
    ring: 'focus:ring-[#004267]/50 dark:focus:ring-blue-500/50'
  }
})

const gererClicJour = (jour) => {
  if (!jour.isCurrentMonth) return
  if (jour.camp) {
    ouvrirPlanning(jour.camp)
  } else {
    selectionnerDate(jour.date)
  }
}

onMounted(async () => {
    await fetchCamps()
})
</script>
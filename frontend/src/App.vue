<template>
  <div class="w-[390px] h-[844px] bg-gray-50 relative overflow-hidden shadow-2xl flex flex-col mx-auto my-8 border border-gray-200 rounded-[2rem]">
    
    <header class="bg-scoutBlue text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center">
      <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
      <p class="text-sm font-light text-blue-100 mt-1">Calendrier des Camps</p>
    </header>

    <div class="bg-white px-4 py-3 flex justify-between items-center z-10">
      <button @click="changerMois(-1)" class="flex items-center text-gray-500 hover:text-gray-700 text-sm font-medium p-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <div class="text-center">
        <h2 class="text-sm font-bold text-gray-900 capitalize">{{ moisActuelTexte }}</h2>
      </div>
      <button @click="changerMois(1)" class="text-gray-500 hover:text-gray-700 p-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <div class="bg-white px-4 pb-4 border-b border-gray-100 shadow-sm z-0">
      <div class="grid grid-cols-7 mb-4 text-center text-xs font-bold text-gray-400 uppercase tracking-wider">
        <div>L</div><div>M</div><div>M</div><div>J</div><div>V</div><div>S</div><div>D</div>
      </div>
      
      <div class="grid grid-cols-7 gap-y-4 text-center text-sm items-center">
        <div 
          v-for="(jour, index) in joursDuCalendrier" 
          :key="index"
          @click="jour.isCurrentMonth ? selectionnerDate(jour.date) : null"
          :class="[
            'relative flex flex-col items-center justify-center py-1 transition-colors',
            jour.isCurrentMonth ? 'cursor-pointer font-medium hover:bg-gray-100 rounded-full text-gray-700' : 'text-gray-300'
          ]"
        >
          <span>{{ jour.dayNumber }}</span>
          
          <div v-if="jour.aUnEvenement" class="w-1.5 h-1.5 bg-scoutBlue rounded-full absolute -bottom-1.5"></div>
        </div>
      </div>
    </div>

    <main class="flex-1 overflow-y-auto p-4 pb-24 scrollbar-hide">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider">À venir ce mois-ci</h3>
      </div>

      <div v-if="loading" class="text-center p-8 text-sm text-gray-500">Chargement...</div>

      <div v-if="!loading && campsDuMois.length === 0" class="text-center p-8 text-sm text-gray-400">
        Aucun week-end prévu en {{ moisActuelTexte }}.
      </div>

      <div 
        v-for="camp in campsDuMois" 
        :key="camp.id" 
        class="bg-white rounded-2xl shadow-sm border-l-4 border-scoutViolet p-4 mb-4 hover:shadow-md transition-shadow"
      >
        <div class="flex gap-4 items-center mb-3">
          <div class="bg-violet-50 rounded-xl px-2 py-2 text-center min-w-[4rem]">
            <span class="block text-[9px] font-bold text-scoutViolet uppercase">{{ formatWeekday(camp.start_date) }}</span>
            <span class="block text-lg font-black text-scoutViolet tracking-tight">{{ formatDay(camp.start_date) }}</span>
          </div>
          <div class="flex-1">
            <h4 class="font-bold text-gray-900 text-lg">{{ camp.name }}</h4>
            <p v-if="camp.location" class="text-xs text-gray-500 mt-0.5">Lieu : {{ camp.location }}</p>
          </div>
        </div>
        <button class="w-full bg-scoutViolet hover:bg-violet-800 text-white text-sm font-semibold py-2.5 rounded-xl flex justify-center items-center gap-2 transition-colors">
          Gérer le week-end
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </button>
      </div>
    </main>

    <button @click="selectionnerDate(new Date())" class="absolute bottom-24 right-6 w-14 h-14 bg-scoutOrange text-white rounded-full shadow-lg flex items-center justify-center hover:bg-orange-600 transition-transform active:scale-95 z-30">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
    </button>
    
    <transition 
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-full"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-full"
    >
      <div v-if="showAddModal" class="absolute inset-0 z-50 flex flex-col justify-end">
        <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity" @click="fermerModal"></div>
        
        <div class="relative bg-white w-full rounded-t-3xl shadow-2xl flex flex-col pb-8 z-10">
          <div class="w-full flex justify-center py-4 cursor-pointer" @click="fermerModal">
            <div class="w-12 h-1.5 bg-gray-200 rounded-full"></div>
          </div>

          <div class="px-6 overflow-y-auto scrollbar-hide">
            <h2 class="text-xl font-extrabold text-gray-900 mb-6">Planifier un événement</h2>

            <div class="flex p-1 bg-gray-100 rounded-xl mb-6">
              <button 
                @click="newEvent.type = 'journee'"
                :class="['flex-1 py-2 text-sm font-bold rounded-lg transition-all', newEvent.type === 'journee' ? 'bg-white text-scoutViolet shadow-sm' : 'text-gray-400 hover:text-gray-600']"
              >
                Journée
              </button>
              <button 
                @click="newEvent.type = 'weekend'"
                :class="['flex-1 py-2 text-sm font-bold rounded-lg transition-all', newEvent.type === 'weekend' ? 'bg-white text-scoutViolet shadow-sm' : 'text-gray-400 hover:text-gray-600']"
              >
                Week-end
              </button>
            </div>

            <div class="space-y-4">
              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Titre de l'événement</label>
                <input v-model="newEvent.name" type="text" placeholder="Ex: WE d'équipage" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 focus:bg-white transition-all">
              </div>

              <div class="flex gap-4">
                <div class="flex-1">
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Début</label>
                  <input v-model="newEvent.startDate" type="date" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 focus:bg-white transition-all">
                </div>
                <div v-if="newEvent.type === 'weekend'" class="flex-1">
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Fin</label>
                  <input v-model="newEvent.endDate" type="date" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 focus:bg-white transition-all">
                </div>
              </div>

              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Lieu</label>
                <input v-model="newEvent.location" type="text" placeholder="Ex: Base de la Guiche" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 focus:bg-white transition-all">
              </div>
            </div>

            <button class="w-full mt-8 bg-scoutViolet hover:bg-violet-800 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">
              Créer l'événement
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    <nav class="absolute bottom-0 w-full bg-white border-t border-gray-200 px-6 py-3 flex justify-between items-center z-40 rounded-b-[2rem]">
      
      <div class="flex flex-col items-center text-gray-400 hover:text-gray-600 cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
        </svg>
        <span class="text-[10px] font-medium mt-1">Unité</span>
      </div>

      <div class="flex flex-col items-center text-scoutViolet cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
        </svg>
        <span class="text-[10px] font-bold mt-1">Camps</span>
      </div>

      <div class="flex flex-col items-center text-gray-400 hover:text-gray-600 cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
        </svg>
        <span class="text-[10px] font-medium mt-1">Matériel</span>
      </div>

      <div class="flex flex-col items-center text-gray-400 hover:text-gray-600 cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <span class="text-[10px] font-medium mt-1">Profil</span>
      </div>

    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// --- 1. ÉTAT DE L'APPLICATION ---
const campsList = ref([])
const loading = ref(true)
const currentDate = ref(new Date())

// --- 2. LOGIQUE API FLASK ---
const fetchCamps = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/camps')
    const json = await response.json()
    if (json.status === 'success') campsList.value = json.data
  } catch (error) {
    console.error('Erreur API:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => fetchCamps())

// --- 3. MOTEUR DU CALENDRIER REACTIF ---
const changerMois = (direction) => {
  const nouvelleDate = new Date(currentDate.value)
  nouvelleDate.setMonth(nouvelleDate.getMonth() + direction)
  currentDate.value = nouvelleDate
}

const moisActuelTexte = computed(() => {
  return currentDate.value.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })
})

const campsDuMois = computed(() => {
  return campsList.value.filter(camp => {
    const dateCamp = new Date(camp.start_date)
    return dateCamp.getMonth() === currentDate.value.getMonth() && 
           dateCamp.getFullYear() === currentDate.value.getFullYear()
  })
})

const joursDuCalendrier = computed(() => {
  const annee = currentDate.value.getFullYear()
  const mois = currentDate.value.getMonth()
  
  const premierJourDuMois = new Date(annee, mois, 1)
  const dernierJourDuMois = new Date(annee, mois + 1, 0)
  
  let decallageDebut = premierJourDuMois.getDay() - 1
  if (decallageDebut === -1) decallageDebut = 6 

  const jours = []
  
  const dernierJourMoisPrecedent = new Date(annee, mois, 0).getDate()
  for (let i = decallageDebut - 1; i >= 0; i--) {
    jours.push({
      dayNumber: dernierJourMoisPrecedent - i,
      isCurrentMonth: false,
      aUnEvenement: false
    })
  }
  
  for (let i = 1; i <= dernierJourDuMois.getDate(); i++) {
    const dateDeLaCase = new Date(annee, mois, i)
    
    const evenementCeJour = campsDuMois.value.some(camp => {
      const dateCamp = new Date(camp.start_date)
      return dateCamp.getDate() === i
    })

    jours.push({
      date: dateDeLaCase,
      dayNumber: i,
      isCurrentMonth: true,
      aUnEvenement: evenementCeJour
    })
  }
  
  const casesRestantes = 42 - jours.length
  for (let i = 1; i <= casesRestantes; i++) {
    jours.push({
      dayNumber: i,
      isCurrentMonth: false,
      aUnEvenement: false
    })
  }
  
  return jours
})

// --- 5. GESTION DU FORMULAIRE D'AJOUT (Bottom Sheet) ---
const showAddModal = ref(false)
const newEvent = ref({
  type: 'weekend', // par défaut, on met 'weekend' (ou 'journee')
  name: '',
  location: '',
  startDate: '',
  endDate: ''
})

// Ouvre le tiroir pré-rempli à la date cliquée
const selectionnerDate = (date) => {
  // Formatage YYYY-MM-DD propre pour les champs <input type="date">
  const annee = date.getFullYear();
  const mois = String(date.getMonth() + 1).padStart(2, '0');
  const jour = String(date.getDate()).padStart(2, '0');
  const dateFormatee = `${annee}-${mois}-${jour}`;
  
  newEvent.value.startDate = dateFormatee
  newEvent.value.endDate = dateFormatee // Par défaut, fin = début
  showAddModal.value = true
}

const fermerModal = () => {
  showAddModal.value = false
}

const formatDay = (d) => new Date(d).toLocaleDateString('fr-FR', { day: '2-digit' })
const formatWeekday = (d) => new Date(d).toLocaleDateString('fr-FR', { weekday: 'short' }).replace('.', '')
</script>
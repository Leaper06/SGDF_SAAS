<template>
  <div class="w-[390px] h-[844px] bg-gray-50 relative overflow-hidden shadow-2xl flex flex-col mx-auto my-8 border border-gray-200 rounded-[2rem]">
    


    <div v-if="currentView === 'calendar'" class="flex-1 flex flex-col min-h-0 relative">
      <div class="bg-scoutBlue text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center transition-all">
      <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
      <p class="text-sm font-light text-blue-100 mt-1">
        {{ currentView === 'calendar' ? 'Calendrier des Camps' : 'Planning du week-end' }}
      </p>
    </div>
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
            jour.isCurrentMonth && jour.etatCamp === 'aucun' ? 'cursor-pointer hover:bg-gray-100 rounded-full' : '',
            !jour.isCurrentMonth ? 'text-gray-300' : 'font-medium',
            
            /* Les classes magiques pour la pilule violette */
            jour.etatCamp === 'debut' ? 'bg-scoutViolet text-white rounded-l-full cursor-pointer' : '',
            jour.etatCamp === 'fin' ? 'bg-scoutViolet text-white rounded-r-full cursor-pointer' : '',
            jour.etatCamp === 'milieu' ? 'bg-scoutViolet text-white cursor-pointer' : '',
            jour.etatCamp === 'aucun' ? 'text-gray-700' : ''
          ]"
        >
          <span>{{ jour.dayNumber }}</span>
          
          <div v-if="jour.etatCamp === 'journee'" class="w-1.5 h-1.5 bg-scoutBlue rounded-full absolute -bottom-1.5"></div>
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
        <button @click="ouvrirPlanning(camp)" class="w-full bg-scoutViolet hover:bg-violet-800 text-white text-sm font-semibold py-2.5 rounded-xl flex justify-center items-center gap-2 transition-colors">
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

            <button @click="soumettreEvenement" class="w-full mt-8 bg-scoutViolet hover:bg-violet-800 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">
                            Créer l'événement
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    </div>
    <div v-else-if="currentView === 'planning'" class="flex-1 flex flex-col min-h-0 relative bg-gray-50">
      <div class="bg-scoutBlue text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center transition-all">
      <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
      <p class="text-sm font-light text-blue-100 mt-1">
        {{ currentView === 'calendar' ? 'Calendrier des Camps' : 'Planning du week-end' }}
      </p>
    </div>
      <div class="bg-white px-4 py-3 flex justify-between items-center border-b border-gray-100 shadow-sm z-10">
        <button @click="currentView = 'calendar'" class="flex items-center text-gray-500 hover:text-gray-700 text-sm font-medium">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
          </svg>
          Retour
        </button>
        <div class="text-center">
          <h2 class="text-sm font-bold text-gray-900">{{ selectedCamp?.name }}</h2>
          <p class="text-[9px] font-bold text-gray-400 uppercase tracking-widest mt-0.5">PIONNIERS-CARAVELLES</p>
        </div>
        <div class="relative">
          <button @click="showCampMenu = !showCampMenu" class="text-gray-400 hover:text-scoutViolet p-1 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
            </svg>
          </button>

          <transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-in" leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
            <div v-if="showCampMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-xl border border-gray-100 py-2 z-50">
              
              <button @click="modifierCamp(); showCampMenu = false" class="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2.5 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                Modifier les infos
              </button>

              <button @click="exporterPlanning(); showCampMenu = false" class="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2.5 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Exporter le planning
              </button>

              <div class="border-t border-gray-100 my-1"></div>

              <button @click="supprimerCamp(); showCampMenu = false" class="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2.5 font-semibold transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Supprimer le week-end
              </button>

            </div>
          </transition>
        </div>
      </div>

      <main class="flex-1 overflow-y-auto pb-24 scrollbar-hide">
        
        <div v-if="Object.keys(slotsParJour).length === 0" class="flex flex-col items-center justify-center p-8 mt-10 text-center">
          <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-sm text-gray-400 font-medium">Aucune activité prévue pour ce week-end.</p>
          <p class="text-xs text-gray-300 mt-1">Utilise le bouton + pour commencer le planning.</p>
        </div>

        <template v-for="(slots, jour) in slotsParJour" :key="jour">
          
          <div 
            @click="joursOuverts[jour] = joursOuverts[jour] === false ? true : false" 
            class="bg-gray-100 px-4 py-2.5 flex justify-between items-center border-y border-gray-200 cursor-pointer transition-colors hover:bg-gray-200"
          >
            <h3 class="text-xs font-bold text-scoutBlue uppercase tracking-wider">{{ jour }}</h3>
            <svg 
              :class="{'rotate-180': joursOuverts[jour] !== false}" 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-4 w-4 text-gray-400 transition-transform duration-300" 
              viewBox="0 0 20 20" fill="currentColor"
            >
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </div>

          <div v-show="joursOuverts[jour] !== false" class="p-4 space-y-4">
            
            <div 
              v-for="slot in slots" 
              :key="slot.id" 
              :class="['bg-white rounded-[1.25rem] shadow-sm border-l-4 p-4 flex gap-4', getTheme(slot.slot_type).border]"
            >
              <div class="min-w-[3rem] text-center pt-0.5">
                <span :class="['block text-sm font-bold', getTheme(slot.slot_type).textTime]">{{ formatHeure(slot.start_time) }}</span>
                <span class="block text-xs font-medium text-gray-400 mt-1">{{ formatHeure(slot.end_time) }}</span>
              </div>
              
              <div class="flex-1">
                <div class="flex justify-between items-start">
                <h4 class="font-bold text-gray-900 text-[15px] pr-2">{{ slot.title }}</h4>
                
                <div class="flex flex-col items-end gap-2">
                  <span :class="['text-[9px] font-bold px-2 py-1.5 rounded-md uppercase tracking-wider', getTheme(slot.slot_type).bgBadge]">
                    {{ formatTypeLabel(slot.slot_type) }}
                  </span>
                  
                  <div class="flex items-center gap-1.5 mt-1">
                    <button @click.stop="modifierSlot(slot)" class="p-1.5 text-gray-300 hover:text-scoutBlue hover:bg-blue-50 rounded-lg transition-all" title="Modifier">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                      </svg>
                    </button>
                    <button @click.stop="supprimerSlot(slot.id)" class="p-1.5 text-gray-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all" title="Supprimer">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              <div class="flex justify-between items-start">
                </div>

              <button 
                v-if="slot.slot_type === 'jeu'"
                @click.stop="ouvrirFicheActivite(slot)" 
                class="mt-3 flex items-center gap-2 px-4 py-2 text-sm font-semibold text-[#e85d22] border border-[#e85d22]/30 rounded-xl bg-white hover:bg-orange-50 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Ouvrir la fiche
              </button>
              

              <button 
                v-if="slot.slot_type === 'repas'"
                @click.stop="ouvrirMenuRepas(slot)" 
                class="mt-3 flex items-center gap-2 px-4 py-2 text-sm font-semibold text-scoutBlue border border-scoutBlue/30 rounded-xl bg-white hover:bg-blue-50 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                </svg>
                Ouvrir le menu
              </button>
              </div>
              
            </div>

          </div>
        </template>
      </main>

      <button @click="ouvrirAjoutSlot" class="absolute bottom-24 right-6 w-14 h-14 bg-[#e85d22] text-white rounded-full shadow-lg shadow-orange-500/30 flex items-center justify-center hover:bg-orange-600 transition-transform active:scale-95 z-30">
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
      leave-to-class="opacity-0 translate-y-full">
      
      <div v-if="showAddSlotModal" class="absolute inset-0 z-50 flex flex-col justify-end">
        <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity" @click="fermerSlotModal"></div>
        
        <div class="relative bg-white w-full rounded-t-3xl shadow-2xl flex flex-col pb-8 z-10">
          <div class="w-full flex justify-center py-4 cursor-pointer" @click="fermerSlotModal">
            <div class="w-12 h-1.5 bg-gray-200 rounded-full"></div>
          </div>

          <div class="px-6 overflow-y-auto scrollbar-hide">
            <h2 class="text-xl font-extrabold text-gray-900 mb-6">Ajouter une activité</h2>

            <div class="space-y-5">
              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Type</label>
                <div class="grid grid-cols-2 gap-2">
                  <button @click="newSlot.slot_type = 'logistique'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', newSlot.slot_type === 'logistique' ? 'border-gray-500 bg-gray-50 text-gray-700' : 'border-gray-100 text-gray-400']">Logistique</button>
                  <button @click="newSlot.slot_type = 'jeu'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', newSlot.slot_type === 'jeu' ? 'border-[#e85d22] bg-orange-50 text-[#e85d22]' : 'border-gray-100 text-gray-400']">Jeu / Anim</button>
                  <button @click="newSlot.slot_type = 'repas'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', newSlot.slot_type === 'repas' ? 'border-scoutBlue bg-blue-50 text-scoutBlue' : 'border-gray-100 text-gray-400']">Repas</button>
                  <button @click="newSlot.slot_type = 'spi'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', newSlot.slot_type === 'spi' ? 'border-[#009ee0] bg-cyan-50 text-[#009ee0]' : 'border-gray-100 text-gray-400']">Veillée / Spi</button>
                </div>
              </div>

              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Titre</label>
                <input v-model="newSlot.title" type="text" placeholder="Ex: Grand Jeu de piste" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 transition-all">
              </div>
        <div v-if="joursDuCamp.length > 1">
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Jour de l'activité</label>
                <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                  <button 
                    v-for="(jour, index) in joursDuCamp" 
                    :key="index"
                    @click="newSlot.selected_day = jour"
                    :class="['whitespace-nowrap px-5 py-3 text-sm font-bold rounded-xl transition-colors border-2 capitalize',
                      newSlot.selected_day?.getTime() === jour.getTime() 
                        ? 'border-[#e85d22] bg-orange-50 text-[#e85d22]' 
                        : 'border-gray-100 bg-gray-50 text-gray-500 hover:bg-gray-100'
                    ]"
                  >
                    {{ formatCourt(jour) }}
                  </button>
                </div>
              </div>

              <div class="flex gap-4">
                <div class="flex-1">
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Heure de début</label>
                  <div class="relative">
                    <input v-model="newSlot.start_hour" type="time" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 text-lg appearance-none">
                  </div>
                </div>
                <div class="flex-1">
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Heure de fin</label>
                  <input v-model="newSlot.end_hour" type="time" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 text-lg appearance-none">
                </div>
              </div>
            </div>
            <button @click="soumettreSlot" class="w-full mt-8 bg-[#e85d22] hover:bg-orange-600 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">
              Ajouter au planning
            </button>
          </div>
        </div>
      </div>
      </transition>
      <transition 
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-full"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-full"
    >
      <div v-if="showEditCampModal" class="absolute inset-0 z-50 flex flex-col justify-end">
        <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity" @click="fermerEditCampModal"></div>
        
        <div class="relative bg-white w-full rounded-t-3xl shadow-2xl flex flex-col pb-8 z-10">
          <div class="w-full flex justify-center py-4 cursor-pointer" @click="fermerEditCampModal">
            <div class="w-12 h-1.5 bg-gray-200 rounded-full"></div>
          </div>

          <div class="px-6 overflow-y-auto scrollbar-hide">
            <h2 class="text-xl font-extrabold text-gray-900 mb-6">Modifier le week-end</h2>

            <div class="space-y-5">
              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Nom du week-end</label>
                <input v-model="editCampForm.name" type="text" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 transition-all">
              </div>

              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Lieu</label>
                <input v-model="editCampForm.location" type="text" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 transition-all">
              </div>

              <div class="flex gap-4">
                <div class="flex-1">
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Début</label>
                  <input v-model="editCampForm.startDate" type="date" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-3 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 text-sm">
                </div>
                <div class="flex-1">
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Fin</label>
                  <input v-model="editCampForm.endDate" type="date" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-3 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 text-sm">
                </div>
              </div>
            </div>

            <button @click="soumettreModificationCamp" class="w-full mt-8 bg-scoutViolet hover:bg-violet-800 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">
              Enregistrer les modifications
            </button>
          </div>
        </div>
      </div>
    </transition>
    <transition 
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-full"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-full"
    >
      <div v-if="showEditSlotModal" class="absolute inset-0 z-50 flex flex-col justify-end">
        <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity" @click="fermerEditSlotModal"></div>
        
        <div class="relative bg-white w-full rounded-t-3xl shadow-2xl flex flex-col pb-8 z-10">
          <div class="w-full flex justify-center py-4 cursor-pointer" @click="fermerEditSlotModal">
            <div class="w-12 h-1.5 bg-gray-200 rounded-full"></div>
          </div>

          <div class="px-6 overflow-y-auto scrollbar-hide">
            <h2 class="text-xl font-extrabold text-gray-900 mb-6">Modifier l'activité</h2>

            <div class="space-y-5">
              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Type</label>
                <div class="grid grid-cols-2 gap-2">
                  <button @click="editSlot.slot_type = 'logistique'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', editSlot.slot_type === 'logistique' ? 'border-gray-500 bg-gray-50 text-gray-700' : 'border-gray-100 text-gray-400']">Logistique</button>
                  <button @click="editSlot.slot_type = 'jeu'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', editSlot.slot_type === 'jeu' ? 'border-[#e85d22] bg-orange-50 text-[#e85d22]' : 'border-gray-100 text-gray-400']">Jeu / Anim</button>
                  <button @click="editSlot.slot_type = 'repas'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', editSlot.slot_type === 'repas' ? 'border-scoutBlue bg-blue-50 text-scoutBlue' : 'border-gray-100 text-gray-400']">Repas</button>
                  <button @click="editSlot.slot_type = 'spi'" :class="['py-2 text-xs font-bold rounded-lg border-2 transition-all', editSlot.slot_type === 'spi' ? 'border-[#009ee0] bg-cyan-50 text-[#009ee0]' : 'border-gray-100 text-gray-400']">Veillée / Spi</button>
                </div>
              </div>

              <div>
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Titre</label>
                <input v-model="editSlot.title" type="text" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 transition-all">
              </div>

              <div v-if="joursDuCamp.length > 1">
                <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Jour de l'activité</label>
                <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                  <button 
                    v-for="(jour, index) in joursDuCamp" 
                    :key="index"
                    @click="editSlot.selected_day = jour"
                    :class="['whitespace-nowrap px-5 py-3 text-sm font-bold rounded-xl transition-colors border-2 capitalize',
                      editSlot.selected_day?.getTime() === jour.getTime() 
                        ? 'border-[#e85d22] bg-orange-50 text-[#e85d22]' 
                        : 'border-gray-100 bg-gray-50 text-gray-500 hover:bg-gray-100'
                    ]"
                  >
                    {{ formatCourt(jour) }}
                  </button>
                </div>
              </div>

              <div class="flex gap-4">
                <div class="flex-1">
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Heure de début</label>
                  <div class="relative">
                    <input v-model="editSlot.start_hour" type="time" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 text-lg appearance-none">
                  </div>
                </div>
                <div class="flex-1">
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Heure de fin</label>
                  <input v-model="editSlot.end_hour" type="time" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 text-lg appearance-none">
                </div>
              </div>
            </div>

            <button @click="soumettreModificationSlot" class="w-full mt-8 bg-[#e85d22] hover:bg-orange-600 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">
              Enregistrer les modifications
            </button>
          </div>
        </div>
      </div>
    </transition>
    </div>
    <div v-else-if="currentView === 'activity_detail' && selectedSlot" class="flex flex-col h-full bg-gray-50 pb-20">
      <div class="bg-scoutBlue text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center transition-all">
      <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
      <p class="text-sm font-light text-blue-100 mt-1">
        Fiche d'activité 
      </p>
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
            {{ formatTypeLabel(selectedSlot.slot_type) }}
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
        
        <div>
          <h2 class="text-3xl font-black text-[#001D2D]">{{ selectedSlot.title }}</h2>
          <div class="flex items-center gap-2 mt-3 text-sm text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span>Resp :</span>
            <span class="bg-gray-100 text-gray-700 px-2 py-0.5 rounded-full font-medium text-xs">Alice</span>
            <span class="bg-gray-100 text-gray-700 px-2 py-0.5 rounded-full font-medium text-xs">Jean</span>
            <button class="text-gray-400 hover:text-gray-600">+</button>
          </div>
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
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
            <button v-else @click="isEditingImaginaire = false" class="text-green-600 bg-green-50 px-3 py-1 text-xs font-bold rounded-lg">
              OK
            </button>
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
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </button>
                  <button @click="supprimerEtape(index)" class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors" title="Supprimer">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
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
            <input 
              v-model="newMaterialName" 
              @keyup.enter="ajouterMateriel"
              type="text" 
              placeholder="Ajouter un objet..." 
              class="flex-1 bg-gray-50 border border-gray-100 text-gray-700 text-sm font-medium rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#003B5C]/30 transition-all"
            >
            <button @click="ajouterMateriel" class="w-12 bg-gray-100 hover:bg-gray-200 text-gray-600 font-bold text-xl rounded-xl transition-colors flex justify-center items-center">
              +
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="currentView === 'menu_builder' && selectedSlot" class="flex flex-col h-full bg-gray-50 pb-20">
        
        <div class="bg-scoutBlue text-white pt-5 pb-6 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative">
            <div class="flex justify-center items-center mb-1">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
            </div>
            <p class="text-center text-blue-100 text-sm font-medium mt-1">Gestion des menus</p>
        </div>

        <div class="bg-white px-4 py-4 shadow-sm z-20 flex justify-between items-center sticky top-0 -mt-4 pt-6">
            <button @click="fermerMenuRepas" class="text-gray-500 hover:text-gray-800 flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                <span class="text-sm font-medium">Planning</span>
            </button>
            <div class="text-center">
                <h2 class="text-sm font-extrabold text-gray-900">{{ selectedSlot.title }}</h2>
            </div>
            <button @click="fermerMenuRepas" class="text-scoutViolet font-bold text-sm">OK</button>
        </div>

        <div class="flex-1 overflow-y-auto p-5 space-y-5 pb-28">
            
            <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1 h-full bg-scoutViolet"></div>
                <div class="flex justify-between items-center mb-1">
                    <div class="flex items-center gap-2 text-scoutViolet">
                        <svg xmlns="http://www.w3.org/2000/xl" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                        <h3 class="font-bold text-gray-800">17 Présents</h3>
                    </div>
                    <button class="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-md font-medium">Modifier</button>
                </div>
                <p class="text-xs text-gray-500 ml-7">14 Pionniers, 3 Chefs. <br> <span class="italic text-gray-400">Louis D. est absent.</span></p>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                <div class="flex items-center justify-between mb-4 border-b border-gray-50 pb-3">
                    <h3 class="font-bold text-gray-800">Composition du menu</h3>
                    <span class="flex items-center gap-1 text-[10px] font-bold text-green-600 bg-green-50 px-2 py-1 rounded-md uppercase tracking-wide">
                        🥬 Équilibré
                    </span>
                </div>

                <div class="flex items-center justify-between py-2 border-b border-gray-50">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-500">🥗</div>
                        <div>
                            <p class="text-xs text-gray-400 font-bold uppercase">Entrée</p>
                            <p class="text-sm font-medium text-gray-900">Carottes râpées vinaigrette</p>
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-between py-2 border-b border-gray-50">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-scoutOrange">🍝</div>
                        <div>
                            <p class="text-xs text-gray-400 font-bold uppercase">Plat</p>
                            <p class="text-sm font-medium text-gray-900">Pâtes Bolognaise</p>
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-between py-2 border-b border-gray-50">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-yellow-50 flex items-center justify-center">🧀</div>
                        <div>
                            <p class="text-xs text-gray-400 font-bold uppercase">Fromage</p>
                            <p class="text-sm font-medium text-gray-900">Camembert & Pain</p>
                        </div>
                    </div>
                </div>

                <div class="flex items-center justify-between py-2">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-500">🍏</div>
                        <div>
                            <p class="text-xs text-gray-400 font-bold uppercase">Dessert</p>
                            <p class="text-sm font-medium text-gray-900">Pommes (vrac)</p>
                        </div>
                    </div>
                </div>

                <button @click="currentView = 'recipe_catalog'" class="w-full mt-4 border-2 border-dashed border-gray-200 rounded-lg py-3 text-sm font-medium text-gray-500 hover:border-scoutViolet hover:text-scoutViolet transition-colors flex justify-center items-center gap-2">
                    <span class="text-lg leading-none">+</span> Ajouter un plat / Recette
                </button>
            </div>
            
            <button @click="alert('Bientôt : Génération automatique du bordereau global !')" class="w-full bg-[#5b2b82] text-white font-bold py-3.5 rounded-xl shadow-md transition-transform active:scale-95 text-sm flex justify-center items-center gap-2">
               🛒 Générer le bordereau de courses
            </button>
        </div>
    </div>
    <div v-else-if="currentView === 'recipe_catalog'" class="flex flex-col h-full bg-bgLight pb-20">
        
        <div class="bg-[#004267] text-white pt-5 pb-6 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative">
            <div class="flex justify-center items-center mb-1">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
            </div>
            <p class="text-center text-blue-100 text-sm font-medium mt-1">Catalogue de recettes</p>
        </div>

        <div class="bg-white px-4 pt-6 pb-3 shadow-sm z-20 sticky top-0 border-b border-gray-100 -mt-4">
            <div class="flex justify-between items-center mb-4">
                <button @click="currentView = 'planning'" class="text-gray-500 hover:text-gray-800 flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
                    <span class="text-sm font-medium">Planning</span>
                </button>
                <h2 class="text-sm font-extrabold text-gray-900">Ajouter un plat</h2>
                <div class="w-10"><button @click="ouvrirEditeurRecette" class="w-8 h-8 rounded-full bg-violet-50 text-[#5b2b82] flex items-center justify-center hover:bg-[#5b2b82] hover:text-white transition-colors">
                    <span class="font-bold text-xl leading-none mb-1">+</span>
                </button></div> 
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
                <button @click="selectedFilter = 'Économique'" :class="['whitespace-nowrap px-3 py-1.5 rounded-full text-xs font-medium border', selectedFilter === 'Économique' ? 'bg-orange-50 text-[#e45a27] border-orange-200' : 'bg-white text-gray-600 border-gray-200']">+ Économique</button>
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
                <button class="w-8 h-8 rounded-full bg-violet-50 text-[#5b2b82] flex items-center justify-center hover:bg-[#5b2b82] hover:text-white transition-colors">
                    <span class="font-bold text-xl leading-none mb-1">+</span>
                </button>
            </div>
            
            <div v-if="filteredRecipes.length === 0" class="text-center p-8 text-gray-400 text-sm">
              Aucune recette ne correspond à ta recherche.
            </div>
            
        </div>
        
    </div>
    <div v-else-if="currentView === 'recipe_builder'" class="flex flex-col h-full bg-bgLight pb-20">
        
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
                    <button @click="newRecipe.is_eco = !newRecipe.is_eco" :class="['px-3 py-1.5 rounded-full text-xs font-medium transition-colors border', newRecipe.is_eco ? 'bg-blue-50 text-blue-600 border-blue-200' : 'bg-white text-gray-500 border-gray-200']">
                        {{ newRecipe.is_eco ? '✓' : '+' }} Économique
                    </button>
                    <button @click="newRecipe.is_fridge_free = !newRecipe.is_fridge_free" :class="['px-3 py-1.5 rounded-full text-xs font-medium transition-colors border', newRecipe.is_fridge_free ? 'bg-purple-50 text-purple-600 border-purple-200' : 'bg-white text-gray-500 border-gray-200']">
                        {{ newRecipe.is_fridge_free ? '✓' : '+' }} Sans frigo
                    </button>
                </div>
            </div>
        </div>
    </div>
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
// --- GESTION DE L'INTENDANCE & RECETTES ---
const searchQuery = ref('')
const selectedFilter = ref('Tous')

// Quelques recettes pour tester l'interface en attendant de brancher la base de données
const recipesList = ref([
  {
    id: 1,
    name: "Salade de chèvre chaud",
    type: "Entrée froide",
    is_vegetarian: true,
    is_pork_free: true,
    is_eco: false
  },
  {
    id: 2,
    name: "Pâtes Bolognaise",
    type: "Plat chaud",
    is_vegetarian: false,
    is_pork_free: false,
    is_eco: true
  },
  {
    id: 3,
    name: "Dahl de Lentilles Corail",
    type: "Plat chaud",
    is_vegetarian: true,
    is_pork_free: true,
    is_eco: true
  }
])

// Fonction pour filtrer dynamiquement les recettes
const filteredRecipes = computed(() => {
  let result = recipesList.value

  // Filtre par recherche texte
  if (searchQuery.value) {
    result = result.filter(r => r.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }

  // Filtres par tags
  if (selectedFilter.value === 'Végétarien') result = result.filter(r => r.is_vegetarian)
  if (selectedFilter.value === 'Sans frigo') result = result.filter(r => r.is_pork_free)
  if (selectedFilter.value === 'Économique') result = result.filter(r => r.is_eco)

  return result
})
// --- GESTION DE L'ÉDITEUR DE RECETTE ---
const newRecipe = ref({
  name: '',
  type: 'Plat chaud',
  ingredients: [
    { id: Date.now(), name: '', qty_child: 80, qty_adult: 120 }
  ],
  is_vegetarian: false,
  is_fridge_free: false, // <-- C'est ici qu'on met le Sans Frigo !
  is_eco: false,
  is_wood_fire: false
})

const ouvrirEditeurRecette = () => {
  // On remet le formulaire à zéro
  newRecipe.value = {
    name: '',
    type: 'Plat chaud',
    ingredients: [ { id: Date.now(), name: '', qty_child: null, qty_adult: null } ],
    is_vegetarian: false,
    is_fridge_free: false,
    is_eco: false,
    is_wood_fire: false
  }
  currentView.value = 'recipe_builder'
}

const ajouterIngredientRecette = () => {
  newRecipe.value.ingredients.push({
    id: Date.now(), name: '', qty_child: null, qty_adult: null
  })
}

const supprimerIngredientRecette = (index) => {
  newRecipe.value.ingredients.splice(index, 1)
}

const partagerRecette = () => {
  if (!newRecipe.value.name) {
    alert("Il faut au moins donner un nom à cette délicieuse recette !")
    return
  }
  
  alert("C'est ici que la recette partira dans la base de données Flask !")
  // Pour l'instant on simule un retour au catalogue
  currentView.value = 'recipe_catalog'
}
const campsList = ref([])
const loading = ref(true)
const currentDate = ref(new Date())
// --- 1. ÉTAT DE L'APPLICATION ---
const currentView = ref('calendar') // Peut être 'calendar' ou 'planning'
const selectedCamp = ref(null)      // Stockera les infos du week-end cliqué
// --- GESTION DE LA FICHE D'ACTIVITÉ ---
const selectedSlot = ref(null)

const currentActivity = ref({
  id: null,
  imaginary_and_objectives: '',
  steps: [],
  materials: []
})

// Fonction qui charge les données quand on clique sur "Ouvrir la fiche"
const ouvrirFicheActivite = async (slot) => {
  selectedSlot.value = slot
  currentView.value = 'activity_detail' // Affiche la page de chargement (le squelette)

  
  try {
    const response = await fetch(`http://localhost:5000/api/planning_slots/${slot.id}/activity`)
    const json = await response.json()
    
    if (json.status === 'success') {
      // On hydrate l'interface avec les données de la base
      currentActivity.value = {
        id: json.data.activity.id,
        imaginary_and_objectives: json.data.activity.imaginary_and_objectives || '',
        steps: json.data.steps || [],
        materials: json.data.materials || []
      }
    }
  } catch (error) {
    console.error("Impossible de charger la fiche :", error)
  }
}
// --- GESTION DU MENU DES REPAS ---
const ouvrirMenuRepas = (slot) => {
  selectedSlot.value = slot
  currentView.value = 'menu_builder' // Nouvelle vue pour la Maquette 1
}

const fermerMenuRepas = () => {
  selectedSlot.value = null
  currentView.value = 'planning'
}

// Fonction qui envoie le gros objet modifié au backend
const sauvegarderFicheActivite = async () => {
  try {
    const response = await fetch(`http://localhost:5000/api/activities/${currentActivity.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentActivity.value)
    })
    const json = await response.json()
    
    if (json.status === 'success') {
      fermerFicheActivite() // Ça s'est bien passé, on retourne au planning
    } else {
      alert("Erreur de sauvegarde : " + json.message)
    }
  } catch (error) {
    console.error("Erreur de sauvegarde :", error)
  }
}

const fermerFicheActivite = () => {
  selectedSlot.value = null
  currentView.value = 'planning'
}

// Gestion de l'Imaginaire
const isEditingImaginaire = ref(false)

// Gestion du Matériel
const newMaterialName = ref('')

const ajouterMateriel = () => {
  if (newMaterialName.value.trim() === '') return
  
  // On l'ajoute visuellement à la liste (on fera la sauvegarde backend plus tard)
  currentActivity.value.materials.push({
    id: Date.now(), // ID temporaire
    item_name: newMaterialName.value,
    is_checked: false
  })
  
  newMaterialName.value = '' // On vide le champ
}

const toggleMateriel = (materiel) => {
  materiel.is_checked = !materiel.is_checked
  // Ici on rajoutera la requête pour mettre à jour la DB
}
// --- GESTION DU DÉROULÉ (TIMELINE) ---
const isAddingStep = ref(false)
const editingStepIndex = ref(null) // Pour savoir quelle étape on est en train de modifier
const newStep = ref({
  title: '',
  description: '',
  duration_minutes: 15
})

// Fonction MAGIQUE pour calculer l'heure de chaque étape
const calculerHeureEtape = (index) => {
  // Sécurité : si on n'a pas d'activité sélectionnée ou pas d'heure de début
  if (!selectedSlot.value || !selectedSlot.value.start_time) return '00:00'
  
  // On part de l'heure de début de l'activité
  let dateEtape = new Date(selectedSlot.value.start_time)
  let minutesCumulees = 0
  
  // On additionne la durée de toutes les étapes PRÉCÉDENTES
  for (let i = 0; i < index; i++) {
    minutesCumulees += currentActivity.value.steps[i].duration_minutes || 0
  }
  
  // On ajoute ces minutes à l'heure de départ
  dateEtape.setMinutes(dateEtape.getMinutes() + minutesCumulees)
  
  // On renvoie le tout au format propre "HH:MM"
  return dateEtape.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

const ouvrirAjoutEtape = () => {
  editingStepIndex.value = null // Mode "Nouvelle étape"
  newStep.value = { title: '', description: '', duration_minutes: 15 }
  isAddingStep.value = true
}

const modifierEtape = (index) => {
  editingStepIndex.value = index // Mode "Modification"
  // On copie les données de l'étape cliquée dans le formulaire
  newStep.value = { ...currentActivity.value.steps[index] }
  isAddingStep.value = true
}

const supprimerEtape = (index) => {
  if(confirm("Veux-tu vraiment supprimer cette étape du déroulé ?")) {
    currentActivity.value.steps.splice(index, 1)
  }
}

const ajouterEtape = () => {
  if (!newStep.value.title) {
    alert("Le titre de l'étape est obligatoire.")
    return
  }
  
  if (editingStepIndex.value !== null) {
    // Si on modifiait une étape existante, on la met à jour
    currentActivity.value.steps[editingStepIndex.value] = { ...newStep.value }
  } else {
    // Sinon, on l'ajoute à la fin
    currentActivity.value.steps.push({
      id: Date.now(), // Temporaire
      title: newStep.value.title,
      description: newStep.value.description,
      duration_minutes: newStep.value.duration_minutes
    })
  }
  
  // On referme l'accordéon et on réinitialise
  isAddingStep.value = false
  editingStepIndex.value = null
}
// Fonction appelée quand on clique sur "Gérer le week-end"
const ouvrirPlanning = async (camp) => {
  selectedCamp.value = camp
  currentView.value = 'planning'
  await fetchSlots(camp.id) // <-- On charge les vrais créneaux ici
}
const slotsList = ref([]) // Stockera les créneaux du camp ouvert
const fetchSlots = async (campId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/camps/${campId}/slots`)
    const json = await response.json()
    if (json.status === 'success') {
      slotsList.value = json.data
    }
  } catch (error) {
    console.error("Erreur lors de la récupération des créneaux :", error)
  }
}

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

// --- GESTION DES MENUS ET ACTIONS ---

// État du menu "3 points" en haut à droite
const showCampMenu = ref(false)

// --- ÉTAT ET LOGIQUE POUR LA MODIFICATION DU CAMP ---
const showEditCampModal = ref(false)
const editCampForm = ref({
  name: '',
  location: '',
  startDate: '',
  endDate: ''
})

const modifierCamp = () => {
  // Petite fonction interne pour nettoyer le format de date (conserver uniquement YYYY-MM-DD)
  const formaterPourInput = (dateStr) => {
    if (!dateStr) return ''
    return dateStr.split('T')[0]
  }

  // On pré-remplit le formulaire avec les valeurs actuelles du week-end ouvert
  editCampForm.value = {
    name: selectedCamp.value.name,
    location: selectedCamp.value.location,
    startDate: formaterPourInput(selectedCamp.value.start_date),
    endDate: formaterPourInput(selectedCamp.value.end_date)
  }
  
  // On ouvre le tiroir de modification
  showEditCampModal.value = true
}

const fermerEditCampModal = () => {
  showEditCampModal.value = false
}



const soumettreModificationCamp = async () => {
  if (!editCampForm.value.name || !editCampForm.value.startDate) {
    alert("Le nom et la date de début sont obligatoires.");
    return;
  }

  try {
    const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editCampForm.value)
    })
    const json = await response.json()

    if (json.status === 'success') {
      fermerEditCampModal()
      
      // LA MAGIE DE LA RÉACTIVITÉ : On met à jour l'affichage immédiatement
      selectedCamp.value.name = editCampForm.value.name
      selectedCamp.value.location = editCampForm.value.location
      selectedCamp.value.start_date = editCampForm.value.startDate
      selectedCamp.value.end_date = editCampForm.value.endDate
      
      // On rafraîchit aussi la liste globale en tâche de fond pour le calendrier
      await fetchCamps()
    } else {
      alert("Erreur lors de la modification : " + json.message)
    }
  } catch (error) {
    console.error("Erreur de modification du camp :", error)
  }
}
 
const exporterPlanning = () => { alert("Bientôt : Export PDF du planning") }
const supprimerCamp = async () => { 
  if(confirm("Veux-tu vraiment supprimer tout ce week-end ?")) {
    try {
      const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}`, {
        method: 'DELETE'
      })
      const json = await response.json()
      
      if (json.status === 'success') {
        // 1. On ferme le menu
        showCampMenu.value = false
        // 2. On retourne sur la vue du calendrier
        currentView.value = 'calendar'
        // 3. On rafraîchit la liste des petits points bleus !
        await fetchCamps() 
      } else {
        alert("Erreur lors de la suppression : " + json.message)
      }
    } catch (error) {
      console.error("Erreur de suppression :", error)
    }
  }
}
const showEditSlotModal = ref(false)
const slotToEditId = ref(null) 
const editSlot = ref({
  title: '',
  slot_type: 'logistique',
  selected_day: null,
  start_hour: '',
  end_hour: ''
})
const modifierSlot = (slot) => {
  try {
    console.log("Tentative d'ouverture de l'activité :", slot.title)
    
    slotToEditId.value = slot.id

    // 1. Fonction ultra-sécurisée pour extraire l'heure
    const getHeureString = (isoString) => {
      if (!isoString) return '12:00' // Sécurité si vide
      const d = new Date(isoString)
      if (isNaN(d.getTime())) return '12:00' // Sécurité si date invalide
      return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
    }

    // 2. Recherche du jour sécurisée
    let matchingDay = joursDuCamp.value[0] // Par défaut, on prend le 1er jour du camp
    
    if (slot.start_time) {
      const baseDate = new Date(slot.start_time)
      // On vérifie que la date n'est pas "Invalid Date" avant de faire des calculs
      if (!isNaN(baseDate.getTime())) {
        baseDate.setHours(0, 0, 0, 0)
        const found = joursDuCamp.value.find(d => d.getTime() === baseDate.getTime())
        if (found) {
          matchingDay = found
        }
      }
    }

    // 3. Pré-remplissage du formulaire
    editSlot.value = {
      title: slot.title || '',
      slot_type: slot.slot_type || 'logistique',
      selected_day: matchingDay,
      start_hour: getHeureString(slot.start_time),
      end_hour: getHeureString(slot.end_time)
    }

    // 4. Déclenchement de l'affichage
    showEditSlotModal.value = true
    console.log("Tiroir ouvert avec succès !")

  } catch (erreur) {
    console.error("Le Javascript a planté pendant l'ouverture :", erreur)
  }
}
const fermerEditSlotModal = () => {
  showEditSlotModal.value = false
}

const soumettreModificationSlot = async () => {
  if (!editSlot.value.title || !editSlot.value.start_hour || !editSlot.value.end_hour) {
    alert("Veuillez remplir le titre et les horaires.")
    return
  }

  try {
    // 1. On recompose la date comme pour l'ajout
    const baseDate = new Date(editSlot.value.selected_day)
    const [startH, startM] = editSlot.value.start_hour.split(':')
    const [endH, endM] = editSlot.value.end_hour.split(':')

    const startDateTime = new Date(baseDate)
    startDateTime.setHours(parseInt(startH), parseInt(startM), 0)

    const endDateTime = new Date(baseDate)
    endDateTime.setHours(parseInt(endH), parseInt(endM), 0)

    if (endDateTime < startDateTime) {
      endDateTime.setDate(endDateTime.getDate() + 1)
    }

    const payload = {
      title: editSlot.value.title,
      slot_type: editSlot.value.slot_type,
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString()
    }

    // 2. On envoie la requête PUT à Flask avec l'ID de l'activité
    const response = await fetch(`http://localhost:5000/api/planning_slots/${slotToEditId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    const json = await response.json()

    if (json.status === 'success') {
      fermerEditSlotModal()
      // 3. On rafraîchit la liste pour voir la modification immédiatement
      await fetchSlots(selectedCamp.value.id) 
    } else {
      alert("Erreur : " + json.message)
    }
  } catch (error) {
    console.error("Erreur d'envoi :", error)
  }
}
 
const supprimerSlot = async (slotId) => {
  if(confirm("Es-tu sûr de vouloir retirer cette activité du planning ?")) {
    try {
      const response = await fetch(`http://localhost:5000/api/planning_slots/${slotId}`, {
        method: 'DELETE'
      })
      const json = await response.json()
      
      if (json.status === 'success') {
        // Succès ! On recharge simplement la liste des créneaux du camp actuel
        await fetchSlots(selectedCamp.value.id)
      } else {
        alert("Erreur lors de la suppression : " + json.message)
      }
    } catch (error) {
      console.error("Erreur de suppression :", error)
    }
  }
}

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
  
// 2. Remplir avec les jours du mois actuel
  for (let i = 1; i <= dernierJourDuMois.getDate(); i++) {
    // On met l'heure à 00:00:00 pour comparer uniquement les dates
    const dateDeLaCase = new Date(annee, mois, i).setHours(0, 0, 0, 0)
    
    let etatCamp = 'aucun' // Peut être : 'aucun', 'journee', 'debut', 'milieu', 'fin'

    // Cherche si un événement chevauche cette date
    const evenementCeJour = campsDuMois.value.find(camp => {
      const start = new Date(camp.start_date).setHours(0, 0, 0, 0)
      const end = camp.end_date ? new Date(camp.end_date).setHours(0, 0, 0, 0) : start
      return dateDeLaCase >= start && dateDeLaCase <= end
    })

    if (evenementCeJour) {
      const start = new Date(evenementCeJour.start_date).setHours(0, 0, 0, 0)
      const end = evenementCeJour.end_date ? new Date(evenementCeJour.end_date).setHours(0, 0, 0, 0) : start

      if (start === end) {
        etatCamp = 'journee' // C'est juste un jour (petit point bleu)
      } else if (dateDeLaCase === start) {
        etatCamp = 'debut'   // Arrondi à gauche
      } else if (dateDeLaCase === end) {
        etatCamp = 'fin'     // Arrondi à droite
      } else {
        etatCamp = 'milieu'  // Carré au milieu
      }
    }

    jours.push({
      date: new Date(annee, mois, i),
      dayNumber: i,
      isCurrentMonth: true,
      etatCamp: etatCamp
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
// Fonction pour envoyer le formulaire au backend
const soumettreEvenement = async () => {
  // 1. Petite vérification de sécurité basique
  if (!newEvent.value.name || !newEvent.value.startDate) {
    alert("Le titre et la date de début sont obligatoires pour les scouts !");
    return;
  }

  try {
    // 2. Appel POST à ton API Flask
    const response = await fetch('http://localhost:5000/api/camps', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newEvent.value)
    });

    const json = await response.json();

    if (json.status === 'success') {
      // 3. Succès ! On ferme le tiroir
      fermerModal();
      
      // 4. On remet le formulaire à zéro pour la prochaine fois
      newEvent.value = { type: 'weekend', name: '', location: '', startDate: '', endDate: '' };
      
      // 5. LA MAGIE VUE.JS : On relance la récupération des camps
      // Cela va mettre à jour 'campsList', ce qui va automatiquement 
      // recalculer le calendrier et afficher le point bleu !
      await fetchCamps();
    } else {
      alert("Erreur lors de la création : " + json.message);
    }
  } catch (error) {
    console.error("Erreur d'envoi :", error);
    alert("Impossible de joindre le serveur pour enregistrer l'événement.");
  }
};
 // --- 6. GESTION DU FORMULAIRE D'AJOUT DE CRÉNEAU (Planning) ---
const showAddSlotModal = ref(false)

// Nouveau format : on sépare le jour et les heures
const newSlot = ref({
  title: '',
  slot_type: 'logistique',
  selected_day: null, // Stockera l'objet Date du jour choisi
  start_hour: '',
  end_hour: ''
})

// Calcule dynamiquement les jours entre start_date et end_date
const joursDuCamp = computed(() => {
  if (!selectedCamp.value) return []
  
  const start = new Date(selectedCamp.value.start_date)
  start.setHours(0, 0, 0, 0)
  
  const end = selectedCamp.value.end_date ? new Date(selectedCamp.value.end_date) : new Date(start)
  end.setHours(0, 0, 0, 0)

  const days = []
  let current = new Date(start)
  while (current <= end) {
    days.push(new Date(current))
    current.setDate(current.getDate() + 1)
  }
  return days
})

const ouvrirAjoutSlot = () => {
  // Par défaut, on sélectionne le tout premier jour du camp
  newSlot.value = { 
    title: '', 
    slot_type: 'logistique', 
    selected_day: joursDuCamp.value[0], 
    start_hour: '', 
    end_hour: '' 
  }
  showAddSlotModal.value = true
}

const fermerSlotModal = () => {
  showAddSlotModal.value = false
}

const soumettreSlot = async () => {
  if (!newSlot.value.title || !newSlot.value.start_hour || !newSlot.value.end_hour) {
    alert("Veuillez remplir le titre et les horaires.")
    return
  }

  try {
    // Recomposition de la date complète pour Supabase (Jour + Heure)
    const baseDate = new Date(newSlot.value.selected_day)
    const [startH, startM] = newSlot.value.start_hour.split(':')
    const [endH, endM] = newSlot.value.end_hour.split(':')

    const startDateTime = new Date(baseDate)
    startDateTime.setHours(parseInt(startH), parseInt(startM), 0)

    const endDateTime = new Date(baseDate)
    endDateTime.setHours(parseInt(endH), parseInt(endM), 0)

    // Petite astuce de chef : si l'activité finit après minuit (ex: veillée de 22h à 01h)
    // on ajoute automatiquement 1 jour à la date de fin !
    if (endDateTime < startDateTime) {
      endDateTime.setDate(endDateTime.getDate() + 1)
    }

    const payload = {
      camp_id: selectedCamp.value.id,
      title: newSlot.value.title,
      slot_type: newSlot.value.slot_type,
      start_time: startDateTime.toISOString(), // Format universel pour la DB
      end_time: endDateTime.toISOString()
    }

    const response = await fetch('http://localhost:5000/api/planning_slots', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    const json = await response.json()

    if (json.status === 'success') {
      fermerSlotModal()
      await fetchSlots(selectedCamp.value.id) // Rafraîchit l'interface
    } else {
      alert("Erreur : " + json.message)
    }
  } catch (error) {
    console.error("Erreur d'envoi :", error)
  }
}

// Fonction utilitaire pour écrire "Sam 26" sur les boutons
const formatCourt = (d) => {
  const date = new Date(d)
  const jour = date.toLocaleDateString('fr-FR', { weekday: 'short' }).replace('.', '')
  const num = date.getDate()
  return `${jour} ${num}`
}
// Organise les créneaux par jour (ex: {"Samedi 26 septembre": [...], "Dimanche 27 septembre": [...]})
const slotsParJour = computed(() => {
  const groupes = {}
  
  slotsList.value.forEach(slot => {
    const dateStr = new Date(slot.start_time).toLocaleDateString('fr-FR', {
      weekday: 'long',
      day: 'numeric',
      month: 'long'
    })
    
    if (!groupes[dateStr]) {
      groupes[dateStr] = []
    }
    groupes[dateStr].push(slot)
  })
  
  return groupes
})

// --- GESTION DE L'AFFICHAGE DU PLANNING ---

// État pour savoir quels jours sont dépliés (accordéons)
const joursOuverts = ref({}) // Par défaut, on laissera ouvert si ce n'est pas "false"

// Fonction pour récupérer les bonnes couleurs et icônes selon le type
const getTheme = (type) => {
  switch (type) {
    case 'jeu':
      return { border: 'border-[#e85d22]', textTime: 'text-[#e85d22]', bgBadge: 'bg-orange-50 text-[#e85d22]' }
    case 'repas':
      return { border: 'border-scoutBlue', textTime: 'text-scoutBlue', bgBadge: 'bg-blue-50 text-scoutBlue' }
    case 'spi':
      return { border: 'border-[#009ee0]', textTime: 'text-[#009ee0]', bgBadge: 'bg-cyan-50 text-[#009ee0]' }
    case 'logistique':
    default:
      return { border: 'border-gray-400', textTime: 'text-gray-700', bgBadge: 'bg-gray-100 text-gray-500' }
  }
}

// Fonction pour formater un type en texte lisible pour le badge
const formatTypeLabel = (type) => {
  const labels = { 'jeu': 'Jeu / Anim', 'repas': 'Intendance', 'spi': 'Temps Spi', 'logistique': 'Logistique' }
  return labels[type] || 'Activité'
}

// Fonctions d'affichage des heures
const formatHeure = (dateTimeStr) => {
  return new Date(dateTimeStr).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

const formatDay = (d) => new Date(d).toLocaleDateString('fr-FR', { day: '2-digit' })
const formatWeekday = (d) => new Date(d).toLocaleDateString('fr-FR', { weekday: 'short' }).replace('.', '')
</script>
<template>
    <div class="flex-1 flex flex-col min-h-0 relative bg-gray-50">
      <div class="bg-scoutBlue text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center transition-all">
        <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
        <p class="text-sm font-light text-blue-100 mt-1">Planning du week-end</p>
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
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                Modifier les infos
              </button>
              <button @click="ouvrirInviteModal" class="w-full text-left px-4 py-3 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-3 border-b border-gray-50">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-scoutBlue" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
              <span class="font-medium">Inviter un chef</span>
          </button>
              <div class="border-t border-gray-100 my-1"></div>
              <button @click="supprimerCamp(); showCampMenu = false" class="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2.5 font-semibold transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
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
          
          <div @click="joursOuverts[jour] = joursOuverts[jour] === false ? true : false" class="bg-gray-100 px-4 py-2.5 flex justify-between items-center border-y border-gray-200 cursor-pointer transition-colors hover:bg-gray-200">
            
            <h3 class="text-xs font-bold text-scoutBlue uppercase tracking-wider">{{ jour }}</h3>
            <svg :class="{'rotate-180': joursOuverts[jour] !== false}" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 transition-transform duration-300" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </div>
          
          <div v-show="joursOuverts[jour] !== false" class="p-4 space-y-4">
            <div v-for="slot in slots" :key="slot.id" :class="['bg-white rounded-[1.25rem] shadow-sm border-l-4 p-4 flex gap-4', getTheme(slot.slot_type).border]">
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
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                      </button>
                      <button @click.stop="supprimerSlot(slot.id)" class="p-1.5 text-gray-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all" title="Supprimer">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                      </button>
                    </div>
                  </div>
                </div>

                <button v-if="slot.slot_type === 'jeu'" @click.stop="ouvrirFicheActivite(slot)" class="mt-3 flex items-center gap-2 px-4 py-2 text-sm font-semibold text-[#e85d22] border border-[#e85d22]/30 rounded-xl bg-white hover:bg-orange-50 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                  Ouvrir la fiche
                </button>
                <button v-if="slot.slot_type === 'repas'" @click.stop="ouvrirMenuRepas(slot)" class="mt-3 flex items-center gap-2 px-4 py-2 text-sm font-semibold text-scoutBlue border border-scoutBlue/30 rounded-xl bg-white hover:bg-blue-50 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
                  Ouvrir le menu
                </button>
                  <button v-if="slot.slot_type === 'logistique'" @click.stop="ouvrirGestionTentes" class="mt-3 flex items-center gap-2 px-4 py-2 text-sm font-semibold text-gray-600 border border-gray-300 rounded-xl bg-white hover:bg-gray-50 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
                Gérer les tentes
              </button>
              </div>
            </div>
          </div>
          
        </template>
<div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-4 flex flex-col gap-3 mb-6">
    <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 bg-blue-50 text-blue-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
        </div>
        <div>
            <h4 class="font-bold text-gray-900">Effectifs & Intendance</h4>
            <p class="text-[11px] text-gray-500">Registre et liste de courses du week-end</p>
        </div>
    </div>
    
    <div class="grid grid-cols-2 gap-2 mt-2">
        <button @click="ouvrirGestionPresence" class="w-full text-xs font-semibold py-2.5 rounded-xl transition-colors bg-gray-100 hover:bg-gray-200 text-gray-700">
            Faire l'appel
        </button>
        
        <button @click="genererBordereauGlobal" class="w-full text-xs font-semibold py-2.5 rounded-xl transition-colors bg-blue-50 hover:bg-blue-100 text-blue-700 flex items-center justify-center gap-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            Courses globales
        </button>
    </div>
</div>
      </main>

      <button @click="ouvrirAjoutSlot" class="absolute bottom-24 right-6 w-14 h-14 bg-[#e85d22] text-white rounded-full shadow-lg shadow-orange-500/30 flex items-center justify-center hover:bg-orange-600 transition-transform active:scale-95 z-30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>

      <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-full">
        <div v-if="showAddSlotModal" class="absolute inset-0 z-50 flex flex-col justify-end">
          <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity" @click="fermerSlotModal"></div>
          <div class="relative bg-white w-full rounded-t-3xl shadow-2xl flex flex-col pb-8 z-10">
            <div class="w-full flex justify-center py-4 cursor-pointer" @click="fermerSlotModal"><div class="w-12 h-1.5 bg-gray-200 rounded-full"></div></div>
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
                    <button v-for="(jour, index) in joursDuCamp" :key="index" @click="newSlot.selected_day = jour" :class="['whitespace-nowrap px-5 py-3 text-sm font-bold rounded-xl transition-colors border-2 capitalize', newSlot.selected_day?.getTime() === jour.getTime() ? 'border-[#e85d22] bg-orange-50 text-[#e85d22]' : 'border-gray-100 bg-gray-50 text-gray-500 hover:bg-gray-100']">{{ formatCourt(jour) }}</button>
                  </div>
                </div>
                <div class="flex gap-4">
                  <div class="flex-1">
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Heure de début</label>
                    <div class="relative"><input v-model="newSlot.start_hour" type="time" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 text-lg appearance-none"></div>
                  </div>
                  <div class="flex-1">
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Heure de fin</label>
                    <input v-model="newSlot.end_hour" type="time" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 text-lg appearance-none">
                  </div>
                </div>
              </div>
              <button @click="soumettreSlot" class="w-full mt-8 bg-[#e85d22] hover:bg-orange-600 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">Ajouter au planning</button>
            </div>
          </div>
        </div>
      </transition>

      <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-full">
        <div v-if="showEditCampModal" class="absolute inset-0 z-50 flex flex-col justify-end">
          <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity" @click="fermerEditCampModal"></div>
          <div class="relative bg-white w-full rounded-t-3xl shadow-2xl flex flex-col pb-8 z-10">
            <div class="w-full flex justify-center py-4 cursor-pointer" @click="fermerEditCampModal"><div class="w-12 h-1.5 bg-gray-200 rounded-full"></div></div>
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
              <button @click="soumettreModificationCamp" class="w-full mt-8 bg-scoutViolet hover:bg-violet-800 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">Enregistrer les modifications</button>
            </div>
          </div>
        </div>
      </transition>

      <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-full">
        <div v-if="showEditSlotModal" class="absolute inset-0 z-50 flex flex-col justify-end">
          <div class="absolute inset-0 bg-gray-900/40 backdrop-blur-sm transition-opacity" @click="fermerEditSlotModal"></div>
          <div class="relative bg-white w-full rounded-t-3xl shadow-2xl flex flex-col pb-8 z-10">
            <div class="w-full flex justify-center py-4 cursor-pointer" @click="fermerEditSlotModal"><div class="w-12 h-1.5 bg-gray-200 rounded-full"></div></div>
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
                    <button v-for="(jour, index) in joursDuCamp" :key="index" @click="editSlot.selected_day = jour" :class="['whitespace-nowrap px-5 py-3 text-sm font-bold rounded-xl transition-colors border-2 capitalize', editSlot.selected_day?.getTime() === jour.getTime() ? 'border-[#e85d22] bg-orange-50 text-[#e85d22]' : 'border-gray-100 bg-gray-50 text-gray-500 hover:bg-gray-100']">{{ formatCourt(jour) }}</button>
                  </div>
                </div>
                <div class="flex gap-4">
                  <div class="flex-1">
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Heure de début</label>
                    <div class="relative"><input v-model="editSlot.start_hour" type="time" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 text-lg appearance-none"></div>
                  </div>
                  <div class="flex-1">
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Heure de fin</label>
                    <input v-model="editSlot.end_hour" type="time" class="w-full bg-gray-50 border border-gray-100 text-gray-900 font-bold rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 text-lg appearance-none">
                  </div>
                </div>
              </div>
              <button @click="soumettreModificationSlot" class="w-full mt-8 bg-[#e85d22] hover:bg-orange-600 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">Enregistrer les modifications</button>
            </div>
          </div>
        </div>
      </transition>
      <transition enter-active-class="transition-opacity duration-200" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition-opacity duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
            <div v-if="showInviteModal" class="fixed inset-0 z-50 flex items-center justify-center px-4">
                <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="fermerInviteModal"></div>
                <div class="bg-white rounded-3xl w-full max-w-sm overflow-hidden shadow-2xl z-10 relative">
                    <div class="bg-scoutBlue p-5 text-white flex justify-between items-center">
                        <h3 class="font-bold text-lg">Inviter un renfort</h3>
                        <button @click="fermerInviteModal" class="text-white/70 hover:text-white p-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <p class="text-sm text-gray-500 font-medium">
                            Saisissez le <strong class="text-gray-800">numéro d'adhérent</strong> du chef extérieur. Ce week-end apparaîtra automatiquement sur son application.
                        </p>
                        <div>
                            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">N° Adhérent SGDF</label>
                            <input v-model="inviteAdherentId" type="text" placeholder="Ex: 162821708" class="w-full border-2 border-gray-100 bg-gray-50 rounded-xl px-4 py-3 font-medium text-gray-900 focus:outline-none focus:border-scoutBlue focus:bg-white transition-colors">
                        </div>
                    </div>
                    
                    <div class="p-4 bg-gray-50 flex gap-3">
                        <button @click="fermerInviteModal" class="flex-1 py-3 text-sm font-bold text-gray-600 bg-white border border-gray-200 rounded-xl hover:bg-gray-100 transition-colors">Annuler</button>
                        <button @click="soumettreInvitation" class="flex-1 py-3 text-sm font-bold text-white bg-scoutBlue rounded-xl hover:bg-blue-800 transition-colors shadow-md">Inviter</button>
                    </div>
                </div>
            </div>
        </transition>
        
      </div>
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-full">
        <div v-if="showTentsModal" class="fixed inset-0 z-50 flex flex-col justify-end">
            <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity" @click="showTentsModal = false"></div>
            
            <div class="relative bg-white w-full h-[85vh] rounded-t-3xl shadow-2xl flex flex-col z-10 overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
                    <div>
                        <h3 class="font-extrabold text-lg text-gray-900">Tentes du week-end</h3>
                        <p class="text-xs text-gray-500 font-medium">Sélectionne le matériel nécessaire</p>
                    </div>
                    <button @click="showTentsModal = false" class="p-2 bg-gray-200 hover:bg-gray-300 rounded-full text-gray-600 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                    </button>
                </div>
                
                <div class="flex-1 overflow-y-auto p-6 space-y-3 bg-gray-50/30">
                    <div v-for="tente in allTents" :key="tente.id" 
                      @click="(tente.status !== 'abimee' && tente.status !== 'deja_reservee') ? toggleTent(tente.id) : null"
                      :class="[
                          'border-2 rounded-2xl p-4 transition-all',
                          (tente.status === 'abimee' || tente.status === 'deja_reservee') ? 'opacity-50 cursor-not-allowed border-gray-200 bg-gray-50' : 'cursor-pointer hover:shadow-sm',
                          selectedTents.includes(tente.id) ? 'border-gray-800 bg-gray-900 text-white shadow-md' : 'border-gray-200 bg-white'
                      ]">
                      
                      <div class="flex justify-between items-center">
                          <div>
                              <h4 :class="['font-bold flex items-center gap-2', selectedTents.includes(tente.id) ? 'text-white' : 'text-gray-900']">
                                  {{ tente.name }}
                                  <span v-if="tente.status === 'abimee'" class="text-[9px] bg-red-100 text-red-600 px-2 py-0.5 rounded font-black uppercase tracking-wider">Abîmée</span>
                                  <span v-if="tente.status === 'deja_reservee'" class="text-[9px] bg-orange-100 text-orange-600 px-2 py-0.5 rounded font-black uppercase tracking-wider">Prise</span>
                              </h4>
                              <p :class="['text-xs mt-1 font-medium', selectedTents.includes(tente.id) ? 'text-gray-300' : 'text-gray-500']">{{ tente.capacity }} places</p>
                          </div>
                          
                          <div :class="[
                              'w-6 h-6 rounded border-2 flex items-center justify-center transition-colors', 
                              selectedTents.includes(tente.id) ? 'bg-white border-white text-gray-900' : 'border-gray-300 bg-transparent'
                          ]">
                              <svg v-if="selectedTents.includes(tente.id)" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                          </div>
                      </div>
                  </div>
                </div>
                
                <div class="p-6 border-t border-gray-100 bg-white shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
                    <div class="flex justify-between items-center mb-4">
                        <span class="text-sm font-bold text-gray-500">Capacité sélectionnée</span>
                        <span class="text-xl font-black text-gray-900">{{ totalCapacity }} places</span>
                    </div>
                    <button @click="sauvegarderTentes" class="w-full bg-gray-900 hover:bg-black text-white font-bold py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">
                        Valider le matériel
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" /></svg>
                    </button>
                </div>
            </div>
        </div>
    </transition>
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-full">
    <div v-if="showAttendanceModal" class="fixed inset-0 z-50 flex flex-col justify-end">
        <div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="showAttendanceModal = false"></div>
        
        <div class="relative bg-white w-full h-[85vh] rounded-t-3xl shadow-2xl flex flex-col z-10 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
                <div>
                    <h3 class="font-extrabold text-lg text-gray-900">Registre de Présence</h3>
                    <p class="text-xs text-gray-500 font-medium">Effectifs du camp</p>
                </div>
                <button @click="showAttendanceModal = false" class="p-2 bg-gray-200 hover:bg-gray-300 rounded-full text-gray-600 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                </button>
            </div>
            
            <div class="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50/30">
                
                <div>
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">La Maîtrise ({{ chefs.length }})</h4>
                    <div class="space-y-2">
                        <div v-for="chef in chefs" :key="chef.id" @click="togglePresence(chef.id)" 
                             :class="['border rounded-2xl p-3 flex justify-between items-center cursor-pointer transition-all', selectedAdherents.includes(String(chef.id)) ? 'border-blue-500 bg-blue-50' : 'border-gray-200 bg-white']">
                            <span class="font-bold text-gray-900 text-sm">{{ chef.prenom }} {{ chef.nom }}</span>
                            <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center', selectedAdherents.includes(String(chef.id)) ? 'bg-blue-500 border-blue-500 text-white' : 'border-gray-300']">
                                <svg v-if="selectedAdherents.includes(String(chef.id))" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                            </div>
                        </div>
                    </div>
                </div>

                <div>
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Les Jeunes ({{ jeunes.length }})</h4>
                    <div class="space-y-2">
                        <div v-for="jeune in jeunes" :key="jeune.id" @click="togglePresence(jeune.id)" 
                             :class="['border rounded-2xl p-3 flex justify-between items-center cursor-pointer transition-all', selectedAdherents.includes(String(jeune.id)) ? 'border-blue-500 bg-blue-50' : 'border-gray-200 bg-white']">
                            <span class="font-bold text-gray-900 text-sm">{{ jeune.prenom }} {{ jeune.nom }}</span>
                            <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center', selectedAdherents.includes(String(jeune.id)) ? 'bg-blue-500 border-blue-500 text-white' : 'border-gray-300']">
                                <svg v-if="selectedAdherents.includes(String(jeune.id))" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            
            <div class="p-6 border-t border-gray-100 bg-white shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
                <div class="flex justify-between items-center mb-4">
                    <span class="text-sm font-bold text-gray-500">Total présents</span>
                    <span class="text-xl font-black text-gray-900">{{ totalPresents }} / {{ chefs.length + jeunes.length }}</span>
                </div>
                <button @click="sauvegarderPresence" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl transition-transform active:scale-95 shadow-md">
                    Enregistrer les présences
                </button>
            </div>
        </div>
    </div>
</transition>
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
</template>

<script setup>
import { 
  currentView, selectedCamp, showCampMenu, modifierCamp, exporterPlanning, supprimerCamp, 
  slotsParJour, joursOuverts, getTheme, formatHeure, formatTypeLabel, modifierSlot, 
  supprimerSlot, ouvrirFicheActivite, ouvrirMenuRepas, ouvrirAjoutSlot, showAddSlotModal, 
  fermerSlotModal, newSlot, joursDuCamp, formatCourt, soumettreSlot, showEditCampModal, 
  fermerEditCampModal, editCampForm, soumettreModificationCamp, showEditSlotModal, 
  fermerEditSlotModal, editSlot, soumettreModificationSlot, showInviteModal, inviteAdherentId,
  ouvrirInviteModal, fermerInviteModal, soumettreInvitation, userToken, groupName, jeunes, chefs, genererBordereauGlobal, showShoppingModal, 
  groupedShoppingList, 
  fermerBordereau, 
  exporterBordereauPDF
} from '../store.js'

import { ref, computed } from 'vue'
// 1. On initialise les tableaux à vide
const allTents = ref([])
const selectedTents = ref([])
const showTentsModal = ref(false)

const totalCapacity = computed(() => {
    return selectedTents.value.reduce((total, tentId) => {
        const tent = allTents.value.find(t => t.id === tentId)
        return total + (tent ? tent.capacity : 0)
    }, 0)
})

// 2. Fonction pour récupérer le catalogue
const chargerTentes = async () => {
    try {
        const nomGroupe = encodeURIComponent(groupName.value)
        
        // On prépare l'URL de base
        let url = `http://localhost:5000/api/tents?group_name=${nomGroupe}`
        
        // NOUVEAU : Si on est sur un week-end précis, on envoie l'ID à Flask
        if (selectedCamp.value) {
            url += `&camp_id=${selectedCamp.value.id}`
        }

        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${userToken.value}` }
        })
        const data = await response.json()
        if (data.status === 'success') {
            allTents.value = data.data
        }
    } catch (error) {
        console.error("Erreur lors du chargement des tentes :", error)
    }
}

// 3. Fonction pour récupérer les tentes déjà cochées pour CE week-end précis
const chargerTentesDuCamp = async (campId) => {
    try {
        const response = await fetch(`http://localhost:5000/api/camps/${campId}/tents`, {
            headers: { 'Authorization': `Bearer ${userToken.value}` }
        })
        const data = await response.json()
        if (data.status === 'success') {
            selectedTents.value = data.selected // Flask nous renvoie juste la liste des IDs [1, 3]
        }
    } catch (error) {
        console.error("Erreur lors du chargement de la sélection :", error)
    }
}


// Fonction pour cocher/décocher une tente au clic
const toggleTent = (tentId) => {
    // On s'assure de contourner les problèmes de type (ex: le nombre 1 vs le texte "1")
    const id = Number(tentId) 
    const index = selectedTents.value.findIndex(t => Number(t) === id)
    
    if (index === -1) {
        // Si elle n'est pas dans la liste, on l'ajoute
        selectedTents.value.push(id)
    } else {
        // Si elle y est déjà, on la retire
        selectedTents.value.splice(index, 1)
    }
}

// La fonction pour sauvegarder la sélection en base de données
const sauvegarderTentes = async () => {
    if (!selectedCamp.value) return

    try {
        const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}/tents`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken.value}`
            },
            body: JSON.stringify({ tents: selectedTents.value })
        })

        const data = await response.json()
        if (data.status === 'success') {
            showTentsModal.value = false
            console.log("✅ Tentes sauvegardées avec succès !")
        }
    } catch (error) {
        console.error("Erreur lors de la sauvegarde :", error)
    }
}

// Fonction qui ouvre la modale ET charge les tentes cochées pour CE camp
const ouvrirGestionTentes = async () => {
    showTentsModal.value = true
    await chargerTentes() // On charge tout le catalogue du groupe
    
    if (selectedCamp.value) {
        try {
            const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}/tents`, {
                headers: { 'Authorization': `Bearer ${userToken.value}` }
            })
            const data = await response.json()
            if (data.status === 'success') {
                // On met à jour les cases cochées
                selectedTents.value = data.selected.map(Number)
            }
        } catch (error) {
            console.error("Erreur lors du chargement de la sélection :", error)
        }
    }
}

const showAttendanceModal = ref(false)
const selectedAdherents = ref([]) // Va contenir les adherent_id cochés

// Calcul dynamique du nombre de présents
const totalPresents = computed(() => selectedAdherents.value.length)

// Fonction pour cocher/décocher
const togglePresence = (adherentId) => {
    const id = String(adherentId) // On force en string pour être sûr
    const index = selectedAdherents.value.indexOf(id)
    if (index === -1) {
        selectedAdherents.value.push(id)
    } else {
        selectedAdherents.value.splice(index, 1)
    }
}

// Ouvrir la modale et charger les données
const ouvrirGestionPresence = async () => {
    showAttendanceModal.value = true
    if (selectedCamp.value) {
        try {
            const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}/attendance`, {
                headers: { 'Authorization': `Bearer ${userToken.value}` }
            })
            const data = await response.json()
            if (data.status === 'success') {
                selectedAdherents.value = data.present.map(String)
            }
        } catch (error) {
            console.error("Erreur lors du chargement des présences :", error)
        }
    }
}

// Sauvegarder dans la DB
const sauvegarderPresence = async () => {
    if (!selectedCamp.value) return
    try {
        const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}/attendance`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken.value}`
            },
            body: JSON.stringify({ present_ids: selectedAdherents.value })
        })
        const data = await response.json()
        if (data.status === 'success') {
            showAttendanceModal.value = false
            console.log("✅ Présences sauvegardées !")
        }
    } catch (error) {
        console.error("Erreur lors de la sauvegarde :", error)
    }
}
// Variable pour stocker la liste de courses
const shoppingList = ref([])
const isGeneratingList = ref(false)

// Fonction pour séparer qui est jeune et qui est chef parmi les présents cochés
const genererListeCourses = async () => {
    if (!selectedCamp.value) return
    isGeneratingList.value = true

    // 1. On compte les jeunes et les adultes en croisant selectedAdherents avec le store
    let nbJeunesPresents = 0
    let nbAdultesPresents = 0

    selectedAdherents.value.forEach(idPresent => {
        // Est-ce que cet ID est dans la liste des jeunes ?
        if (jeunes.value.some(j => String(j.id) === idPresent)) {
            nbJeunesPresents++
        }
        // Est-ce que cet ID est dans la liste des chefs ?
        else if (chefs.value.some(c => String(c.id) === idPresent)) {
            nbAdultesPresents++
        }
    })

    console.log(`Génération pour : ${nbJeunesPresents} jeunes et ${nbAdultesPresents} adultes`)

    // 2. On appelle Flask avec ces bons paramètres
    try {
        const url = `http://localhost:5000/api/camps/${selectedCamp.value.id}/shopping-list?jeunes=${nbJeunesPresents}&adultes=${nbAdultesPresents}`
        
        const response = await fetch(url, {
            headers: { 'Authorization': `Bearer ${userToken.value}` }
        })
        const data = await response.json()
        
        if (data.status === 'success') {
            shoppingList.value = data.data
            console.log("Liste de courses :", shoppingList.value)
        }
    } catch (error) {
        console.error("Erreur lors de la génération :", error)
    } finally {
        isGeneratingList.value = false
    }
}
</script>
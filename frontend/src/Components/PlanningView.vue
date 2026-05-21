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
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                Modifier les infos
              </button>
              <button @click="exporterPlanning(); showCampMenu = false" class="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2.5 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                Exporter le planning
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
    </div>
</template>

<script setup>
import { 
  currentView, selectedCamp, showCampMenu, modifierCamp, exporterPlanning, supprimerCamp, 
  slotsParJour, joursOuverts, getTheme, formatHeure, formatTypeLabel, modifierSlot, 
  supprimerSlot, ouvrirFicheActivite, ouvrirMenuRepas, ouvrirAjoutSlot, showAddSlotModal, 
  fermerSlotModal, newSlot, joursDuCamp, formatCourt, soumettreSlot, showEditCampModal, 
  fermerEditCampModal, editCampForm, soumettreModificationCamp, showEditSlotModal, 
  fermerEditSlotModal, editSlot, soumettreModificationSlot 
} from '../store.js'
</script>
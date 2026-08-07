<template>
    <div class="flex-1 flex flex-col min-h-0 relative bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      
      <div class="bg-scoutBlue dark:bg-gray-800 text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center shrink-0 transition-colors">
        <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
        <p class="text-sm font-light text-blue-100 dark:text-gray-300 mt-1 transition-colors">Planning du week-end</p>
      </div>
      
      <div class="bg-white dark:bg-gray-800 px-4 py-3 flex justify-center items-center border-b border-gray-100 dark:border-gray-700 shadow-sm z-10 shrink-0 transition-colors">
        <div class="max-w-5xl mx-auto w-full flex justify-between items-center">
            <button @click="$router.push('/camps')" class="flex items-center text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 text-sm font-medium transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Retour
            </button>
            <div class="text-center">
            <h2 class="text-sm font-bold text-gray-900 dark:text-white transition-colors">{{ selectedCamp?.name }}</h2>
            </div>
            <div class="relative">
            <button @click="showCampMenu = !showCampMenu" class="text-gray-400 dark:text-gray-500 hover:text-scoutViolet dark:hover:text-purple-400 p-1 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                </svg>
            </button>

            <transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-in" leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
                <div v-if="showCampMenu" class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-100 dark:border-gray-700 py-2 z-50 transition-colors">
                <button @click="modifierCamp(); showCampMenu = false" class="w-full text-left px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2.5 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                    Modifier les infos
                </button>

                <button @click="ouvrirInviteModal" class="w-full text-left px-4 py-3 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-3 border-b border-gray-50 dark:border-gray-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-scoutBlue dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    <span class="font-medium">Inviter un chef</span>
                </button>
                <button @click="exporterDossierWeekEnd" class="w-full text-left px-4 py-3 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-3 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-600 dark:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span class="font-medium">Exporter le dossier (PDF)</span>
                </button>
                <button @click="creerModele" class="w-full text-left px-4 py-3 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-3 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-orange-500 dark:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                </svg>
                <span class="font-medium">Enregistrer comme modèle</span>
                </button>
                <div class="border-t border-gray-100 dark:border-gray-700 my-1 transition-colors"></div>
                <button @click="supprimerCamp(); showCampMenu = false" class="w-full text-left px-4 py-2.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 flex items-center gap-2.5 font-semibold transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    Supprimer le week-end
                </button>
                </div>
            </transition>
            </div>
        </div>
      </div>
      
      <main class="flex-1 overflow-y-auto pb-24 md:pb-8 scrollbar-hide">
        <div class="max-w-5xl mx-auto w-full pt-4">

            <div v-if="Object.keys(slotsParJour).length === 0" class="flex flex-col items-center justify-center p-8 mt-10 text-center">
                <div class="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-300 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                </div>
                <p class="text-sm text-gray-400 dark:text-gray-500 font-medium transition-colors">Aucune activité prévue pour ce week-end.</p>
                <p class="text-xs text-gray-300 dark:text-gray-600 mt-1 transition-colors">Utilise le bouton + pour commencer le planning.</p>
            </div>
            
            <template v-for="(slots, jour) in slotsParJour" :key="jour">
                
                <div @click="joursOuverts[jour] = joursOuverts[jour] === false ? true : false" class="bg-gray-100 dark:bg-gray-800 px-4 py-2.5 flex justify-between items-center border-y border-gray-200 dark:border-gray-700 cursor-pointer transition-colors hover:bg-gray-200 dark:hover:bg-gray-700">
                <h3 class="text-xs font-bold text-scoutBlue dark:text-blue-400 uppercase tracking-wider transition-colors">{{ jour }}</h3>
                <svg :class="{'rotate-180': joursOuverts[jour] !== false}" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 dark:text-gray-500 transition-transform duration-300" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
                </div>
                
                <div v-show="joursOuverts[jour] !== false" class="p-4 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                    <div v-for="slot in slots" :key="slot.id" :class="['bg-white dark:bg-gray-800 rounded-[1.25rem] shadow-sm border-l-4 p-4 flex flex-col justify-between gap-4 transition-colors hover:shadow-md', getTheme(slot.slot_type).border]">
                        <div class="flex gap-4">
                            <div class="min-w-[3rem] text-center pt-0.5">
                                <span :class="['block text-sm font-bold', getTheme(slot.slot_type).textTime]">{{ formatHeure(slot.start_time) }}</span>
                                <span class="block text-xs font-medium text-gray-400 dark:text-gray-500 mt-1 transition-colors">{{ formatHeure(slot.end_time) }}</span>
                            </div>
                            <div class="flex-1 min-w-0">
                                <div class="flex justify-between items-start">
                                <h4 class="font-bold text-gray-900 dark:text-white text-[15px] pr-2 transition-colors">{{ slot.title }}</h4>
                                <div class="flex flex-col items-end gap-2 shrink-0">
                                    <span :class="['text-[9px] font-bold px-2 py-1.5 rounded-md uppercase tracking-wider', getTheme(slot.slot_type).bgBadge]">
                                    {{ formatTypeLabel(slot.slot_type) }}
                                    </span>
                                    <div class="flex items-center gap-1.5 mt-1">
                                    <button @click.stop="modifierSlot(slot)" class="p-1.5 text-gray-300 dark:text-gray-500 hover:text-scoutBlue dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-gray-700 rounded-lg transition-all" title="Modifier">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                                    </button>
                                    <button @click.stop="supprimerSlot(slot.id)" class="p-1.5 text-gray-300 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-gray-700 rounded-lg transition-all" title="Supprimer">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                    </button>
                                    </div>
                                </div>
                                </div>
                            </div>
                        </div>

                        <div class="mt-auto pt-2">
                            <button v-if="slot.slot_type === 'jeu'" @click.stop="ouvrirFicheActivite(slot)" class="w-full flex justify-center items-center gap-2 px-4 py-2.5 text-sm font-semibold text-[#e85d22] dark:text-orange-400 border border-[#e85d22]/30 dark:border-orange-500/30 rounded-xl bg-white dark:bg-gray-800 hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                            Ouvrir la fiche
                            </button>
                            <button v-if="slot.slot_type === 'repas'" @click.stop="ouvrirMenuRepas(slot)" class="w-full flex justify-center items-center gap-2 px-4 py-2.5 text-sm font-semibold text-scoutBlue dark:text-blue-400 border border-scoutBlue/30 dark:border-blue-500/30 rounded-xl bg-white dark:bg-gray-800 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
                            Ouvrir le menu
                            </button>
                        </div>
                    </div>
                </div>
            </template>

            <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 flex flex-col gap-3 mb-6 mx-4 md:mx-0 transition-colors">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center shrink-0 bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-400 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                    </div>
                    <div>
                        <h4 class="font-bold text-gray-900 dark:text-white transition-colors">Effectifs, Intendance & Matériel</h4>
                        <p class="text-[11px] text-gray-500 dark:text-gray-400 transition-colors">Registre, courses et matériel du week-end</p>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-2">
                    <button @click="ouvrirGestionPresence" class="w-full text-sm font-semibold py-3 rounded-xl transition-colors bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200">
                        Présence au week-end
                    </button>

                    <button @click="ouvrirGestionTentes" class="w-full text-sm font-semibold py-3 rounded-xl transition-colors bg-amber-50 dark:bg-amber-900/30 hover:bg-amber-100 dark:hover:bg-amber-800/40 text-amber-700 dark:text-amber-400 flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                        </svg>
                        Tentes & Matériel
                    </button>
                    
                    <button @click="genererBordereauGlobal" class="w-full text-sm font-semibold py-3 rounded-xl transition-colors bg-blue-50 dark:bg-blue-900/30 hover:bg-blue-100 dark:hover:bg-blue-800/40 text-blue-700 dark:text-blue-400 flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                        Courses globales
                    </button>
                </div>

            </div>

        </div> </main>

      <button @click="ouvrirAjoutSlot" class="absolute bottom-24 md:bottom-8 right-6 w-14 h-14 bg-[#e85d22] text-white rounded-full shadow-lg shadow-orange-500/30 dark:shadow-orange-900/50 flex items-center justify-center hover:bg-orange-600 transition-transform active:scale-95 z-30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>

      <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
        <div v-if="showAddSlotModal" class="absolute inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
          <div class="absolute inset-0 bg-gray-900/40 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="fermerSlotModal"></div>
          <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-xl rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col pb-8 md:pb-6 z-10 transition-colors">
            <div class="w-full flex justify-center py-4 md:hidden cursor-pointer" @click="fermerSlotModal"><div class="w-12 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full transition-colors"></div></div>
            <div class="px-6 md:pt-6 overflow-y-auto scrollbar-hide">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-xl font-extrabold text-gray-900 dark:text-white transition-colors">Ajouter une activité</h2>
                <button @click="fermerSlotModal" class="hidden md:block text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </div>
              <div class="space-y-5">
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
              </div>
              <button @click="soumettreSlot" class="w-full mt-8 bg-[#e85d22] dark:bg-orange-600 hover:bg-orange-600 dark:hover:bg-orange-500 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">Ajouter au planning</button>
            </div>
          </div>
        </div>
      </transition>

      <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
        <div v-if="showEditSlotModal" class="absolute inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
          <div class="absolute inset-0 bg-gray-900/40 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="fermerEditSlotModal"></div>
          <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-xl rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col pb-8 md:pb-6 z-10 transition-colors">
            <div class="w-full flex justify-center py-4 md:hidden cursor-pointer" @click="fermerEditSlotModal"><div class="w-12 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full transition-colors"></div></div>
            <div class="px-6 md:pt-6 overflow-y-auto scrollbar-hide">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-xl font-extrabold text-gray-900 dark:text-white transition-colors">Modifier l'activité</h2>
                <button @click="fermerEditSlotModal" class="hidden md:block text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </div>
              <div class="space-y-5">
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
              </div>
              <button @click="soumettreModificationSlot" class="w-full mt-8 bg-[#e85d22] dark:bg-orange-600 hover:bg-orange-600 dark:hover:bg-orange-500 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">Enregistrer les modifications</button>
            </div>
          </div>
        </div>
      </transition>

      <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
        <div v-if="showEditCampModal" class="absolute inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
          <div class="absolute inset-0 bg-gray-900/40 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="fermerEditCampModal"></div>
          <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-xl rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col pb-8 md:pb-6 z-10 transition-colors">
            <div class="w-full flex justify-center py-4 md:hidden cursor-pointer" @click="fermerEditCampModal"><div class="w-12 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full transition-colors"></div></div>
            <div class="px-6 md:pt-6 overflow-y-auto scrollbar-hide">
              <div class="flex justify-between items-center mb-6">
                <h2 class="text-xl font-extrabold text-gray-900 dark:text-white transition-colors">Modifier le week-end</h2>
                <button @click="fermerEditCampModal" class="hidden md:block text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 transition-colors">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </div>
              <div class="space-y-5">
                <div>
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Nom du week-end</label>
                  <input v-model="editCampForm.name" type="text" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 dark:focus:ring-purple-500/50 transition-all">
                </div>
                <div>
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Lieu</label>
                  <input v-model="editCampForm.location" type="text" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 dark:focus:ring-purple-500/50 transition-all">
                </div>
                <div class="flex gap-4">
                  <div class="flex-1">
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Début</label>
                    <input v-model="editCampForm.startDate" type="date" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-3 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 dark:focus:ring-purple-500/50 text-sm transition-all">
                  </div>
                  <div class="flex-1">
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 transition-colors">Fin</label>
                    <input v-model="editCampForm.endDate" type="date" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-3 py-3.5 focus:outline-none focus:ring-2 focus:ring-scoutViolet/50 dark:focus:ring-purple-500/50 text-sm transition-all">
                  </div>
                </div>
              </div>
              <button @click="soumettreModificationCamp" class="w-full mt-8 bg-scoutViolet dark:bg-purple-600 hover:bg-violet-800 dark:hover:bg-purple-700 text-white font-bold text-lg py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">Enregistrer les modifications</button>
            </div>
          </div>
        </div>
      </transition>

      <transition enter-active-class="transition-opacity duration-200" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition-opacity duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
            <div v-if="showInviteModal" class="fixed inset-0 z-50 flex items-center justify-center px-4">
                <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-colors" @click="fermerInviteModal"></div>
                <div class="bg-white dark:bg-gray-800 rounded-3xl w-full max-w-sm overflow-hidden shadow-2xl z-10 relative transition-colors">
                    <div class="bg-scoutBlue dark:bg-gray-900 p-5 text-white flex justify-between items-center transition-colors border-b dark:border-gray-700">
                        <h3 class="font-bold text-lg">Inviter un renfort</h3>
                        <button @click="fermerInviteModal" class="text-white/70 hover:text-white p-1">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    
                    <div class="p-6 space-y-4">
                        <p class="text-sm text-gray-500 dark:text-gray-400 font-medium transition-colors">
                            Saisissez le <strong class="text-gray-800 dark:text-gray-200">numéro d'adhérent</strong> du chef extérieur. Ce week-end apparaîtra automatiquement sur son application.
                        </p>
                        <div>
                            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 transition-colors">N° Adhérent SGDF</label>
                            <input v-model="inviteAdherentId" type="text" placeholder="Ex: 162821708" class="w-full border-2 border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 rounded-xl px-4 py-3 font-medium text-gray-900 dark:text-white focus:outline-none focus:border-scoutBlue dark:focus:border-blue-500 focus:bg-white dark:focus:bg-gray-800 transition-colors">
                        </div>
                    </div>
                    
                    <div class="p-4 bg-gray-50 dark:bg-gray-800/50 flex gap-3 transition-colors border-t dark:border-gray-700">
                        <button @click="fermerInviteModal" class="flex-1 py-3 text-sm font-bold text-gray-600 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">Annuler</button>
                        <button @click="soumettreInvitation" class="flex-1 py-3 text-sm font-bold text-white bg-scoutBlue dark:bg-blue-600 rounded-xl hover:bg-blue-800 dark:hover:bg-blue-700 transition-colors shadow-md">Inviter</button>
                    </div>
                </div>
            </div>
        </transition>

        <transition enter-active-class="transition-opacity duration-200" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition-opacity duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
            <div v-if="isExporting" class="fixed inset-0 z-50 flex items-center justify-center p-4">
                <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm"></div>
                <div class="relative bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-2xl flex items-center gap-4 text-gray-900 dark:text-white border border-gray-100 dark:border-gray-700 z-10">
                    <svg class="animate-spin h-6 w-6 text-scoutBlue dark:text-blue-400 shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <div>
                        <h4 class="font-bold text-sm">Génération du PDF en cours...</h4>
                        <p class="text-xs text-gray-500 dark:text-gray-400 font-medium mt-0.5">Le dossier sera téléchargé automatiquement dans quelques secondes.</p>
                    </div>
                </div>
            </div>
        </transition>
        
      </div>
      
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
        <div v-if="showTentsModal" class="fixed inset-0 pb-20 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
            <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="fermerGestionTentes"></div>
            
            <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-2xl h-[85vh] md:max-h-[85vh] md:h-auto rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col z-10 overflow-hidden transition-colors">
                <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/50 transition-colors">
                    <div>
                        <h3 class="font-extrabold text-lg text-gray-900 dark:text-white transition-colors">Matériel & Logistique</h3>
                        <p class="text-xs text-gray-500 dark:text-gray-400 font-medium transition-colors">Checklist de matériel et réservation de tentes</p>
                    </div>
                    <button @click="fermerGestionTentes" class="p-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full text-gray-600 dark:text-gray-300 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                    </button>
                </div>

                <!-- Onglets (Matériel vs Tentes) -->
                <div class="px-6 pt-3 bg-gray-50/50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-700 flex gap-2">
                    <button @click="activeLogistiqueTab = 'materiel'" :class="['pb-2.5 px-4 text-xs font-bold border-b-2 transition-all flex items-center gap-2', activeLogistiqueTab === 'materiel' ? 'border-scoutBlue dark:border-blue-400 text-scoutBlue dark:text-blue-400' : 'border-transparent text-gray-400 dark:text-gray-500 hover:text-gray-600']">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>
                        Matériel à emporter ({{ campMaterials.length }})
                    </button>
                    <button @click="activeLogistiqueTab = 'tentes'" :class="['pb-2.5 px-4 text-xs font-bold border-b-2 transition-all flex items-center gap-2', activeLogistiqueTab === 'tentes' ? 'border-scoutBlue dark:border-blue-400 text-scoutBlue dark:text-blue-400' : 'border-transparent text-gray-400 dark:text-gray-500 hover:text-gray-600']">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
                        Tentes ({{ selectedTents.length }})
                    </button>
                </div>
                
                <!-- CONTENU ONGLET 1 : MATÉRIEL -->
                <div v-if="activeLogistiqueTab === 'materiel'" class="flex-1 overflow-y-auto p-6 space-y-5 bg-gray-50/30 dark:bg-gray-900/30 transition-colors">
                    
                    <!-- Barre d'outils modèles -->
                    <div class="bg-white dark:bg-gray-800 p-4 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm space-y-3">
                        <div class="flex flex-col md:flex-row gap-2.5 items-stretch md:items-center justify-between">
                            <div class="flex-1 flex gap-2">
                                <select v-model="selectedMaterialTemplateId" class="flex-1 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs font-medium rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500">
                                    <option value="">-- Choisir un modèle de matériel --</option>
                                    <option v-for="tmpl in materialTemplates" :key="tmpl.id" :value="tmpl.id">{{ tmpl.name }} ({{ tmpl.items?.length || 0 }} éléments)</option>
                                </select>
                                <button @click="appliquerTemplateMateriel(selectedCamp?.id, selectedMaterialTemplateId)" :disabled="!selectedMaterialTemplateId" class="px-4 py-2.5 bg-scoutBlue dark:bg-blue-600 disabled:opacity-40 hover:bg-blue-700 text-white font-bold text-xs rounded-xl transition-colors shrink-0">
                                    Appliquer
                                </button>
                            </div>
                            <button @click="enregistrerNouveauTemplateMateriel" class="px-3 py-2.5 border border-scoutBlue/30 text-scoutBlue dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 font-bold text-xs rounded-xl transition-colors shrink-0 flex items-center justify-center gap-1.5">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>
                                Sauvegarder comme modèle
                            </button>
                        </div>
                    </div>

                    <!-- Formulaire d'ajout d'élément -->
                    <div class="flex gap-2">
                        <input v-model="newMaterialItemName" @keyup.enter="ajouterMaterielCamp(selectedCamp?.id)" type="text" placeholder="Ajouter du matériel (ex: Malle pharma, Bâche, Corde...)" class="flex-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-colors">
                        <button @click="ajouterMaterielCamp(selectedCamp?.id)" class="px-5 py-3 bg-[#e85d22] dark:bg-orange-600 hover:bg-orange-600 text-white font-bold text-sm rounded-xl transition-transform active:scale-95 shadow-sm shrink-0">
                            + Ajouter
                        </button>
                    </div>

                    <!-- Checklist du matériel -->
                    <div v-if="campMaterials.length === 0" class="text-center py-10 bg-white dark:bg-gray-800 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700 p-6">
                        <p class="text-sm font-medium text-gray-400 dark:text-gray-500">Aucun matériel dans la liste.</p>
                        <p class="text-xs text-gray-300 dark:text-gray-600 mt-1">Ajoute du matériel ci-dessus ou choisis un modèle réutilisable !</p>
                    </div>

                    <div v-else class="space-y-2">
                        <div v-for="(item, index) in campMaterials" :key="item.id || index" @click="toggleMaterielCamp(index, selectedCamp?.id)" class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl p-3.5 flex items-center justify-between cursor-pointer hover:border-gray-300 dark:hover:border-gray-600 transition-all shadow-sm group">
                            <div class="flex items-center gap-3">
                                <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center transition-colors', item.is_checked ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-gray-300 dark:border-gray-600']">
                                    <svg v-if="item.is_checked" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                                </div>
                                <span :class="['text-sm font-bold transition-colors', item.is_checked ? 'text-gray-400 dark:text-gray-500 line-through' : 'text-gray-900 dark:text-white']">
                                    {{ item.name }}
                                </span>
                            </div>
                            <button @click.stop="supprimerMaterielCamp(index, selectedCamp?.id)" class="text-gray-300 dark:text-gray-600 hover:text-red-500 p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/30 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- CONTENU ONGLET 2 : TENTES -->
                <template v-if="activeLogistiqueTab === 'tentes'">
                    <div class="flex-1 overflow-y-auto p-6 space-y-3 bg-gray-50/30 dark:bg-gray-900/30 transition-colors">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                            <div v-for="tente in allTents" :key="tente.id" 
                            @click="(tente.status !== 'abimee' && tente.status !== 'deja_reservee') ? toggleTent(tente.id) : null"
                            :class="[
                                'border-2 rounded-2xl p-4 transition-all',
                                (tente.status === 'abimee' || tente.status === 'deja_reservee') ? 'opacity-50 cursor-not-allowed border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800' : 'cursor-pointer hover:shadow-sm dark:hover:border-gray-600',
                                selectedTents.includes(tente.id) ? 'border-gray-800 dark:border-gray-500 bg-gray-900 dark:bg-gray-700 text-white shadow-md' : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
                            ]">
                            
                                <div class="flex justify-between items-center">
                                    <div>
                                        <h4 :class="['font-bold flex items-center gap-2 transition-colors', selectedTents.includes(tente.id) ? 'text-white' : 'text-gray-900 dark:text-white']">
                                            {{ tente.name }}
                                            <span v-if="tente.status === 'abimee'" class="text-[9px] bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 px-2 py-0.5 rounded font-black uppercase tracking-wider transition-colors">Abîmée</span>
                                            <span v-if="tente.status === 'deja_reservee'" class="text-[9px] bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 px-2 py-0.5 rounded font-black uppercase tracking-wider transition-colors">Prise</span>
                                        </h4>
                                        <p :class="['text-xs mt-1 font-medium transition-colors', selectedTents.includes(tente.id) ? 'text-gray-300' : 'text-gray-500 dark:text-gray-400']">
                                            {{ tente.capacity }} places
                                        </p>
                                        
                                        <button 
                                            v-if="selectedTents.includes(tente.id)" 
                                            @click.stop="ouvrirDeclarationIncident(tente)" 
                                            class="mt-2 text-[10px] uppercase font-bold text-orange-500 dark:text-orange-400 hover:text-orange-400 dark:hover:text-orange-300 flex items-center transition-colors gap-1"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                            </svg>
                                            Signaler un problème
                                        </button>
                                    </div>
                                    
                                    <div :class="[
                                        'w-6 h-6 rounded border-2 flex items-center justify-center transition-colors shrink-0', 
                                        selectedTents.includes(tente.id) ? 'bg-white border-white text-gray-900' : 'border-gray-300 dark:border-gray-600 bg-transparent'
                                    ]">
                                        <svg v-if="selectedTents.includes(tente.id)" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="p-6 border-t border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] transition-colors">
                        <div class="flex justify-between items-center mb-4">
                            <span class="text-sm font-bold text-gray-500 dark:text-gray-400 transition-colors">Capacité sélectionnée</span>
                            <span class="text-xl font-black text-gray-900 dark:text-white transition-colors">{{ totalCapacity }} places</span>
                        </div>
                        <button @click="sauvegarderTentes" class="w-full bg-gray-900 dark:bg-blue-600 hover:bg-black dark:hover:bg-blue-700 text-white font-bold py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">
                            Valider les tentes
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" /></svg>
                        </button>
                    </div>
                </template>
            </div>
        </div>
    </transition>

    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
    <div v-if="showAttendanceModal" class="fixed inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
        <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-colors" @click="showAttendanceModal = false"></div>
        
        <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-xl h-[85vh] md:max-h-[85vh] md:h-auto rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col z-10 overflow-hidden transition-colors">
            <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/50 transition-colors">
                <div>
                    <h3 class="font-extrabold text-lg text-gray-900 dark:text-white transition-colors">Registre de Présence</h3>
                    <p class="text-xs text-gray-500 dark:text-gray-400 font-medium transition-colors">Effectifs du camp</p>
                </div>
                <button @click="showAttendanceModal = false" class="p-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full text-gray-600 dark:text-gray-300 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
                </button>
            </div>
            
            <div class="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50/30 dark:bg-gray-900/30 transition-colors">
                
                <div>
                    <h4 class="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-3 transition-colors">La Maîtrise ({{ campChefs.length }})</h4>
                    <div class="space-y-2 grid grid-cols-1 md:grid-cols-2 md:gap-2 md:space-y-0">
                        <div v-for="chef in campChefs" :key="chef.adherent_id" @click="togglePresence(chef.adherent_id)"
                             :class="['border rounded-2xl p-3 flex justify-between items-center cursor-pointer transition-all', selectedAdherents.includes(String(chef.adherent_id)) ? 'border-blue-500 dark:border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600']">
                            <span class="font-bold text-gray-900 dark:text-white text-sm transition-colors">{{ chef.first_name }} {{ chef.last_name }}</span>
                            <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center transition-colors', selectedAdherents.includes(String(chef.adherent_id)) ? 'bg-blue-500 border-blue-500 text-white' : 'border-gray-300 dark:border-gray-600']">
                                <svg v-if="selectedAdherents.includes(String(chef.adherent_id))" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                            </div>
                        </div>
                    </div>
                </div>

                <div>
                    <h4 class="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-3 transition-colors">Les Jeunes ({{ campJeunes.length }})</h4>
                    <div class="space-y-2 grid grid-cols-1 md:grid-cols-2 md:gap-2 md:space-y-0">
                        <div v-for="jeune in campJeunes" :key="jeune.adherent_id" @click="togglePresence(jeune.adherent_id)" 
                            :class="['border rounded-2xl p-3 flex justify-between items-center cursor-pointer transition-all', selectedAdherents.includes(String(jeune.adherent_id)) ? 'border-blue-500 dark:border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600']">
                            <span class="font-bold text-gray-900 dark:text-white text-sm transition-colors">{{ jeune.first_name }} {{ jeune.last_name }}</span>
                            <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center transition-colors', selectedAdherents.includes(String(jeune.adherent_id)) ? 'bg-blue-500 border-blue-500 text-white' : 'border-gray-300 dark:border-gray-600']">
                                <svg v-if="selectedAdherents.includes(String(jeune.adherent_id))" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            
            <div class="p-6 border-t border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] transition-colors">
                <div class="flex justify-between items-center mb-4">
                    <span class="text-sm font-bold text-gray-500 dark:text-gray-400 transition-colors">Total présents</span>
                    <span class="text-xl font-black text-gray-900 dark:text-white transition-colors">{{ totalPresents }} / {{ campChefs.length + campJeunes.length }}</span>
                </div>
                <button @click="sauvegarderPresence" class="w-full bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-500 text-white font-bold py-4 rounded-xl transition-transform active:scale-95 shadow-md">
                    Enregistrer les présences
                </button>
            </div>
        </div>
    </div>
    </transition>

    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
        <div v-if="showShoppingModal" class="fixed inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6 printable-modal">
                <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-colors no-print" @click="fermerBordereau"></div>
                
                <div class="relative bg-gray-50 dark:bg-gray-900 w-full md:max-w-2xl h-[90%] md:h-auto md:max-h-[90vh] rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col z-10 overflow-hidden printable-content transition-colors">
                    
                    <div class="bg-[#004267] dark:bg-gray-800 text-white pt-5 pb-6 px-6 shrink-0 text-center rounded-t-3xl md:rounded-t-3xl border-b-4 border-[#003B5C] dark:border-gray-700 transition-colors">
                        <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
                        <p class="text-sm font-medium text-blue-100 dark:text-gray-300 mt-0.5 transition-colors">Bordereau d'achats</p>
                    </div>

                    <div class="bg-gray-50 dark:bg-gray-800 px-4 py-3 flex justify-between items-center shrink-0 shadow-sm border-b border-gray-100 dark:border-gray-700 z-10 transition-colors">
                        <button @click="fermerBordereau" class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 no-print transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" /></svg>
                        </button>
                        <div class="text-center">
                            <h2 class="text-[15px] font-extrabold text-gray-900 dark:text-white transition-colors">Courses du Week-end</h2>
                            <p class="text-[10px] text-gray-400 dark:text-gray-500 font-bold uppercase tracking-widest mt-0.5 transition-colors">3 REPAS • 17 PERSONNES</p>
                        </div>
                        <button @click="exporterBordereauPDF" class="p-2 text-[#5b2b82] dark:text-purple-400 hover:bg-violet-50 dark:hover:bg-purple-900/30 rounded-full transition-colors no-print">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" /></svg>
                        </button>
                    </div>

                    <div class="flex-1 overflow-y-auto p-4 pb-20">
                        
                        <div class="bg-[#5b2b82] dark:bg-purple-900/60 border border-transparent dark:border-purple-800 text-white rounded-xl p-4 mb-6 shadow-md flex justify-between items-center no-print transition-colors">
                            <div>
                                <h3 class="font-bold">Marge de sécurité (Rab)</h3>
                                <p class="text-xs text-violet-200 dark:text-purple-300 mt-0.5 transition-colors">Quantités augmentées de +10%</p>
                            </div>
                            <div @click="rabEnabled = !rabEnabled" :class="['w-12 h-6 rounded-full p-1 cursor-pointer transition-colors duration-300 ease-in-out', rabEnabled ? 'bg-violet-400 dark:bg-purple-500' : 'bg-violet-900 dark:bg-gray-700']">
                                <div :class="['w-4 h-4 bg-white rounded-full shadow-sm transform transition-transform duration-300 ease-in-out', rabEnabled ? 'translate-x-6' : 'translate-x-0']"></div>
                            </div>
                        </div>

                        <div v-for="(items, category) in groupedShoppingList" :key="category" class="mb-6">
                            <h3 class="flex items-center gap-2 text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-3 ml-1 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                                {{ category }}
                            </h3>

                            <div class="space-y-2 grid grid-cols-1 md:grid-cols-2 md:gap-2 md:space-y-0">
                                <label v-for="(item, index) in items" :key="index" class="rounded-xl p-3 shadow-sm border flex items-center justify-between cursor-pointer transition-all hover:border-violet-200 dark:hover:border-purple-700 group" :class="item.isChecked ? 'border-violet-200 dark:border-purple-800 bg-violet-50/30 dark:bg-purple-900/20 opacity-75' : 'bg-white dark:bg-gray-800 border-gray-100 dark:border-gray-700'">
                                    
                                    <div class="flex items-center gap-3">
                                        <div :class="['w-5 h-5 rounded border flex items-center justify-center transition-colors', item.isChecked ? 'bg-[#5b2b82] dark:bg-purple-600 border-[#5b2b82] dark:border-purple-600' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 group-hover:border-[#5b2b82] dark:group-hover:border-purple-500']">
                                            <input type="checkbox" v-model="item.isChecked" class="hidden">
                                            <svg v-if="item.isChecked" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
                                        </div>
                                        
                                        <span :class="['text-[15px] font-bold transition-colors', item.isChecked ? 'text-gray-500 dark:text-gray-400 line-through' : 'text-[#001D2D] dark:text-white']">
                                            {{ item.name }}
                                        </span>
                                    </div>

                                    <div class="font-black text-[#5b2b82] dark:text-purple-300 bg-violet-50 dark:bg-purple-900/40 px-3 py-1.5 rounded-lg text-sm border border-violet-100 dark:border-purple-800/50 transition-colors">
                                        {{ item.displayQty }} <span class="text-xs font-bold">{{ item.displayUnit }}</span>
                                    </div>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </transition>

    <transition enter-active-class="transition-opacity duration-200" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition-opacity duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="showIncidentModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex justify-center items-center z-50 p-4 transition-colors">
            <div class="bg-white dark:bg-gray-800 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl flex flex-col max-h-[90vh] transition-colors">
                <div class="p-6 bg-orange-50 dark:bg-gray-900 border-b border-orange-100 dark:border-gray-700 flex justify-between items-center shrink-0 transition-colors">
                    <div>
                        <h3 class="text-xl font-black text-gray-900 dark:text-white tracking-tight transition-colors">Signaler un incident</h3>
                        <p class="text-sm font-medium text-orange-600 dark:text-orange-400 mt-1 transition-colors">Tente : {{ incidentForm.nom }}</p>
                    </div>
                    <button @click="fermerDeclarationIncident" class="p-2 bg-white dark:bg-gray-800 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-full shadow-sm transition-colors">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </button>
                </div>
                
                <div class="p-6 overflow-y-auto flex-1 space-y-4 bg-gray-50/50 dark:bg-gray-800/50 transition-colors">
                    <div>
                        <label class="block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 transition-colors">État de la tente</label>
                        <select v-model="incidentForm.etat" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/50 transition-colors">
                            <option value="Endommagée">Endommagée (Toile déchirée, tendeur cassé...)</option>
                            <option value="Incomplète">Incomplète (Manque sardines, piquet...)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 transition-colors">Description du problème</label>
                        <textarea v-model="incidentForm.notes_incident" rows="4" placeholder="Ex: Il manque 4 sardines et la fermeture de la porte coince..." class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/50 resize-none transition-colors"></textarea>
                    </div>
                </div>
                
                <div class="p-6 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 shrink-0 transition-colors">
                    <button @click="soumettreIncident" class="w-full py-3.5 bg-orange-500 hover:bg-orange-600 text-white text-sm font-bold rounded-xl shadow-md transition-colors">
                        Enregistrer l'incident
                    </button>
                </div>
            </div>
        </div>
    </transition>

</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { 
  showIncidentModal, incidentForm, ouvrirDeclarationIncident, fermerDeclarationIncident, soumettreIncident,
  campMaterials, materialTemplates, newMaterialItemName, isSavingMaterials, fetchCampMaterials, sauvegarderMaterielCamp,
  ajouterMaterielCamp, supprimerMaterielCamp, toggleMaterielCamp, fetchMaterialTemplates, appliquerTemplateMateriel, creerTemplateMateriel,
  subscribeToMaterials, unsubscribeFromMaterials
} from '../stores/logistiqueStore.js'

const activeLogistiqueTab = ref('materiel')
const selectedMaterialTemplateId = ref('')

const enregistrerNouveauTemplateMateriel = () => {
    const nom = prompt("Nom du modèle de matériel (ex: Matériel WE classique) :")
    if (nom && nom.trim() !== '') {
        creerTemplateMateriel(nom.trim())
    }
}
import { 
  searchQuery, selectedFilter, recipesList, currentMeal, currentMealRecipes, newRecipe, 
  shoppingList, showShoppingModal, rabEnabled, currentShoppingMealId, filteredRecipes, 
  groupedShoppingList, chargerCatalogueRecettes, ouvrirEditeurRecette, ajouterIngredientRecette, 
  supprimerIngredientRecette, partagerRecette, ouvrirMenuRepas, retirerRecette, ajouterRecetteAuMenu, 
  fermerMenuRepas, genererBordereau, genererBordereauGlobal, fermerBordereau, exporterBordereauPDF 
} from '../stores/intendanceStore.js'
import { userToken, loginToSGDF, isLoggingIn, loginError, chefBranch, groupName, isDemoMode } from '../stores/authStore.js'
import { getTheme, formatHeure, formatTypeLabel, formatCourt } from '../utils/helpers.js'
import { adherentsList, isLoadingAdherents, jeunes, chefs, fetchAdherents } from '../stores/adherentsStore.js'
import { 
  selectedCamp, campsList, loading, currentDate, showCampMenu,
  showAddModal, newEvent, showEditCampModal, editCampForm,
  moisActuelTexte, campsDuMois, joursDuCalendrier, joursDuCamp,
  changerMois, selectionnerDate, fermerModal, fetchCamps, 
  soumettreEvenement, modifierCamp, fermerEditCampModal, 
  soumettreModificationCamp, supprimerCamp, creerTemplateAPartirDeCamp 
} from '../stores/campsStore.js'

const creerModele = () => {
    showCampMenu.value = false;
    const nom = prompt("Entrez le nom du nouveau modèle :");
    if (nom && nom.trim() !== "") {
        creerTemplateAPartirDeCamp(selectedCamp.value.id, nom.trim());
    }
}
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
import { API_BASE_URL } from '../api/config.js' 

const campJeunes = ref([])
const campChefs = ref([])

const isExporting = ref(false)

const allTents = ref([])
const selectedTents = ref([])
const showTentsModal = ref(false)

const totalCapacity = computed(() => {
    return selectedTents.value.reduce((total, tentId) => {
        const tent = allTents.value.find(t => t.id === tentId)
        return total + (tent ? tent.capacity : 0)
    }, 0)
})

const chargerTentes = async () => {
    try {
        const nomGroupe = encodeURIComponent(groupName.value)
        let url = `${API_BASE_URL}/tents?group_name=${nomGroupe}`
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

const chargerTentesDuCamp = async (campId) => {
    try {
        const response = await fetch(`${API_BASE_URL}/camps/${campId}/tents`, {
            headers: { 'Authorization': `Bearer ${userToken.value}` }
        })
        const data = await response.json()
        if (data.status === 'success') {
            selectedTents.value = data.selected
        }
    } catch (error) {
        console.error("Erreur lors du chargement de la sélection :", error)
    }
}


const toggleTent = (tentId) => {
    const id = Number(tentId) 
    const index = selectedTents.value.findIndex(t => Number(t) === id)
    if (index === -1) {
        selectedTents.value.push(id)
    } else {
        selectedTents.value.splice(index, 1)
    }
}

const sauvegarderTentes = async () => {
    if (isDemoMode.value) { showTentsModal.value = false; return }
    if (!selectedCamp.value) return
    try {
        const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/tents`, {
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

const ouvrirGestionTentes = async () => {
    showTentsModal.value = true
    if (selectedCamp.value) {
        fetchCampMaterials(selectedCamp.value.id)
        fetchMaterialTemplates()
        subscribeToMaterials(selectedCamp.value.id)
    }
    if (isDemoMode.value) {
        allTents.value = [
            { id: 1, name: 'Tente Patrouille Tigres', capacity: 8, status: 'disponible' },
            { id: 2, name: 'Tente Patrouille Panthères', capacity: 8, status: 'abimee' },
            { id: 3, name: 'Tente Maîtrise', capacity: 3, status: 'disponible' }
        ]
        selectedTents.value = [1]
        return
    }
    await chargerTentes()
    if (selectedCamp.value) {
        try {
            const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/tents`, {
                headers: { 'Authorization': `Bearer ${userToken.value}` }
            })
            const data = await response.json()
            if (data.status === 'success') {
                selectedTents.value = data.selected.map(Number)
            }
        } catch (error) {
            console.error("Erreur lors du chargement de la sélection :", error)
        }
    }
}

const fermerGestionTentes = () => {
    showTentsModal.value = false
    unsubscribeFromMaterials()
}

const showAttendanceModal = ref(false)

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


// Sauvegarder dans la DB
const sauvegarderPresence = async () => {
    if (isDemoMode.value) { showAttendanceModal.value = false; return }
    if (!selectedCamp.value) return
    try {
        const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/attendance`, {
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
    // === INTERCEPTION MODE DÉMO ===
    if (isDemoMode.value) {
        setTimeout(() => {
            shoppingList.value = [
                { name: 'Pâtes', displayQty: 2, displayUnit: 'kg' }, 
                { name: 'Sauce Tomate', displayQty: 3, displayUnit: 'bocaux' },
                { name: 'Gruyère râpé', displayQty: 500, displayUnit: 'g' }
            ]
            isGeneratingList.value = false
        }, 600)
        return
    }
    // =============================
    // 2. On appelle Flask avec ces bons paramètres
    try {
        const url = `${API_BASE_URL}/camps/${selectedCamp.value.id}/shopping-list?jeunes=${nbJeunesPresents}&adultes=${nbAdultesPresents}`
        
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
onMounted(() => {
    fetchAdherents() 
})

const exporterDossierWeekEnd = async () => {
    // On ferme le menu déroulant
    showCampMenu.value = false 
    
    if (!selectedCamp.value) return
    
    isExporting.value = true
    
    try {
        // Appel à l'API pour générer le PDF complet du week-end
        const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/export-dossier`, {
            method: 'GET',
            headers: { 
                'Authorization': `Bearer ${userToken.value}` 
            }
        })

        if (!response.ok) {
            throw new Error("Erreur lors de la génération du dossier")
        }

        // Récupération du fichier sous forme de Blob
        const blob = await response.blob()
        
        // Création d'un lien temporaire pour forcer le téléchargement
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        
        // Nommage dynamique du fichier
        const nomFichier = selectedCamp.value.name ? selectedCamp.value.name.replace(/\s+/g, '_') : 'weekend'
        a.download = `Dossier_${nomFichier}.pdf`
        
        document.body.appendChild(a)
        a.click()
        
        // Nettoyage
        window.URL.revokeObjectURL(url)
        a.remove()
        
    } catch (error) {
        console.error("Erreur lors de l'export du dossier :", error)
        // Ici tu peux ajouter une notification d'erreur pour l'utilisateur
    } finally {
        isExporting.value = false
    }
}

const ouvrirGestionPresence = async () => {
    // === INTERCEPTION MODE DÉMO ===
    if (isDemoMode.value) {
        showAttendanceModal.value = true
        selectedAdherents.value = ['demo-chef-loic', 'demo-jeune-1']
        return
    }
    // =============================
    
    showAttendanceModal.value = true
    
    if (selectedCamp.value) {
        try {
            // 1. On récupère le "Roster" (la liste de l'unité du camp)
            const rosterResponse = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/roster`, {
                headers: { 'Authorization': `Bearer ${userToken.value}` }
            })
            const rosterData = await rosterResponse.json()
            
            if (rosterData.status === 'success') {
                // On trie les résultats dans nos nouvelles variables
                campJeunes.value = rosterData.data.filter(m => m.is_jeune)
                campChefs.value = rosterData.data.filter(m => m.is_chef)
            }

            // 2. On récupère ceux qui sont déjà cochés présents
            const presenceResponse = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/attendance`, {
                headers: { 'Authorization': `Bearer ${userToken.value}` }
            })
            const presenceData = await presenceResponse.json()
            
            if (presenceData.status === 'success') {
                selectedAdherents.value = presenceData.present.map(String)
            }
        } catch (error) {
            console.error("Erreur lors du chargement des présences :", error)
        }
    }
}

</script>
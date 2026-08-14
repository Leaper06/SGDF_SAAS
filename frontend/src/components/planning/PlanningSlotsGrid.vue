<template>
  <div class="max-w-5xl mx-auto w-full pt-2">
    <!-- Barre d'Onglets de Jours Sticky & Selector Mode de Vue -->
    <div class="sticky top-0 z-20 bg-gray-50/95 dark:bg-gray-900/95 backdrop-blur-md px-4 py-3 border-b border-gray-200/80 dark:border-gray-800 flex items-center justify-between gap-3 mb-4">
      <!-- Filtre par Jour -->
      <div class="flex items-center gap-1.5 overflow-x-auto scrollbar-hide py-1">
        <button 
          @click="selectedDayFilter = 'Tous'" 
          :class="['px-3.5 py-1.5 text-xs font-bold rounded-xl transition-all whitespace-nowrap border', selectedDayFilter === 'Tous' ? 'bg-[#5b2b82] text-white border-[#5b2b82] shadow-sm' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:bg-gray-100']"
        >
          Tous les jours
        </button>
        <button 
          v-for="jour in Object.keys(slotsParJour)" 
          :key="jour"
          @click="selectedDayFilter = jour"
          :class="['px-3.5 py-1.5 text-xs font-bold rounded-xl transition-all whitespace-nowrap border capitalize', selectedDayFilter === jour ? 'bg-[#5b2b82] text-white border-[#5b2b82] shadow-sm' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:bg-gray-100']"
        >
          {{ jour.split(' ')[0] }} {{ jour.split(' ')[1] || '' }}
        </button>
      </div>

      <!-- Toggle Vue Grille / Vue Frise Timeline -->
      <div class="flex items-center bg-gray-200 dark:bg-gray-800 p-1 rounded-xl shrink-0 border border-gray-300 dark:border-gray-700">
        <button 
          @click="viewMode = 'grid'" 
          :class="['p-1.5 rounded-lg transition-colors', viewMode === 'grid' ? 'bg-white dark:bg-gray-700 text-[#5b2b82] dark:text-purple-300 shadow-xs' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400']"
          title="Vue Cartes"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
        </button>
        <button 
          @click="viewMode = 'timeline'" 
          :class="['p-1.5 rounded-lg transition-colors', viewMode === 'timeline' ? 'bg-white dark:bg-gray-700 text-[#5b2b82] dark:text-purple-300 shadow-xs' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400']"
          title="Vue Frise Chronologique"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Message de planning vide -->
    <div v-if="Object.keys(slotsParJour).length === 0" class="flex flex-col items-center justify-center p-8 mt-10 text-center">
      <div class="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-300 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <p class="text-sm text-gray-400 dark:text-gray-500 font-medium transition-colors">Aucune activité prévue pour ce week-end.</p>
      <p class="text-xs text-gray-300 dark:text-gray-600 mt-1 transition-colors">Utilise le bouton + pour commencer le planning.</p>
    </div>
    
    <!-- CONTENU DU PLANNING PAR JOUR -->
    <template v-for="(slots, jour) in displayedSlotsParJour" :key="jour">
      <!-- En-tête de Jour de l'accordéon -->
      <div class="bg-gray-100 dark:bg-gray-800 px-4 py-2.5 flex justify-between items-center border-y border-gray-200 dark:border-gray-700 transition-colors">
        <div @click="onToggleJour(jour)" class="flex items-center gap-2 cursor-pointer flex-1">
          <h3 class="text-xs font-bold text-scoutBlue dark:text-blue-400 uppercase tracking-wider transition-colors flex items-center gap-2">
            <span>{{ jour }}</span>
            <span class="text-[10px] text-gray-400 font-normal lowercase">({{ slots.length }} créneau{{ slots.length > 1 ? 'x' : '' }})</span>
          </h3>
          <svg :class="{'rotate-180': joursOuverts[jour] !== false}" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 dark:text-gray-500 transition-transform duration-300" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </div>

        <!-- Bouton Décaler le planning de 15m -->
        <button 
          @click.stop="decalerPlanning(jour, 15)"
          class="px-2.5 py-1 text-[11px] font-bold text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-900/30 border border-amber-200 dark:border-amber-800 rounded-lg hover:bg-amber-100 dark:hover:bg-amber-800/50 transition-colors flex items-center gap-1 shrink-0"
          title="Décaler la suite de la journée de +15 min"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>+15 min</span>
        </button>
      </div>
      
      <!-- MODE VUE CARTES GRID -->
      <div v-if="viewMode === 'grid'" v-show="joursOuverts[jour] !== false" class="p-4 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <div v-for="slot in slots" :key="slot.id" :class="['bg-white dark:bg-gray-800 rounded-[1.25rem] shadow-sm border-l-4 p-4 flex flex-col justify-between gap-3 transition-colors hover:shadow-md', getTheme(slot.slot_type).border]">
          <div class="flex gap-4">
            <div class="min-w-[3rem] text-center pt-0.5">
              <span :class="['block text-sm font-bold', getTheme(slot.slot_type).textTime]">{{ formatHeure(slot.start_time) }}</span>
              <span class="block text-xs font-medium text-gray-400 dark:text-gray-500 mt-1 transition-colors">{{ formatHeure(slot.end_time) }}</span>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-start">
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white text-[15px] pr-2 transition-colors">{{ slot.title }}</h4>
                  
                  <!-- Badge Chef Responsable -->
                  <div v-if="slot.responsible_name" class="flex items-center gap-1.5 mt-2 text-[11px] font-semibold text-purple-700 dark:text-purple-300 bg-purple-50 dark:bg-purple-900/30 border border-purple-100 dark:border-purple-800/40 px-2.5 py-0.5 rounded-md w-fit">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span>Resp: {{ slot.responsible_name }}</span>
                  </div>
                </div>

                <div class="flex flex-col items-end gap-2 shrink-0">
                  <span :class="['text-[9px] font-bold px-2 py-1.5 rounded-md uppercase tracking-wider', getTheme(slot.slot_type).bgBadge]">
                    {{ formatTypeLabel(slot.slot_type) }}
                  </span>
                  <div class="flex items-center gap-1.5 mt-1">
                    <button @click.stop="onModifierSlot(slot)" class="p-1.5 text-gray-300 dark:text-gray-500 hover:text-scoutBlue dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-gray-700 rounded-lg transition-all" title="Modifier">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                    </button>
                    <button @click.stop="onSupprimerSlot(slot.id)" class="p-1.5 text-gray-300 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-gray-700 rounded-lg transition-all" title="Supprimer">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-auto pt-2">
            <button v-if="slot.slot_type === 'jeu'" @click.stop="onOuvrirFicheActivite(slot)" class="w-full flex justify-center items-center gap-2 px-4 py-2 text-sm font-semibold text-[#e85d22] dark:text-orange-400 border border-[#e85d22]/30 dark:border-orange-500/30 rounded-xl bg-white dark:bg-gray-800 hover:bg-orange-50 dark:hover:bg-orange-900/20 active:scale-95 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              Ouvrir la fiche
            </button>
            <button v-if="slot.slot_type === 'repas'" @click.stop="onOuvrirMenuRepas(slot)" class="w-full flex justify-center items-center gap-2 px-4 py-2 text-sm font-semibold text-scoutBlue dark:text-blue-400 border border-scoutBlue/30 dark:border-blue-500/30 rounded-xl bg-white dark:bg-gray-800 hover:bg-blue-50 dark:hover:bg-blue-900/20 active:scale-95 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
              Ouvrir le menu
            </button>
          </div>
        </div>
      </div>

      <!-- MODE VUE CHRONOLOGIQUE TIMELINE (Design Premium) -->
      <div v-else-if="viewMode === 'timeline'" v-show="joursOuverts[jour] !== false" class="p-4 sm:p-6 space-y-6">
        <div class="relative pl-6 sm:pl-8 space-y-6 before:absolute before:left-3 sm:before:left-4 before:top-2 before:bottom-2 before:w-0.5 before:bg-gradient-to-b before:from-[#5b2b82] before:via-purple-400 before:to-indigo-500 dark:before:from-purple-500 dark:before:via-purple-700 dark:before:to-indigo-800">
          <div v-for="slot in slots" :key="slot.id" class="relative group">
            <!-- Puce / Node de la Timeline avec Effet de Halo -->
            <div class="absolute -left-[1.85rem] sm:-left-[2.1rem] top-3.5 w-4 h-4 rounded-full bg-[#5b2b82] dark:bg-purple-500 ring-4 ring-purple-100 dark:ring-purple-900/50 flex items-center justify-center shadow-md">
              <div class="w-1.5 h-1.5 rounded-full bg-white"></div>
            </div>

            <!-- Carte du Créneau Timeline avec Glassmorphism & Bordure Thématique -->
            <div :class="['bg-white dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl p-4 sm:p-5 border-l-4 shadow-xs hover:shadow-md transition-all border border-gray-100 dark:border-gray-700/60 flex flex-col sm:flex-row sm:items-center justify-between gap-4', getTheme(slot.slot_type).border]">
              <!-- Informations Principales : Heures, Titre & Chef Responsable -->
              <div class="space-y-1.5 flex-1 min-w-0">
                <div class="flex flex-wrap items-center gap-2">
                  <!-- Tag Heures Pill -->
                  <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700/70 text-gray-700 dark:text-gray-300 text-xs font-bold border border-gray-200/60 dark:border-gray-600/50">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>{{ formatHeure(slot.start_time) }} - {{ formatHeure(slot.end_time) }}</span>
                  </div>

                  <!-- Badge Type de créneau -->
                  <span :class="['text-[9px] font-bold px-2 py-0.5 rounded-md uppercase tracking-wider', getTheme(slot.slot_type).bgBadge]">
                    {{ formatTypeLabel(slot.slot_type) }}
                  </span>
                </div>

                <!-- Titre Activité -->
                <h4 class="text-base font-extrabold text-gray-900 dark:text-white tracking-tight leading-snug">{{ slot.title }}</h4>

                <!-- Badge Chef Responsable -->
                <div v-if="slot.responsible_name" class="flex items-center gap-1.5 text-xs font-semibold text-purple-700 dark:text-purple-300 bg-purple-50 dark:bg-purple-900/30 border border-purple-100 dark:border-purple-800/40 px-2.5 py-1 rounded-lg w-fit">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-purple-600 dark:text-purple-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span>Chef responsable : <strong class="font-bold">{{ slot.responsible_name }}</strong></span>
                </div>
              </div>

              <!-- Boutons d'Action Repas / Jeu / Édition -->
              <div class="flex items-center gap-2 shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-gray-100 dark:border-gray-700/50 justify-end">
                <button v-if="slot.slot_type === 'jeu'" @click.stop="onOuvrirFicheActivite(slot)" class="px-3 py-1.5 text-xs font-bold text-[#e85d22] dark:text-orange-400 bg-orange-50 dark:bg-orange-900/30 border border-orange-200 dark:border-orange-800 rounded-xl hover:bg-orange-100 transition-colors flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                  <span>Fiche</span>
                </button>
                <button v-if="slot.slot_type === 'repas'" @click.stop="onOuvrirMenuRepas(slot)" class="px-3 py-1.5 text-xs font-bold text-scoutBlue dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-xl hover:bg-blue-100 transition-colors flex items-center gap-1">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>
                  <span>Menu</span>
                </button>

                <button @click.stop="onModifierSlot(slot)" class="p-2 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-gray-700 rounded-lg transition-colors" title="Modifier">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
                <button @click.stop="onSupprimerSlot(slot.id)" class="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-gray-700 rounded-lg transition-colors" title="Supprimer">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Cartouche d'actions bas : Effectifs, Tentes, Courses -->
    <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-5 flex flex-col gap-3 mb-6 mx-4 md:mx-0 transition-colors mt-6">
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
        <button @click="onAction('ouvrirPresence')" class="w-full text-sm font-semibold py-3 rounded-xl transition-all active:scale-95 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200">
          Présence au week-end
        </button>

        <button @click="onAction('ouvrirTentes')" class="w-full text-sm font-semibold py-3 rounded-xl transition-all active:scale-95 bg-amber-50 dark:bg-amber-900/30 hover:bg-amber-100 dark:hover:bg-amber-800/40 text-amber-700 dark:text-amber-400 flex items-center justify-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          Tentes & Matériel
        </button>
        
        <button @click="onAction('ouvrirCourses')" class="w-full text-sm font-semibold py-3 rounded-xl transition-all active:scale-95 bg-blue-50 dark:bg-blue-900/30 hover:bg-blue-100 dark:hover:bg-blue-800/40 text-blue-700 dark:text-blue-400 flex items-center justify-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          Courses globales
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { getTheme, formatHeure, formatTypeLabel } from '../../utils/helpers.js'
import { triggerHaptic } from '../../utils/haptics.js'
import { selectedDayFilter, viewMode, decalerPlanning } from '../../stores/planningStore.js'

const props = defineProps({
  slotsParJour: { type: Object, default: () => ({}) },
  joursOuverts: { type: Object, default: () => ({}) }
})

const emit = defineEmits([
  'toggleJour', 'modifierSlot', 'supprimerSlot', 'ouvrirFicheActivite',
  'ouvrirMenuRepas', 'ouvrirPresence', 'ouvrirTentes', 'ouvrirCourses'
])

const displayedSlotsParJour = computed(() => {
  if (selectedDayFilter.value === 'Tous') return props.slotsParJour
  const result = {}
  if (props.slotsParJour[selectedDayFilter.value]) {
    result[selectedDayFilter.value] = props.slotsParJour[selectedDayFilter.value]
  }
  return result
})

// --- ÉVÉNEMENTS AVEC RETOUR HAPTIQUE ---
const onToggleJour = (jour) => {
  triggerHaptic('light')
  emit('toggleJour', jour)
}

const onModifierSlot = (slot) => {
  triggerHaptic('light')
  emit('modifierSlot', slot)
}

const onSupprimerSlot = (id) => {
  triggerHaptic('medium')
  emit('supprimerSlot', id)
}

const onOuvrirFicheActivite = (slot) => {
  triggerHaptic('light')
  emit('ouvrirFicheActivite', slot)
}

const onOuvrirMenuRepas = (slot) => {
  triggerHaptic('light')
  emit('ouvrirMenuRepas', slot)
}

const onAction = (eventName) => {
  triggerHaptic('light')
  emit(eventName)
}
</script>

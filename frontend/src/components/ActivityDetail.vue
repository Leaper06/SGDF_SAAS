<template>
  <!-- DOCUMENT D'IMPRESSION DÉDIÉ (PDF MULTI-PAGES HAUTE DÉFINITION CLAIR, ÉLÉGANT ET STRUCTURE) -->
  <div class="print-only printable-activity-sheet w-full bg-white text-gray-900 font-sans">
    
    <!-- EN-TÊTE SCOUT DESIGN -->
    <div style="border-bottom: 2px solid #003B5C; padding-bottom: 12px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end;">
      <div>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
          <span style="background-color: #e85d22; color: white; padding: 2px 8px; border-radius: 9999px; font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: 0.5px;">
            {{ formatTypeLabel(selectedSlot?.slot_type) }}
          </span>
          <span style="font-size: 11px; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px;">FICHE D'ACTIVITÉ</span>
        </div>
        <h1 style="font-size: 22px; font-weight: 900; color: #003B5C; margin: 0; line-height: 1.2;">{{ selectedSlot?.title || 'Fiche d\'activité' }}</h1>
      </div>

      <div style="text-align: right;">
        <div v-if="selectedSlot?.start_time" style="background-color: #f3e8ff; border: 1px solid #d8b4fe; color: #581c87; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 800; display: inline-block;">
          {{ formatHeure(selectedSlot?.start_time) }} <span v-if="calculerHeureFinEstimee()">➔ {{ calculerHeureFinEstimee() }}</span>
          <span v-if="calculerDureeTotaleMinutes() > 0" style="color: #ea580c; margin-left: 4px;">({{ Math.floor(calculerDureeTotaleMinutes() / 60) > 0 ? Math.floor(calculerDureeTotaleMinutes() / 60) + 'h' : '' }}{{ calculerDureeTotaleMinutes() % 60 > 0 ? (calculerDureeTotaleMinutes() % 60 + 'm') : '' }})</span>
        </div>
        <div style="font-size: 10px; font-weight: 700; color: #6b7280; margin-top: 4px;">Scouts et Guides de France</div>
      </div>
    </div>

    <!-- BANNIÈRE DES CHEFS -->
    <div style="background-color: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; padding: 10px 14px; margin-bottom: 16px; font-size: 11px; display: flex; justify-content: space-between; align-items: center;" class="break-inside-avoid">
      <div v-if="selectedSlot?.responsible_name" style="color: #581c87; font-weight: 700;">
        Organisé par : <strong style="font-weight: 900;">{{ selectedSlot.responsible_name }}</strong>
      </div>
      <div v-if="selectedResponsiblesDetails.length > 0" style="color: #374151;">
        <span style="font-weight: 700; color: #9ca3af; text-transform: uppercase; font-size: 9px;">Chefs présents : </span>
        <span style="font-weight: 700;">{{ selectedResponsiblesDetails.map(c => c.prenom + ' ' + c.nom).join(', ') }}</span>
      </div>
      <div v-else style="color: #9ca3af; font-style: italic;">Aucun chef présent renseigné</div>
    </div>

    <!-- IMAGINAIRE & OBJECTIFS -->
    <div v-if="currentActivity?.imaginary_and_objectives" style="background-color: #faf5ff; border-left: 4px solid #581c87; border-top: 1px solid #f3e8ff; border-right: 1px solid #f3e8ff; border-bottom: 1px solid #f3e8ff; border-radius: 10px; padding: 12px 14px; margin-bottom: 16px;" class="break-inside-avoid">
      <div style="font-size: 11px; font-weight: 900; color: #581c87; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
        Imaginaire & Objectifs pédagogiques
      </div>
      <p style="font-size: 11px; color: #1f2937; margin: 0; line-height: 1.5; white-space: pre-wrap; font-weight: 500;">{{ currentActivity.imaginary_and_objectives }}</p>
    </div>

    <!-- TABLEAU DEUX COLONNES INFOS TERRAIN & MATÉRIEL -->
    <table style="width: 100%; border-collapse: separate; border-spacing: 12px 0; margin-left: -12px; margin-right: -12px; margin-bottom: 16px;" class="break-inside-avoid">
      <tr>
        <!-- Terrain & Plan B -->
        <td style="width: 50%; vertical-align: top; background-color: #ecfdf5; border-left: 4px solid #059669; border-top: 1px solid #d1fae5; border-right: 1px solid #d1fae5; border-bottom: 1px solid #d1fae5; border-radius: 10px; padding: 12px; font-size: 11px;">
          <div style="font-size: 10px; font-weight: 900; color: #065f46; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">
            Terrain & Plan B Pluie
          </div>
          <div v-if="locationInfo" style="margin-bottom: 4px;">
            <span style="color: #6b7280; font-weight: 600;">Emplacement : </span>
            <strong style="color: #111827;">{{ locationInfo }}</strong>
          </div>
          <div v-if="weatherPlanB">
            <span style="color: #6b7280; font-weight: 600;">Repli Pluie : </span>
            <strong style="color: #111827;">{{ weatherPlanB }}</strong>
          </div>
          <div v-if="!locationInfo && !weatherPlanB" style="color: #9ca3af; font-style: italic;">Aucun lieu spécifié</div>
        </td>

        <!-- Matériel -->
        <td style="width: 50%; vertical-align: top; background-color: #eff6ff; border-left: 4px solid #2563eb; border-top: 1px solid #dbeafe; border-right: 1px solid #dbeafe; border-bottom: 1px solid #dbeafe; border-radius: 10px; padding: 12px; font-size: 11px;">
          <div style="font-size: 10px; font-weight: 900; color: #1e40af; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">
            Matériel nécessaire
          </div>
          <div v-if="currentActivity?.materials && currentActivity.materials.length > 0" style="display: flex; flex-wrap: wrap; gap: 6px;">
            <span v-for="mat in currentActivity.materials" :key="mat.id" style="background-color: white; border: 1px solid #bfdbfe; border-radius: 6px; padding: 2px 8px; font-size: 10px; font-weight: 700; color: #1e3a8a; display: inline-flex; align-items: center; gap: 4px;">
              <span style="width: 8px; height: 8px; border: 1px solid #93c5fd; border-radius: 2px; display: inline-block;"></span>
              <span>{{ mat.item_name }}</span>
            </span>
          </div>
          <div v-else style="color: #9ca3af; font-style: italic;">Aucun matériel listé</div>
        </td>
      </tr>
    </table>

    <!-- TABLEAU DU DÉROULÉ CLAIR ET STRUCTURE -->
    <div style="margin-bottom: 16px;">
      <div style="border-bottom: 2px solid #e5e7eb; padding-bottom: 6px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 12px; font-weight: 900; color: #003B5C; text-transform: uppercase; letter-spacing: 0.5px;">
          Le Déroulé de l'Activité
        </span>
        <span style="font-size: 11px; font-weight: 700; color: #9ca3af;">{{ currentActivity?.steps?.length || 0 }} étapes</span>
      </div>

      <table style="width: 100%; border-collapse: separate; border-spacing: 0 8px;">
        <tr 
          v-for="(step, index) in currentActivity?.steps" 
          :key="step.id" 
          class="break-inside-avoid print-step-item"
        >
          <!-- Colonne Heure/Durée -->
          <td style="width: 100px; vertical-align: top; background-color: #f9fafb; border: 1px solid #e5e7eb; border-top-left-radius: 10px; border-bottom-left-radius: 10px; padding: 10px; text-align: center;">
            <div style="font-size: 13px; font-weight: 900; color: #003B5C; line-height: 1;">{{ calculerHeureEtape(index) }}</div>
            <div style="font-size: 9px; font-weight: 800; color: #ea580c; background-color: #fff7ed; border: 1px solid #ffedd5; border-radius: 4px; padding: 1px 4px; margin-top: 4px; display: inline-block;">
              {{ step.duration_minutes }} min
            </div>
          </td>

          <!-- Colonne Titre & Description -->
          <td style="vertical-align: top; background-color: #ffffff; border: 1px solid #e5e7eb; border-left: none; border-top-right-radius: 10px; border-bottom-right-radius: 10px; padding: 10px 14px;">
            <div style="font-size: 12px; font-weight: 800; color: #111827; margin-bottom: 2px;">{{ step.title }}</div>
            <div v-if="step.description" style="font-size: 11px; color: #4b5563; line-height: 1.4; white-space: pre-wrap;">{{ step.description }}</div>
          </td>
        </tr>
      </table>
    </div>

    <!-- PIED DE PAGE -->
    <div style="margin-top: 24px; padding-top: 8px; border-top: 1px solid #e5e7eb; display: flex; justify-content: space-between; font-size: 9px; color: #9ca3af; font-weight: 600;" class="break-inside-avoid">
      <span>PolyMaîtrise — SGDF SAAS</span>
      <span>Fiche imprimée le {{ new Date().toLocaleDateString('fr-FR') }}</span>
    </div>

  </div>

  <!-- INTERFACE ECRAN (Masquée lors de l'impression PDF) -->
  <div class="flex flex-col h-full bg-gray-50 dark:bg-gray-900 md:pb-0 transition-colors duration-300 print:hidden">
      
      <!-- EN-TÊTE -->
      <div class="bg-scoutBlue dark:bg-gray-800 text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center transition-colors shrink-0">
        <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
        <p class="text-sm font-light text-blue-100 dark:text-gray-300 mt-1">Fiche d'activité</p>
      </div>
      
      <!-- BARRE D'ACTIONS CENTRÉE -->
      <div class="bg-white dark:bg-gray-800 px-4 py-3 shadow-sm z-10 shrink-0 border-b border-transparent dark:border-gray-700 transition-colors print:hidden">
        <div class="max-w-5xl mx-auto w-full flex justify-between items-center">
          <button @click="fermerFicheActivite" class="flex items-center text-gray-500 dark:text-gray-400 hover:text-[#003B5C] dark:hover:text-blue-300 transition-colors font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            Planning
          </button>

          <div class="flex items-center gap-2">
            <span class="text-[10px] font-bold px-2.5 py-1 rounded-md uppercase tracking-wider bg-orange-100 dark:bg-orange-900/30 text-[#e85d22] dark:text-orange-400 transition-colors">
              {{ formatTypeLabel(selectedSlot?.slot_type) }}
            </span>
            <span v-if="calculerDureeTotaleMinutes() > 0" class="text-[10px] font-bold px-2.5 py-1 rounded-md uppercase tracking-wider bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 transition-colors flex items-center gap-1" title="Durée calculée à partir des étapes">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <span>{{ Math.floor(calculerDureeTotaleMinutes() / 60) > 0 ? Math.floor(calculerDureeTotaleMinutes() / 60) + 'h' : '' }}{{ calculerDureeTotaleMinutes() % 60 > 0 ? (calculerDureeTotaleMinutes() % 60 + 'm') : '' }}</span>
              <span v-if="calculerHeureFinEstimee()" class="text-gray-400">({{ formatHeure(selectedSlot?.start_time) }} ➔ {{ calculerHeureFinEstimee() }})</span>
            </span>
          </div>

          <div class="flex items-center gap-2">
            <button @click="imprimerFiche" class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 text-xs font-bold hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" /></svg>
              <span class="hidden sm:inline">Imprimer / PDF</span>
            </button>
            <button @click="sauvegarderFicheActivite" class="bg-[#432C7A] dark:bg-purple-600 hover:bg-purple-800 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all shadow-xs">
              Enregistrer
            </button>
          </div>
        </div>
      </div>

      <!-- CONTENU PRINCIPAL (Scrollable) -->
      <div class="flex-1 overflow-y-auto p-4 md:p-8 pb-28 md:pb-8 scrollbar-hide">
        
        <!-- WRAPPER GLOBAL POUR LIMITER LA LARGEUR SUR PC -->
        <div class="max-w-5xl mx-auto w-full">
          <!-- LIGNE DES ORGANISATEURS ET DES CHEFS PRÉSENTS -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 bg-gray-50/50 dark:bg-gray-800/40 p-4 rounded-2xl border border-gray-100 dark:border-gray-700/60 transition-colors print:border-gray-200">
            <!-- Chef(s) Organisateur(s) du jeu (définis au niveau du créneau planning) -->
            <div v-if="selectedSlot?.responsible_name" class="flex items-center gap-2 text-xs font-bold text-purple-700 dark:text-purple-300 bg-purple-50 dark:bg-purple-900/30 px-3 py-1.5 rounded-xl border border-purple-200 dark:border-purple-800/40 w-fit">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-purple-600 dark:text-purple-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span>Organisé par : <strong class="font-extrabold">{{ selectedSlot.responsible_name }}</strong></span>
            </div>

            <!-- Chefs Présents / Encadrants de l'activité (définis dans la fiche) -->
            <div class="flex flex-wrap items-center gap-2 text-sm text-gray-500 dark:text-gray-400 transition-colors">
              <span class="font-bold text-xs uppercase tracking-wider text-gray-400 dark:text-gray-500">Chefs présents :</span>
              
              <span v-if="selectedResponsiblesDetails.length === 0" class="text-xs italic text-gray-400 dark:text-gray-500">Aucun chef ajouté</span>
              
              <span 
                v-for="chef in selectedResponsiblesDetails" 
                :key="chef.id" 
                class="inline-flex items-center gap-1.5 bg-white dark:bg-gray-800 text-[#432C7A] dark:text-purple-300 px-3 py-1 rounded-full font-bold text-xs border border-purple-200 dark:border-purple-800/60 shadow-xs transition-colors"
              >
                <span>{{ chef.prenom }} {{ chef.nom }}</span>
                <button 
                  @click="retirerChefPresent(chef.id)" 
                  class="text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors p-0.5 rounded-full hover:bg-red-50 dark:hover:bg-red-900/30 print:hidden" 
                  title="Retirer ce chef des chefs présents"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </span>
              
              <button @click="ouvrirGestionResponsables" class="w-7 h-7 rounded-full bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 hover:bg-purple-100 dark:hover:bg-purple-900/60 border border-purple-200 dark:border-purple-700 flex items-center justify-center transition-all shadow-xs cursor-pointer print:hidden" title="Gérer les chefs présents">
                <span class="text-sm font-bold leading-none">+</span>
              </button>
            </div>
          </div>

          <!-- LA GRILLE MAGIQUE EN 2 COLONNES SUR PC -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

            <!-- COLONNE DE GAUCHE : LE DÉROULÉ (Prend 7 ou 8 colonnes sur 12) -->
            <div class="lg:col-span-7 xl:col-span-8">
              <div class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] dark:shadow-none border border-gray-100 dark:border-gray-700 transition-colors h-full">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
                  <div class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#e85d22] dark:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h3 class="font-bold text-[#001D2D] dark:text-white text-lg transition-colors">Le Déroulé</h3>
                  </div>

                  <!-- Trames types en 1 clic -->
                  <div class="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-hide print:hidden">
                    <span class="text-[10px] font-bold text-gray-400 uppercase tracking-wider shrink-0">Trames :</span>
                    <button @click="injecterTrameType('grand_jeu')" class="px-2 py-1 bg-orange-50 dark:bg-orange-900/30 text-[#e85d22] dark:text-orange-300 text-xs font-bold rounded-lg border border-orange-200 dark:border-orange-800 shrink-0 hover:bg-orange-100 transition-colors flex items-center gap-1" title="Injecter la trame type Grand Jeu">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9" /></svg>
                      <span>Grand Jeu</span>
                    </button>
                    <button @click="injecterTrameType('veillee')" class="px-2 py-1 bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs font-bold rounded-lg border border-purple-200 dark:border-purple-800 shrink-0 hover:bg-purple-100 transition-colors flex items-center gap-1" title="Injecter la trame type Veillée">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
                      <span>Veillée</span>
                    </button>
                    <button @click="injecterTrameType('olympiades')" class="px-2 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-bold rounded-lg border border-blue-200 dark:border-blue-800 shrink-0 hover:bg-blue-100 transition-colors flex items-center gap-1" title="Injecter la trame type Olympiades">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 3v4M3 5h4m6 0h.01M19 5h.01M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
                      <span>Olympiades</span>
                    </button>
                  </div>
                </div>
                
                <div class="relative pl-2.5">
                  <div class="absolute left-[15px] top-2 bottom-4 w-0.5 bg-[#e85d22]/30 dark:bg-orange-500/30"></div>

                  <div v-for="(step, index) in currentActivity.steps" :key="step.id" class="relative mb-6 pl-7 group">
                    <div class="absolute left-0 top-1.5 w-2.5 h-2.5 bg-[#e85d22] dark:bg-orange-500 rounded-full border-2 border-white dark:border-gray-800 box-content shadow-sm transition-colors"></div>
                    <div class="flex justify-between items-start gap-2">
                      <div class="flex-1">
                        <div class="flex items-baseline gap-2">
                          <span class="font-extrabold text-gray-900 dark:text-white text-[15px] transition-colors">{{ calculerHeureEtape(index) }}</span>
                          <span class="text-xs text-gray-400 dark:text-gray-500 font-semibold tracking-wide transition-colors">({{ step.duration_minutes }} min)</span>
                        </div>
                        <h4 class="text-[15px] font-bold text-[#003B5C] dark:text-blue-300 mt-1 transition-colors">{{ step.title }}</h4>
                        <p v-if="step.description" class="text-sm text-gray-500 dark:text-gray-400 mt-1 leading-snug transition-colors">{{ step.description }}</p>
                      </div>
                      <div class="flex gap-1 pt-1 opacity-100 print:hidden">
                        <button @click="modifierEtape(index)" class="p-1.5 text-gray-400 dark:text-gray-500 hover:text-[#e85d22] dark:hover:text-orange-400 hover:bg-orange-50 dark:hover:bg-orange-900/30 rounded-lg transition-colors" title="Modifier">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                        </button>
                        <button @click="supprimerEtape(index)" class="p-1.5 text-gray-400 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors" title="Supprimer">
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Formulaire d'ajout d'étape -->
                  <div v-if="isAddingStep" class="relative pl-7 mt-4 print:hidden">
                    <div class="absolute left-0 top-1.5 w-2.5 h-2.5 bg-gray-300 dark:bg-gray-600 rounded-full border-2 border-white dark:border-gray-800 box-content transition-colors"></div>
                    <div class="bg-orange-50/50 dark:bg-orange-900/10 rounded-xl p-4 border border-orange-100 dark:border-orange-800/30 transition-colors">
                      <input v-model="newStep.title" type="text" placeholder="Titre de l'étape (ex: Lancement)" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm font-bold text-[#003B5C] dark:text-blue-300 mb-3 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 transition-colors">
                      <textarea v-model="newStep.description" placeholder="Description courte (optionnelle)" rows="2" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-700 dark:text-gray-300 mb-3 focus:outline-none focus:ring-2 focus:ring-[#e85d22]/50 transition-colors"></textarea>
                      <div class="flex items-center gap-3 mb-4">
                        <label class="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Durée :</label>
                        <div class="flex items-center bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden focus-within:ring-2 focus-within:ring-[#e85d22]/50 transition-colors">
                          <input v-model="newStep.duration_minutes" type="number" min="1" class="w-16 px-2 py-1.5 text-sm font-bold text-center bg-transparent text-gray-900 dark:text-white focus:outline-none">
                          <span class="text-xs text-gray-500 dark:text-gray-400 pr-3 font-medium bg-gray-50 dark:bg-gray-800 h-full flex items-center transition-colors">min</span>
                        </div>
                      </div>
                      <div class="flex gap-2">
                        <button @click="ajouterEtape" class="flex-1 bg-[#e85d22] dark:bg-orange-600 text-white text-sm font-bold py-2.5 rounded-lg hover:bg-orange-600 dark:hover:bg-orange-500 transition-colors shadow-sm">Valider</button>
                        <button @click="isAddingStep = false" class="flex-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-300 text-sm font-bold py-2.5 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">Annuler</button>
                      </div>
                    </div>
                  </div>

                  <div v-else class="relative pl-7 mt-2 print:hidden">
                    <div class="absolute left-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-white dark:bg-gray-800 border-2 border-gray-300 dark:border-gray-600 rounded-full box-content transition-colors"></div>
                    <button @click="ouvrirAjoutEtape" class="bg-orange-50 dark:bg-orange-900/20 text-[#e85d22] dark:text-orange-400 border border-orange-100 dark:border-orange-800/30 font-semibold text-sm px-4 py-2 rounded-xl hover:bg-orange-100 dark:hover:bg-orange-900/40 transition-colors flex items-center gap-1.5">
                      <span class="text-lg leading-none mb-0.5">+</span> Ajouter une étape
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- COLONNE DE DROITE : LIEU, PLAN B, IMAGINAIRE & MATÉRIEL -->
            <div class="lg:col-span-5 xl:col-span-4 space-y-6">
              
              <!-- Carte Lieu & Plan B Météo -->
              <div class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] dark:shadow-none border border-gray-100 dark:border-gray-700 space-y-4 transition-colors print:hidden">
                <div class="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-600 dark:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <h3 class="font-bold text-[#001D2D] dark:text-white text-lg transition-colors">Lieu & Plan B Météo</h3>
                </div>

                <div>
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Emplacement prévu</label>
                  <input v-model="locationInfo" type="text" placeholder="Ex: Grand Bois, Clairière Est" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 text-sm font-semibold text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500/40">
                </div>

                <div>
                  <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 00-9.78 2.096A4.001 4.001 0 003 15z" /></svg>
                    <span>Repli en cas de pluie (Plan B)</span>
                  </label>
                  <input v-model="weatherPlanB" type="text" placeholder="Ex: Sous la grande tente mess ou le préau" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 text-sm text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-emerald-500/40">
                </div>
              </div>

              <!-- Carte Imaginaire -->
              <div class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] dark:shadow-none border border-gray-100 dark:border-gray-700 relative group transition-colors print:hidden">
                <div class="flex justify-between items-center mb-3">
                  <div class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[#432C7A] dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                    <h3 class="font-bold text-[#001D2D] dark:text-white text-lg transition-colors">Imaginaire & Objectifs</h3>
                  </div>
                  <button v-if="!isEditingImaginaire" @click="isEditingImaginaire = true" class="text-[#432C7A] dark:text-purple-300 bg-purple-50 dark:bg-purple-900/30 p-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-all print:hidden">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                  </button>
                  <button v-else @click="isEditingImaginaire = false" class="text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/30 px-3 py-1 text-xs font-bold rounded-lg transition-colors print:hidden">OK</button>
                </div>
                <p v-if="!isEditingImaginaire" class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed whitespace-pre-wrap cursor-pointer transition-colors" @click="isEditingImaginaire = true">
                  {{ currentActivity.imaginary_and_objectives || "Aucun imaginaire renseigné" }}
                </p>
                <textarea v-else v-model="currentActivity.imaginary_and_objectives" rows="4" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl p-3 text-sm text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#432C7A]/50 dark:focus:ring-purple-500/50 transition-all print:hidden" placeholder="Rédigez l'imaginaire ici..." autofocus></textarea>
              </div>

              <!-- Carte Matériel -->
              <div class="bg-white dark:bg-gray-800 rounded-2xl p-5 shadow-[0_2px_10px_rgba(0,0,0,0.04)] dark:shadow-none border border-gray-100 dark:border-gray-700 transition-colors print:hidden">
                <div class="flex items-center justify-between mb-4">
                  <div class="flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-700 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                    </svg>
                    <h3 class="font-bold text-[#001D2D] dark:text-white text-lg transition-colors">Matériel</h3>
                  </div>
                  <button v-if="currentActivity.materials && currentActivity.materials.length > 0" @click="exporterVersLogistique" class="text-xs font-bold text-scoutBlue dark:text-blue-400 hover:underline flex items-center gap-1 print:hidden" title="Envoyer le matériel manquant à la logistique">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>
                    <span>Logistique</span>
                  </button>
                </div>

                <div class="space-y-3 mb-4">
                  <div v-for="mat in currentActivity.materials" :key="mat.id" class="flex items-center gap-3 cursor-pointer group" @click="toggleMateriel(mat)">
                    <div :class="['w-5 h-5 rounded border flex justify-center items-center transition-colors', mat.is_checked ? 'bg-[#003B5C] dark:bg-blue-600 border-[#003B5C] dark:border-blue-600' : 'border-gray-300 dark:border-gray-600 group-hover:border-[#003B5C] dark:group-hover:border-blue-400']">
                      <svg v-if="mat.is_checked" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <span :class="['text-sm font-medium transition-all', mat.is_checked ? 'text-gray-400 dark:text-gray-600 line-through' : 'text-gray-700 dark:text-gray-300']">
                      {{ mat.item_name }}
                    </span>
                  </div>
                  <p v-if="currentActivity.materials.length === 0" class="text-xs text-gray-400 dark:text-gray-500 italic transition-colors">Aucun matériel listé pour le moment.</p>
                </div>

                <div class="flex gap-2">
                  <input v-model="newMaterialName" @keyup.enter="ajouterMateriel" type="text" placeholder="Ajouter un objet..." class="flex-1 bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-700 text-gray-700 dark:text-gray-200 text-sm font-medium rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-[#003B5C]/30 dark:focus:ring-blue-500/30 transition-all">
                  <button @click="ajouterMateriel" class="w-12 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300 font-bold text-xl rounded-xl transition-colors flex justify-center items-center">+</button>
                </div>
              </div>

            </div>
          </div> <!-- Fin de la grille 2 colonnes -->
        </div> <!-- Fin du Wrapper Max-width -->
      </div>
    </div>

    <!-- MODALE DES RESPONSABLES (Centrée sur PC) -->
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
      <div v-if="showResponsiblesModal" class="fixed inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
        <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm" @click="showResponsiblesModal = false"></div>
        
        <!-- Largeur max (md:max-w-lg) et bords arrondis (md:rounded-3xl) -->
        <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-lg h-[60vh] md:h-auto md:max-h-[85vh] rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col z-10 overflow-hidden transition-colors">
          <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/50 transition-colors">
            <div>
              <h3 class="font-extrabold text-lg text-[#001D2D] dark:text-white transition-colors">Responsables</h3>
              <p class="text-xs text-gray-500 dark:text-gray-400 font-medium transition-colors">Chefs présents au week-end</p>
            </div>
            <button @click="showResponsiblesModal = false" class="p-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full text-gray-600 dark:text-gray-300 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
            </button>
          </div>
          
          <div class="flex-1 overflow-y-auto p-6 space-y-2 bg-gray-50/30 dark:bg-gray-900/30 transition-colors">
            <div v-if="presentChefs.length === 0" class="text-center text-gray-500 dark:text-gray-400 text-sm mt-4 transition-colors">
              Aucun chef n'est marqué comme présent pour ce camp.
            </div>
            <div v-for="chef in presentChefs" :key="chef.id" @click="toggleResponsible(chef.id)" 
                 :class="['border rounded-2xl p-3 flex justify-between items-center cursor-pointer transition-all', activityResponsibles.includes(String(chef.id)) ? 'border-[#432C7A] dark:border-purple-500 bg-purple-50 dark:bg-purple-900/20' : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-purple-200 dark:hover:border-purple-800']">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden flex items-center justify-center shrink-0 transition-colors">
                  <img v-if="chef.photo" :src="chef.photo" class="w-full h-full object-cover">
                  <span v-else class="text-xs font-bold text-gray-500 dark:text-gray-400">{{ chef.prenom.charAt(0) }}{{ chef.nom.charAt(0) }}</span>
                </div>
                <span class="font-bold text-gray-900 dark:text-white text-sm transition-colors">{{ chef.prenom }} {{ chef.nom }}</span>
              </div>
              <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center transition-colors', activityResponsibles.includes(String(chef.id)) ? 'bg-[#432C7A] dark:bg-purple-600 border-[#432C7A] dark:border-purple-600 text-white' : 'border-gray-300 dark:border-gray-600']">
                <svg v-if="activityResponsibles.includes(String(chef.id))" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
              </div>
            </div>
          </div>
          
          <div class="p-6 border-t border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] transition-colors">
            <button @click="sauvegarderResponsables" class="w-full bg-[#432C7A] dark:bg-purple-600 hover:bg-purple-900 dark:hover:bg-purple-700 text-white font-bold py-3.5 rounded-xl transition-all active:scale-95 shadow-md">
              Valider les responsables
            </button>
          </div>
        </div>
      </div>
    </transition>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { userToken, loginToSGDF, isLoggingIn, loginError } from '../stores/authStore.js'
import { fetchAdherents } from '../stores/adherentsStore.js'

import { 
  selectedSlot, slotsList, showEditSlotModal, slotToEditId, editSlot, joursOuverts, 
  showAddSlotModal, newSlot, currentActivity, isEditingImaginaire, newMaterialName, 
  isAddingStep, editingStepIndex, newStep, showResponsiblesModal, activityResponsibles, 
  presentChefs, showInviteModal, inviteAdherentId, slotsParJour, selectedResponsiblesDetails, 
  ouvrirPlanning, fetchSlots, exporterPlanning, ouvrirAjoutSlot, fermerSlotModal, soumettreSlot, 
  modifierSlot, fermerEditSlotModal, soumettreModificationSlot, supprimerSlot, ouvrirFicheActivite, 
  sauvegarderFicheActivite, fermerFicheActivite, ajouterMateriel, toggleMateriel, calculerHeureEtape, 
  ouvrirAjoutEtape, modifierEtape, supprimerEtape, ajouterEtape, injecterTrameType, calculerDureeTotaleMinutes,
  calculerHeureFinEstimee, ouvrirGestionResponsables, toggleResponsible, sauvegarderResponsables, 
  retirerChefPresent, chargerResponsablesActivite, ouvrirInviteModal, fermerInviteModal, soumettreInvitation
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

import { ajouterMaterielsPlusieursAuCamp } from '../stores/logistiqueStore.js'

const locationInfo = ref('Lieu-dit du Bois de la Campagne')
const weatherPlanB = ref('Repli sous le préau du grand mess')

const imprimerFiche = () => {
  isEditingImaginaire.value = false
  window.print()
}

const exporterVersLogistique = async () => {
  if (!currentActivity.value || !currentActivity.value.materials || currentActivity.value.materials.length === 0) {
    alert("Aucun matériel n'est saisi pour cette activité.")
    return
  }
  const campId = selectedCamp.value?.id
  if (!campId) {
    alert("Veuillez d'abord sélectionner un camp pour lui ajouter ce matériel.")
    return
  }

  const itemsToExport = currentActivity.value.materials.map(m => m.item_name).filter(Boolean)
  if (itemsToExport.length === 0) {
    alert("Aucun élément de matériel à exporter.")
    return
  }

  const addedCount = await ajouterMaterielsPlusieursAuCamp(campId, itemsToExport)
  if (addedCount > 0) {
    alert(`Succès ! ${addedCount} élément(s) de matériel (${itemsToExport.join(', ')}) ont été ajoutés à la liste Matériel globale du camp (Module Logistique) !`)
  } else {
    alert("Tous les éléments de matériel de cette activité sont déjà présents dans la Malle Matériel du camp.")
  }
}

onMounted(() => {
    fetchAdherents() 
})
</script>
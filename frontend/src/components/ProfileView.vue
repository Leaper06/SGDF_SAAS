<template>
  <!-- Remplacement de pb-36 par pb-36 md:pb-8 car la barre du bas n'est plus là sur PC -->
  <div class="flex-1 overflow-y-auto p-4 md:p-8 pb-36 md:pb-8 bg-gray-50 dark:bg-gray-900 h-full transition-colors duration-300 scrollbar-hide">
    
    <!-- CONTENEUR GLOBAL CENTRÉ SUR PC -->
    <div class="max-w-3xl mx-auto w-full space-y-8">
      
      <!-- SECTION : MON PROFIL -->
      <div>
        <h2 class="text-2xl font-black text-gray-900 dark:text-white mb-6 transition-colors">Mon Profil</h2>
        
        <div class="bg-white dark:bg-gray-800 p-5 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-4 transition-colors">
          <div class="w-14 h-14 bg-blue-100 dark:bg-[#004267]/40 text-[#004267] dark:text-blue-300 rounded-full flex items-center justify-center font-black text-2xl shrink-0 uppercase transition-colors">
            {{ initialeAvatar }}
          </div>
          
          <div class="flex-1 min-w-0">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white truncate transition-colors">{{ chefFullName }}</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400 font-medium transition-colors">N° Adhérent : {{ chefAdherentId || 'Non renseigné' }}</p>
            
            <div class="flex gap-2 mt-3 flex-wrap">
              <span v-if="groupName" class="text-[10px] bg-[#004267]/10 dark:bg-[#004267]/40 text-[#004267] dark:text-blue-200 px-2 py-1 rounded-md font-black uppercase tracking-wider transition-colors">
                {{ groupName }}
              </span>
              <span v-if="chefBranch" class="text-[10px] bg-cyan-100 dark:bg-cyan-900/40 text-cyan-800 dark:text-cyan-300 px-2 py-1 rounded-md font-black uppercase tracking-wider transition-colors">
                {{ chefBranch }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION : APPARENCE -->
      <div>
          <h4 class="text-[11px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3 pl-2 transition-colors">Apparence</h4>
          <div class="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center justify-between transition-colors">
              <div class="flex items-center gap-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
                  <span class="font-bold text-gray-800 dark:text-gray-100 text-sm transition-colors">Mode Sombre</span>
              </div>
              
              <button 
                  @click="toggleDarkMode" 
                  :class="isDarkMode ? 'bg-[#004267] dark:bg-blue-500' : 'bg-gray-200 dark:bg-gray-600'" 
                  class="w-12 h-6 rounded-full relative transition-colors duration-300 focus:outline-none"
              >
                  <span 
                      :class="isDarkMode ? 'translate-x-6' : 'translate-x-1'" 
                      class="w-4 h-4 bg-white rounded-full absolute top-1 left-0 transition-transform duration-300 shadow-sm"
                  ></span>
              </button>
          </div>
      </div>

      <!-- SECTION : APPLICATION (NOUVEAU BLOC DISCRET) -->
      <div>
          <h4 class="text-[11px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3 pl-2 transition-colors">Application</h4>
          <router-link 
              to="/mentions-legales" 
              class="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center justify-between hover:border-gray-200 dark:hover:border-gray-700 transition-all group"
          >
              <div class="flex items-center gap-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-[#004267] dark:group-hover:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  <span class="font-bold text-gray-800 dark:text-gray-100 text-sm transition-colors">Mentions Légales & RGPD</span>
              </div>
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-gray-400 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
              </svg>
          </router-link>
      </div>

      <!-- SECTION : LIENS UTILES -->
      <div>
          <div class="flex items-center justify-between mb-3 pl-2 pr-1">
              <h4 class="text-[11px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest transition-colors">Liens Utiles</h4>
              <button @click="ouvrirModaleLien" class="text-[#004267] dark:text-blue-400 text-[11px] font-bold uppercase tracking-wider flex items-center gap-1 hover:opacity-70 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
                  Ajouter
              </button>
          </div>

          <!-- LA NOUVELLE GRILLE POUR LES LIENS FAVORIS -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <a 
                  v-for="(lien, index) in liensFavoris" 
                  :key="index" 
                  :href="lien.url" 
                  target="_blank" 
                  class="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 flex items-center justify-between hover:border-blue-200 dark:hover:border-gray-600 transition-all group"
              >
                  <div class="flex items-center gap-3 truncate pr-4">
                      <div class="bg-blue-50 dark:bg-gray-700 p-2 rounded-lg text-blue-500 dark:text-blue-400 transition-colors">
                          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                      </div>
                      <span class="font-bold text-gray-800 dark:text-gray-200 text-sm truncate transition-colors">{{ lien.nom }}</span>
                  </div>
                  <button @click.prevent="supprimerLien(index)" class="text-gray-300 dark:text-gray-500 hover:text-red-500 dark:hover:text-red-400 p-1 transition-colors shrink-0">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1-1h3M4 7h16" /></svg>
                  </button>
              </a>
          </div>

          <div v-if="liensFavoris.length === 0" class="text-sm text-gray-500 dark:text-gray-400 italic p-6 text-center bg-gray-200/40 dark:bg-gray-800/50 rounded-2xl border border-dashed border-gray-300 dark:border-gray-700 transition-colors">
              Aucun lien enregistré.<br>Ajoutez l'intranet, vos grilles d'évaluation ou vos dossiers partagés.
          </div>
      </div>

      <!-- BOUTON SE DÉCONNECTER (Contraint dans la largeur du wrapper) -->
      <div class="pt-4">
          <button @click="logout" class="w-full bg-red-50 dark:bg-red-500/10 hover:bg-red-100 dark:hover:bg-red-500/20 text-red-600 dark:text-red-400 font-bold py-4 rounded-2xl transition-colors flex justify-center items-center gap-2 border border-red-100 dark:border-red-500/20 shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
              Se déconnecter
          </button>
      </div>

    </div>
  </div>

  <!-- MODALE NOUVEAU FAVORI (Adaptée PC au centre de l'écran) -->
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
      <div v-if="showLinkModal" class="fixed inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
          <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="fermerModaleLien"></div>
          
          <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-sm rounded-t-3xl md:rounded-3xl p-6 shadow-2xl z-10 transition-colors">
              
              <div class="flex items-center justify-between mb-6">
                  <h3 class="text-xl font-black text-[#004267] dark:text-white transition-colors">Nouveau favori</h3>
                  <button @click="fermerModaleLien" class="p-2 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-300 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
              </div>

              <form @submit.prevent="validerLien" class="space-y-4">
                  <div>
                      <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-2 pl-1 transition-colors">Nom du lien</label>
                      <div class="relative">
                          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                          </div>
                          <input 
                              v-model="linkForm.nom" 
                              type="text" 
                              required
                              placeholder="Dossier Sanitaire, Intranet..." 
                              class="w-full pl-11 pr-4 py-3.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-[#004267]/20 dark:focus:ring-blue-500/30 focus:border-[#004267] dark:focus:border-blue-500 transition-all text-sm font-medium text-gray-900 dark:text-white"
                          >
                      </div>
                  </div>

                  <div>
                      <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-2 pl-1 transition-colors">Adresse Web (URL)</label>
                      <div class="relative">
                          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                          </div>
                          <input 
                              v-model="linkForm.url" 
                              type="url" 
                              required
                              placeholder="sgdf.fr" 
                              class="w-full pl-11 pr-4 py-3.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl focus:bg-white dark:focus:bg-gray-800 focus:ring-2 focus:ring-[#004267]/20 dark:focus:ring-blue-500/30 focus:border-[#004267] dark:focus:border-blue-500 transition-all text-sm font-medium text-gray-900 dark:text-white"
                          >
                      </div>
                  </div>

                  <div class="pt-4 flex gap-3">
                      <button 
                          type="button" 
                          @click="fermerModaleLien" 
                          class="flex-1 px-4 py-3.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 font-bold rounded-xl hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                      >
                          Annuler
                      </button>
                      <button 
                          type="submit" 
                          class="flex-1 px-4 py-3.5 bg-[#004267] dark:bg-blue-600 text-white font-bold rounded-xl shadow-lg hover:bg-[#003B5C] dark:hover:bg-blue-700 transition-colors flex justify-center items-center gap-2"
                      >
                          Enregistrer
                          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
                      </button>
                  </div>
              </form>
          </div>
      </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { userEmail, chefAdherentId, groupName, chefBranch, logout } from '../stores/authStore.js'
import { adherentsList } from '../stores/adherentsStore.js'
import { isDarkMode, toggleDarkMode } from '../stores/themeStore.js'

const monProfil = computed(() => {
    if (!adherentsList.value || !chefAdherentId.value) return null
    return adherentsList.value.find(adherent => adherent.id === chefAdherentId.value)
})

const chefFullName = computed(() => {
    if (monProfil.value && monProfil.value.prenom && monProfil.value.nom) {
        return `${monProfil.value.prenom} ${monProfil.value.nom}`
    }
    return userEmail.value
})

const initialeAvatar = computed(() => {
    if (monProfil.value && monProfil.value.prenom) {
        return monProfil.value.prenom.charAt(0)
    }
    return userEmail.value ? userEmail.value.charAt(0) : 'C'
})


// --- GESTION DES FAVORIS ---
const liensFavoris = ref([])

// Variables pour la modale
const showLinkModal = ref(false)
const linkForm = ref({ nom: '', url: '' })

onMounted(() => {
    const savedLinks = localStorage.getItem('sgdf_liens_favoris')
    if (savedLinks) {
        liensFavoris.value = JSON.parse(savedLinks)
    }
})

const sauvegarderFavoris = () => {
    localStorage.setItem('sgdf_liens_favoris', JSON.stringify(liensFavoris.value))
}

const ouvrirModaleLien = () => {
    linkForm.value = { nom: '', url: '' }
    showLinkModal.value = true
}

const fermerModaleLien = () => {
    showLinkModal.value = false
}

const validerLien = () => {
    if (!linkForm.value.nom) return alert("Le nom est obligatoire")
    if (!linkForm.value.url) return alert("L'URL est obligatoire")

    let finalUrl = linkForm.value.url
    
    if (!finalUrl.startsWith('http://') && !finalUrl.startsWith('https://')) {
        finalUrl = 'https://' + finalUrl
    }

    liensFavoris.value.push({ 
        nom: linkForm.value.nom, 
        url: finalUrl 
    })
    
    sauvegarderFavoris()
    fermerModaleLien()
}

const supprimerLien = (index) => {
    if (confirm("Retirer ce lien de vos favoris ?")) {
        liensFavoris.value.splice(index, 1)
        sauvegarderFavoris()
    }
}
</script>
<template>
    <div class="flex flex-col h-full bg-gray-50 dark:bg-gray-900 pb-20 relative transition-colors duration-300">
        
        <!-- HEADER UNITÉ -->
        <div class="bg-[#004267] dark:bg-gray-800 text-white pt-5 pb-6 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative shrink-0 transition-colors">
            <div class="flex justify-between items-center mb-1">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
                <button @click="logout" class="text-xs bg-white/20 hover:bg-white/30 px-3 py-1.5 rounded-md transition-colors font-medium flex items-center gap-1.5">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                    Déconnexion
                </button>
            </div>
            <p class="text-center text-blue-100 dark:text-gray-300 text-sm font-medium mt-1 transition-colors">Registre de l'Unité</p>
        </div>

        <!-- BANDEAU PREMIÈRE CONNEXION (IDENTIFICATION) -->
        <div v-if="needsIdentification" class="bg-orange-50 dark:bg-orange-900/20 border-b border-orange-200 dark:border-orange-900/50 p-5 z-20 transition-colors">
            <h2 class="text-[#e85d22] dark:text-orange-400 font-black text-lg mb-2 transition-colors">Bienvenue À toi ! </h2>
            <p class="text-sm text-orange-800 dark:text-orange-300 font-medium mb-4 transition-colors">
                C'est ta première connexion. Pour que l'application fonctionne parfaitement, clique sur ton profil dans la liste des chefs ci-dessous :
            </p>
            
            <div class="grid grid-cols-1 gap-2">
                <button 
                    v-for="chef in chefs" 
                    :key="chef.id"
                    @click="confirmerIdentite(chef)"
                    class="bg-white dark:bg-gray-800 border border-orange-200 dark:border-orange-900/50 p-3 rounded-xl shadow-sm flex items-center justify-between hover:bg-orange-100 dark:hover:bg-orange-900/40 transition-colors"
                >
                    <span class="font-bold text-gray-800 dark:text-white transition-colors">{{ chef.prenom }} {{ chef.nom }}</span>
                    <span class="text-xs font-bold text-orange-500 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/40 px-2 py-1 rounded transition-colors">C'est moi !</span>
                </button>
            </div>
        </div>

        <!-- SPINNER CHARGEMENT -->
        <div v-if="isLoadingAdherents" class="flex-1 flex flex-col items-center justify-center space-y-4">
            <svg class="animate-spin h-8 w-8 text-[#004267] dark:text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            <p class="text-sm font-bold text-gray-500 dark:text-gray-400 animate-pulse transition-colors">Récupération depuis l'intranet...</p>
        </div>

        <!-- LISTES DES ADHÉRENTS -->
        <div v-else class="flex-1 overflow-y-auto p-4 pb-28 space-y-6">
            
            <!-- SECTION JEUNES -->
            <div>
                <h3 :class="[branchStyles.text, 'flex items-center gap-2 text-xs font-bold uppercase tracking-wider mb-3 ml-1 transition-colors']">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                    {{ unitName }} ({{ jeunes.length }})
                </h3>
                <div class="grid grid-cols-1 gap-3">
                    <div v-for="membre in jeunes" :key="membre.id" @click="ouvrirFiche(membre)" :class="['bg-white dark:bg-gray-800 rounded-2xl p-3 shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-4 cursor-pointer transition-colors', branchStyles.borderHover]">                        
                        <div class="w-12 h-12 rounded-full overflow-hidden bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center shrink-0 border-2 border-white dark:border-gray-800 shadow-sm transition-colors">
                            <img v-if="membre.photo" :src="membre.photo" class="w-full h-full object-cover">
                            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-[50%] w-[50%] opacity-50 text-gray-400 dark:text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <div class="flex-1 min-w-0">
                            <h4 class="font-bold text-gray-900 dark:text-white truncate text-[15px] transition-colors">{{ membre.prenom }} {{ membre.nom }}</h4>
                            <div class="flex items-center gap-2 mt-1">
                                <span v-if="membre.hasFiche" class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 transition-colors">Fiche Sanitaire</span>
                                <span v-else class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-red-50 dark:bg-red-900/30 text-red-500 dark:text-red-400 transition-colors">Fiche Manquante</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SECTION MAÎTRISE (CHEFS) -->
            <div class="pt-4">
                <h3 class="flex items-center gap-2 text-xs font-bold text-[#5b2b82] dark:text-purple-400 uppercase tracking-wider mb-3 ml-1 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 14l9-5-9-5-9 5 9 5z" /><path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /></svg>
                    La Maîtrise ({{ chefs.length }})
                </h3>
                <div class="grid grid-cols-1 gap-3">
                    <div v-for="membre in chefs" :key="membre.id" @click="ouvrirFiche(membre)" class="bg-white dark:bg-gray-800 rounded-2xl p-3 shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-4 cursor-pointer hover:border-violet-200 dark:hover:border-purple-500/50 transition-colors">
                        <div class="w-12 h-12 rounded-full overflow-hidden bg-violet-100 dark:bg-purple-900/30 flex items-center justify-center shrink-0 border-2 border-white dark:border-gray-800 shadow-sm transition-colors">
                            <img v-if="membre.photo" :src="membre.photo" class="w-full h-full object-cover">
                            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-[50%] w-[50%] opacity-50 text-gray-400 dark:text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <div class="flex-1 min-w-0">
                            <h4 class="font-bold text-gray-900 dark:text-white truncate text-[15px] transition-colors">{{ membre.prenom }} {{ membre.nom }}</h4>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <!-- ======================================= -->
        <!-- MODALE : FICHE D'UN MEMBRE              -->
        <!-- ======================================= -->
        <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-full">
            <div v-if="selectedMember" class="fixed inset-0 z-50 flex flex-col justify-end">
                <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="fermerFiche"></div>
                
                <div class="relative bg-white dark:bg-gray-800 w-full rounded-t-3xl shadow-2xl flex flex-col z-10 overflow-hidden pb-8 transition-colors">
                    
                    <!-- BANDEAU HAUT MODALE -->
                    <div :class="['h-24 w-full relative transition-colors', selectedMember.isJeune ? branchStyles.bg : 'bg-[#5b2b82] dark:bg-purple-900/60']">
                        <div class="absolute -bottom-10 left-6 w-24 h-24 rounded-full overflow-hidden bg-white dark:bg-gray-800 border-4 border-white dark:border-gray-800 shadow-lg flex items-center justify-center cursor-pointer transition-colors" @click="$refs.photoInput.click()">
                            <img v-if="selectedMember.photo" :src="selectedMember.photo" class="w-full h-full object-cover">
                            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-[50%] w-[50%] opacity-50 text-gray-400 dark:text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <button @click="fermerFiche" class="absolute top-4 right-4 bg-black/20 hover:bg-black/30 p-2 rounded-full text-white transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>

                    <div class="px-6 pt-14 space-y-6">
                        <!-- IDENTITÉ -->
                        <div>
                            <h2 class="text-2xl font-black text-gray-900 dark:text-white transition-colors">{{ selectedMember.prenom }} <span class="uppercase">{{ selectedMember.nom }}</span></h2>
                            <p class="text-sm font-bold text-gray-400 dark:text-gray-500 mt-0.5 transition-colors">N° {{ selectedMember.id }}</p>
                        </div>

                        <div class="space-y-3">
                            
                            <!-- DOCUMENTS -->
                            <div class="space-y-3">
                                <h3 class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider transition-colors">Documents</h3>
                                
                                <div class="bg-gray-50 dark:bg-gray-900/50 border border-gray-100 dark:border-gray-700 rounded-xl p-4 flex flex-col gap-4 transition-colors">
                                    <div class="flex items-center gap-3">
                                        <div :class="['w-10 h-10 rounded-full flex items-center justify-center shrink-0 transition-colors', selectedMember.ficheUrl ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/30 text-red-500 dark:text-red-400']">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                            </svg>
                                        </div>
                                        <div>
                                            <p class="text-sm font-bold text-gray-900 dark:text-white transition-colors">Fiche Sanitaire</p>
                                            <p :class="['text-xs font-semibold mt-0.5 transition-colors', selectedMember.ficheUrl ? 'text-green-600 dark:text-green-400' : 'text-red-500 dark:text-red-400']">
                                                {{ selectedMember.ficheUrl ? 'À jour et stockée' : 'Document manquant' }}
                                            </p>
                                        </div>
                                    </div>
                                    
                                    <div class="flex gap-2">
                                        <button v-if="selectedMember.ficheUrl" @click="consulterFiche" class="flex-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 text-xs font-bold py-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors shadow-sm">
                                            Consulter
                                        </button>
                                        <button @click="$refs.ficheInput.click()" :class="['flex-1 text-xs font-bold py-2.5 rounded-lg transition-colors shadow-sm', selectedMember.ficheUrl ? 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700' : 'bg-[#004267] dark:bg-blue-600 text-white hover:bg-blue-900 dark:hover:bg-blue-700']">
                                            {{ selectedMember.ficheUrl ? 'Remplacer' : 'Importer (PDF / IMG)' }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                                
                            <input type="file" accept="image/png, image/jpeg, application/pdf" ref="ficheInput" @change="handleFicheUpload" class="hidden">
                            
                            <!-- PROGRESSION PERSONNELLE (UNIQUEMENT POUR LES JEUNES) -->
                            <div v-if="selectedMember.isJeune" class="space-y-3 pt-3">
                                <div class="flex justify-between items-center">
                                    <h3 class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider transition-colors">Progression Personnelle</h3>
                                    <button @click="sauvegarderProgression" :class="['text-xs font-bold px-3 py-1.5 rounded-lg transition-colors shadow-sm', branchStyles.btn]">
                                        {{ isSavingProgression ? 'Enregistrement...' : 'Enregistrer' }}
                                    </button>
                                </div>
                                
                                <div :class="['border rounded-xl p-4 space-y-3 transition-colors', branchStyles.lightBg, branchStyles.lightBorder]">
                                    <div>
                                        <label :class="['block text-[10px] font-bold uppercase tracking-wider mb-1 transition-colors', branchStyles.text]">Étape / Insigne (Atout, Cap...)</label>
                                        <input 
                                            v-model="selectedMember.progressionSymbole" 
                                            type="text" 
                                            placeholder="Ex: Atout de la Rencontre" 
                                            :class="['w-full bg-white dark:bg-gray-900 border text-gray-900 dark:text-white font-medium rounded-lg px-3 py-2 text-sm focus:outline-none transition-colors placeholder-gray-400 dark:placeholder-gray-600', branchStyles.lightBorder, branchStyles.focusBorder]"
                                        >
                                    </div>
                                    <div>
                                        <label :class="['block text-[10px] font-bold uppercase tracking-wider mb-1 transition-colors', branchStyles.text]">Défi / Action à réaliser</label>
                                        <textarea 
                                            v-model="selectedMember.progressionAction" 
                                            rows="2" 
                                            placeholder="Ex: Organiser un grand jeu..." 
                                            :class="['w-full bg-white dark:bg-gray-900 border text-gray-900 dark:text-white font-medium rounded-lg px-3 py-2 text-sm focus:outline-none transition-colors resize-none placeholder-gray-400 dark:placeholder-gray-600', branchStyles.lightBorder, branchStyles.focusBorder]"
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <input type="file" accept="image/*" ref="photoInput" @change="handlePhotoUpload" class="hidden">
                </div>
            </div>
        </transition>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { adherentsList, isLoadingAdherents, jeunes, chefs, fetchAdherents } from '../stores/adherentsStore.js'
import { 
    userToken, loginToSGDF, isLoggingIn, loginError, userEmail, 
    needsIdentification, chefAdherentId, unitName, groupName, chefBranch, logout 
} from '../stores/authStore.js'
import { API_BASE_URL } from '../api/config.js'

const selectedMember = ref(null)
const photoInput = ref(null)

const getInitials = (nom, prenom) => {
    return (prenom?.charAt(0) || '') + (nom?.charAt(0) || '')
}

const ouvrirFiche = (membre) => { selectedMember.value = membre }
const fermerFiche = () => { selectedMember.value = null }

// On lance le chargement à l'ouverture de la page
onMounted(() => {
    fetchAdherents()
})

// Définition des couleurs thématiques avec le support du MODE SOMBRE !
const branchStyles = computed(() => {
  if (chefBranch.value === 'Louja') {
    return {
      bg: 'bg-[#e85d22] dark:bg-orange-600', 
      text: 'text-[#e85d22] dark:text-orange-400', 
      borderHover: 'hover:border-orange-200 dark:hover:border-orange-500/50',
      lightBg: 'bg-orange-50/50 dark:bg-orange-900/10', 
      lightBorder: 'border-orange-100 dark:border-orange-900/30',
      focusBorder: 'focus:border-[#e85d22] dark:focus:border-orange-500', 
      btn: 'text-[#e85d22] dark:text-orange-300 bg-orange-50 dark:bg-orange-900/30 hover:bg-orange-100 dark:hover:bg-orange-900/50'
    }
  }
  if (chefBranch.value === 'Piok') {
    return {
      bg: 'bg-[#da291c] dark:bg-red-600', 
      text: 'text-[#da291c] dark:text-red-400', 
      borderHover: 'hover:border-red-200 dark:hover:border-red-500/50',
      lightBg: 'bg-red-50/50 dark:bg-red-900/10', 
      lightBorder: 'border-red-100 dark:border-red-900/30',
      focusBorder: 'focus:border-[#da291c] dark:focus:border-red-500', 
      btn: 'text-[#da291c] dark:text-red-300 bg-red-50 dark:bg-red-900/30 hover:bg-red-100 dark:hover:bg-red-900/50'
    }
  }
  // Par défaut : Scout-Guide (Bleu)
  return {
    bg: 'bg-[#004267] dark:bg-blue-800', 
    text: 'text-[#004267] dark:text-blue-400', 
    borderHover: 'hover:border-blue-200 dark:hover:border-blue-500/50',
    lightBg: 'bg-blue-50/50 dark:bg-blue-900/10', 
    lightBorder: 'border-blue-100 dark:border-blue-900/30',
    focusBorder: 'focus:border-[#004267] dark:focus:border-blue-500', 
    btn: 'text-[#004267] dark:text-blue-300 bg-blue-50 dark:bg-blue-900/30 hover:bg-blue-100 dark:hover:bg-blue-900/50'
  }
})

// Fonction universelle pour envoyer un fichier (Photo ou PDF) au serveur
const uploadToServer = async (file, type) => {
    if (!selectedMember.value || !file) return
    
    // Pour envoyer un fichier physique via fetch, il faut utiliser FormData
    const formData = new FormData()
    formData.append('file', file)
    formData.append('type', type) // 'photo' ou 'fiche'

    try {
        const response = await fetch(`${API_BASE_URL}/adherents/${selectedMember.value.id}/upload`, {
            method: 'POST',
            body: formData
        })
        
        const json = await response.json()
        
        if (json.status === 'success') {
            // Le serveur nous renvoie l'URL finale, on met à jour l'interface
            if (type === 'photo') {
                selectedMember.value.photo = json.url
            } else if (type === 'fiche') {
                selectedMember.value.ficheUrl = json.url
                selectedMember.value.hasFiche = true
            }
        } else {
            alert("Erreur lors de l'envoi : " + json.message)
        }
    } catch (error) {
        console.error("Erreur d'upload :", error)
        alert("Impossible d'envoyer le document.")
    }
}

const handlePhotoUpload = (event) => {
    const file = event.target.files[0]
    uploadToServer(file, 'photo')
}

const handleFicheUpload = (event) => {
    const file = event.target.files[0]
    uploadToServer(file, 'fiche')
}

const consulterFiche = () => {
    if (!selectedMember.value || !selectedMember.value.ficheUrl) return
    window.open(selectedMember.value.ficheUrl, '_blank')
}

const isSavingProgression = ref(false)

const sauvegarderProgression = async () => {
    if (!selectedMember.value) return
    
    isSavingProgression.value = true
    try {
        const payload = {
            progression_symbole: selectedMember.value.progressionSymbole,
            progression_action: selectedMember.value.progressionAction
        }

        const response = await fetch(`${API_BASE_URL}/adherents/${selectedMember.value.id}/progression`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
        
        const json = await response.json()
        
        if (json.status !== 'success') {
            alert("Erreur lors de la sauvegarde : " + json.message)
        }
    } catch (error) {
        console.error("Erreur de sauvegarde progression :", error)
        alert("Impossible de joindre le serveur.")
    } finally {
        setTimeout(() => { isSavingProgression.value = false }, 500)
    }
}

const confirmerIdentite = async (chefChoisi) => {
    try {
        const response = await fetch(`${API_BASE_URL}/chef/identify`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken.value}`
            },
            body: JSON.stringify({ adherent_id: chefChoisi.id })
        })
        
        const json = await response.json()
        if (json.status === 'success') {
            needsIdentification.value = false
            chefAdherentId.value = chefChoisi.id
            localStorage.setItem('sgdf_chef_id', chefChoisi.id)

            // Détection immédiate
            if (['214', '215'].includes(chefChoisi.code)) chefBranch.value = 'Louja'
            else if (['222', '223'].includes(chefChoisi.code)) chefBranch.value = 'Scout-Guide'
            else if (['224', '225'].includes(chefChoisi.code)) chefBranch.value = 'Piok'
            
            localStorage.setItem('sgdf_chef_branch', chefBranch.value)
            console.log(" Branche du chef connecté :", chefBranch.value)
        }
    } catch (error) {
        console.error("Erreur de liaison :", error)
    }
}
</script>
<template>
  <div class="flex-1 flex flex-col min-h-0 relative bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
    
    <!-- En-tête du Planning -->
    <PlanningHeader 
      :selectedCamp="selectedCamp"
      :showCampMenu="showCampMenu"
      @goBack="$router.push('/camps')"
      @toggleMenu="showCampMenu = !showCampMenu"
      @editCamp="modifierCamp(); showCampMenu = false"
      @inviteChef="ouvrirInviteModal"
      @exportPdf="exporterDossierWeekEnd"
      @createTemplate="creerModele"
      @deleteCamp="supprimerCamp(); showCampMenu = false"
    />
    
    <!-- Contenu Principal : Grille des Créneaux -->
    <main class="flex-1 overflow-y-auto pb-24 md:pb-8 scrollbar-hide">
      <PlanningSlotsGrid
        :slotsParJour="slotsParJour"
        :joursOuverts="joursOuverts"
        @toggleJour="(jour) => joursOuverts[jour] = joursOuverts[jour] === false ? true : false"
        @modifierSlot="modifierSlot"
        @supprimerSlot="supprimerSlot"
        @ouvrirFicheActivite="ouvrirFicheActivite"
        @ouvrirMenuRepas="ouvrirMenuRepas"
        @ouvrirPresence="ouvrirGestionPresence"
        @ouvrirTentes="ouvrirGestionTentes"
        @ouvrirCourses="genererBordereauGlobal"
      />
    </main>

    <!-- Bouton Flottant Ajouter Activité -->
    <button @click="ouvrirAjoutSlot" class="absolute bottom-24 md:bottom-8 right-6 w-14 h-14 bg-[#e85d22] text-white rounded-full shadow-lg shadow-orange-500/30 dark:shadow-orange-900/50 flex items-center justify-center hover:bg-orange-600 transition-transform active:scale-95 z-30">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
    </button>

    <!-- Modale Création / Édition de Créneau -->
    <SlotEditorModal
      :showAddModal="showAddSlotModal"
      :showEditModal="showEditSlotModal"
      :newSlot="newSlot"
      :editSlot="editSlot"
      :joursDuCamp="joursDuCamp"
      @closeAdd="fermerSlotModal"
      @closeEdit="fermerEditSlotModal"
      @submitAdd="soumettreSlot"
      @submitEdit="soumettreModificationSlot"
    />

    <!-- Modale Édition des infos du Camp -->
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

    <!-- Modale Inviter un Chef -->
    <InviteChefModal
      :showModal="showInviteModal"
      v-model:inviteAdherentId="inviteAdherentId"
      @close="fermerInviteModal"
      @submitInvite="soumettreInvitation"
    />

    <!-- Indicator Export PDF -->
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

    <!-- Modale Matériel & Logistique -->
    <CampMaterialsModal
      :showModal="showTentsModal"
      v-model:activeTab="activeLogistiqueTab"
      v-model:selectedMaterialTemplateId="selectedMaterialTemplateId"
      v-model:newMaterialItemName="newMaterialItemName"
      :campMaterials="campMaterials"
      :materialTemplates="materialTemplates"
      :allTents="allTents"
      :selectedTents="selectedTents"
      @close="fermerGestionTentes"
      @applyTemplate="appliquerTemplateMateriel(selectedCamp?.id, selectedMaterialTemplateId)"
      @saveTemplate="enregistrerNouveauTemplateMateriel"
      @addMaterial="ajouterMaterielCamp(selectedCamp?.id)"
      @deleteMaterial="(index) => supprimerMaterielCamp(index, selectedCamp?.id)"
      @toggleMaterial="(index) => toggleMaterielCamp(index, selectedCamp?.id)"
      @toggleTent="toggleTent"
      @reportIncident="ouvrirDeclarationIncident"
      @saveTents="sauvegarderTentes"
    />

    <!-- Modale Registre de Présence -->
    <PresenceRegisterModal
      :showModal="showAttendanceModal"
      :campJeunes="campJeunes"
      :campChefs="campChefs"
      :selectedAdherents="selectedAdherents"
      @close="showAttendanceModal = false"
      @togglePresence="togglePresence"
      @savePresence="sauvegarderPresence"
    />

    <!-- Modale Bordereau de Courses Global -->
    <GlobalShoppingModal
      :showModal="showShoppingModal"
      :groupedShoppingList="groupedShoppingList"
      :rabEnabled="rabEnabled"
      @close="fermerBordereau"
      @exportPdf="exporterBordereauPDF"
      @toggleRab="rabEnabled = !rabEnabled"
    />

    <!-- Modale Signaler Incident -->
    <IncidentModal
      :showModal="showIncidentModal"
      :incidentForm="incidentForm"
      @close="fermerDeclarationIncident"
      @submitIncident="soumettreIncident"
    />

  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'

// Importation des sous-composants réusinés
import PlanningHeader from './planning/PlanningHeader.vue'
import PlanningSlotsGrid from './planning/PlanningSlotsGrid.vue'
import SlotEditorModal from './planning/SlotEditorModal.vue'
import PresenceRegisterModal from './planning/PresenceRegisterModal.vue'
import GlobalShoppingModal from './planning/GlobalShoppingModal.vue'
import CampMaterialsModal from './planning/CampMaterialsModal.vue'
import InviteChefModal from './planning/InviteChefModal.vue'
import IncidentModal from './planning/IncidentModal.vue'

// Stores
import { 
  showIncidentModal, incidentForm, ouvrirDeclarationIncident, fermerDeclarationIncident, soumettreIncident,
  campMaterials, materialTemplates, newMaterialItemName, fetchCampMaterials,
  ajouterMaterielCamp, supprimerMaterielCamp, toggleMaterielCamp, fetchMaterialTemplates, appliquerTemplateMateriel, creerTemplateMateriel,
  subscribeToMaterials, unsubscribeFromMaterials
} from '../stores/logistiqueStore.js'

import { 
  shoppingList, showShoppingModal, rabEnabled, groupedShoppingList, 
  ouvrirMenuRepas, genererBordereauGlobal, fermerBordereau, exporterBordereauPDF 
} from '../stores/intendanceStore.js'

import { userToken, groupName, isDemoMode } from '../stores/authStore.js'
import { jeunes, chefs, fetchAdherents } from '../stores/adherentsStore.js'
import { 
  selectedCamp, showCampMenu, showEditCampModal, editCampForm, joursDuCamp,
  modifierCamp, fermerEditCampModal, soumettreModificationCamp, supprimerCamp, creerTemplateAPartirDeCamp 
} from '../stores/campsStore.js'

import { 
  showEditSlotModal, editSlot, joursOuverts, showAddSlotModal, newSlot, 
  showInviteModal, inviteAdherentId, slotsParJour,
  ouvrirAjoutSlot, fermerSlotModal, soumettreSlot, modifierSlot, fermerEditSlotModal, 
  soumettreModificationSlot, supprimerSlot, ouvrirFicheActivite, 
  ouvrirInviteModal, fermerInviteModal, soumettreInvitation
} from '../stores/planningStore.js'

const selectedAdherents = ref([])

import { API_BASE_URL } from '../api/config.js' 

const activeLogistiqueTab = ref('materiel')
const selectedMaterialTemplateId = ref('')

const enregistrerNouveauTemplateMateriel = () => {
  const nom = prompt("Nom du modèle de matériel (ex: Matériel WE classique) :")
  if (nom && nom.trim() !== '') {
    creerTemplateMateriel(nom.trim())
  }
}

const creerModele = () => {
  showCampMenu.value = false;
  const nom = prompt("Entrez le nom du nouveau modèle :");
  if (nom && nom.trim() !== "") {
    creerTemplateAPartirDeCamp(selectedCamp.value.id, nom.trim());
  }
}

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

const togglePresence = (adherentId) => {
  const id = String(adherentId)
  const index = selectedAdherents.value.indexOf(id)
  if (index === -1) {
    selectedAdherents.value.push(id)
  } else {
    selectedAdherents.value.splice(index, 1)
  }
}

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

onMounted(() => {
  fetchAdherents() 
})

const exporterDossierWeekEnd = async () => {
  showCampMenu.value = false 
  if (!selectedCamp.value) return
  isExporting.value = true
  
  try {
    const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/export-dossier`, {
      method: 'GET',
      headers: { 
        'Authorization': `Bearer ${userToken.value}` 
      }
    })

    if (!response.ok) {
      throw new Error("Erreur lors de la génération du dossier")
    }

    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const nomFichier = selectedCamp.value.name ? selectedCamp.value.name.replace(/\s+/g, '_') : 'weekend'
    a.download = `Dossier_${nomFichier}.pdf`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    a.remove()
  } catch (error) {
    console.error("Erreur lors de l'export du dossier :", error)
  } finally {
    isExporting.value = false
  }
}

const ouvrirGestionPresence = async () => {
  if (isDemoMode.value) {
    showAttendanceModal.value = true
    selectedAdherents.value = ['demo-chef-loic', 'demo-jeune-1']
    return
  }
  
  showAttendanceModal.value = true
  
  if (selectedCamp.value) {
    try {
      const rosterResponse = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/roster`, {
        headers: { 'Authorization': `Bearer ${userToken.value}` }
      })
      const rosterData = await rosterResponse.json()
      
      if (rosterData.status === 'success') {
        campJeunes.value = rosterData.data.filter(m => m.is_jeune)
        campChefs.value = rosterData.data.filter(m => m.is_chef)
      }

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
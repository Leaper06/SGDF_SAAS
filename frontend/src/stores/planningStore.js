import { ref, computed } from 'vue'
import router from '../router.js'
import { API_BASE_URL } from '../api/config.js'
import { selectedCamp, joursDuCamp } from './campsStore.js'
import { userToken } from './authStore.js'
import { chefs } from './adherentsStore.js'

// ==========================================
// ÉTAT GLOBAL (Variables)
// ==========================================
export const selectedSlot = ref(null)
export const slotsList = ref([])

// Formulaires et modales des créneaux
export const showEditSlotModal = ref(false)
export const slotToEditId = ref(null) 
export const editSlot = ref({ title: '', slot_type: 'logistique', selected_day: null, start_hour: '', end_hour: '' })
export const joursOuverts = ref({})
export const showAddSlotModal = ref(false)
export const newSlot = ref({ title: '', slot_type: 'logistique', selected_day: null, start_hour: '', end_hour: '' })

// Fiche d'activité (imaginaire, étapes, matériel)
export const currentActivity = ref({ id: null, imaginary_and_objectives: '', steps: [], materials: [] })
export const isEditingImaginaire = ref(false)
export const newMaterialName = ref('')
export const isAddingStep = ref(false)
export const editingStepIndex = ref(null)
export const newStep = ref({ title: '', description: '', duration_minutes: 15 })

// Responsables d'activité
export const showResponsiblesModal = ref(false)
export const activityResponsibles = ref([]) 
export const presentChefs = ref([]) 

// Invitation chef externe
export const showInviteModal = ref(false)
export const inviteAdherentId = ref('')

// ==========================================
// CALCULS (Computed)
// ==========================================
export const slotsParJour = computed(() => {
  const groupes = {}
  slotsList.value.forEach(slot => {
    const dateStr = new Date(slot.start_time).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })
    if (!groupes[dateStr]) groupes[dateStr] = []
    groupes[dateStr].push(slot)
  })
  return groupes
})

export const selectedResponsiblesDetails = computed(() => {
    return chefs.value.filter(c => activityResponsibles.value.includes(String(c.id)))
})

// ==========================================
// ACTIONS (Fonctions liées au Planning)
// ==========================================
export const ouvrirPlanning = async (camp) => {
  selectedCamp.value = camp
  router.push('/planning') 
  await fetchSlots(camp.id)
}

export const fetchSlots = async (campId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/camps/${campId}/slots`)
    const json = await response.json()
    if (json.status === 'success') slotsList.value = json.data
  } catch (error) { console.error("Erreur :", error) }
}

export const exporterPlanning = () => { alert("Bientôt : Export PDF") }

export const ouvrirAjoutSlot = () => {
  newSlot.value = { title: '', slot_type: 'logistique', selected_day: joursDuCamp.value[0], start_hour: '', end_hour: '' }
  showAddSlotModal.value = true
}

export const fermerSlotModal = () => showAddSlotModal.value = false

export const soumettreSlot = async () => {
  if (!newSlot.value.title || !newSlot.value.start_hour || !newSlot.value.end_hour) return alert("Remplir titre et horaires.");
  try {
    const baseDate = new Date(newSlot.value.selected_day)
    const [startH, startM] = newSlot.value.start_hour.split(':')
    const [endH, endM] = newSlot.value.end_hour.split(':')
    const startDateTime = new Date(baseDate); startDateTime.setHours(parseInt(startH), parseInt(startM), 0)
    const endDateTime = new Date(baseDate); endDateTime.setHours(parseInt(endH), parseInt(endM), 0)
    if (endDateTime < startDateTime) endDateTime.setDate(endDateTime.getDate() + 1)

    const payload = { camp_id: selectedCamp.value.id, title: newSlot.value.title, slot_type: newSlot.value.slot_type, start_time: startDateTime.toISOString(), end_time: endDateTime.toISOString() }
    const response = await fetch(`${API_BASE_URL}/planning_slots`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    const json = await response.json()
    if (json.status === 'success') { fermerSlotModal(); await fetchSlots(selectedCamp.value.id) }
  } catch (error) { console.error("Erreur :", error) }
}

export const modifierSlot = (slot) => {
  slotToEditId.value = slot.id
  const getHeureString = (isoString) => {
    if (!isoString) return '12:00'
    const d = new Date(isoString); if (isNaN(d.getTime())) return '12:00'
    return `${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
  }
  let matchingDay = joursDuCamp.value[0]
  if (slot.start_time) {
    const baseDate = new Date(slot.start_time)
    if (!isNaN(baseDate.getTime())) {
      baseDate.setHours(0, 0, 0, 0)
      const found = joursDuCamp.value.find(d => d.getTime() === baseDate.getTime())
      if (found) matchingDay = found
    }
  }
  editSlot.value = { title: slot.title || '', slot_type: slot.slot_type || 'logistique', selected_day: matchingDay, start_hour: getHeureString(slot.start_time), end_hour: getHeureString(slot.end_time) }
  showEditSlotModal.value = true
}

export const fermerEditSlotModal = () => showEditSlotModal.value = false

export const soumettreModificationSlot = async () => {
  if (!editSlot.value.title || !editSlot.value.start_hour || !editSlot.value.end_hour) return alert("Remplir le titre et horaires.")
  try {
    const baseDate = new Date(editSlot.value.selected_day)
    const [startH, startM] = editSlot.value.start_hour.split(':')
    const [endH, endM] = editSlot.value.end_hour.split(':')
    const startDateTime = new Date(baseDate); startDateTime.setHours(parseInt(startH), parseInt(startM), 0)
    const endDateTime = new Date(baseDate); endDateTime.setHours(parseInt(endH), parseInt(endM), 0)
    if (endDateTime < startDateTime) endDateTime.setDate(endDateTime.getDate() + 1)

    const payload = { title: editSlot.value.title, slot_type: editSlot.value.slot_type, start_time: startDateTime.toISOString(), end_time: endDateTime.toISOString() }
    const response = await fetch(`${API_BASE_URL}/planning_slots/${slotToEditId.value}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    const json = await response.json()
    if (json.status === 'success') { fermerEditSlotModal(); await fetchSlots(selectedCamp.value.id) }
  } catch (error) { console.error("Erreur :", error) }
}

export const supprimerSlot = async (slotId) => {
  if(confirm("Retirer cette activité du planning ?")) {
    try {
      const response = await fetch(`${API_BASE_URL}/planning_slots/${slotId}`, { method: 'DELETE' })
      const json = await response.json()
      if (json.status === 'success') await fetchSlots(selectedCamp.value.id)
    } catch (error) { console.error("Erreur :", error) }
  }
}

// ==========================================
// ACTIONS (Fiche d'Activité)
// ==========================================
export const ouvrirFicheActivite = async (slot) => {
  selectedSlot.value = slot; router.push('/activity')
  try {
    const response = await fetch(`${API_BASE_URL}/planning_slots/${slot.id}/activity`)
    const json = await response.json()
    if (json.status === 'success') {
      currentActivity.value = { id: json.data.activity.id, imaginary_and_objectives: json.data.activity.imaginary_and_objectives || '', steps: json.data.steps || [], materials: json.data.materials || [] }
    }
    await chargerResponsablesActivite()
  } catch (error) { console.error("Erreur :", error) }
}
export const sauvegarderFicheActivite = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/activities/${currentActivity.value.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(currentActivity.value) })
    const json = await response.json()
    if (json.status === 'success') fermerFicheActivite()
  } catch (error) { console.error("Erreur :", error) }
}
export const fermerFicheActivite = () => { selectedSlot.value = null; router.push('/planning') }
export const ajouterMateriel = () => {
  if (newMaterialName.value.trim() === '') return
  currentActivity.value.materials.push({ id: Date.now(), item_name: newMaterialName.value, is_checked: false })
  newMaterialName.value = ''
}
export const toggleMateriel = (materiel) => { materiel.is_checked = !materiel.is_checked }
export const calculerHeureEtape = (index) => {
  if (!selectedSlot.value || !selectedSlot.value.start_time) return '00:00'
  let dateEtape = new Date(selectedSlot.value.start_time)
  let minutesCumulees = 0
  for (let i = 0; i < index; i++) minutesCumulees += currentActivity.value.steps[i].duration_minutes || 0
  dateEtape.setMinutes(dateEtape.getMinutes() + minutesCumulees)
  return dateEtape.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}
export const ouvrirAjoutEtape = () => { editingStepIndex.value = null; newStep.value = { title: '', description: '', duration_minutes: 15 }; isAddingStep.value = true }
export const modifierEtape = (index) => { editingStepIndex.value = index; newStep.value = { ...currentActivity.value.steps[index] }; isAddingStep.value = true }
export const supprimerEtape = (index) => { if(confirm("Supprimer cette étape ?")) currentActivity.value.steps.splice(index, 1) }
export const ajouterEtape = () => {
  if (!newStep.value.title) return alert("Le titre est obligatoire.")
  if (editingStepIndex.value !== null) currentActivity.value.steps[editingStepIndex.value] = { ...newStep.value }
  else currentActivity.value.steps.push({ id: Date.now(), title: newStep.value.title, description: newStep.value.description, duration_minutes: newStep.value.duration_minutes })
  isAddingStep.value = false; editingStepIndex.value = null
}

// ==========================================
// ACTIONS (Responsables & Invités)
// ==========================================
export const ouvrirGestionResponsables = async () => {
    if (!currentActivity.value || !selectedCamp.value) return
    try {
        const attRes = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/attendance`, { headers: { 'Authorization': `Bearer ${userToken.value}` } })
        const attData = await attRes.json()
        if (attData.status === 'success' && attData.present.length > 0) {
            const presentIds = attData.present.map(String)
            presentChefs.value = chefs.value.filter(c => presentIds.includes(String(c.id)))
        } else presentChefs.value = chefs.value 
    } catch (e) { presentChefs.value = chefs.value }

    try {
        const res = await fetch(`${API_BASE_URL}/activities/${currentActivity.value.id}/responsibles`, { headers: { 'Authorization': `Bearer ${userToken.value}` } })
        const data = await res.json()
        if (data.status === 'success') activityResponsibles.value = data.data.map(String)
    } catch (e) { console.error(e) }
    showResponsiblesModal.value = true
}

export const toggleResponsible = (id) => {
    const strId = String(id)
    const index = activityResponsibles.value.indexOf(strId)
    if (index === -1) activityResponsibles.value.push(strId)
    else activityResponsibles.value.splice(index, 1)
}

export const sauvegarderResponsables = async () => {
    try {
        const res = await fetch(`${API_BASE_URL}/activities/${currentActivity.value.id}/responsibles`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${userToken.value}` },
            body: JSON.stringify({ adherent_ids: activityResponsibles.value })
        })
        const data = await res.json()
        if (data.status === 'success') showResponsiblesModal.value = false
    } catch (e) { console.error(e) }
}

export const chargerResponsablesActivite = async () => {
    if (!currentActivity.value) return
    try {
        const res = await fetch(`${API_BASE_URL}/activities/${currentActivity.value.id}/responsibles`, { headers: { 'Authorization': `Bearer ${userToken.value}` } })
        const data = await res.json()
        if (data.status === 'success') activityResponsibles.value = data.data.map(String)
    } catch (e) { console.error(e) }
}

export const ouvrirInviteModal = () => { inviteAdherentId.value = ''; showInviteModal.value = true }
export const fermerInviteModal = () => { showInviteModal.value = false }

export const soumettreInvitation = async () => {
  if (!inviteAdherentId.value || !selectedCamp.value) return alert("Veuillez saisir un numéro d'adhérent.")
  try {
    const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/guests`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${userToken.value}` },
      body: JSON.stringify({ adherent_id: inviteAdherentId.value.trim() })
    })
    const json = await response.json()
    if (json.status === 'success') { alert("Le chef a bien été ajouté au week-end !"); fermerInviteModal() } 
    else alert("Erreur : " + json.message)
  } catch (error) { alert("Impossible de joindre le serveur.") }
}
import { ref, computed } from 'vue'
import router from '../router.js'
import { API_BASE_URL } from '../api/config.js'
import { selectedCamp, joursDuCamp } from './campsStore.js'
import { userToken, isDemoMode } from './authStore.js'
import { chefs } from './adherentsStore.js'
import { supabase } from '../api/supabase.js'

// ==========================================
// ÉTAT GLOBAL (Variables)
// ==========================================
export const selectedSlot = ref(null)
export const slotsList = ref([])

// Formulaires et modales des créneaux
export const showEditSlotModal = ref(false)
export const slotToEditId = ref(null) 
export const editSlot = ref({ title: '', slot_type: 'service', selected_day: null, start_hour: '', end_hour: '', responsible_name: '' })
export const joursOuverts = ref({})
export const showAddSlotModal = ref(false)
export const newSlot = ref({ title: '', slot_type: 'service', selected_day: null, start_hour: '', end_hour: '', responsible_name: '' })
export const selectedDayFilter = ref('Tous')
export const viewMode = ref('grid') // 'grid' | 'timeline'

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
export const campChefsList = ref([]) 

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
    const list = campChefsList.value.length > 0 ? campChefsList.value : chefs.value
    return list.filter(c => activityResponsibles.value.includes(String(c.id)))
})

// ==========================================
// ACTIONS (Fonctions liées au Planning)
// ==========================================
export const ouvrirPlanning = async (camp) => {
  selectedCamp.value = camp
  router.push('/planning') 
  await fetchSlots(camp.id)
  await chargerChefsCamp(camp.id)
  subscribeToPlanning(camp.id)
}

// ==========================================
// ABONNEMENTS TEMPS RÉEL (Supabase)
// ==========================================
let planningSubscription = null
export const subscribeToPlanning = (campId) => {
  if (planningSubscription) supabase.removeChannel(planningSubscription)
  
  planningSubscription = supabase.channel('planning-channel')
    .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'planning_slots', filter: `camp_id=eq.${campId}` }, () => fetchSlots(campId))
    .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'planning_slots', filter: `camp_id=eq.${campId}` }, () => fetchSlots(campId))
    .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'planning_slots' }, () => fetchSlots(campId))
    .subscribe()
}

let activitySubscription = null
export const subscribeToActivity = (activityId) => {
  if (activitySubscription) supabase.removeChannel(activitySubscription)

  activitySubscription = supabase.channel('activity-channel')
    .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'activities', filter: `id=eq.${activityId}` }, () => reFetchActivity())
    .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'activities', filter: `id=eq.${activityId}` }, () => reFetchActivity())
    .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'activities' }, () => reFetchActivity())
    
    .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'activity_steps', filter: `activity_id=eq.${activityId}` }, () => reFetchActivity())
    .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'activity_steps', filter: `activity_id=eq.${activityId}` }, () => reFetchActivity())
    .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'activity_steps' }, () => reFetchActivity())
    
    .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'activity_materials', filter: `activity_id=eq.${activityId}` }, () => reFetchActivity())
    .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'activity_materials', filter: `activity_id=eq.${activityId}` }, () => reFetchActivity())
    .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'activity_materials' }, () => reFetchActivity())
    
    .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'activity_responsibles', filter: `activity_id=eq.${activityId}` }, () => chargerResponsablesActivite())
    .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'activity_responsibles', filter: `activity_id=eq.${activityId}` }, () => chargerResponsablesActivite())
    .on('postgres_changes', { event: 'DELETE', schema: 'public', table: 'activity_responsibles' }, () => chargerResponsablesActivite())
    .subscribe()
}

const reFetchActivity = async () => {
  if (!selectedSlot.value || !selectedSlot.value.id) return
  try {
    const response = await fetch(`${API_BASE_URL}/planning_slots/${selectedSlot.value.id}/activity`)
    const json = await response.json()
    if (json.status === 'success') {
      currentActivity.value = { 
        id: json.data.activity.id, 
        imaginary_and_objectives: json.data.activity.imaginary_and_objectives || '', 
        steps: json.data.steps || [], 
        materials: json.data.materials || [] 
      }
    }
  } catch (error) { console.error("Erreur de rafraîchissement temps réel :", error) }
}

export const fetchSlots = async (campId) => {
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    const d1 = new Date(selectedCamp.value?.start_date || new Date())
    const d2 = new Date(d1); d2.setDate(d2.getDate() + 1)
    
    const makeSlot = (dateObj, hStart, mStart, hEnd, mEnd, title, type) => {
      const s = new Date(dateObj); s.setHours(hStart, mStart, 0)
      const e = new Date(dateObj); e.setHours(hEnd, mEnd, 0)
      return { id: `demo-slot-${Date.now()}-${Math.random().toString(36).substring(2,6)}`, title, slot_type: type, start_time: s.toISOString(), end_time: e.toISOString() }
    }

    slotsList.value = [
      // Samedi
      makeSlot(d1, 14, 0, 14, 30, "Accueil & Rassemblement", "rassemblement"),
      makeSlot(d1, 14, 30, 16, 0, "Montage des tentes & Installation", "service"),
      makeSlot(d1, 16, 0, 16, 30, "Goûter & Lancement de l'Imaginaire", "service"),
      makeSlot(d1, 16, 30, 18, 30, "Grand Jeu de piste en forêt", "jeu"),
      makeSlot(d1, 18, 30, 19, 30, "Temps libre & Douches", "temps_libre"),
      makeSlot(d1, 19, 30, 21, 0, "Dîner Trappeur & Concours Cuisine", "repas"),
      makeSlot(d1, 21, 0, 22, 30, "Veillée autour du feu", "veillée"),
      makeSlot(d1, 22, 30, 23, 0, "Extinction des feux & Coucher", "nuit"),

      // Dimanche
      makeSlot(d2, 8, 0, 9, 0, "Petit-Déjeuner & Réveil", "repas"),
      makeSlot(d2, 9, 0, 9, 30, "Temps Spirituel & Réflexion", "temps_spirituel"),
      makeSlot(d2, 9, 30, 11, 30, "Olympiades de Patrouille", "jeu"),
      makeSlot(d2, 11, 30, 12, 0, "Rangement des affaires", "service"),
      makeSlot(d2, 12, 0, 13, 30, "Déjeuner & Pique-Nique", "repas"),
      makeSlot(d2, 13, 30, 15, 0, "Démontage du campement & Nettoyage", "service"),
      makeSlot(d2, 15, 0, 16, 0, "Rassemblement de clôture & Départ", "rassemblement")
    ]
    return
  }
  // =============================
  try {
    const response = await fetch(`${API_BASE_URL}/camps/${campId}/slots`)
    const json = await response.json()
    if (json.status === 'success') slotsList.value = json.data
  } catch (error) { console.error("Erreur :", error) }
}

export const exporterPlanning = () => { alert("Bientôt : Export PDF") }

export const ouvrirAjoutSlot = () => {
  newSlot.value = { title: '', slot_type: 'service', selected_day: joursDuCamp.value[0], start_hour: '', end_hour: '', responsible_name: '' }
  showAddSlotModal.value = true
}

export const fermerSlotModal = () => showAddSlotModal.value = false

export const soumettreSlot = async () => {
  if (!newSlot.value.title || !newSlot.value.start_hour || !newSlot.value.end_hour) return alert("Remplir titre et horaires.");
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    const baseDate = new Date(newSlot.value.selected_day)
    const [startH, startM] = newSlot.value.start_hour.split(':')
    const [endH, endM] = newSlot.value.end_hour.split(':')
    const startDateTime = new Date(baseDate); startDateTime.setHours(parseInt(startH), parseInt(startM), 0)
    const endDateTime = new Date(baseDate); endDateTime.setHours(parseInt(endH), parseInt(endM), 0)
    
    slotsList.value.push({
      id: 'demo-new-slot-' + Date.now(),
      title: newSlot.value.title,
      slot_type: newSlot.value.slot_type,
      start_time: startDateTime.toISOString(),
      end_time: endDateTime.toISOString(),
      responsible_name: newSlot.value.responsible_name || ''
    })
    fermerSlotModal()
    return
  }
  // =============================
  try {
    const baseDate = new Date(newSlot.value.selected_day)
    const [startH, startM] = newSlot.value.start_hour.split(':')
    const [endH, endM] = newSlot.value.end_hour.split(':')
    const startDateTime = new Date(baseDate); startDateTime.setHours(parseInt(startH), parseInt(startM), 0)
    const endDateTime = new Date(baseDate); endDateTime.setHours(parseInt(endH), parseInt(endM), 0)
    if (endDateTime < startDateTime) endDateTime.setDate(endDateTime.getDate() + 1)

    const payload = { 
      camp_id: selectedCamp.value.id, 
      title: newSlot.value.title, 
      slot_type: newSlot.value.slot_type, 
      start_time: startDateTime.toISOString(), 
      end_time: endDateTime.toISOString(),
      responsible_name: newSlot.value.responsible_name || ''
    }
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
  editSlot.value = { 
    title: slot.title || '', 
    slot_type: slot.slot_type || 'service', 
    selected_day: matchingDay, 
    start_hour: getHeureString(slot.start_time), 
    end_hour: getHeureString(slot.end_time),
    responsible_name: slot.responsible_name || ''
  }
  showEditSlotModal.value = true
}

export const fermerEditSlotModal = () => showEditSlotModal.value = false

export const soumettreModificationSlot = async () => {
  if (!editSlot.value.title || !editSlot.value.start_hour || !editSlot.value.end_hour) return alert("Remplir le titre et horaires.")
    // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    const index = slotsList.value.findIndex(s => s.id === slotToEditId.value)
    if (index !== -1) {
      const baseDate = new Date(editSlot.value.selected_day)
      const [startH, startM] = editSlot.value.start_hour.split(':')
      const [endH, endM] = editSlot.value.end_hour.split(':')
      const startDateTime = new Date(baseDate); startDateTime.setHours(parseInt(startH), parseInt(startM), 0)
      const endDateTime = new Date(baseDate); endDateTime.setHours(parseInt(endH), parseInt(endM), 0)
      
      slotsList.value[index].title = editSlot.value.title
      slotsList.value[index].slot_type = editSlot.value.slot_type
      slotsList.value[index].start_time = startDateTime.toISOString()
      slotsList.value[index].end_time = endDateTime.toISOString()
      slotsList.value[index].responsible_name = editSlot.value.responsible_name || ''
    }
    fermerEditSlotModal()
    return
  }
  // =============================
  try {
    const baseDate = new Date(editSlot.value.selected_day)
    const [startH, startM] = editSlot.value.start_hour.split(':')
    const [endH, endM] = editSlot.value.end_hour.split(':')
    const startDateTime = new Date(baseDate); startDateTime.setHours(parseInt(startH), parseInt(startM), 0)
    const endDateTime = new Date(baseDate); endDateTime.setHours(parseInt(endH), parseInt(endM), 0)
    if (endDateTime < startDateTime) endDateTime.setDate(endDateTime.getDate() + 1)

    const payload = { 
      title: editSlot.value.title, 
      slot_type: editSlot.value.slot_type, 
      start_time: startDateTime.toISOString(), 
      end_time: endDateTime.toISOString(),
      responsible_name: editSlot.value.responsible_name || ''
    }
    const response = await fetch(`${API_BASE_URL}/planning_slots/${slotToEditId.value}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    const json = await response.json()
    if (json.status === 'success') { fermerEditSlotModal(); await fetchSlots(selectedCamp.value.id) }
  } catch (error) { console.error("Erreur :", error) }
}

export const decalerPlanning = (jourStr, minutesDelta = 15) => {
  const targetSlots = slotsParJour.value[jourStr]
  if (!targetSlots || targetSlots.length === 0) return
  
  targetSlots.forEach(slot => {
    const s = new Date(slot.start_time)
    const e = new Date(slot.end_time)
    s.setMinutes(s.getMinutes() + minutesDelta)
    e.setMinutes(e.getMinutes() + minutesDelta)
    slot.start_time = s.toISOString()
    slot.end_time = e.toISOString()
    
    if (!isDemoMode.value) {
      fetch(`${API_BASE_URL}/planning_slots/${slot.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: slot.title,
          slot_type: slot.slot_type,
          start_time: slot.start_time,
          end_time: slot.end_time,
          responsible_name: slot.responsible_name || ''
        })
      }).catch(err => console.error("Erreur décalage API :", err))
    }
  })
}

export const supprimerSlot = async (slotId) => {
  if(confirm("Retirer cette activité du planning ?")) {
    // === INTERCEPTION MODE DÉMO ===
    if (isDemoMode.value) {
      slotsList.value = slotsList.value.filter(s => s.id !== slotId)
      return
    }
    // =============================
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
export const chargerChefsCamp = async (campId) => {
  if (!campId) return
  if (isDemoMode.value) {
    campChefsList.value = [
      { id: 'demo-chef-loic', nom: 'Test', prenom: 'Utilisateur', code: '222' },
      { id: 'demo-chef-2', nom: 'DUPONT', prenom: 'Robert', code: '222' }
    ]
    return
  }
  try {
    const rosterRes = await fetch(`${API_BASE_URL}/camps/${campId}/roster`, {
      headers: { 'Authorization': `Bearer ${userToken.value}` }
    })
    const rosterData = await rosterRes.json()
    if (rosterData.status === 'success' && rosterData.data) {
      campChefsList.value = rosterData.data
        .filter(m => m.is_chef)
        .map(m => ({
          id: String(m.adherent_id),
          nom: m.last_name || m.nom || '',
          prenom: m.first_name || m.prenom || '',
          code: m.code || '222',
          photo: m.photo || null
        }))
    }
  } catch (e) {
    console.error("Erreur lors du chargement des chefs du camp :", e)
  }
}

export const ouvrirFicheActivite = async (slot) => {
  selectedSlot.value = slot; router.push('/activity')
  try {
    const response = await fetch(`${API_BASE_URL}/planning_slots/${slot.id}/activity`)
    const json = await response.json()
    if (json.status === 'success') {
      currentActivity.value = { id: json.data.activity.id, imaginary_and_objectives: json.data.activity.imaginary_and_objectives || '', steps: json.data.steps || [], materials: json.data.materials || [] }
      subscribeToActivity(currentActivity.value.id)
    }
    if (selectedCamp.value && campChefsList.value.length === 0) {
      await chargerChefsCamp(selectedCamp.value.id)
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
export const fermerFicheActivite = () => { 
  if (activitySubscription) supabase.removeChannel(activitySubscription)
  selectedSlot.value = null; router.push('/planning') 
}
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

export const injecterTrameType = (type) => {
  if (!currentActivity.value) return
  if (currentActivity.value.steps && currentActivity.value.steps.length > 0) {
    if (!confirm("Injecter une trame type remplacera les étapes actuelles. Continuer ?")) return
  }
  
  if (type === 'grand_jeu') {
    currentActivity.value.imaginary_and_objectives = currentActivity.value.imaginary_and_objectives || "Grand Jeu d'Imaginaire Scout : Développer la cohésion d'équipe et l'esprit d'initiative à travers des épreuves variées."
    currentActivity.value.steps = [
      { id: Date.now() + 1, title: "Lancement Imaginaire & Saynète", description: "Mise en scène avec les chefs costumés pour plonger les jeunes dans l'univers du jeu.", duration_minutes: 15 },
      { id: Date.now() + 2, title: "Explication des Règles & Équipes", description: "Présentation des consignes de sécurité, de la carte du terrain et distribution des rôles.", duration_minutes: 15 },
      { id: Date.now() + 3, title: "Épreuves & Rotation sur les Postes", description: "Défis par patrouilles sur les différents ateliers du terrain (noeuds, pistage, agilité).", duration_minutes: 90 },
      { id: Date.now() + 4, title: "Épreuve Finale & Chasse au Trésor", description: "Rassemblement de tous les indices pour la confrontation finale entre équipes.", duration_minutes: 30 },
      { id: Date.now() + 5, title: "Débriefing, Rassemblement & Rangement", description: "Annonce de l'équipe gagnante, rangement du matériel et retour au calme.", duration_minutes: 15 }
    ]
  } else if (type === 'veillee') {
    currentActivity.value.imaginary_and_objectives = currentActivity.value.imaginary_and_objectives || "Veillée Scout autour du feu : Développer l'expression artistique, l'écoute et terminer la journée dans un climat chaleureux."
    currentActivity.value.steps = [
      { id: Date.now() + 1, title: "Chant d'ouverture & Accueil", description: "Lancement du feu de veillée et chant d'accroche pour rassembler l'unité.", duration_minutes: 10 },
      { id: Date.now() + 2, title: "Saynètes & Sketchs des Patrouilles", description: "Passage des petites scènes préparées par les équipes.", duration_minutes: 45 },
      { id: Date.now() + 3, title: "Grand jeu d'ambiance / Chansons", description: "Bans, chants scouts à répondre et jeux de veillée dynamiques.", duration_minutes: 20 },
      { id: Date.now() + 4, title: "Conte & Histoire de veillée", description: "Histoire calme racontée par les chefs pour amener le calme.", duration_minutes: 15 },
      { id: Date.now() + 5, title: "Prière / Réflexion & Coucher", description: "Chant de prière scout (Prière du Scout ou Cantique des Patrouilles) puis départ silencieux vers les tentes.", duration_minutes: 10 }
    ]
  } else if (type === 'olympiades') {
    currentActivity.value.imaginary_and_objectives = currentActivity.value.imaginary_and_objectives || "Olympiades d'Unité : Compétition sportive et technique amicale favorisant le dépassement de soi et l'entraide."
    currentActivity.value.steps = [
      { id: Date.now() + 1, title: "Rassemblement & Allumage de la Flamme", description: "Présentation des équipes, du cri de guerre et des arbitres.", duration_minutes: 10 },
      { id: Date.now() + 2, title: "Rotation sur les Ateliers Olympiques", description: "Parcours du combattant, souque à la corde, tir à l'arc, froissartage express.", duration_minutes: 75 },
      { id: Date.now() + 3, title: "Grande Finale d'Unité", description: "Ultime relais entre les capitaines de patrouille.", duration_minutes: 30 },
      { id: Date.now() + 4, title: "Podiums & Remise des Medailles", description: "Cérémonie de remise des prix et félicitations à toutes les patrouilles.", duration_minutes: 15 }
    ]
  }
}

export const calculerDureeTotaleMinutes = () => {
  if (!currentActivity.value || !currentActivity.value.steps) return 0
  return currentActivity.value.steps.reduce((sum, s) => sum + (parseInt(s.duration_minutes) || 0), 0)
}

export const calculerHeureFinEstimee = () => {
  if (!selectedSlot.value || !selectedSlot.value.start_time) return ''
  const start = new Date(selectedSlot.value.start_time)
  if (isNaN(start.getTime())) return ''
  const duree = calculerDureeTotaleMinutes()
  const end = new Date(start.getTime() + duree * 60000)
  return end.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

// ==========================================
// ACTIONS (Responsables & Invités)
// ==========================================
export const ouvrirGestionResponsables = async () => {
    if (!currentActivity.value || !selectedCamp.value) return
    
    await chargerChefsCamp(selectedCamp.value.id)
    const availableChefs = campChefsList.value.length > 0 ? campChefsList.value : chefs.value

    try {
        const attRes = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/attendance`, { headers: { 'Authorization': `Bearer ${userToken.value}` } })
        const attData = await attRes.json()
        if (attData.status === 'success' && attData.present && attData.present.length > 0) {
            const presentIds = attData.present.map(String)
            const filtered = availableChefs.filter(c => presentIds.includes(String(c.id)))
            presentChefs.value = filtered.length > 0 ? filtered : availableChefs
        } else {
            presentChefs.value = availableChefs
        }
    } catch (e) { 
        presentChefs.value = availableChefs 
    }

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

export const retirerChefPresent = async (chefId) => {
    const strId = String(chefId)
    const index = activityResponsibles.value.indexOf(strId)
    if (index !== -1) {
        activityResponsibles.value.splice(index, 1)
        await sauvegarderResponsables()
    }
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
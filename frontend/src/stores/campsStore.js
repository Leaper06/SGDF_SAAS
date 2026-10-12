// src/stores/campsStore.js
import { ref, computed } from 'vue'
import router from '../router.js'
import { API_BASE_URL } from '../api/config.js'
import { userToken, isDemoMode, unitId, unitName } from './authStore.js' 
import { demoSlotsByCamp, buildDemoTemplates } from './demoPlanningData.js'

export const campsList = ref([])
export const templatesList = ref([])
export const selectedCamp = ref(null)
export const loading = ref(true)
export const currentDate = ref(new Date())
export const showCampMenu = ref(false)

// Modales et Formulaires pour les Camps
export const showAddModal = ref(false)
export const newEvent = ref({ type: 'weekend', name: '', location: '', startDate: '', endDate: '', templateId: '' })
export const showEditCampModal = ref(false)
export const editCampForm = ref({ name: '', location: '', startDate: '', endDate: '' })

// --- COMPUTED (Calculs d'affichage) ---
export const moisActuelTexte = computed(() => currentDate.value.toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' }))

export const campsDuMois = computed(() => campsList.value.filter(camp => {
  const dateCamp = new Date(camp.start_date)
  return dateCamp.getMonth() === currentDate.value.getMonth() && dateCamp.getFullYear() === currentDate.value.getFullYear()
}))

export const joursDuCalendrier = computed(() => {
  const annee = currentDate.value.getFullYear()
  const mois = currentDate.value.getMonth()
  const premierJourDuMois = new Date(annee, mois, 1)
  const dernierJourDuMois = new Date(annee, mois + 1, 0)
  
  let decallageDebut = premierJourDuMois.getDay() - 1
  if (decallageDebut === -1) decallageDebut = 6 

  const jours = []
  const dernierJourMoisPrecedent = new Date(annee, mois, 0).getDate()
  for (let i = decallageDebut - 1; i >= 0; i--) {
    jours.push({ dayNumber: dernierJourMoisPrecedent - i, isCurrentMonth: false, aUnEvenement: false })
  }
  
  for (let i = 1; i <= dernierJourDuMois.getDate(); i++) {
    const dateDeLaCase = new Date(annee, mois, i).setHours(0, 0, 0, 0)
    let etatCamp = 'aucun'
    
    const evenementCeJour = campsDuMois.value.find(camp => {
      const start = new Date(camp.start_date).setHours(0, 0, 0, 0)
      const end = camp.end_date ? new Date(camp.end_date).setHours(0, 0, 0, 0) : start
      return dateDeLaCase >= start && dateDeLaCase <= end
    })

    if (evenementCeJour) {
      const start = new Date(evenementCeJour.start_date).setHours(0, 0, 0, 0)
      const end = evenementCeJour.end_date ? new Date(evenementCeJour.end_date).setHours(0, 0, 0, 0) : start
      if (start === end) etatCamp = 'journee'
      else if (dateDeLaCase === start) etatCamp = 'debut'
      else if (dateDeLaCase === end) etatCamp = 'fin'
      else etatCamp = 'milieu'
    }

    jours.push({ 
      date: new Date(annee, mois, i), dayNumber: i, isCurrentMonth: true, 
      etatCamp: etatCamp, camp: evenementCeJour || null
    })
  }

  const casesRestantes = 42 - jours.length
  for (let i = 1; i <= casesRestantes; i++) {
    jours.push({ dayNumber: i, isCurrentMonth: false, aUnEvenement: false })
  }
  return jours
})

export const joursDuCamp = computed(() => {
  if (!selectedCamp.value) return []
  const start = new Date(selectedCamp.value.start_date)
  start.setHours(0, 0, 0, 0)
  const end = selectedCamp.value.end_date ? new Date(selectedCamp.value.end_date) : new Date(start)
  end.setHours(0, 0, 0, 0)
  const days = []
  let current = new Date(start)
  while (current <= end) {
    days.push(new Date(current))
    current.setDate(current.getDate() + 1)
  }
  return days
})

// --- ACTIONS (Fonctions) ---
export const changerMois = (direction) => {
  const nouvelleDate = new Date(currentDate.value)
  nouvelleDate.setMonth(nouvelleDate.getMonth() + direction)
  currentDate.value = nouvelleDate
}

export const selectionnerDate = (date) => {
  const annee = date.getFullYear();
  const mois = String(date.getMonth() + 1).padStart(2, '0');
  const jour = String(date.getDate()).padStart(2, '0');
  const dateFormatee = `${annee}-${mois}-${jour}`;
  ouvrirAssistantWeekEnd(dateFormatee)
}

export const fermerModal = () => showAddModal.value = false
export const fermerEditCampModal = () => showEditCampModal.value = false

export const fetchTemplates = async () => {
  if (!userToken.value) return
  if (isDemoMode.value) {
    if (!templatesList.value.length) templatesList.value = buildDemoTemplates()
    return
  }
  try {
    const response = await fetch(`${API_BASE_URL}/camps/templates`, {
      headers: { 'Authorization': `Bearer ${userToken.value}` }
    })
    const json = await response.json()
    if (json.status === 'success') templatesList.value = json.data
  } catch (error) { console.error('Erreur API templates:', error) }
}

export const fetchCamps = async () => {
  if (!userToken.value) return
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    const today = new Date()
    const saturday = new Date(today)
    saturday.setDate(today.getDate() + (6 - today.getDay())) // Prochain Samedi
    const sunday = new Date(saturday)
    sunday.setDate(saturday.getDate() + 1) // Prochain Dimanche
    
    setTimeout(() => {
      campsList.value = [
        { id: 'demo-camp-1', name: 'Week-end de rentrée', location: 'Base de la Guiche', start_date: saturday.toISOString(), end_date: sunday.toISOString() },
        { id: 'demo-camp-2', name: 'Réunion Maîtrise', location: 'Local', start_date: today.toISOString(), end_date: today.toISOString() }
      ]
      loading.value = false
    }, 500)
    return
  }
  // =============================
  try {
    const response = await fetch(`${API_BASE_URL}/camps`, {
      headers: { 'Authorization': `Bearer ${userToken.value}` }
    })
    const json = await response.json()
    if (json.status === 'success') campsList.value = json.data
  } catch (error) { console.error('Erreur API:', error) } 
  finally { loading.value = false }
}

export const soumettreEvenement = async () => {
  if (!newEvent.value.name || !newEvent.value.startDate) { alert("Titre et date obligatoires !"); return; }
  
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    campsList.value.push({
      id: 'demo-new-' + Date.now(), 
      name: newEvent.value.name,
      location: newEvent.value.location,
      start_date: newEvent.value.startDate,
      end_date: newEvent.value.endDate || newEvent.value.startDate
    })
    fermerModal()
    newEvent.value = { type: 'weekend', name: '', location: '', startDate: '', endDate: '', templateId: '' }
    return
  }
  // =============================
  
  try {
    // 1. On prépare le paquet de données en ajoutant l'ID de l'unité
    const payload = {
        name: newEvent.value.name,
        location: newEvent.value.location,
        start_date: newEvent.value.startDate,
        end_date: newEvent.value.endDate || newEvent.value.startDate,
        type: newEvent.value.type,
        unit_id: unitId.value,
        unit_name: unitName.value,
        template_id: newEvent.value.templateId || null
    };

    const response = await fetch(`${API_BASE_URL}/camps`, {
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userToken.value}`
      }, 
      // 2. On envoie notre payload au lieu de newEvent.value
      body: JSON.stringify(payload)
    });
    
    const json = await response.json();
    
    if (json.status === 'success') {
      fermerModal();
      newEvent.value = { type: 'weekend', name: '', location: '', startDate: '', endDate: '', templateId: '' };
      await fetchCamps();
    } else { 
        alert("Erreur : " + json.message); 
    }
  } catch (error) { 
      console.error("Erreur :", error); 
  }
};

export const modifierCamp = () => {
  const formaterPourInput = (dateStr) => { if (!dateStr) return ''; return dateStr.split('T')[0] }
  editCampForm.value = {
    name: selectedCamp.value.name, location: selectedCamp.value.location,
    startDate: formaterPourInput(selectedCamp.value.start_date), endDate: formaterPourInput(selectedCamp.value.end_date)
  }
  showEditCampModal.value = true
}

export const soumettreModificationCamp = async () => {
  if (!editCampForm.value.name || !editCampForm.value.startDate) return alert("Le nom et la date sont obligatoires.");
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    selectedCamp.value.name = editCampForm.value.name
    selectedCamp.value.location = editCampForm.value.location
    selectedCamp.value.start_date = editCampForm.value.startDate
    selectedCamp.value.end_date = editCampForm.value.endDate
    fermerEditCampModal()
    return
  }
  // =============================
  try {
    const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(editCampForm.value)
    })
    const json = await response.json()
    if (json.status === 'success') {
      fermerEditCampModal()
      selectedCamp.value.name = editCampForm.value.name
      selectedCamp.value.location = editCampForm.value.location
      selectedCamp.value.start_date = editCampForm.value.startDate
      selectedCamp.value.end_date = editCampForm.value.endDate
      await fetchCamps()
    } else { alert("Erreur : " + json.message) }
  } catch (error) { console.error("Erreur :", error) }
}

export const supprimerCamp = async () => { 
  if(confirm("Supprimer tout ce week-end ?")) {
    // === INTERCEPTION MODE DÉMO ===
    if (isDemoMode.value) {
      campsList.value = campsList.value.filter(c => c.id !== selectedCamp.value.id)
      showCampMenu.value = false
      router.push('/camps')
      return
    }
    // =============================
    try {
      const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}`, { method: 'DELETE' })
      const json = await response.json()
      if (json.status === 'success') {
        showCampMenu.value = false; router.push('/camps'); await fetchCamps() 
      } else { alert("Erreur : " + json.message) }
    } catch (error) { console.error("Erreur :", error) }
  }
}

export const creerTemplateAPartirDeCamp = async (campId, templateName) => {
    if (isDemoMode.value) {
        const camp = campsList.value.find(c => c.id === campId)
        const id = 'demo-tmpl-' + Date.now()
        demoSlotsByCamp[id] = (demoSlotsByCamp[campId] || []).map(slot => ({ ...slot, id: `${id}-${slot.id}` }))
        templatesList.value.push({
            id, name: templateName, unit_id: 'demo-unit-id', is_template: true,
            start_date: camp?.start_date, end_date: camp?.end_date
        })
        alert("Modèle créé avec succès !")
        return
    }
    try {
        const response = await fetch(`${API_BASE_URL}/camps/${campId}/make-template`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${userToken.value}` 
            },
            body: JSON.stringify({ name: templateName })
        })
        const json = await response.json()
        if (json.status === 'success') {
            alert("Week-end enregistré comme modèle avec succès !")
            await fetchTemplates()
        } else {
            alert("Erreur : " + json.message)
        }
    } catch (e) {
        console.error("Erreur création template :", e)
    }
}

export const supprimerTemplateCamp = async (templateId) => {
    if (!confirm("Supprimer ce modèle de planning ?")) return
    if (isDemoMode.value) {
        templatesList.value = templatesList.value.filter(t => t.id !== templateId)
        return
    }
    try {
        const response = await fetch(`${API_BASE_URL}/camps/${templateId}`, { method: 'DELETE' })
        const json = await response.json()
        if (json.status === 'success') {
            await fetchTemplates()
        } else {
            alert("Erreur lors de la suppression")
        }
    } catch (e) {
        console.error("Erreur suppression template planning :", e)
    }
}

// ==========================================
// ASSISTANT DE CRÉATION & MODÈLES (planning « à la chaîne »)
// ==========================================
export const showPlanningWizard = ref(false)
export const wizardStartDate = ref('')

// Ouvre l'assistant de création d'un week-end (depuis le bouton + ou une date du calendrier)
export const ouvrirAssistantWeekEnd = (startDate = '') => {
  wizardStartDate.value = startDate
  showPlanningWizard.value = true
}

// Créneaux d'un modèle (ou d'un camp), au format de l'API
export const chargerCreneauxCamp = async (campId) => {
  if (isDemoMode.value) return demoSlotsByCamp[campId] || []
  try {
    const response = await fetch(`${API_BASE_URL}/camps/${campId}/slots`)
    const json = await response.json()
    return json.status === 'success' ? json.data : []
  } catch (error) {
    console.error('Erreur chargement des créneaux :', error)
    return []
  }
}

// Crée un week-end ou un modèle avec ses créneaux (format API). Retourne le camp créé ou null.
export const creerCampAvecCreneaux = async ({ name, location = '', startDate, endDate, slots, isTemplate = false }) => {
  if (isDemoMode.value) {
    const camp = {
      id: (isTemplate ? 'demo-tmpl-' : 'demo-new-') + Date.now(),
      name, location, start_date: startDate, end_date: endDate,
      is_template: isTemplate, unit_id: isTemplate ? 'demo-unit-id' : undefined
    }
    demoSlotsByCamp[camp.id] = slots.map((slot, i) => ({ ...slot, id: `${camp.id}-${i}` }))
    if (isTemplate) templatesList.value.push(camp)
    else campsList.value.push(camp)
    return camp
  }
  try {
    const response = await fetch(`${API_BASE_URL}/camps`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, location, start_date: startDate, end_date: endDate, is_template: isTemplate, slots })
    })
    const json = await response.json()
    if (json.status !== 'success') { alert("Erreur : " + (json.message || json.error)); return null }
    if (isTemplate) await fetchTemplates()
    else await fetchCamps()
    return json.data[0]
  } catch (error) {
    console.error('Erreur création :', error)
    return null
  }
}

// Enregistre des changements de structure d'un week-end ou d'un modèle de l'unité :
// `slots` = créneaux nouveaux (id « nouveau-... ») ou modifiés, `deletedIds` = créneaux supprimés.
// Un créneau absent de la liste n'est jamais supprimé (un autre chef a pu l'ajouter entre-temps).
// Retourne { ok, created } avec la correspondance id provisoire → id définitif des créneaux créés.
export const enregistrerCreneauxCamp = async (campId, slots, deletedIds = []) => {
  if (isDemoMode.value) {
    const list = (demoSlotsByCamp[campId] || []).filter(slot => !deletedIds.includes(slot.id))
    const created = []
    slots.forEach((slot, i) => {
      const existing = list.find(s => s.id === slot.id)
      if (existing) {
        Object.assign(existing, { title: slot.title, start_time: slot.start_time, end_time: slot.end_time })
      } else {
        const id = `${campId}-n${Date.now()}-${i}`
        list.push({ ...slot, id })
        created.push({ client_id: slot.id, id })
      }
    })
    demoSlotsByCamp[campId] = list
    return { ok: true, created }
  }
  try {
    const response = await fetch(`${API_BASE_URL}/camps/${campId}/slots`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slots, deleted_ids: deletedIds })
    })
    const json = await response.json()
    if (json.status !== 'success') return { ok: false, created: [] }
    return { ok: true, created: json.created || [] }
  } catch (error) {
    console.error('Erreur enregistrement du planning :', error)
    return { ok: false, created: [] }
  }
}

// Renomme un modèle et enregistre les changements de ses créneaux
export const enregistrerModele = async (template, { name, endDate, slots, deletedIds }) => {
  if (isDemoMode.value) {
    Object.assign(template, { name, end_date: endDate })
    return (await enregistrerCreneauxCamp(template.id, slots, deletedIds)).ok
  }
  const response = await fetch(`${API_BASE_URL}/camps/${template.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, location: template.location, startDate: template.start_date, endDate })
  })
  const json = await response.json()
  if (json.status !== 'success') { alert("Erreur : " + (json.message || json.error)); return false }
  const { ok } = await enregistrerCreneauxCamp(template.id, slots, deletedIds)
  await fetchTemplates()
  return ok
}

// Copie un modèle (commun ou de l'unité) dans les modèles de l'unité
export const dupliquerModele = async (template) => {
  const slots = (await chargerCreneauxCamp(template.id)).map(({ title, slot_type, start_time, end_time }) => ({ title, slot_type, start_time, end_time }))
  return creerCampAvecCreneaux({
    name: `${template.name} (copie)`, startDate: template.start_date, endDate: template.end_date, slots, isTemplate: true
  })
}

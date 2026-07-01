// src/stores/campsStore.js
import { ref, computed } from 'vue'
import router from '../router.js'
import { API_BASE_URL } from '../api/config.js'
import { userToken, isDemoMode } from './authStore.js' 

export const campsList = ref([])
export const selectedCamp = ref(null)
export const loading = ref(true)
export const currentDate = ref(new Date())
export const showCampMenu = ref(false)

// Modales et Formulaires pour les Camps
export const showAddModal = ref(false)
export const newEvent = ref({ type: 'weekend', name: '', location: '', startDate: '', endDate: '' })
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
  newEvent.value.startDate = dateFormatee
  newEvent.value.endDate = dateFormatee
  showAddModal.value = true
}

export const fermerModal = () => showAddModal.value = false
export const fermerEditCampModal = () => showEditCampModal.value = false

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
      id: 'demo-new-' + Date.now(), // Faux ID unique
      name: newEvent.value.name,
      location: newEvent.value.location,
      start_date: newEvent.value.startDate,
      end_date: newEvent.value.endDate || newEvent.value.startDate
    })
    fermerModal()
    newEvent.value = { type: 'weekend', name: '', location: '', startDate: '', endDate: '' }
    return
  }
  // =============================
  try {
    const response = await fetch(`${API_BASE_URL}/camps`, {
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userToken.value}`
      }, 
      body: JSON.stringify(newEvent.value)
    });
    const json = await response.json();
    if (json.status === 'success') {
      fermerModal();
      newEvent.value = { type: 'weekend', name: '', location: '', startDate: '', endDate: '' };
      await fetchCamps();
    } else { alert("Erreur : " + json.message); }
  } catch (error) { console.error("Erreur :", error); }
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
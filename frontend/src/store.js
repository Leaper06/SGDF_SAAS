import { ref, computed, watch } from 'vue'

// ==========================================
// ÉTAT GLOBAL DE L'APPLICATION
// ==========================================
export const currentView = ref('unite')
export const selectedCamp = ref(null)
export const selectedSlot = ref(null)
export const campsList = ref([])
export const loading = ref(true)
export const currentDate = ref(new Date())

export const searchQuery = ref('')
export const selectedFilter = ref('Tous')
export const recipesList = ref([])

export const currentMeal = ref(null)
export const currentMealRecipes = ref([])
export const showCampMenu = ref(false)

export const slotsList = ref([])

// ==========================================
// FORMULAIRES ET MODALES
// ==========================================
export const showEditCampModal = ref(false)
export const editCampForm = ref({ name: '', location: '', startDate: '', endDate: '' })

export const showEditSlotModal = ref(false)
export const slotToEditId = ref(null) 
export const editSlot = ref({ title: '', slot_type: 'logistique', selected_day: null, start_hour: '', end_hour: '' })
export const joursOuverts = ref({})

export const showAddModal = ref(false)
export const newEvent = ref({ type: 'weekend', name: '', location: '', startDate: '', endDate: '' })

export const showAddSlotModal = ref(false)
export const newSlot = ref({ title: '', slot_type: 'logistique', selected_day: null, start_hour: '', end_hour: '' })

export const currentActivity = ref({ id: null, imaginary_and_objectives: '', steps: [], materials: [] })
export const isEditingImaginaire = ref(false)
export const newMaterialName = ref('')
export const isAddingStep = ref(false)
export const editingStepIndex = ref(null)
export const newStep = ref({ title: '', description: '', duration_minutes: 15 })

export const newRecipe = ref({
  name: '', type: 'Plat chaud',
  ingredients: [{ id: Date.now(), name: '', qty_child: 80, qty_adult: 120 }],
  is_vegetarian: false, is_fridge_free: false, is_eco: false, is_wood_fire: false
})
//variable bordereau
export const shoppingList = ref([])
export const showShoppingModal = ref(false)
export const rabEnabled = ref(false)
export const currentShoppingMealId = ref(null)

//var info chef 
export const userEmail = ref(localStorage.getItem('sgdf_email') || null)
export const needsIdentification = ref(localStorage.getItem('sgdf_needs_id') === 'true')
// ==========================================
// CALCULS (COMPUTED)
// ==========================================
export const filteredRecipes = computed(() => {
  let result = recipesList.value
  if (searchQuery.value) result = result.filter(r => r.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
  if (selectedFilter.value === 'Végétarien') result = result.filter(r => r.is_vegetarian)
  if (selectedFilter.value === 'Sans frigo') result = result.filter(r => r.is_fridge_free)
  if (selectedFilter.value === 'Feu de bois') result = result.filter(r => r.is_wood_fire)
  
  return result
})
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

    jours.push({ date: new Date(annee, mois, i), dayNumber: i, isCurrentMonth: true, etatCamp: etatCamp })
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

export const slotsParJour = computed(() => {
  const groupes = {}
  slotsList.value.forEach(slot => {
    const dateStr = new Date(slot.start_time).toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })
    if (!groupes[dateStr]) groupes[dateStr] = []
    groupes[dateStr].push(slot)
  })
  return groupes
})

// ==========================================
// FONCTIONS (MÉTHODES)
// ==========================================
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

export const fetchCamps = async () => {
  if (!userToken.value) return // Si pas connecté, on ne charge rien

  try {
    const response = await fetch('http://localhost:5000/api/camps', {
      headers: { 'Authorization': `Bearer ${userToken.value}` }
    })
    const json = await response.json()
    if (json.status === 'success') campsList.value = json.data
  } catch (error) { console.error('Erreur API:', error) } 
  finally { loading.value = false }
}

export const soumettreEvenement = async () => {
  if (!newEvent.value.name || !newEvent.value.startDate) { alert("Titre et date obligatoires !"); return; }
  try {
    const response = await fetch('http://localhost:5000/api/camps', {
      method: 'POST', 
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userToken.value}` // NOUVEAU
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

export const ouvrirPlanning = async (camp) => {
  selectedCamp.value = camp
  currentView.value = 'planning'
  await fetchSlots(camp.id)
}

export const fetchSlots = async (campId) => {
  try {
    const response = await fetch(`http://localhost:5000/api/camps/${campId}/slots`)
    const json = await response.json()
    if (json.status === 'success') slotsList.value = json.data
  } catch (error) { console.error("Erreur :", error) }
}

export const modifierCamp = () => {
  const formaterPourInput = (dateStr) => { if (!dateStr) return ''; return dateStr.split('T')[0] }
  editCampForm.value = {
    name: selectedCamp.value.name, location: selectedCamp.value.location,
    startDate: formaterPourInput(selectedCamp.value.start_date), endDate: formaterPourInput(selectedCamp.value.end_date)
  }
  showEditCampModal.value = true
}

export const fermerEditCampModal = () => showEditCampModal.value = false

export const soumettreModificationCamp = async () => {
  if (!editCampForm.value.name || !editCampForm.value.startDate) return alert("Le nom et la date sont obligatoires.");
  try {
    const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}`, {
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
    try {
      const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}`, { method: 'DELETE' })
      const json = await response.json()
      if (json.status === 'success') {
        showCampMenu.value = false; currentView.value = 'calendar'; await fetchCamps() 
      } else { alert("Erreur : " + json.message) }
    } catch (error) { console.error("Erreur :", error) }
  }
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
    const response = await fetch('http://localhost:5000/api/planning_slots', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
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
    const response = await fetch(`http://localhost:5000/api/planning_slots/${slotToEditId.value}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
    const json = await response.json()
    if (json.status === 'success') { fermerEditSlotModal(); await fetchSlots(selectedCamp.value.id) }
  } catch (error) { console.error("Erreur :", error) }
}

export const supprimerSlot = async (slotId) => {
  if(confirm("Retirer cette activité du planning ?")) {
    try {
      const response = await fetch(`http://localhost:5000/api/planning_slots/${slotId}`, { method: 'DELETE' })
      const json = await response.json()
      if (json.status === 'success') await fetchSlots(selectedCamp.value.id)
    } catch (error) { console.error("Erreur :", error) }
  }
}

// RECETTES ET INTENDANCE
export const chargerCatalogueRecettes = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/recipes')
    const json = await response.json()
    if (json.status === 'success') recipesList.value = json.data
  } catch (error) { console.error("Erreur :", error) }
}

export const ouvrirEditeurRecette = () => {
  newRecipe.value = { name: '', type: 'Plat chaud', ingredients: [ { id: Date.now(), name: '', qty_child: null, qty_adult: null } ], is_vegetarian: false, is_fridge_free: false, is_wood_fire: false}
  currentView.value = 'recipe_builder'
}
export const ajouterIngredientRecette = () => newRecipe.value.ingredients.push({ id: Date.now(), name: '', qty_child: null, qty_adult: null })
export const supprimerIngredientRecette = (index) => newRecipe.value.ingredients.splice(index, 1)

export const partagerRecette = async () => {
  if (!newRecipe.value.name) return alert("Il faut un nom de recette !")
  try {
    const response = await fetch('http://localhost:5000/api/recipes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(newRecipe.value) })
    const json = await response.json()
    if (json.status === 'success') { chargerCatalogueRecettes(); currentView.value = 'recipe_catalog' }
  } catch (error) { console.error("Erreur :", error) }
}

export const getRecipeIcon = (type) => {
  const t = (type || '').toLowerCase()
  if (t.includes('entrée')) return { emoji: '🥗', bg: 'bg-green-100', text: 'text-green-600' }
  if (t.includes('plat')) return { emoji: '🍝', bg: 'bg-orange-100', text: 'text-[#e45a27]' }
  if (t.includes('dessert') || t.includes('fruit')) return { emoji: '🍏', bg: 'bg-blue-100', text: 'text-blue-500' }
  return { emoji: '🧀', bg: 'bg-yellow-50', text: 'text-yellow-600' }
}

export const ouvrirMenuRepas = async (slot) => {
  selectedSlot.value = slot; currentView.value = 'menu_builder'; currentMealRecipes.value = []; currentMeal.value = null
  try {
    const response = await fetch(`http://localhost:5000/api/planning_slots/${slot.id}/meal`)
    const json = await response.json()
    if (json.status === 'success') { currentMeal.value = json.data.meal; currentMealRecipes.value = json.data.recipes || [] }
  } catch (error) { console.error("Erreur :", error) }
}
export const retirerRecette = async (index, recipe_id) => {
  if (!currentMeal.value) return
  try {
    const response = await fetch(`http://localhost:5000/api/meals/${currentMeal.value.id}/recipes/${recipe_id}`, { method: 'DELETE' })
    const json = await response.json()
    if (json.status === 'success') currentMealRecipes.value.splice(index, 1)
  } catch (error) { console.error("Erreur :", error) }
}
export const ajouterRecetteAuMenu = async (recipe) => {
  if (!currentMeal.value) return
  try {
    const response = await fetch(`http://localhost:5000/api/meals/${currentMeal.value.id}/recipes`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ recipe_id: recipe.id }) })
    const json = await response.json()
    if (json.status === 'success') { currentMealRecipes.value.push(recipe); currentView.value = 'menu_builder' }
  } catch (error) { console.error("Erreur :", error) }
}
export const fermerMenuRepas = () => { selectedSlot.value = null; currentView.value = 'planning' }

// --- BORDEREAU ---

export const genererBordereau = async () => {
  if (!currentMeal.value) return
  
  if (currentShoppingMealId.value === currentMeal.value.id) {
    showShoppingModal.value = true
    return
  }

  try {
    const response = await fetch(`http://localhost:5000/api/meals/${currentMeal.value.id}/shopping-list?adults=17&children=0`)
    const json = await response.json()
    
    if (json.status === 'success') {
      shoppingList.value = json.data.map(item => ({...item, isChecked: false}))
      currentShoppingMealId.value = currentMeal.value.id // On mémorise l'ID
      showShoppingModal.value = true
    }
  } catch (error) {
    console.error("Erreur de génération :", error)
  }
}

export const fermerBordereau = () => {
  showShoppingModal.value = false
}

export const exporterBordereauPDF = () => {
  window.print()
}
watch(
  shoppingList,
  (newList) => {
    if (currentShoppingMealId.value && newList.length > 0) {
      localStorage.setItem(
        `shopping_list_${currentShoppingMealId.value}`,
        JSON.stringify(newList)
      )
    }
  },
  { deep: true } // 'deep: true' est indispensable pour voir les changements À L'INTÉRIEUR des objets (comme isChecked)
)

// --- CALCUL INTELLIGENT DU BORDEREAU ---
export const groupedShoppingList = computed(() => {
  const groups = {}
  
  shoppingList.value.forEach(item => {
    const cat = item.category || 'Autre'
    if (!groups[cat]) groups[cat] = []
    
    let finalQty = item.qty
    if (rabEnabled.value) {
      finalQty = Math.ceil(finalQty * 1.1)
    }
    
    let displayQty = finalQty
    let displayUnit = item.unit
    
    if (displayUnit.toLowerCase() === 'g' && finalQty >= 1000) {
      displayQty = (finalQty / 1000).toFixed(1).replace('.0', '')
      displayUnit = 'kg'
    } else if (displayUnit.toLowerCase() === 'ml' && finalQty >= 1000) {
      displayQty = (finalQty / 1000).toFixed(1).replace('.0', '')
      displayUnit = 'L'
    }
    
    item.displayQty = displayQty
    item.displayUnit = displayUnit
    
    groups[cat].push(item) 
  })
  
  return groups
})

// ACTIVITÉS
export const ouvrirFicheActivite = async (slot) => {
  selectedSlot.value = slot; currentView.value = 'activity_detail'
  try {
    const response = await fetch(`http://localhost:5000/api/planning_slots/${slot.id}/activity`)
    const json = await response.json()
    if (json.status === 'success') {
      currentActivity.value = { id: json.data.activity.id, imaginary_and_objectives: json.data.activity.imaginary_and_objectives || '', steps: json.data.steps || [], materials: json.data.materials || [] }
    }
  } catch (error) { console.error("Erreur :", error) }
}
export const sauvegarderFicheActivite = async () => {
  try {
    const response = await fetch(`http://localhost:5000/api/activities/${currentActivity.value.id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(currentActivity.value) })
    const json = await response.json()
    if (json.status === 'success') fermerFicheActivite()
  } catch (error) { console.error("Erreur :", error) }
}
export const fermerFicheActivite = () => { selectedSlot.value = null; currentView.value = 'planning' }
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

// OUTILS FORMATAGE
export const getTheme = (type) => {
  switch (type) {
    case 'jeu': return { border: 'border-[#e85d22]', textTime: 'text-[#e85d22]', bgBadge: 'bg-orange-50 text-[#e85d22]' }
    case 'repas': return { border: 'border-scoutBlue', textTime: 'text-scoutBlue', bgBadge: 'bg-blue-50 text-scoutBlue' }
    case 'spi': return { border: 'border-[#009ee0]', textTime: 'text-[#009ee0]', bgBadge: 'bg-cyan-50 text-[#009ee0]' }
    default: return { border: 'border-gray-400', textTime: 'text-gray-700', bgBadge: 'bg-gray-100 text-gray-500' }
  }
}
export const formatTypeLabel = (type) => {
  const labels = { 'jeu': 'Jeu / Anim', 'repas': 'Intendance', 'spi': 'Temps Spi', 'logistique': 'Logistique' }
  return labels[type] || 'Activité'
}
export const formatHeure = (dateTimeStr) => new Date(dateTimeStr).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
export const formatCourt = (d) => {
  const date = new Date(d)
  return `${date.toLocaleDateString('fr-FR', { weekday: 'short' }).replace('.', '')} ${date.getDate()}`
}
export const formatDay = (d) => new Date(d).toLocaleDateString('fr-FR', { day: '2-digit' })
export const formatWeekday = (d) => new Date(d).toLocaleDateString('fr-FR', { weekday: 'short' }).replace('.', '')
// ==========================================
// AUTHENTIFICATION SGDF (INTRANEXT)
// ==========================================
export const userToken = ref(localStorage.getItem('sgdf_token') || null)
export const isLoggingIn = ref(false)
export const loginError = ref('')

export const loginToSGDF = async (username, password) => {
  if (!username || !password) {
    loginError.value = "Veuillez remplir tous les champs."
    return
  }
  
  isLoggingIn.value = true
  loginError.value = ''
  
  try {
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    
    const json = await response.json()
    
    if (response.ok && json.token) {
      
      userToken.value = json.token
      userEmail.value = json.email // On stocke l'email renvoyé par Flask
      needsIdentification.value = json.needs_identification // On stocke si c'est son 1er login ou pas
      
      localStorage.setItem('sgdf_token', json.token)
      localStorage.setItem('sgdf_email', json.email) 
      localStorage.setItem('sgdf_needs_id', json.needs_identification)
      // -------------------------------
      
      await fetchCamps()
      currentView.value = 'unite'
    } else {
      loginError.value = json.error || "Identifiants incorrects ou intranet indisponible."
    }
  } catch (error) {
    console.error("Erreur de connexion :", error)
    loginError.value = "Impossible de joindre le serveur. Vérifiez que Flask tourne."
  } finally {
    isLoggingIn.value = false
  }
}


  export const logout = () => {
  userToken.value = null
  userEmail.value = null
  needsIdentification.value = false
  
  localStorage.removeItem('sgdf_token')
  localStorage.removeItem('sgdf_email')
  localStorage.removeItem('sgdf_needs_id') 
  
  currentView.value = 'calendar'
}

// --- INVITATION CHEF EXTERNE ---
export const showInviteModal = ref(false)
export const inviteAdherentId = ref('')

export const ouvrirInviteModal = () => {
  inviteAdherentId.value = ''
  showCampMenu.value = false // Ferme le menu des 3 petits points
  showInviteModal.value = true
}

export const fermerInviteModal = () => {
  showInviteModal.value = false
}

export const soumettreInvitation = async () => {
  if (!inviteAdherentId.value || !selectedCamp.value) {
    alert("Veuillez saisir un numéro d'adhérent.")
    return
  }

  try {
    const response = await fetch(`http://localhost:5000/api/camps/${selectedCamp.value.id}/guests`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${userToken.value}`
      },
      body: JSON.stringify({ adherent_id: inviteAdherentId.value.trim() })
    })

    const json = await response.json()
    if (json.status === 'success') {
      alert("Le chef a bien été ajouté au week-end !")
      fermerInviteModal()
    } else {
      alert("Erreur : " + json.message)
    }
  } catch (error) {
    console.error("Erreur d'invitation :", error)
    alert("Impossible de joindre le serveur.")
  }
}

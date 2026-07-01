import { ref, computed, watch } from 'vue'
import router from '../router.js'
import { API_BASE_URL } from '../api/config.js'
import { selectedCamp } from './campsStore.js'
import { userToken, isDemoMode } from './authStore.js'
import { jeunes, chefs } from './adherentsStore.js'
import { selectedSlot } from './planningStore.js'

// ==========================================
// ÉTAT GLOBAL (Variables)
// ==========================================
export const searchQuery = ref('')
export const selectedFilter = ref('Tous')
export const recipesList = ref([])

export const currentMeal = ref(null)
export const currentMealRecipes = ref([])

export const newRecipe = ref({
  name: '', type: 'Plat chaud',
  ingredients: [{ id: Date.now(), name: '', qty_child: 80, qty_adult: 120 }],
  is_vegetarian: false, is_fridge_free: false, is_eco: false, is_wood_fire: false
})

export const shoppingList = ref([])
export const showShoppingModal = ref(false)
export const rabEnabled = ref(false)
export const currentShoppingMealId = ref(null)

// ==========================================
// CALCULS (Computed)
// ==========================================
export const filteredRecipes = computed(() => {
  let result = recipesList.value
  if (searchQuery.value) result = result.filter(r => r.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
  if (selectedFilter.value === 'Végétarien') result = result.filter(r => r.is_vegetarian)
  if (selectedFilter.value === 'Sans frigo') result = result.filter(r => r.is_fridge_free)
  if (selectedFilter.value === 'Feu de bois') result = result.filter(r => r.is_wood_fire)
  return result
})

export const groupedShoppingList = computed(() => {
  const groups = {}
  shoppingList.value.forEach(item => {
    const cat = item.category || 'Autre'
    if (!groups[cat]) groups[cat] = []
    
    let finalQty = item.qty
    if (rabEnabled.value) finalQty = Math.ceil(finalQty * 1.1)
    let displayQty = finalQty || 0
    let displayUnit = item.unit || '' 

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

// ==========================================
// ACTIONS (Fonctions)
// ==========================================
export const chargerCatalogueRecettes = async () => {
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    recipesList.value = [
      { id: 'demo-1', name: 'Pâtes Carbonara', type: 'Plat principal', is_vegetarian: false, is_fridge_free: false, is_wood_fire: true },
      { id: 'demo-2', name: 'Salade de riz', type: 'Entrée', is_vegetarian: true, is_fridge_free: true, is_wood_fire: false }
    ]
    return
  }
  // =============================
  try {
    const response = await fetch(`${API_BASE_URL}/recipes`)
    const json = await response.json()
    if (json.status === 'success') recipesList.value = json.data
  } catch (error) { console.error("Erreur :", error) }
}

export const ouvrirEditeurRecette = () => {
  newRecipe.value = { name: '', type: 'Plat chaud', ingredients: [ { id: Date.now(), name: '', qty_child: null, qty_adult: null } ], is_vegetarian: false, is_fridge_free: false, is_wood_fire: false}
  router.push('/recipe-builder')
}
export const ajouterIngredientRecette = () => newRecipe.value.ingredients.push({ id: Date.now(), name: '', qty_child: null, qty_adult: null })
export const supprimerIngredientRecette = (index) => newRecipe.value.ingredients.splice(index, 1)

export const partagerRecette = async () => {
  if (!newRecipe.value.name) return alert("Il faut un nom de recette !")
  try {
    const response = await fetch(`${API_BASE_URL}/recipes`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(newRecipe.value) })
    const json = await response.json()
    if (json.status === 'success') { chargerCatalogueRecettes(); router.push('/recipes') }
  } catch (error) { console.error("Erreur :", error) }
}

export const ouvrirMenuRepas = async (slot) => {
  selectedSlot.value = slot
  currentMealRecipes.value = []
  currentMeal.value = null
  currentShoppingMealId.value = slot.id

  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
      currentMealRecipes.value = [
          { id: 'demo-recette-1', name: 'Salade composée', type: 'Entrée' },
          { id: 'demo-recette-2', name: 'Pâtes Carbonara', type: 'Plat principal' },
          { id: 'demo-recette-3', name: 'Bananes', type: 'Dessert' }
      ]
      router.push('/menu')
      return 
  }
  // =============================

  router.push('/menu')
  try {
    const response = await fetch(`${API_BASE_URL}/planning_slots/${slot.id}/meal`)
    const json = await response.json()
    if (json.status === 'success') { 
        currentMeal.value = json.data.meal
        currentMealRecipes.value = json.data.recipes || [] 
    }
  } catch (error) { console.error("Erreur :", error) }
}

export const retirerRecette = async (index, recipe_id) => {
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    currentMealRecipes.value.splice(index, 1)
    return
  }
  // =============================
  if (!currentMeal.value) return
  try {
    const response = await fetch(`${API_BASE_URL}/meals/${currentMeal.value.id}/recipes/${recipe_id}`, { method: 'DELETE' })
    const json = await response.json()
    if (json.status === 'success') currentMealRecipes.value.splice(index, 1)
  } catch (error) { console.error("Erreur :", error) }
}

export const ajouterRecetteAuMenu = async (recipe) => {
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    currentMealRecipes.value.push(recipe)
    router.push('/menu')
    return
  }
  // =============================
  if (!currentMeal.value) return
  const dejaPresent = currentMealRecipes.value.some(r => r.id === recipe.id)
  if (dejaPresent) {
      alert("Cette recette est déjà dans votre menu !")
      router.push('/menu') 
      return 
  }
  try {
    const response = await fetch(`${API_BASE_URL}/meals/${currentMeal.value.id}/recipes`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ recipe_id: recipe.id }) })
    const json = await response.json()
    if (json.status === 'success') { currentMealRecipes.value.push(recipe); router.push('/menu') }
  } catch (error) { console.error("Erreur :", error) }
}

export const fermerMenuRepas = () => { selectedSlot.value = null; router.push('/planning') }

export const genererBordereau = async () => {
  // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    shoppingList.value = [
      { name: 'Pâtes', qty: 2, unit: 'kg', isChecked: false, category: 'Epicerie' }, 
      { name: 'Lardons', qty: 500, unit: 'g', isChecked: false, category: 'Frais' },
      { name: 'Bananes', qty: 15, unit: 'pièces', isChecked: false, category: 'Fruits' }
    ]
    showShoppingModal.value = true
    return
  }
  // =============================

  if (!currentMeal.value) return
  
  try {
    let nbJeunesPresents = 0, nbAdultesPresents = 0
    if (selectedCamp.value) {
      const attRes = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/attendance`, { headers: { 'Authorization': `Bearer ${userToken.value}` } })
      const attData = await attRes.json()
      if (attData.status === 'success' && attData.present.length > 0) {
          const presentsIds = attData.present.map(String)
          presentsIds.forEach(idPresent => {
              if (jeunes.value.some(j => String(j.id) === idPresent)) nbJeunesPresents++
              else if (chefs.value.some(c => String(c.id) === idPresent)) nbAdultesPresents++
          })
      } else { nbJeunesPresents = jeunes.value.length; nbAdultesPresents = chefs.value.length }
    } else { nbJeunesPresents = jeunes.value.length; nbAdultesPresents = chefs.value.length }

    const response = await fetch(`${API_BASE_URL}/meals/${currentMeal.value.id}/shopping-list?adults=${nbAdultesPresents}&children=${nbJeunesPresents}`, { headers: { 'Authorization': `Bearer ${userToken.value}` } })
    const json = await response.json()
    if (json.status === 'success') {
      shoppingList.value = json.data.map(item => ({...item, isChecked: false}))
      currentShoppingMealId.value = currentMeal.value.id 
      showShoppingModal.value = true
    }
  } catch (error) { console.error("Erreur de génération :", error) }
}
export const genererBordereauGlobal = async () => {
    if (!selectedCamp.value) return
    // === INTERCEPTION MODE DÉMO ===
  if (isDemoMode.value) {
    shoppingList.value = [
      { name: 'Pâtes', qty: 2, unit: 'kg', isChecked: false, category: 'Epicerie' }, 
      { name: 'Lardons', qty: 500, unit: 'g', isChecked: false, category: 'Frais' },
      { name: 'Bananes', qty: 15, unit: 'pièces', isChecked: false, category: 'Fruits' }
    ]
    showShoppingModal.value = true
    return
  }
  // =============================
    try {
        let nbJeunesPresents = 0, nbAdultesPresents = 0
        const attRes = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/attendance`, { headers: { 'Authorization': `Bearer ${userToken.value}` } })
        const attData = await attRes.json()
        if (attData.status === 'success' && attData.present.length > 0) {
            const presentsIds = attData.present.map(String)
            presentsIds.forEach(idPresent => {
                if (jeunes.value.some(j => String(j.id) === idPresent)) nbJeunesPresents++
                else if (chefs.value.some(c => String(c.id) === idPresent)) nbAdultesPresents++
            })
        } else { nbJeunesPresents = jeunes.value.length; nbAdultesPresents = chefs.value.length }

        const response = await fetch(`${API_BASE_URL}/camps/${selectedCamp.value.id}/shopping-list?adults=${nbAdultesPresents}&children=${nbJeunesPresents}`, { headers: { 'Authorization': `Bearer ${userToken.value}` } })
        const json = await response.json()
        if (json.status === 'success') {
            shoppingList.value = json.data.map(item => ({...item, isChecked: false}))
            currentShoppingMealId.value = `global_${selectedCamp.value.id}` 
            showShoppingModal.value = true
        }
    } catch (error) { console.error("Erreur de génération globale :", error) }
}

export const fermerBordereau = () => { showShoppingModal.value = false }
export const exporterBordereauPDF = () => { window.print() }

// ==========================================
// SAUVEGARDE LOCALE (Watchers)
// ==========================================
watch(
  shoppingList,
  (newList) => {
    if (currentShoppingMealId.value && newList.length > 0) {
      localStorage.setItem(`shopping_list_${currentShoppingMealId.value}`, JSON.stringify(newList))
    }
  },
  { deep: true } 
)
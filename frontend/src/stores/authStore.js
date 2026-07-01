// src/stores/authStore.js
import { ref, computed } from 'vue'
import router from '../router.js'
import { API_BASE_URL } from '../api/config.js'

// ==========================================
// VARIABLES D'ÉTAT (Mémoire)
// ==========================================
export const userToken = ref(localStorage.getItem('sgdf_token') || null)
export const isLoggingIn = ref(false)
export const loginError = ref('')

export const userEmail = ref(localStorage.getItem('sgdf_email') || null)
export const needsIdentification = ref(localStorage.getItem('sgdf_needs_id') === 'true')
export const chefAdherentId = ref(localStorage.getItem('sgdf_chef_id') || null)
export const chefBranch = ref(localStorage.getItem('sgdf_chef_branch') || 'Inconnue')
export const unitName = ref(localStorage.getItem('sgdf_unit_name') || "Mon Unité")

// NOUVEAU : Le flag qui indique si on est en démo (pas de localStorage, ça reset au F5)
export const isDemoMode = ref(false) 

// ==========================================
// CALCULS (Computed)
// ==========================================
export const groupName = computed(() => {
    if (!unitName.value) return ''
    const parties = unitName.value.split(' - ')
    return parties.length > 1 ? parties[1].trim() : unitName.value.trim()
})

// ==========================================
// ACTIONS (Fonctions)
// ==========================================

// NOUVELLE FONCTION : Simule une connexion parfaite pour les testeurs
export const loginDemo = () => {
    isLoggingIn.value = true
    loginError.value = ''

    // On simule un léger délai réseau pour l'UX
    setTimeout(() => {
        isDemoMode.value = true
        userToken.value = 'sandbox-demo-token'
        userEmail.value = 'user.test@demo.sgdf.fr'
        needsIdentification.value = false
        chefAdherentId.value = 'Id-demo-chef'
        unitName.value = "MOUSSES ST MALO - NOTRE DAME D'ALETH (14)"
        chefBranch.value = 'SG'
        
        isLoggingIn.value = false
        router.push('/unite')
    }, 800)
}

export const loginToSGDF = async (username, password) => {
  if (!username || !password) {
    loginError.value = "Veuillez remplir tous les champs."
    return
  }
  
  isLoggingIn.value = true
  loginError.value = ''
  
  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    })
    
    const json = await response.json()
    
  if (response.ok && json.token) {
      userToken.value = json.token
      userEmail.value = json.email 
      needsIdentification.value = json.needs_identification 
      chefAdherentId.value = json.adherent_id
      
      localStorage.setItem('sgdf_token', json.token)
      localStorage.setItem('sgdf_email', json.email) 
      localStorage.setItem('sgdf_needs_id', json.needs_identification) 
      if (json.adherent_id) localStorage.setItem('sgdf_chef_id', json.adherent_id) 
      if (json.unit_name) {
        unitName.value = json.unit_name
        localStorage.setItem('sgdf_unit_name', json.unit_name)
      }
      
      const redirectPath = localStorage.getItem('sgdf_redirect_after_login')
      if (redirectPath) {
          localStorage.removeItem('sgdf_redirect_after_login') 
          router.push(redirectPath) 
      } else {
          router.push('/unite') 
      }
    } else {
      loginError.value = json.error || "Identifiants incorrects."
    }
  } catch (error) {
    console.error("Erreur de connexion :", error)
    loginError.value = "Impossible de joindre le serveur."
  } finally {
    isLoggingIn.value = false
  }
}

export const logout = () => {
  userToken.value = null
  userEmail.value = null
  needsIdentification.value = false
  isDemoMode.value = false // On remet l'application en mode réel
  
  localStorage.removeItem('sgdf_token')
  localStorage.removeItem('sgdf_email')
  localStorage.removeItem('sgdf_needs_id') 
  localStorage.removeItem('sgdf_chef_id')      
  localStorage.removeItem('sgdf_chef_branch')
  
  router.push('/login')
}
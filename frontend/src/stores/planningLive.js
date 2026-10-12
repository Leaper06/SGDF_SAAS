// src/stores/planningLive.js
// Planning partagé entre les chefs : présence, notifications de modification, secours par vérification régulière.
import { ref } from 'vue'
import { rejoindrePlanning } from '../api/realtime.js'
import { chefAdherentId, userEmail } from './authStore.js'
import { chefs } from './adherentsStore.js'

// Si le temps réel est indisponible (réseau, mode démo), on vérifie le planning à cet intervalle
const POLLING_INTERVAL_MS = 20000

export const othersOnPlanning = ref([])   // autres chefs présents : [{ name, editing }]
export const lastRemoteChange = ref(null) // dernière modification reçue : { by, at }

let session = null
let pollTimer = null

const monPrenom = () => {
  const moi = chefs.value.find(c => String(c.id) === String(chefAdherentId.value))
  return moi?.prenom || (userEmail.value || 'Un chef').split('@')[0]
}

// Modifications faites ailleurs dans l'écran du planning (fenêtre d'un créneau, +15 min...)
const onModificationLocale = () => session?.annoncerChangement()

/**
 * Démarre le partage du planning d'un week-end.
 * @param refresh fonction qui recharge les créneaux depuis l'API
 */
export const demarrerPlanningPartage = async (campId, refresh) => {
  arreterPlanningPartage()
  window.addEventListener('planning-modifie', onModificationLocale)
  pollTimer = setInterval(() => {
    if (!session || !session.estConnecte()) refresh()
  }, POLLING_INTERVAL_MS)

  session = await rejoindrePlanning(campId, { name: monPrenom() }, {
    onChange: (payload) => {
      lastRemoteChange.value = { by: payload.by, at: Date.now() }
      refresh()
    },
    onPresence: (people) => { othersOnPlanning.value = people }
  })
}

export const arreterPlanningPartage = () => {
  window.removeEventListener('planning-modifie', onModificationLocale)
  if (pollTimer) clearInterval(pollTimer)
  pollTimer = null
  session?.quitter()
  session = null
  othersOnPlanning.value = []
  lastRemoteChange.value = null
}

export const annoncerChangement = () => session?.annoncerChangement()
export const indiquerEdition = (slotId) => session?.indiquerEdition(slotId)

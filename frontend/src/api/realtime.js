// src/api/realtime.js
// Planning à plusieurs en temps réel, via le service Realtime de Supabase.
// - Les paramètres (clé publique, nom secret du canal) sont fournis par notre API aux seuls chefs autorisés.
// - Les messages ne transportent aucune donnée : seulement « le planning a changé » et la présence
//   (prénom des chefs connectés, créneau en cours de modification). Chacun recharge ensuite via l'API.
import { RealtimeClient } from '@supabase/realtime-js'
import { API_BASE_URL } from './config.js'

let client = null

// Identifiant de cet onglet : un même chef peut être connecté sur son téléphone et son ordinateur
const tabId = `onglet-${Math.random().toString(36).slice(2, 10)}`

/**
 * Rejoint le canal temps réel d'un week-end.
 * @param campId  identifiant du week-end
 * @param me      { name } : prénom affiché aux autres chefs
 * @param onChange(payload)   appelé quand un autre chef a modifié le planning
 * @param onPresence(people)  appelé avec la liste des autres chefs présents [{ name, editing }]
 * @returns l'objet de session, ou null si le temps réel n'est pas disponible (mode démo, serveur non configuré)
 */
export const rejoindrePlanning = async (campId, me, { onChange, onPresence }) => {
  let config
  try {
    const response = await fetch(`${API_BASE_URL}/camps/${campId}/realtime`)
    config = await response.json()
  } catch {
    return null
  }
  if (config.status !== 'success' || !config.enabled) return null

  if (!client) {
    client = new RealtimeClient(`${config.url.replace(/^http/, 'ws')}/realtime/v1`, { params: { apikey: config.key } })
  }

  const channel = client.channel(config.channel, {
    config: { broadcast: { self: false }, presence: { key: tabId } }
  })
  let presenceState = { name: me.name, editing: null }

  channel.on('broadcast', { event: 'planning-change' }, ({ payload }) => onChange(payload || {}))
  channel.on('presence', { event: 'sync' }, () => {
    const others = Object.entries(channel.presenceState())
      .filter(([key]) => key !== tabId)
      .map(([, metas]) => metas[0])
      .filter(Boolean)
    onPresence(others)
  })
  channel.subscribe((status) => {
    if (status === 'SUBSCRIBED') channel.track(presenceState)
  })

  return {
    // Prévient les autres chefs que le planning vient d'être modifié
    annoncerChangement: () => channel.send({ type: 'broadcast', event: 'planning-change', payload: { by: me.name } }),
    // Indique le créneau en cours de modification (null quand on n'en modifie plus)
    indiquerEdition: (slotId) => {
      presenceState = { ...presenceState, editing: slotId }
      channel.track(presenceState)
    },
    estConnecte: () => channel.state === 'joined',
    quitter: () => client.removeChannel(channel)
  }
}

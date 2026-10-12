// src/utils/planningSlots.js
// Outils du planning « à la chaîne » : types de créneaux, journées types, calculs d'horaires
// et conversion entre les créneaux de l'API (dates ISO) et ceux de l'éditeur (jour + minutes).

// Types de créneaux de l'application, avec une durée par défaut et des titres fréquents.
// Le type décide de ce qui s'attache au créneau : « jeu » → fiche d'activité, « repas » → menu et courses.
export const SLOT_TYPES = [
  {
    key: 'jeu', label: 'Jeu / Anim', defaultDuration: 120,
    chip: 'bg-orange-50 text-[#e85d22] border-orange-200', block: 'border-[#e85d22]',
    suggestions: ['Grand jeu', 'Veillée', 'Jeu de piste', 'Olympiades', 'Jeu de nuit', 'Atelier']
  },
  {
    key: 'repas', label: 'Repas', defaultDuration: 60,
    chip: 'bg-blue-50 text-[#004267] border-blue-200', block: 'border-[#004267]',
    suggestions: ['Petit-déjeuner', 'Déjeuner', 'Goûter', 'Dîner', 'Pique-nique']
  },
  {
    key: 'service', label: 'Service', defaultDuration: 30,
    chip: 'bg-amber-50 text-amber-700 border-amber-200', block: 'border-amber-500',
    suggestions: ['Montage des tentes', 'Vaisselle', 'Rangement', 'Douches', 'Démontage', 'Coucher']
  },
  {
    key: 'autre', label: 'Autre', defaultDuration: 30,
    chip: 'bg-gray-100 text-gray-700 border-gray-200', block: 'border-gray-400',
    suggestions: ['Accueil', 'Temps spi', 'Temps libre', 'Rassemblement', 'Départ', 'Réveil']
  }
]

export const DURATIONS = [15, 30, 45, 60, 90, 120, 150, 180]

// Les anciens créneaux peuvent avoir un type hors liste (« veillée », « nuit »...) : affichés comme « Autre »
export const typeOf = (key) => SLOT_TYPES.find(t => t.key === key) || SLOT_TYPES[3]

// --- Heures exprimées en minutes depuis minuit (840 = 14:00) ---
export const toMinutes = (hhmm) => {
  const [h, m] = hhmm.split(':').map(Number)
  return h * 60 + m
}

export const formatTime = (minutes) => {
  const m = ((minutes % 1440) + 1440) % 1440
  return `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`
}

export const formatDuration = (minutes) => {
  if (minutes < 60) return `${minutes} min`
  const h = Math.floor(minutes / 60)
  const m = minutes % 60
  return m ? `${h} h ${String(m).padStart(2, '0')}` : `${h} h`
}

// Identifiant provisoire d'un créneau pas encore enregistré (l'API le reconnaît comme nouveau)
let nextId = 1
export const newId = () => `nouveau-${Date.now()}-${nextId++}`

// Créneau de l'éditeur : jour (0 = premier jour), début et fin en minutes
export const makeSlot = (day, type, title, start, duration) => ({
  id: newId(), day, type, title, start, end: start + duration, hasContent: false
})

export const slotsOfDay = (slots, day) =>
  slots.filter(s => s.day === day).sort((a, b) => a.start - b.start)

// Trous et chevauchements entre créneaux consécutifs d'une même journée
export const analyseDay = (daySlots) => {
  const issues = []
  for (let i = 1; i < daySlots.length; i++) {
    const previous = daySlots[i - 1]
    const current = daySlots[i]
    if (current.start > previous.end) {
      issues.push({ kind: 'gap', after: previous.id, start: previous.end, end: current.start })
    } else if (current.start < previous.end) {
      issues.push({ kind: 'overlap', after: previous.id, start: current.start, end: previous.end })
    }
  }
  return issues
}

// --- Journées types : squelettes prêts à l'emploi. Créneau : [heure, type, titre, durée en minutes] ---
export const DAY_PROFILES = [
  {
    key: 'arrivee', label: 'Arrivée', hint: "Début l'après-midi, jusqu'au coucher",
    slots: [
      ['14:00', 'autre', 'Accueil', 30], ['14:30', 'service', 'Montage des tentes', 60],
      ['15:30', 'jeu', 'Grand jeu', 90], ['17:00', 'repas', 'Goûter', 30], ['17:30', 'autre', 'Temps libre', 60],
      ['18:30', 'service', 'Douches', 30], ['19:00', 'repas', 'Dîner', 60], ['20:00', 'service', 'Vaisselle', 30],
      ['20:30', 'jeu', 'Veillée', 90], ['22:00', 'service', 'Coucher', 30]
    ]
  },
  {
    key: 'complete', label: 'Journée complète', hint: 'Du réveil au coucher',
    slots: [
      ['07:30', 'autre', 'Réveil', 30], ['08:00', 'repas', 'Petit-déjeuner', 60], ['09:00', 'service', 'Rangement', 30],
      ['09:30', 'autre', 'Temps spi', 30], ['10:00', 'jeu', 'Activité du matin', 120], ['12:00', 'repas', 'Déjeuner', 60],
      ['13:00', 'service', 'Vaisselle', 30], ['13:30', 'autre', 'Temps calme', 60], ['14:30', 'jeu', 'Grand jeu', 150],
      ['17:00', 'repas', 'Goûter', 30], ['17:30', 'autre', 'Temps libre', 60], ['18:30', 'service', 'Douches', 30],
      ['19:00', 'repas', 'Dîner', 60], ['20:00', 'service', 'Vaisselle', 30], ['20:30', 'jeu', 'Veillée', 90],
      ['22:00', 'service', 'Coucher', 30]
    ]
  },
  {
    key: 'depart_midi', label: 'Départ midi', hint: 'Fin avant le déjeuner',
    slots: [
      ['07:30', 'autre', 'Réveil', 30], ['08:00', 'repas', 'Petit-déjeuner', 60], ['09:00', 'service', 'Démontage des tentes', 60],
      ['10:00', 'jeu', 'Activité du matin', 90], ['11:30', 'autre', 'Rassemblement de clôture', 30], ['12:00', 'autre', 'Départ', 15]
    ]
  },
  {
    key: 'depart_aprem', label: "Départ l'après-midi", hint: 'Déjeuner sur place, départ vers 15 h',
    slots: [
      ['07:30', 'autre', 'Réveil', 30], ['08:00', 'repas', 'Petit-déjeuner', 60], ['09:00', 'autre', 'Temps spi', 30],
      ['09:30', 'jeu', 'Activité du matin', 150], ['12:00', 'repas', 'Déjeuner', 60], ['13:00', 'service', 'Démontage des tentes', 90],
      ['14:30', 'autre', 'Rassemblement de clôture', 30], ['15:00', 'autre', 'Départ', 15]
    ]
  },
  { key: 'vide', label: 'Journée vide', hint: 'Je remplis moi-même', slots: [] }
]

export const slotsFromProfile = (profileKey, day, offset = 0) => {
  const profile = DAY_PROFILES.find(p => p.key === profileKey)
  return (profile ? profile.slots : []).map(([time, type, title, duration]) =>
    makeSlot(day, type, title, toMinutes(time) + offset, duration))
}

// --- Dates réelles ---
// Un modèle créé directement n'a pas de vraie date : on l'ancre sur un samedi de référence
export const TEMPLATE_REFERENCE_DATE = '2000-01-01'

const ONE_DAY_MS = 24 * 60 * 60 * 1000

// Minuit (heure locale) du jour d'une date
export const localMidnight = (dateLike) => {
  const d = new Date(dateLike)
  return new Date(d.getFullYear(), d.getMonth(), d.getDate())
}

// Date « AAAA-MM-JJ » (heure locale) d'une date
export const toDateInput = (dateLike) => {
  const d = new Date(dateLike)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// Nombre de jours d'un camp ou d'un modèle (au moins 1)
export const dayCountOf = (startDate, endDate) => {
  if (!endDate) return 1
  return Math.max(1, Math.round((localMidnight(endDate) - localMidnight(startDate)) / ONE_DAY_MS) + 1)
}

// Créneaux de l'API → créneaux de l'éditeur (jour relatif au premier jour, minutes locales)
export const toEditorSlots = (apiSlots, firstDay) => {
  const origin = localMidnight(firstDay)
  return apiSlots.map(slot => {
    const start = new Date(slot.start_time)
    const end = new Date(slot.end_time)
    const day = Math.round((localMidnight(start) - origin) / ONE_DAY_MS)
    const startMinutes = start.getHours() * 60 + start.getMinutes()
    return {
      id: slot.id, day, type: slot.slot_type, title: slot.title,
      start: startMinutes, end: startMinutes + Math.round((end - start) / 60000),
      hasContent: !!slot.has_content
    }
  })
}

// Créneaux de l'éditeur → format de l'API (heure murale locale, convertie en ISO)
export const toApiSlots = (editorSlots, firstDay) => {
  const origin = localMidnight(firstDay)
  const at = (day, minutes) => new Date(origin.getFullYear(), origin.getMonth(), origin.getDate() + day, 0, minutes)
  return editorSlots.map(slot => ({
    id: slot.id,
    title: slot.title,
    slot_type: slot.type,
    start_time: at(slot.day, slot.start).toISOString(),
    end_time: at(slot.day, slot.end).toISOString()
  }))
}

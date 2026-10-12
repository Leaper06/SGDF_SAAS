// src/stores/demoPlanningData.js
// Données du mode Démo pour les plannings et les modèles, au même format que l'API.
// Les créneaux sont gardés en mémoire par camp : les modifications faites en démo persistent
// tant que la page n'est pas rechargée.
import { reactive } from 'vue'
import { makeSlot, toMinutes, toApiSlots, TEMPLATE_REFERENCE_DATE } from '../utils/planningSlots.js'

// Créneaux par identifiant de camp (week-end ou modèle), format API
export const demoSlotsByCamp = reactive({})

// Construit des créneaux API à partir de lignes [jour, type, titre, heure, durée en minutes]
const buildSlots = (rows) => toApiSlots(
  rows.map(([day, type, title, time, duration]) => makeSlot(day, type, title, toMinutes(time), duration)),
  TEMPLATE_REFERENCE_DATE
)

const DEMO_TEMPLATES = [
  {
    id: 'demo-tmpl-weekend', name: 'Week-end type (Samedi 14h - Dimanche 16h)', unit_id: null, days: 2,
    rows: [
      [0, 'autre', 'Accueil', '14:00', 15], [0, 'service', 'Installation tentes', '14:15', 60],
      [0, 'jeu', 'Grand Jeu de lancement', '15:15', 75], [0, 'repas', 'Goûter', '16:30', 30],
      [0, 'service', 'Préparation Repas du soir', '17:30', 90], [0, 'repas', 'Dîner du soir', '19:00', 60],
      [0, 'service', 'Vaisselle', '20:00', 45], [0, 'jeu', 'Veillée', '21:00', 90],
      [0, 'autre', 'Cinquième & Coucher', '23:00', 30],
      [1, 'repas', 'Petit-déjeuner & Réveil', '08:00', 60], [1, 'service', 'Rangement tentes & du camp', '09:00', 60],
      [1, 'autre', 'Temps Spirituel', '10:00', 30], [1, 'autre', 'Point Pédagogique', '10:30', 30],
      [1, 'repas', 'Cuisine', '11:00', 75], [1, 'repas', 'Déjeuner', '12:15', 45],
      [1, 'service', 'Rangement & Vaisselle', '13:00', 45], [1, 'jeu', "Grand Jeu de l'après-midi", '13:45', 75],
      [1, 'service', 'Goûter & Débrief du week-end', '15:00', 30], [1, 'service', 'Rassemblement & Départ', '15:30', 30]
    ]
  },
  {
    id: 'demo-tmpl-journee', name: 'Journée type (09h - 16h)', unit_id: null, days: 1,
    rows: [
      [0, 'service', 'Rassemblement & Lancement', '09:00', 30], [0, 'jeu', 'Activité du matin', '09:30', 150],
      [0, 'repas', 'Pique-nique', '12:00', 60], [0, 'autre', 'Temps calme', '13:00', 30],
      [0, 'jeu', "Grand Jeu de l'après-midi", '13:30', 90], [0, 'repas', 'Goûter & Débrief', '15:00', 30],
      [0, 'service', 'Rangement & Départ', '15:30', 30]
    ]
  },
  {
    id: 'demo-tmpl-rentree', name: 'WE de rentrée (version 2025)', unit_id: 'demo-unit-id', days: 2,
    rows: [
      [0, 'autre', 'Accueil des parents', '10:00', 30], [0, 'jeu', 'Jeux de connaissance', '10:30', 90],
      [0, 'repas', 'Pique-nique', '12:00', 60], [0, 'service', 'Montage des tentes', '13:00', 60],
      [0, 'jeu', 'Grand jeu de lancement', '14:00', 150], [0, 'repas', 'Dîner', '19:00', 60],
      [0, 'jeu', 'Veillée', '20:30', 90],
      [1, 'repas', 'Petit-déjeuner', '08:00', 60], [1, 'autre', 'Messe', '10:00', 60],
      [1, 'repas', 'Déjeuner', '12:00', 60], [1, 'autre', 'Rassemblement de clôture', '14:00', 30]
    ]
  }
]

// Modèles de démo au format de /api/camps/templates (et leurs créneaux dans demoSlotsByCamp)
export const buildDemoTemplates = () => DEMO_TEMPLATES.map(t => {
  if (!demoSlotsByCamp[t.id]) demoSlotsByCamp[t.id] = buildSlots(t.rows)
  const end = new Date(TEMPLATE_REFERENCE_DATE)
  end.setDate(end.getDate() + t.days - 1)
  return {
    id: t.id, name: t.name, unit_id: t.unit_id, is_template: true,
    start_date: TEMPLATE_REFERENCE_DATE, end_date: end.toISOString().slice(0, 10)
  }
})

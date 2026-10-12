<template>
  <div class="fixed inset-0 z-[55] flex justify-center bg-gray-900/40 backdrop-blur-sm">
    <div class="w-full md:max-w-2xl h-full flex flex-col bg-gray-50 dark:bg-gray-900 md:shadow-2xl">
      <!-- En-tête -->
      <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 flex items-center gap-3 shrink-0">
        <button @click="$emit('cancel')" class="text-gray-400 hover:text-gray-600 text-2xl leading-none" title="Fermer">×</button>
        <div class="flex-1 min-w-0">
          <div class="text-[10px] font-black uppercase tracking-wider text-[#5b2b82]">{{ headerKicker }}</div>
          <div class="font-black text-gray-900 dark:text-white truncate">{{ form.name || 'Sans titre' }}</div>
        </div>
        <div v-if="!editedTemplate" class="flex gap-1">
          <span v-for="s in STEPS" :key="s" :class="['w-2 h-2 rounded-full', step === s ? 'bg-[#e85d22]' : 'bg-gray-200 dark:bg-gray-600']"></span>
        </div>
      </div>

      <!-- 1. Informations -->
      <div v-if="step === 'infos'" class="flex-1 overflow-y-auto p-4 space-y-4">
        <label class="block">
          <span class="field-label">{{ isTemplate ? 'Nom du modèle' : "Titre de l'événement" }}</span>
          <input v-model="form.name" :placeholder="isTemplate ? 'Ex : WE de patrouille' : 'Ex : Week-end de rentrée'" class="field-input">
        </label>
        <div>
          <span class="field-label">Durée</span>
          <div class="grid grid-cols-4 gap-2">
            <button v-for="n in [1, 2, 3, 4]" :key="n" @click="form.dayCount = n"
              :class="['py-2 rounded-xl text-sm font-bold border-2', form.dayCount === n ? 'border-[#5b2b82] bg-purple-50 text-[#5b2b82] dark:bg-purple-900/20' : 'border-gray-100 dark:border-gray-700 text-gray-500 bg-white dark:bg-gray-800']">
              {{ n === 1 ? 'Journée' : n + ' jours' }}
            </button>
          </div>
        </div>
        <template v-if="!isTemplate">
          <label class="block">
            <span class="field-label">Premier jour</span>
            <input v-model="form.startDate" type="date" class="field-input">
          </label>
          <label class="block">
            <span class="field-label">Lieu</span>
            <input v-model="form.location" placeholder="Ex : Base de la Guiche" class="field-input">
          </label>
        </template>
        <button @click="step = 'composer'" :disabled="!form.name.trim() || (!isTemplate && !form.startDate)"
          class="w-full py-3 rounded-xl font-bold text-white bg-[#e85d22] disabled:opacity-40">
          Continuer : composer les journées
        </button>
      </div>

      <!-- 2. Composer chaque journée -->
      <DayComposer v-else-if="step === 'composer'" :key="form.dayCount" class="flex-1 min-h-0"
        :day-labels="dayLabels" :default-sources="defaultSources" :templates="availableTemplates" :loading="loadingTemplates"
        @back="step = 'infos'" @confirm="onComposed" />

      <!-- 3. Ajuster -->
      <template v-else>
        <div v-if="editedTemplate" class="px-4 pt-3 shrink-0">
          <input v-model="form.name" class="field-input" placeholder="Nom du modèle">
        </div>
        <p v-if="loadingTemplates" class="p-4 text-sm text-gray-400">Chargement...</p>
        <DayEditor v-else :slots="slots" :day-labels="dayLabels" class="flex-1 min-h-0" />
        <div class="p-3 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shrink-0 space-y-2">
          <label v-if="!isTemplate" class="flex items-center gap-2 text-sm font-semibold text-gray-700 dark:text-gray-200">
            <input type="checkbox" v-model="alsoSaveAsTemplate" class="w-4 h-4 accent-[#5b2b82]">
            Enregistrer aussi comme modèle de mon unité
          </label>
          <input v-if="alsoSaveAsTemplate" v-model="templateName" class="field-input" placeholder="Nom du modèle">
          <div class="flex gap-2">
            <button v-if="!editedTemplate" @click="step = 'composer'" class="px-4 py-3 rounded-xl font-bold text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300">Retour</button>
            <button @click="finish" :disabled="saving || !form.name.trim()" class="flex-1 py-3 rounded-xl font-bold text-white bg-[#e85d22] disabled:opacity-40">
              {{ saving ? 'Enregistrement...' : finishLabel }}
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
// Assistant de planning : création d'un week-end, création ou modification d'un modèle.
// Étapes : informations → composer chaque journée (journées types, jours de modèles) → ajuster à la chaîne.
import { ref, reactive, computed, onMounted } from 'vue'
import DayComposer from './DayComposer.vue'
import DayEditor from './DayEditor.vue'
import {
  templatesList, fetchTemplates, chargerCreneauxCamp, creerCampAvecCreneaux, enregistrerModele
} from '../../stores/campsStore.js'
import {
  toEditorSlots, toApiSlots, dayCountOf, toDateInput, TEMPLATE_REFERENCE_DATE
} from '../../utils/planningSlots.js'

const props = defineProps({
  mode: { type: String, default: 'weekend' },        // 'weekend' ou 'template'
  editedTemplate: { type: Object, default: null },    // modèle à modifier (mode 'template')
  startDate: { type: String, default: '' }            // premier jour proposé (AAAA-MM-JJ)
})
const emit = defineEmits(['cancel', 'done'])

const STEPS = ['infos', 'composer', 'ajuster']
const isTemplate = computed(() => props.mode === 'template')

const nextSaturday = () => {
  const d = new Date()
  d.setDate(d.getDate() + ((6 - d.getDay() + 7) % 7 || 7))
  return toDateInput(d)
}

const form = reactive({
  name: props.editedTemplate?.name || '',
  dayCount: props.editedTemplate ? dayCountOf(props.editedTemplate.start_date, props.editedTemplate.end_date) : 2,
  startDate: props.startDate || nextSaturday(),
  location: ''
})

const step = ref(props.editedTemplate ? 'ajuster' : 'infos')
const slots = reactive([])
const alsoSaveAsTemplate = ref(false)
const templateName = ref('')
const saving = ref(false)

const headerKicker = computed(() => props.editedTemplate ? 'Modifier un modèle' : isTemplate.value ? 'Nouveau modèle' : 'Nouvel événement')
const finishLabel = computed(() => isTemplate.value ? 'Enregistrer le modèle' : `Créer l'événement (${slots.length} créneaux)`)

// Libellés des jours : dates réelles pour un week-end, « Jour 1, Jour 2… » pour un modèle
const dayLabels = computed(() => Array.from({ length: form.dayCount }, (_, i) => {
  if (isTemplate.value) return `Jour ${i + 1}`
  const [y, m, d] = form.startDate.split('-').map(Number)
  return new Date(y, m - 1, d + i).toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' })
}))

// Proposition par défaut : arrivée le premier jour, journées complètes au milieu, départ l'après-midi
const defaultSources = computed(() => Array.from({ length: form.dayCount }, (_, i) => {
  if (form.dayCount === 1) return 'profil:vide'
  if (i === 0) return 'profil:arrivee'
  return i === form.dayCount - 1 ? 'profil:depart_aprem' : 'profil:complete'
}))

// --- Modèles disponibles pour composer (créneaux convertis au format de l'éditeur) ---
const availableTemplates = ref([])
let initialSlotIds = [] // créneaux du modèle au chargement (pour savoir lesquels ont été supprimés)
const loadingTemplates = ref(true)

onMounted(async () => {
  await fetchTemplates()
  const others = templatesList.value.filter(t => t.id !== props.editedTemplate?.id)
  availableTemplates.value = await Promise.all(others.map(async (t) => ({
    id: t.id,
    name: t.name,
    isUnit: !!t.unit_id,
    dayCount: dayCountOf(t.start_date, t.end_date),
    slots: toEditorSlots(await chargerCreneauxCamp(t.id), t.start_date)
  })))
  availableTemplates.value.sort((a, b) => Number(b.isUnit) - Number(a.isUnit))
  if (props.editedTemplate) {
    slots.push(...toEditorSlots(await chargerCreneauxCamp(props.editedTemplate.id), props.editedTemplate.start_date))
    initialSlotIds = slots.map(s => s.id)
  }
  loadingTemplates.value = false
})

const onComposed = (composedSlots) => {
  slots.splice(0, slots.length, ...composedSlots)
  templateName.value = `Modèle — ${form.name}`
  step.value = 'ajuster'
}

const addDays = (dateInput, n) => {
  const [y, m, d] = dateInput.split('-').map(Number)
  return toDateInput(new Date(y, m - 1, d + n))
}

// Nouveaux créneaux : sans identifiant (l'API les crée)
const newApiSlots = (firstDay) => toApiSlots(slots, firstDay).map(({ id, ...slot }) => slot)

const finish = async () => {
  saving.value = true
  try {
    if (props.editedTemplate) {
      const start = toDateInput(props.editedTemplate.start_date)
      const ok = await enregistrerModele(props.editedTemplate, {
        name: form.name.trim(), endDate: addDays(start, form.dayCount - 1), slots: toApiSlots(slots, start),
        deletedIds: initialSlotIds.filter(id => !slots.some(s => s.id === id))
      })
      if (ok) emit('done', { kind: 'template' })
      return
    }

    const firstDay = isTemplate.value ? TEMPLATE_REFERENCE_DATE : form.startDate
    const lastDay = addDays(firstDay, form.dayCount - 1)
    const created = await creerCampAvecCreneaux({
      name: form.name.trim(), location: form.location, startDate: firstDay, endDate: lastDay,
      slots: newApiSlots(firstDay), isTemplate: isTemplate.value
    })
    if (!created) return

    let template = null
    if (!isTemplate.value && alsoSaveAsTemplate.value) {
      template = await creerCampAvecCreneaux({
        name: templateName.value.trim() || form.name.trim(), startDate: firstDay, endDate: lastDay,
        slots: newApiSlots(firstDay), isTemplate: true
      })
    }
    emit('done', { kind: isTemplate.value ? 'template' : 'weekend', camp: created, template })
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.field-label { @apply block text-xs font-bold uppercase tracking-wider text-gray-400 mb-1.5; }
.field-input { @apply w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2.5 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#5b2b82]/40; }
</style>

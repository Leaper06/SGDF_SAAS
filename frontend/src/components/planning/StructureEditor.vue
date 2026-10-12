<template>
  <div class="fixed inset-0 z-[55] flex justify-center bg-gray-900/40 backdrop-blur-sm">
    <div class="w-full md:max-w-2xl h-full flex flex-col bg-gray-50 dark:bg-gray-900 md:shadow-2xl">
      <div class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 flex items-center gap-3 shrink-0">
        <div class="flex-1 min-w-0">
          <div class="text-[10px] font-black uppercase tracking-wider text-[#5b2b82]">Modifier les horaires</div>
          <div class="font-black text-gray-900 dark:text-white truncate">{{ camp.name }}</div>
        </div>
        <span :class="['text-xs font-semibold shrink-0', saveStatus.className]">{{ saveStatus.label }}</span>
        <button @click="close" :disabled="closing" class="px-3 py-1.5 rounded-lg text-sm font-bold text-white bg-[#e85d22] disabled:opacity-50">Terminé</button>
      </div>

      <!-- Chefs présents et dernière modification reçue -->
      <div v-if="others.length || remoteNotice" class="px-4 pt-2 shrink-0 space-y-1">
        <p v-if="others.length" class="text-xs font-semibold text-[#5b2b82] dark:text-purple-300">
          👥 {{ others.map(o => o.name).join(', ') }} {{ others.length > 1 ? 'sont' : 'est' }} aussi sur ce planning
        </p>
        <p v-if="remoteNotice" class="text-xs text-gray-500">{{ remoteNotice }}</p>
      </div>
      <p class="px-4 pt-2 text-[11px] text-gray-400 shrink-0">
        Enregistrement automatique. Les fiches d'activité et les menus restent attachés à leur créneau (point vert : déjà remplis).
      </p>

      <DayEditor :slots="editorSlots" :day-labels="dayLabels" :initial-composer-open="startWithComposer"
        :editing-by="editingBy" class="flex-1 min-h-0" @focus-slot="indiquerEdition" />
    </div>
  </div>
</template>

<script setup>
// Réorganisation du planning d'un week-end avec l'éditeur « à la chaîne », à plusieurs chefs :
// - chaque modification est enregistrée automatiquement (seulement ce qui a changé),
// - les modifications des autres chefs arrivent en direct et sont fusionnées,
// - on voit qui est présent et quel créneau un autre chef est en train de modifier.
import { reactive, ref, computed, watch, onUnmounted } from 'vue'
import DayEditor from './DayEditor.vue'
import { toEditorSlots, toApiSlots } from '../../utils/planningSlots.js'
import { enregistrerCreneauxCamp } from '../../stores/campsStore.js'
import { othersOnPlanning, lastRemoteChange, annoncerChangement, indiquerEdition } from '../../stores/planningLive.js'

const props = defineProps({
  camp: { type: Object, required: true },
  slots: { type: Array, required: true },      // créneaux du week-end (format API), rechargés quand un autre chef modifie
  days: { type: Array, required: true },       // dates des jours du week-end
  startWithComposer: { type: Boolean, default: false }
})
const emit = defineEmits(['close'])

const SAVE_DELAY_MS = 700
const RETRY_DELAY_MS = 10000

const editorSlots = reactive(toEditorSlots(props.slots, props.camp.start_date))

// Dernier état connu du serveur, créneau par créneau : sert à calculer ce qui a changé localement
const fingerprint = (slot) => `${slot.day}|${slot.start}|${slot.end}|${slot.title}`
let synced = new Map(editorSlots.map(s => [s.id, fingerprint(s)]))

const status = ref('saved') // 'saved' | 'pending' | 'saving' | 'offline'
const closing = ref(false)
let saveTimer = null
let saving = null

const saveStatus = computed(() => ({
  saved: { label: '✓ Enregistré', className: 'text-green-600' },
  pending: { label: 'Modifications…', className: 'text-gray-400' },
  saving: { label: 'Enregistrement…', className: 'text-gray-400' },
  offline: { label: 'Pas de réseau : en attente', className: 'text-amber-600' }
}[status.value]))

const dayLabels = computed(() => props.days.map(d =>
  new Date(d).toLocaleDateString('fr-FR', { weekday: 'short', day: 'numeric', month: 'short' })))

// --- Enregistrement automatique des changements locaux ---
const localChanges = () => {
  const changed = editorSlots.filter(s => synced.get(s.id) !== fingerprint(s))
  const currentIds = new Set(editorSlots.map(s => s.id))
  const deletedIds = [...synced.keys()].filter(id => !currentIds.has(id))
  return { changed, deletedIds }
}

const save = async () => {
  if (saving) return saving
  const { changed, deletedIds } = localChanges()
  if (!changed.length && !deletedIds.length) { status.value = 'saved'; return }

  status.value = 'saving'
  const sent = new Map(changed.map(s => [s.id, fingerprint(s)]))
  saving = enregistrerCreneauxCamp(props.camp.id, toApiSlots(changed, props.camp.start_date), deletedIds)
  const { ok, created } = await saving
  saving = null

  if (!ok) {
    status.value = 'offline'
    saveTimer = setTimeout(save, RETRY_DELAY_MS)
    return
  }
  // Les créneaux créés reçoivent leur identifiant définitif
  created.forEach(({ client_id, id }) => {
    const slot = editorSlots.find(s => s.id === client_id)
    if (slot) slot.id = id
    sent.set(id, sent.get(client_id))
    sent.delete(client_id)
  })
  sent.forEach((value, id) => synced.set(id, value))
  deletedIds.forEach(id => synced.delete(id))
  annoncerChangement()
  // D'autres modifications ont pu être faites pendant l'enregistrement
  scheduleSave()
}

const scheduleSave = () => {
  clearTimeout(saveTimer)
  const { changed, deletedIds } = localChanges()
  if (!changed.length && !deletedIds.length) { status.value = 'saved'; return }
  status.value = 'pending'
  saveTimer = setTimeout(save, SAVE_DELAY_MS)
}

watch(editorSlots, scheduleSave, { deep: true })

// --- Modifications reçues des autres chefs (rechargement des créneaux par le parent) ---
// Un créneau modifié localement et pas encore enregistré n'est jamais écrasé.
watch(() => props.slots, (serverSlots) => {
  const fresh = toEditorSlots(serverSlots, props.camp.start_date)
  const freshIds = new Set(fresh.map(s => s.id))
  const isLocallyChanged = (slot) => !synced.has(slot.id) || synced.get(slot.id) !== fingerprint(slot)

  // Créneaux supprimés par un autre chef (et non modifiés ici)
  for (let i = editorSlots.length - 1; i >= 0; i--) {
    const slot = editorSlots[i]
    if (!freshIds.has(slot.id) && synced.has(slot.id) && !isLocallyChanged(slot)) {
      editorSlots.splice(i, 1)
      synced.delete(slot.id)
    }
  }
  // Créneaux ajoutés ou modifiés par un autre chef
  fresh.forEach(serverSlot => {
    const local = editorSlots.find(s => s.id === serverSlot.id)
    if (!local) {
      if (!synced.has(serverSlot.id)) editorSlots.push(serverSlot) // pas supprimé ici entre-temps
    } else if (!isLocallyChanged(local)) {
      Object.assign(local, serverSlot)
    } else {
      local.hasContent = serverSlot.hasContent
      return
    }
    synced.set(serverSlot.id, fingerprint(serverSlot))
  })
})

// --- Présence ---
const others = computed(() => othersOnPlanning.value)
const editingBy = computed(() => Object.fromEntries(
  others.value.filter(o => o.editing).map(o => [o.editing, o.name])))

const remoteNotice = computed(() => {
  const change = lastRemoteChange.value
  if (!change || Date.now() - change.at > 60000) return ''
  return `${change.by || 'Un chef'} vient de modifier le planning.`
})

// --- Fermeture : on enregistre ce qui reste avant de quitter ---
const close = async () => {
  closing.value = true
  clearTimeout(saveTimer)
  await save()
  if (status.value === 'offline' && !confirm("Certaines modifications n'ont pas pu être enregistrées (pas de réseau). Quitter quand même ?")) {
    closing.value = false
    return
  }
  indiquerEdition(null)
  emit('close')
}

onUnmounted(() => clearTimeout(saveTimer))
</script>

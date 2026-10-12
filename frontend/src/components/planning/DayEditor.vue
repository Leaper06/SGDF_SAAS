<template>
  <div class="flex flex-col h-full min-h-0">
    <!-- Jours -->
    <div class="flex gap-2 px-4 pt-3 overflow-x-auto shrink-0">
      <button v-for="(label, day) in dayLabels" :key="day" @click="currentDay = day"
        :class="['shrink-0 px-3 py-1.5 rounded-full text-sm font-bold border transition-colors',
          currentDay === day ? 'bg-[#5b2b82] text-white border-[#5b2b82]' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700']">
        {{ label }} <span class="opacity-70">({{ slotsOfDay(slots, day).length }})</span>
      </button>
    </div>

    <!-- Actions sur la journée -->
    <div v-if="dayLabels.length > 1 || daySlots.length" class="flex gap-3 px-4 pt-2 text-xs font-bold shrink-0">
      <template v-for="(label, day) in dayLabels" :key="'copy' + day">
        <button v-if="day !== currentDay && daySlots.length" @click="copyDayTo(day)" class="text-[#5b2b82] underline">Copier vers {{ label }}</button>
      </template>
      <button v-if="daySlots.length" @click="clearDay" class="text-red-500 underline ml-auto">Vider la journée</button>
    </div>

    <!-- Créneaux de la journée -->
    <div class="flex-1 min-h-0 overflow-y-auto px-4 py-3 space-y-2">
      <p v-if="!daySlots.length" class="text-sm text-gray-400 text-center py-8">
        Journée vide : ajoutez des créneaux avec la barre ci-dessous.
      </p>

      <template v-for="slot in daySlots" :key="slot.id">
        <div :class="['rounded-xl border-l-4 bg-white dark:bg-gray-800 shadow-sm px-3 py-2 flex items-center gap-2 relative', typeOf(slot.type).block,
            editingBy[slot.id] ? 'ring-2 ring-[#5b2b82]/50' : '']"
          @focusin="$emit('focus-slot', slot.id)" @focusout="$emit('focus-slot', null)">
          <!-- Un autre chef modifie ce créneau en ce moment -->
          <span v-if="editingBy[slot.id]" class="absolute -top-2 right-3 text-[10px] font-bold text-white bg-[#5b2b82] rounded-full px-2 py-0.5">✎ {{ editingBy[slot.id] }}</span>
          <span v-if="slot.hasContent" class="shrink-0 w-2 h-2 rounded-full bg-green-500" title="Fiche ou menu rempli"></span>
          <input type="time" :value="formatTime(slot.start)" @change="setStart(slot, $event.target.value)"
            class="w-[5.2rem] shrink-0 bg-gray-50 dark:bg-gray-900 rounded-lg px-1.5 py-1 text-xs font-bold text-gray-700 dark:text-gray-200">
          <input v-model="slot.title" class="flex-1 min-w-0 bg-transparent font-bold text-sm text-gray-900 dark:text-white focus:outline-none focus:bg-gray-50 dark:focus:bg-gray-700 rounded px-1">
          <select :value="slot.end - slot.start" @change="slot.end = slot.start + Number($event.target.value)"
            class="shrink-0 bg-gray-50 dark:bg-gray-900 rounded-lg px-1 py-1 text-xs font-semibold text-gray-600 dark:text-gray-300">
            <option v-for="d in durationOptions(slot)" :key="d" :value="d">{{ formatDuration(d) }}</option>
          </select>
          <button @click="removeSlot(slot)" class="text-gray-300 hover:text-red-500 text-lg leading-none px-1" title="Supprimer">×</button>
        </div>

        <!-- Trou ou chevauchement avec le créneau suivant -->
        <div v-for="issue in issuesAfter(slot.id)" :key="issue.kind + slot.id"
          :class="['text-xs font-semibold rounded-lg px-3 py-1.5 flex items-center justify-between',
            issue.kind === 'gap' ? 'bg-gray-100 dark:bg-gray-800 text-gray-500' : 'bg-red-50 text-red-600']">
          <span v-if="issue.kind === 'gap'">Trou de {{ formatDuration(issue.end - issue.start) }}</span>
          <span v-else>Chevauchement de {{ formatDuration(issue.end - issue.start) }}</span>
          <button v-if="issue.kind === 'gap'" @click="fillGap(issue)" class="text-[#5b2b82] underline">Temps libre</button>
          <button v-else @click="resolveOverlap(slot)" class="underline">Décaler la suite</button>
        </div>
      </template>
    </div>

    <!-- Barre de saisie (repliée en un bouton quand la journée est déjà remplie, pour voir le planning) -->
    <button v-if="!composerOpen" @click="composerOpen = true"
      class="mx-3 mb-3 mt-1 py-2.5 rounded-xl border-2 border-dashed border-[#e85d22]/50 text-[#e85d22] text-sm font-bold shrink-0">
      + Ajouter un créneau (à partir de {{ formatTime(nextStart) }})
    </button>
    <div v-else class="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-3 space-y-2 shrink-0 shadow-[0_-4px_12px_rgba(0,0,0,0.05)]">
      <div class="flex justify-between items-center">
        <span class="text-xs font-black uppercase tracking-wider text-gray-400">Ajouter un créneau</span>
        <button v-if="daySlots.length" @click="composerOpen = false" class="text-xs font-bold text-gray-400">Replier ▾</button>
      </div>
      <div class="flex gap-1.5 overflow-x-auto">
        <button v-for="t in SLOT_TYPES" :key="t.key" @click="selectType(t.key)"
          :class="['shrink-0 px-3 py-1 rounded-full text-xs font-bold border', composer.type === t.key ? t.chip + ' ring-2 ring-offset-1 ring-[#5b2b82]/40' : 'border-gray-200 text-gray-500']">
          {{ t.label }}
        </button>
      </div>
      <div class="flex gap-1.5 overflow-x-auto">
        <button v-for="title in typeOf(composer.type).suggestions" :key="title" @click="composer.title = title"
          class="shrink-0 px-2.5 py-1 rounded-lg text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200">{{ title }}</button>
      </div>
      <div class="flex gap-2">
        <input v-model="composer.title" @keyup.enter="addSlot" placeholder="Titre du créneau"
          class="flex-1 min-w-0 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2.5 text-sm font-semibold dark:text-white focus:outline-none focus:ring-2 focus:ring-[#5b2b82]/40">
        <button @click="addSlot" :disabled="!composer.title.trim()" class="bg-[#e85d22] disabled:opacity-40 text-white font-bold px-4 rounded-xl text-sm">Ajouter</button>
      </div>
      <div class="flex items-center gap-2 text-xs font-bold text-gray-500 flex-wrap">
        <span>Début</span>
        <button @click="composer.start = nextStart - 15" class="step-btn">−15</button>
        <input type="time" :value="formatTime(nextStart)" @change="composer.start = toMinutes($event.target.value)"
          class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-1.5 py-0.5 text-sm text-gray-900 dark:text-white">
        <button @click="composer.start = nextStart + 15" class="step-btn">+15</button>
        <span class="ml-1">Durée</span>
        <select v-model.number="composer.duration" class="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-1 py-0.5 text-gray-900 dark:text-white">
          <option v-for="d in DURATIONS" :key="d" :value="d">{{ formatDuration(d) }}</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
// Éditeur de planning « à la chaîne » : on enchaîne les créneaux d'une journée sans ouvrir de fenêtre.
// Utilisé pour créer ou réorganiser un week-end, et pour les modèles. `slots` est modifié directement
// (tableau réactif) ; l'enregistrement est fait par le composant parent.
import { ref, computed, reactive, watch } from 'vue'
import {
  SLOT_TYPES, DURATIONS, typeOf, formatTime, formatDuration, toMinutes,
  makeSlot, newId, slotsOfDay, analyseDay
} from '../../utils/planningSlots.js'

const props = defineProps({
  slots: { type: Array, required: true },        // créneaux { id, day, type, title, start, end }
  dayLabels: { type: Array, required: true },    // ex : ['Samedi 17 oct.', 'Dimanche 18 oct.']
  emptyDayStart: { type: Number, default: 9 * 60 }, // début proposé quand une journée est vide
  initialComposerOpen: { type: Boolean, default: false },
  editingBy: { type: Object, default: () => ({}) } // créneaux modifiés par d'autres chefs : { idCréneau: prénom }
})
defineEmits(['focus-slot'])

const currentDay = ref(0)
const composer = reactive({ type: 'jeu', title: '', duration: 120, start: null })
// Barre de saisie dépliée d'office seulement si la journée est vide
const composerOpen = ref(false)

const daySlots = computed(() => slotsOfDay(props.slots, currentDay.value))
const issues = computed(() => analyseDay(daySlots.value))
const issuesAfter = (slotId) => issues.value.filter(i => i.after === slotId)

// Début proposé : fin du dernier créneau de la journée, sauf si l'utilisateur l'a changé
const nextStart = computed(() => {
  if (composer.start !== null) return composer.start
  const last = daySlots.value[daySlots.value.length - 1]
  return last ? last.end : props.emptyDayStart
})
watch(currentDay, () => {
  composer.start = null
  composerOpen.value = props.initialComposerOpen || daySlots.value.length === 0
}, { immediate: true })

const durationOptions = (slot) => [...new Set([...DURATIONS, slot.end - slot.start])].sort((a, b) => a - b)

const selectType = (key) => {
  composer.type = key
  composer.duration = typeOf(key).defaultDuration
}

const addSlot = () => {
  if (!composer.title.trim()) return
  props.slots.push(makeSlot(currentDay.value, composer.type, composer.title.trim(), nextStart.value, composer.duration))
  composer.title = ''
  composer.start = null
}

const removeAt = (predicate) => {
  for (let i = props.slots.length - 1; i >= 0; i--) {
    if (predicate(props.slots[i])) props.slots.splice(i, 1)
  }
}

// Un créneau dont la fiche d'activité ou le menu est rempli perdrait ce contenu : on demande confirmation
const confirmLoss = (slots) => {
  const filled = slots.filter(s => s.hasContent)
  if (!filled.length) return true
  const names = filled.map(s => `« ${s.title} »`).join(', ')
  return confirm(`${names} : la fiche d'activité ou le menu déjà rempli sera supprimé. Continuer ?`)
}

const removeSlot = (slot) => {
  if (confirmLoss([slot])) removeAt(s => s.id === slot.id)
}

const clearDay = () => {
  if (confirmLoss(daySlots.value)) removeAt(s => s.day === currentDay.value)
}

const setStart = (slot, hhmm) => {
  const duration = slot.end - slot.start
  slot.start = toMinutes(hhmm)
  slot.end = slot.start + duration
}

const fillGap = (gap) => {
  props.slots.push(makeSlot(currentDay.value, 'autre', 'Temps libre', gap.start, gap.end - gap.start))
}

// Décale tous les créneaux suivants pour qu'ils commencent après celui-ci
const resolveOverlap = (slot) => {
  const following = daySlots.value.filter(s => s.start >= slot.start && s.id !== slot.id)
  const delta = slot.end - following[0].start
  following.forEach(s => { s.start += delta; s.end += delta })
}

// Remplace le contenu d'un autre jour par celui du jour affiché
const copyDayTo = (targetDay) => {
  if (!confirmLoss(slotsOfDay(props.slots, targetDay))) return
  removeAt(s => s.day === targetDay)
  daySlots.value.forEach(s => props.slots.push({ ...s, id: newId(), day: targetDay, hasContent: false }))
  currentDay.value = targetDay
}
</script>

<style scoped>
.step-btn {
  @apply px-2 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 active:scale-95;
}
</style>

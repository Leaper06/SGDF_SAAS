<template>
  <div class="flex flex-col h-full min-h-0">
    <div class="flex-1 min-h-0 overflow-y-auto px-4 py-3 space-y-5">
      <!-- Raccourci : un modèle complet pour tout le week-end -->
      <section>
        <h3 class="section-title">Partir d'un modèle complet</h3>
        <p v-if="loading" class="text-sm text-gray-400">Chargement des modèles...</p>
        <p v-else-if="!templates.length" class="text-sm text-gray-400">Aucun modèle disponible.</p>
        <div class="space-y-1.5">
          <button v-for="tmpl in templates" :key="tmpl.id" @click="applyTemplate(tmpl)"
            :class="['w-full text-left rounded-xl border-2 px-3 py-2 flex items-center justify-between gap-2 transition-colors',
              appliedTemplateId === tmpl.id ? 'border-[#5b2b82] bg-purple-50 dark:bg-purple-900/20' : 'border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800']">
            <div class="min-w-0">
              <div class="font-bold text-sm text-gray-900 dark:text-white truncate">{{ tmpl.name }}</div>
              <div class="text-[11px] text-gray-500">{{ tmpl.dayCount }} jour{{ tmpl.dayCount > 1 ? 's' : '' }} · {{ tmpl.slots.length }} créneaux</div>
            </div>
            <span :class="['shrink-0 text-[10px] font-black uppercase px-2 py-0.5 rounded-full', tmpl.isUnit ? 'bg-orange-100 text-[#e85d22]' : 'bg-blue-100 text-[#004267]']">
              {{ tmpl.isUnit ? 'Mon unité' : 'Commun' }}
            </span>
          </button>
        </div>
        <p v-if="templateWarning" class="text-[11px] text-amber-700 mt-1.5">{{ templateWarning }}</p>
      </section>

      <!-- Composition jour par jour -->
      <section>
        <h3 class="section-title">Ou composer chaque journée</h3>
        <div class="space-y-3">
          <div v-for="(label, day) in dayLabels" :key="day" class="bg-white dark:bg-gray-800 rounded-xl p-3 shadow-sm">
            <div class="flex items-center justify-between mb-2">
              <span class="font-black text-gray-900 dark:text-white capitalize">{{ label }}</span>
              <span class="text-[11px] text-gray-400">{{ slotsForDay(day).length }} créneaux</span>
            </div>
            <select v-model="sources[day]" @change="appliedTemplateId = null"
              class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-2 py-2 text-sm font-semibold text-gray-900 dark:text-white">
              <optgroup label="Journées types">
                <option v-for="p in DAY_PROFILES" :key="p.key" :value="'profil:' + p.key">{{ p.label }} — {{ p.hint }}</option>
              </optgroup>
              <optgroup v-for="tmpl in templates" :key="tmpl.id" :label="(tmpl.isUnit ? 'Mon modèle · ' : 'Modèle commun · ') + tmpl.name">
                <option v-for="d in tmpl.dayCount" :key="d" :value="`modele:${tmpl.id}:${d - 1}`">{{ tmpl.name }} — jour {{ d }}</option>
              </optgroup>
            </select>
            <div v-if="sources[day].startsWith('profil:') && sources[day] !== 'profil:vide'" class="flex items-center gap-2 mt-2 text-xs font-bold text-gray-500">
              <span>Décaler la journée</span>
              <button @click="offsets[day] -= 30" class="step-btn">−30 min</button>
              <span class="text-gray-900 dark:text-white">{{ offsets[day] >= 0 ? '+' : '−' }}{{ formatDuration(Math.abs(offsets[day])) }}</span>
              <button @click="offsets[day] += 30" class="step-btn">+30 min</button>
            </div>
          </div>
        </div>
      </section>
    </div>

    <div class="p-3 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shrink-0 flex gap-2">
      <button @click="$emit('back')" class="px-4 py-3 rounded-xl font-bold text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300">Retour</button>
      <button @click="confirm" class="flex-1 py-3 rounded-xl font-bold text-white bg-[#e85d22]">Continuer : ajuster ({{ totalCount }} créneaux)</button>
    </div>
  </div>
</template>

<script setup>
// Étape « composer chaque journée » de l'assistant : chaque jour part d'une journée type,
// d'un jour d'un modèle (de l'unité ou commun), ou de rien.
import { ref, reactive, computed } from 'vue'
import { DAY_PROFILES, formatDuration, slotsFromProfile, newId } from '../../utils/planningSlots.js'

const props = defineProps({
  dayLabels: { type: Array, required: true },
  defaultSources: { type: Array, default: () => [] },
  // Modèles disponibles : { id, name, isUnit, dayCount, slots } avec des créneaux au format de l'éditeur
  templates: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false }
})
const emit = defineEmits(['confirm', 'back'])

const sources = reactive(props.dayLabels.map((_, day) => props.defaultSources[day] || 'profil:vide'))
const offsets = reactive(props.dayLabels.map(() => 0))
const appliedTemplateId = ref(null)
const templateWarning = ref('')

const applyTemplate = (tmpl) => {
  props.dayLabels.forEach((_, day) => {
    sources[day] = day < tmpl.dayCount ? `modele:${tmpl.id}:${day}` : 'profil:vide'
    offsets[day] = 0
  })
  appliedTemplateId.value = tmpl.id
  const n = props.dayLabels.length
  templateWarning.value = tmpl.dayCount > n
    ? `Ce modèle compte ${tmpl.dayCount} jours : seuls les ${n} premiers sont repris.`
    : tmpl.dayCount < n ? `Ce modèle compte ${tmpl.dayCount} jour(s) : les jours suivants restent vides, à composer ci-dessous.` : ''
}

// Créneaux produits par la source choisie pour un jour (copies indépendantes du modèle)
const slotsForDay = (day) => {
  const source = sources[day]
  if (source.startsWith('profil:')) return slotsFromProfile(source.slice(7), day, offsets[day])
  const [, templateId, templateDay] = source.split(':')
  const tmpl = props.templates.find(t => String(t.id) === templateId)
  if (!tmpl) return []
  return tmpl.slots
    .filter(s => s.day === Number(templateDay))
    .map(s => ({ ...s, id: newId(), day, hasContent: false }))
}

const totalCount = computed(() => props.dayLabels.reduce((sum, _, day) => sum + slotsForDay(day).length, 0))

const confirm = () => emit('confirm', props.dayLabels.flatMap((_, day) => slotsForDay(day)))
</script>

<style scoped>
.section-title { @apply text-xs font-black uppercase tracking-wider text-gray-400 mb-2; }
.step-btn { @apply px-2 py-0.5 rounded-md bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 active:scale-95; }
</style>

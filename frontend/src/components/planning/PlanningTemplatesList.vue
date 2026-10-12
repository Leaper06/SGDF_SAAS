<template>
  <div class="space-y-4">
    <p v-if="message" class="rounded-xl bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300 text-sm font-semibold px-3 py-2">{{ message }}</p>

    <button @click="creating = true" class="w-full py-2.5 rounded-xl text-sm font-bold text-white bg-[#e85d22]">+ Créer un modèle de planning</button>

    <section>
      <h4 class="text-xs font-black uppercase tracking-wider text-gray-400 mb-2">Modèles de mon unité</h4>
      <p v-if="!unitTemplates.length" class="text-sm text-gray-400 py-2">
        Aucun modèle pour l'instant. Créez-en un, ou enregistrez un week-end comme modèle.
      </p>
      <div class="space-y-2">
        <div v-for="tmpl in unitTemplates" :key="tmpl.id" class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl p-3 shadow-sm">
          <h5 class="font-bold text-gray-900 dark:text-white text-sm">{{ tmpl.name }}</h5>
          <p class="text-xs text-gray-400 mb-2">{{ describe(tmpl) }}</p>
          <div class="flex gap-2 text-xs font-bold">
            <button @click="editing = tmpl" class="flex-1 py-1.5 rounded-lg bg-[#5b2b82] text-white">Modifier</button>
            <button @click="duplicate(tmpl)" class="flex-1 py-1.5 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200">Dupliquer</button>
            <button @click="remove(tmpl)" class="px-3 py-1.5 rounded-lg bg-red-50 dark:bg-red-900/30 text-red-600">Supprimer</button>
          </div>
        </div>
      </div>
    </section>

    <section>
      <h4 class="text-xs font-black uppercase tracking-wider text-gray-400 mb-2">Modèles communs</h4>
      <div class="space-y-2">
        <div v-for="tmpl in commonTemplates" :key="tmpl.id" class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl p-3 shadow-sm">
          <h5 class="font-bold text-gray-900 dark:text-white text-sm">{{ tmpl.name }}</h5>
          <p class="text-xs text-gray-400 mb-2">{{ describe(tmpl) }} · fourni par PolyMaîtrise</p>
          <button @click="duplicate(tmpl)" class="w-full py-1.5 rounded-lg text-xs font-bold bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200">
            Copier dans mes modèles pour le personnaliser
          </button>
        </div>
      </div>
    </section>

    <PlanningWizard v-if="creating" mode="template" @cancel="creating = false" @done="onSaved('Modèle créé.')" />
    <PlanningWizard v-if="editing" mode="template" :edited-template="editing" @cancel="editing = null" @done="onSaved('Modèle enregistré.')" />
  </div>
</template>

<script setup>
// Gestion des modèles de planning (Profil → Gérer mes modèles) :
// créer un modèle de zéro, le modifier, le dupliquer, le supprimer ; copier un modèle commun.
import { ref, computed, onMounted } from 'vue'
import PlanningWizard from './PlanningWizard.vue'
import { templatesList, fetchTemplates, supprimerTemplateCamp, dupliquerModele } from '../../stores/campsStore.js'
import { dayCountOf } from '../../utils/planningSlots.js'

const creating = ref(false)
const editing = ref(null)
const message = ref('')

onMounted(fetchTemplates)

const unitTemplates = computed(() => templatesList.value.filter(t => t.unit_id))
const commonTemplates = computed(() => templatesList.value.filter(t => !t.unit_id))

const describe = (tmpl) => {
  const days = dayCountOf(tmpl.start_date, tmpl.end_date)
  return `${days === 1 ? 'Journée' : days + ' jours'}`
}

const duplicate = async (tmpl) => {
  const copy = await dupliquerModele(tmpl)
  if (copy) message.value = `« ${copy.name} » ajouté à vos modèles.`
}

const remove = async (tmpl) => {
  await supprimerTemplateCamp(tmpl.id)
  message.value = ''
}

const onSaved = (text) => {
  creating.value = false
  editing.value = null
  message.value = text
}
</script>

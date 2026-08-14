<template>
  <transition enter-active-class="transition-opacity duration-200" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition-opacity duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
    <div v-if="showModal" class="fixed inset-0 bg-black/60 backdrop-blur-sm flex justify-center items-center z-50 p-4 transition-colors">
      <div class="bg-white dark:bg-gray-800 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl flex flex-col max-h-[90vh] transition-colors">
        <div class="p-6 bg-orange-50 dark:bg-gray-900 border-b border-orange-100 dark:border-gray-700 flex justify-between items-center shrink-0 transition-colors">
          <div>
            <h3 class="text-xl font-black text-gray-900 dark:text-white tracking-tight transition-colors">Signaler un incident</h3>
            <p class="text-sm font-medium text-orange-600 dark:text-orange-400 mt-1 transition-colors">Tente : {{ incidentForm.nom }}</p>
          </div>
          <button @click="$emit('close')" class="p-2 bg-white dark:bg-gray-800 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 rounded-full shadow-sm transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1 space-y-4 bg-gray-50/50 dark:bg-gray-800/50 transition-colors">
          <div>
            <label class="block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 transition-colors">État de la tente</label>
            <select v-model="incidentForm.etat" class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/50 transition-colors">
              <option value="Endommagée">Endommagée (Toile déchirée, tendeur cassé...)</option>
              <option value="Incomplète">Incomplète (Manque sardines, piquet...)</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 transition-colors">Description du problème</label>
            <textarea v-model="incidentForm.notes_incident" rows="4" placeholder="Ex: Il manque 4 sardines et la fermeture de la porte coince..." class="w-full bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-orange-500/50 resize-none transition-colors"></textarea>
          </div>
        </div>
        
        <div class="p-6 bg-white dark:bg-gray-800 border-t border-gray-100 dark:border-gray-700 shrink-0 transition-colors">
          <button @click="$emit('submitIncident')" class="w-full py-3.5 bg-orange-500 hover:bg-orange-600 text-white text-sm font-bold rounded-xl shadow-md transition-colors">
            Enregistrer l'incident
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  showModal: Boolean,
  incidentForm: { type: Object, default: () => ({}) }
})

defineEmits(['close', 'submitIncident'])
</script>

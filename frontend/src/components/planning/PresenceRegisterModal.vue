<template>
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
    <div v-if="showModal" class="fixed inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
      <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-colors" @click="$emit('close')"></div>
      
      <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-xl h-[85vh] md:max-h-[85vh] md:h-auto rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col z-10 overflow-hidden transition-colors">
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/50 transition-colors">
          <div>
            <h3 class="font-extrabold text-lg text-gray-900 dark:text-white transition-colors">Registre de Présence</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400 font-medium transition-colors">Effectifs du camp</p>
          </div>
          <button @click="$emit('close')" class="p-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full text-gray-600 dark:text-gray-300 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50/30 dark:bg-gray-900/30 transition-colors">
          <div>
            <h4 class="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-3 transition-colors">La Maîtrise ({{ campChefs.length }})</h4>
            <div class="space-y-2 grid grid-cols-1 md:grid-cols-2 md:gap-2 md:space-y-0">
              <div v-for="chef in campChefs" :key="chef.adherent_id" @click="onTogglePresence(chef.adherent_id)"
                   :class="['border rounded-2xl p-3 flex justify-between items-center cursor-pointer transition-all active:scale-95', selectedAdherents.includes(String(chef.adherent_id)) ? 'border-blue-500 dark:border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600']">
                <span class="font-bold text-gray-900 dark:text-white text-sm transition-colors">{{ chef.first_name }} {{ chef.last_name }}</span>
                <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center transition-colors', selectedAdherents.includes(String(chef.adherent_id)) ? 'bg-blue-500 border-blue-500 text-white' : 'border-gray-300 dark:border-gray-600']">
                  <svg v-if="selectedAdherents.includes(String(chef.adherent_id))" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h4 class="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-3 transition-colors">Les Jeunes ({{ campJeunes.length }})</h4>
            <div class="space-y-2 grid grid-cols-1 md:grid-cols-2 md:gap-2 md:space-y-0">
              <div v-for="jeune in campJeunes" :key="jeune.adherent_id" @click="onTogglePresence(jeune.adherent_id)" 
                   :class="['border rounded-2xl p-3 flex justify-between items-center cursor-pointer transition-all active:scale-95', selectedAdherents.includes(String(jeune.adherent_id)) ? 'border-blue-500 dark:border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 hover:border-gray-300 dark:hover:border-gray-600']">
                <span class="font-bold text-gray-900 dark:text-white text-sm transition-colors">{{ jeune.first_name }} {{ jeune.last_name }}</span>
                <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center transition-colors', selectedAdherents.includes(String(jeune.adherent_id)) ? 'bg-blue-500 border-blue-500 text-white' : 'border-gray-300 dark:border-gray-600']">
                  <svg v-if="selectedAdherents.includes(String(jeune.adherent_id))" xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-6 border-t border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] transition-colors">
          <div class="flex justify-between items-center mb-4">
            <span class="text-sm font-bold text-gray-500 dark:text-gray-400 transition-colors">Total présents</span>
            <span class="text-xl font-black text-gray-900 dark:text-white transition-colors">{{ selectedAdherents.length }} / {{ campChefs.length + campJeunes.length }}</span>
          </div>
          <button @click="onSavePresence" class="w-full bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-500 text-white font-bold py-4 rounded-xl transition-all active:scale-95 shadow-md">
            Enregistrer les présences
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { triggerHaptic } from '../../utils/haptics.js'

defineProps({
  showModal: Boolean,
  campJeunes: { type: Array, default: () => [] },
  campChefs: { type: Array, default: () => [] },
  selectedAdherents: { type: Array, default: () => [] }
})

const emit = defineEmits(['close', 'togglePresence', 'savePresence'])

const onTogglePresence = (id) => {
  triggerHaptic('light')
  emit('togglePresence', id)
}

const onSavePresence = () => {
  triggerHaptic('success')
  emit('savePresence')
}
</script>

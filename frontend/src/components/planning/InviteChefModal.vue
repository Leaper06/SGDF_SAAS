<template>
  <transition enter-active-class="transition-opacity duration-200" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition-opacity duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center px-4">
      <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-colors" @click="$emit('close')"></div>
      <div class="bg-white dark:bg-gray-800 rounded-3xl w-full max-w-sm overflow-hidden shadow-2xl z-10 relative transition-colors">
        <div class="bg-scoutBlue dark:bg-gray-900 p-5 text-white flex justify-between items-center transition-colors border-b dark:border-gray-700">
          <h3 class="font-bold text-lg">Inviter un renfort</h3>
          <button @click="$emit('close')" class="text-white/70 hover:text-white p-1">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        
        <div class="p-6 space-y-4">
          <p class="text-sm text-gray-500 dark:text-gray-400 font-medium transition-colors">
            Saisissez le <strong class="text-gray-800 dark:text-gray-200">numéro d'adhérent</strong> du chef extérieur. Ce week-end apparaîtra automatiquement sur son application.
          </p>
          <div>
            <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-2 transition-colors">N° Adhérent SGDF</label>
            <input :value="inviteAdherentId" @input="$emit('update:inviteAdherentId', $event.target.value)" type="text" placeholder="Ex: 162821708" class="w-full border-2 border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 rounded-xl px-4 py-3 font-medium text-gray-900 dark:text-white focus:outline-none focus:border-scoutBlue dark:focus:border-blue-500 focus:bg-white dark:focus:bg-gray-800 transition-colors">
          </div>
        </div>
        
        <div class="p-4 bg-gray-50 dark:bg-gray-800/50 flex gap-3 transition-colors border-t dark:border-gray-700">
          <button @click="$emit('close')" class="flex-1 py-3 text-sm font-bold text-gray-600 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">Annuler</button>
          <button @click="$emit('submitInvite')" class="flex-1 py-3 text-sm font-bold text-white bg-scoutBlue dark:bg-blue-600 rounded-xl hover:bg-blue-800 dark:hover:bg-blue-700 transition-colors shadow-md">Inviter</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  showModal: Boolean,
  inviteAdherentId: String
})

defineEmits(['close', 'submitInvite', 'update:inviteAdherentId'])
</script>

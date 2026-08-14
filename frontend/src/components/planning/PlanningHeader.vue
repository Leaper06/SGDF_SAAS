<template>
  <div class="bg-scoutBlue dark:bg-gray-800 text-white pt-6 pb-4 px-4 rounded-b-3xl shadow-md z-20 flex flex-col items-center shrink-0 transition-colors">
    <h1 class="text-2xl font-bold tracking-wide">PolyMaîtrise</h1>
    <p class="text-sm font-light text-blue-100 dark:text-gray-300 mt-1 transition-colors">Planning du week-end</p>
  </div>
  
  <div class="bg-white dark:bg-gray-800 px-4 py-3 flex justify-center items-center border-b border-gray-100 dark:border-gray-700 shadow-sm z-10 shrink-0 transition-colors">
    <div class="max-w-5xl mx-auto w-full flex justify-between items-center">
      <button @click="$emit('goBack')" class="flex items-center text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 text-sm font-medium transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Retour
      </button>
      <div class="text-center">
        <h2 class="text-sm font-bold text-gray-900 dark:text-white transition-colors">{{ selectedCamp?.name }}</h2>
      </div>
      <div class="relative">
        <button @click="$emit('toggleMenu')" class="text-gray-400 dark:text-gray-500 hover:text-scoutViolet dark:hover:text-purple-400 p-1 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
          </svg>
        </button>

        <transition enter-active-class="transition duration-100 ease-out" enter-from-class="transform scale-95 opacity-0" enter-to-class="transform scale-100 opacity-100" leave-active-class="transition duration-75 ease-in" leave-from-class="transform scale-100 opacity-100" leave-to-class="transform scale-95 opacity-0">
          <div v-if="showCampMenu" class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-100 dark:border-gray-700 py-2 z-50 transition-colors">
            <button @click="$emit('editCamp')" class="w-full text-left px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-2.5 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
              Modifier les infos
            </button>

            <button @click="$emit('inviteChef')" class="w-full text-left px-4 py-3 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-3 border-b border-gray-50 dark:border-gray-700 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-scoutBlue dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
              <span class="font-medium">Inviter un chef</span>
            </button>

            <button @click="$emit('exportPdf')" class="w-full text-left px-4 py-3 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-3 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-600 dark:text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span class="font-medium">Exporter le dossier (PDF)</span>
            </button>

            <button @click="$emit('createTemplate')" class="w-full text-left px-4 py-3 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center gap-3 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-orange-500 dark:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
              </svg>
              <span class="font-medium">Enregistrer comme modèle</span>
            </button>

            <div class="border-t border-gray-100 dark:border-gray-700 my-1 transition-colors"></div>

            <button @click="$emit('deleteCamp')" class="w-full text-left px-4 py-2.5 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 flex items-center gap-2.5 font-semibold transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              Supprimer le week-end
            </button>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  selectedCamp: Object,
  showCampMenu: Boolean
})

defineEmits(['goBack', 'toggleMenu', 'editCamp', 'inviteChef', 'exportPdf', 'createTemplate', 'deleteCamp'])
</script>

<template>
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-4" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-4">
    <div v-if="message" role="alert" class="fixed bottom-20 md:bottom-6 left-4 right-4 md:left-auto md:right-6 md:max-w-sm z-[60] bg-red-600 dark:bg-red-700 text-white text-sm font-semibold px-4 py-3 rounded-xl shadow-lg flex items-start gap-3">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
      </svg>
      <span class="flex-1">{{ message }}</span>
      <button @click="message = ''" class="shrink-0 opacity-80 hover:opacity-100" aria-label="Fermer">✕</button>
    </div>
  </transition>
</template>

<script setup>
// Affiche les échecs de requêtes signalés par l'intercepteur réseau (src/api/config.js)
import { ref, onMounted, onUnmounted } from 'vue'

const DISPLAY_DURATION_MS = 6000

const message = ref('')
let hideTimer = null

const handleApiProblem = (event) => {
  message.value = event.detail.message
  if (hideTimer) clearTimeout(hideTimer)
  hideTimer = setTimeout(() => { message.value = '' }, DISPLAY_DURATION_MS)
}

onMounted(() => window.addEventListener('api-problem', handleApiProblem))

onUnmounted(() => {
  window.removeEventListener('api-problem', handleApiProblem)
  if (hideTimer) clearTimeout(hideTimer)
})
</script>

<template>
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 -translate-y-4" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 -translate-y-4">
    <div v-if="!isOnline || showRestoredBanner" :class="['w-full py-2 px-4 text-xs font-bold text-center flex items-center justify-center gap-2 z-50 shrink-0 shadow-sm transition-colors', isOnline ? 'bg-emerald-600 text-white' : 'bg-amber-500 dark:bg-amber-600 text-white']">
      
      <!-- Icône Hors-Ligne -->
      <svg v-if="!isOnline" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 5.636a9 9 0 010 12.728m-12.728 0a9 9 0 010-12.728m2.828 2.828a6 6 0 018.484 0m-8.484 8.484a6 6 0 010-8.484M12 12h.01" />
      </svg>
      
      <!-- Icône En Ligne Rétabli -->
      <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
      </svg>

      <span>
        {{ isOnline ? 'Connexion rétablie ! Données synchronisées.' : 'Mode Hors-Ligne : Vous avez accès aux données mises en cache.' }}
      </span>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isOnline = ref(navigator.onLine)
const showRestoredBanner = ref(false)
let restoredTimer = null

const handleOnline = () => {
  isOnline.value = true
  showRestoredBanner.value = true
  if (restoredTimer) clearTimeout(restoredTimer)
  restoredTimer = setTimeout(() => {
    showRestoredBanner.value = false
  }, 4000)
}

const handleOffline = () => {
  isOnline.value = false
  showRestoredBanner.value = false
}

onMounted(() => {
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
})

onUnmounted(() => {
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
  if (restoredTimer) clearTimeout(restoredTimer)
})
</script>

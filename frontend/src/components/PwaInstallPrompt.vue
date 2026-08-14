<template>
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-10 scale-95" enter-to-class="opacity-100 translate-y-0 scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 scale-100" leave-to-class="opacity-0 translate-y-10 scale-95">
    <div v-if="showPrompt && !isStandalone" class="fixed bottom-20 md:bottom-6 left-4 right-4 md:left-auto md:right-6 md:max-w-sm bg-scoutBlue dark:bg-gray-800 text-white rounded-2xl p-4 shadow-2xl z-50 border border-blue-400/30 dark:border-gray-700 flex flex-col gap-3 transition-colors">
      <div class="flex items-start justify-between">
        <div class="flex items-center gap-3">
          <img src="/icons/pwa-192x192.png" alt="PolyMaîtrise" class="w-10 h-10 rounded-xl shadow-md shrink-0 border border-white/20">
          <div>
            <h4 class="font-bold text-sm">Installer PolyMaîtrise</h4>
            <p class="text-[11px] text-blue-100 dark:text-gray-300 mt-0.5">Accès rapide & mode hors-ligne sur le terrain</p>
          </div>
        </div>
        <button @click="dismiss" class="text-white/60 hover:text-white p-1 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>
      </div>

      <div class="flex gap-2 mt-1">
        <button @click="dismiss" class="flex-1 py-2.5 text-xs font-bold text-blue-100 dark:text-gray-300 bg-white/10 hover:bg-white/20 rounded-xl transition-colors">
          Plus tard
        </button>
        <button @click="installPwa" class="flex-1 py-2.5 text-xs font-bold text-scoutBlue bg-white hover:bg-gray-100 rounded-xl transition-colors shadow-md flex items-center justify-center gap-1.5">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-[#e85d22]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
          Installer (1 Clic)
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const showPrompt = ref(false)
let deferredPrompt = null

const isStandalone = computed(() => {
  return window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true
})

const handleBeforeInstallPrompt = (e) => {
  e.preventDefault()
  deferredPrompt = e
  console.log('✅ Event beforeinstallprompt reçu par le navigateur !')
  showPrompt.value = true
}

const installPwa = async () => {
  if (deferredPrompt) {
    showPrompt.value = false
    deferredPrompt.prompt()
    const choiceResult = await deferredPrompt.userChoice
    console.log(`Résultat utilisateur : ${choiceResult.outcome}`)
    deferredPrompt = null
  }
}

const dismiss = () => {
  showPrompt.value = false
}

onMounted(() => {
  // Réinitialisation du localStorage pour les tests de dev
  localStorage.removeItem('pwa_prompt_dismissed')
  window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
})

onUnmounted(() => {
  window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
})
</script>

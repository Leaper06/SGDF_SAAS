<template>
  <div>
    <!-- 1. Banner Pop-up automatique sur Android (Chrome) -->
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-10 scale-95" enter-to-class="opacity-100 translate-y-0 scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 scale-100" leave-to-class="opacity-0 translate-y-10 scale-95">
      <div v-if="showPrompt && !isStandalone && isMobile && !isIOS" class="fixed bottom-20 left-4 right-4 md:left-auto md:right-6 md:max-w-sm bg-scoutBlue dark:bg-gray-800 text-white rounded-2xl p-4 shadow-2xl z-50 border border-blue-400/30 dark:border-gray-700 flex flex-col gap-3 transition-colors">
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

    <!-- 2. Banner Pop-up discret spécifique iOS (Safari sur iPhone / iPad) -->
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-10 scale-95" enter-to-class="opacity-100 translate-y-0 scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 scale-100" leave-to-class="opacity-0 translate-y-10 scale-95">
      <div v-if="showIosBanner && !isStandalone && isIOS" class="fixed bottom-20 left-4 right-4 max-w-sm mx-auto bg-[#004267] dark:bg-gray-800 text-white rounded-2xl p-4 shadow-2xl z-50 border border-blue-400/30 dark:border-gray-700 flex flex-col gap-3 transition-colors">
        <div class="flex items-start justify-between">
          <div class="flex items-center gap-3">
            <img src="/icons/pwa-192x192.png" alt="PolyMaîtrise" class="w-10 h-10 rounded-xl shadow-md shrink-0 border border-white/20">
            <div>
              <h4 class="font-bold text-sm">Installer sur iPhone</h4>
              <p class="text-[11px] text-blue-100 dark:text-gray-300 mt-0.5">Accès rapide 1-clic depuis votre écran d'accueil</p>
            </div>
          </div>
          <button @click="dismissIosBanner" class="text-white/60 hover:text-white p-1 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>

        <div class="flex gap-2 mt-1">
          <button @click="dismissIosBanner" class="flex-1 py-2.5 text-xs font-bold text-blue-100 dark:text-gray-300 bg-white/10 hover:bg-white/20 rounded-xl transition-colors">
            Plus tard
          </button>
          <button @click="showGuideModal = true; dismissIosBanner()" class="flex-1 py-2.5 text-xs font-bold text-[#004267] bg-white hover:bg-gray-100 rounded-xl transition-colors shadow-md flex items-center justify-center gap-1.5">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-[#e85d22]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" /></svg>
            Tuto (2 sec) 📱
          </button>
        </div>
      </div>
    </transition>

    <!-- 3. Modale d'aide pour installation manuelle -->
    <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
      <div v-if="showGuideModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm" @click="showGuideModal = false"></div>
        <div class="relative bg-white dark:bg-gray-800 w-full max-w-md rounded-3xl p-6 shadow-2xl z-10 space-y-4 border border-gray-100 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <img src="/icons/pwa-192x192.png" alt="PolyMaîtrise" class="w-10 h-10 rounded-xl shadow-md border border-gray-200 dark:border-gray-700">
              <div>
                <h3 class="font-extrabold text-base text-gray-900 dark:text-white">Installer l'application</h3>
                <p class="text-xs text-gray-500 dark:text-gray-400">PolyMaîtrise Web App</p>
              </div>
            </div>
            <button @click="showGuideModal = false" class="p-2 bg-gray-100 dark:bg-gray-700 rounded-full text-gray-500 dark:text-gray-300">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>

          <div v-if="deferredPrompt && !isIOS" class="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-2xl border border-blue-200 dark:border-blue-800">
            <p class="text-xs text-blue-900 dark:text-blue-200 mb-3 font-medium">L'installation automatique en 1 clic est disponible !</p>
            <button @click="installPwa" class="w-full py-3 bg-[#004267] hover:bg-[#003350] text-white font-bold rounded-xl text-sm transition-colors shadow-md flex items-center justify-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
              Installer PolyMaîtrise (1 Clic)
            </button>
          </div>

          <div v-else class="space-y-3">
            <p class="text-xs text-gray-600 dark:text-gray-300">
              Pour ajouter l'application sur votre écran d'accueil :
            </p>

            <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-2xl space-y-2 border border-gray-200 dark:border-gray-700 text-xs">
              <div v-if="isIOS" class="space-y-2 text-gray-800 dark:text-gray-200">
                <div class="font-bold text-[#004267] dark:text-blue-400 flex items-center gap-1.5">
                  📱 Sur iPhone / iPad (Safari) :
                </div>
                <ol class="list-decimal pl-4 space-y-2 leading-relaxed">
                  <li>Touchez l'icône <strong>Partager</strong> <span class="inline-block px-1.5 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-[11px]">⎋</span> en bas de Safari.</li>
                  <li>Faites défiler vers le bas et sélectionnez <strong>"Sur l'écran d'accueil"</strong> <span class="inline-block px-1.5 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-[11px]">+</span>.</li>
                  <li>Appuyez sur <strong>Ajouter</strong> en haut à droite.</li>
                </ol>
              </div>

              <div v-else class="space-y-2 text-gray-800 dark:text-gray-200">
                <div class="font-bold text-[#004267] dark:text-blue-400">📱 Sur Android / Chrome :</div>
                <ol class="list-decimal pl-4 space-y-2 leading-relaxed">
                  <li>Ouvrez le menu du navigateur (les <strong>3 petits points ⋮</strong> en haut à droite).</li>
                  <li>Sélectionnez <strong>"Ajouter à l'écran d'accueil"</strong> ou <strong>"Installer l'application"</strong>.</li>
                </ol>
              </div>
            </div>

            <div v-if="isLanIp" class="bg-amber-50 dark:bg-amber-900/30 p-3 rounded-xl border border-amber-200 dark:border-amber-800 text-[11px] text-amber-800 dark:text-amber-200">
              💡 <strong>Accès LAN (HTTP) :</strong> Les navigateurs exigent l'adresse <code>localhost</code> ou du <code>HTTPS</code> pour afficher la pop-up 1-clic. Via l'IP LAN, utilisez l'option <em>"Ajouter à l'écran d'accueil"</em> dans le menu du navigateur.
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const showPrompt = ref(false)
const showIosBanner = ref(false)
const showGuideModal = ref(false)
let deferredPrompt = null

const isStandalone = computed(() => {
  return window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true
})

const isMobile = computed(() => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
})

const isIOS = computed(() => {
  return (/iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) && !window.MSStream
})

const isLanIp = computed(() => {
  const host = window.location.hostname
  return host !== 'localhost' && host !== '127.0.0.1' && !window.location.protocol.startsWith('https')
})

const handleBeforeInstallPrompt = (e) => {
  e.preventDefault()
  deferredPrompt = e
  // Uniquement sur appareil mobile Android (pas sur PC desktop)
  if (isMobile.value && !isIOS.value) {
    showPrompt.value = true
  }
}

const installPwa = async () => {
  if (deferredPrompt) {
    showPrompt.value = false
    showGuideModal.value = false
    deferredPrompt.prompt()
    const choiceResult = await deferredPrompt.userChoice
    console.log(`Résultat utilisateur : ${choiceResult.outcome}`)
    deferredPrompt = null
  }
}

const dismiss = () => {
  showPrompt.value = false
}

const dismissIosBanner = () => {
  showIosBanner.value = false
  localStorage.setItem('ios_banner_dismissed', 'true')
}

const handleOpenGuide = () => {
  showGuideModal.value = true
}

onMounted(() => {
  window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
  window.addEventListener('open-pwa-guide', handleOpenGuide)

  // Sur iOS, si non standalone et non rejeté récemment, on affiche le discret banner iOS
  if (isIOS.value && !isStandalone.value && !localStorage.getItem('ios_banner_dismissed')) {
    setTimeout(() => {
      showIosBanner.value = true
    }, 1500)
  }
})

onUnmounted(() => {
  window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
  window.removeEventListener('open-pwa-guide', handleOpenGuide)
})
</script>

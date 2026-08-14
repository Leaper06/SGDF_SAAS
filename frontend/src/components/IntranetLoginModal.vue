<template>
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
    <div v-if="showSyncModal" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="closeModal"></div>
      
      <!-- Modal Content -->
      <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl w-full max-w-sm p-6 overflow-hidden">
        <div class="text-center mb-6">
          <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-orange-600 dark:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 class="text-lg font-black text-gray-900 dark:text-white">Session Intranet Expirée</h2>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Votre session à l'intranet a expiré. Veuillez re-saisir votre mot de passe pour autoriser la mise à jour des données.
          </p>
        </div>

        <form @submit.prevent="submitSync">
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-bold text-gray-700 dark:text-gray-300 mb-1">Mot de passe Intranet</label>
              <input 
                v-model="password" 
                type="password" 
                required
                class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl text-gray-900 dark:text-white focus:outline-none focus:border-[#004267] dark:focus:border-blue-500 transition-colors"
                placeholder="Votre mot de passe SGDF"
              >
            </div>
            
            <p v-if="errorMsg" class="text-xs text-red-500 text-center font-medium">{{ errorMsg }}</p>

            <div class="flex gap-3 mt-6">
              <button type="button" @click="closeModal" class="flex-1 px-4 py-3 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-xl text-sm font-bold hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors">
                Annuler
              </button>
              <button type="submit" :disabled="isSyncing" class="flex-1 px-4 py-3 bg-[#004267] dark:bg-blue-600 text-white rounded-xl text-sm font-bold hover:bg-blue-900 dark:hover:bg-blue-700 flex items-center justify-center gap-2 transition-colors disabled:opacity-50">
                <svg v-if="isSyncing" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                <span>Synchroniser</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'
import { showSyncModal, isSyncing, syncAdherents } from '../stores/adherentsStore.js'

const password = ref('')
const errorMsg = ref('')

const closeModal = () => {
  showSyncModal.value = false
  password.value = ''
  errorMsg.value = ''
}

const submitSync = async () => {
  if (!password.value) return
  errorMsg.value = ''
  
  const success = await syncAdherents(password.value)
  if (success) {
    closeModal()
  } else {
    errorMsg.value = "Identifiants incorrects ou erreur réseau."
  }
}
</script>

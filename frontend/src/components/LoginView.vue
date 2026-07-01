<template>
    <!-- Conteneur principal : Fond gris sur PC pour faire ressortir la carte -->
    <div class="flex flex-col md:flex-row h-full w-full bg-white dark:bg-gray-900 md:bg-gray-50 md:dark:bg-gray-900 transition-colors duration-300 md:items-center md:justify-center md:p-6 relative">
        
        <!-- La carte centrée sur PC (prend toute la place sur mobile) -->
        <div class="flex flex-col md:flex-row w-full h-full md:h-auto md:max-h-[700px] md:max-w-4xl md:bg-white md:dark:bg-gray-800 md:shadow-2xl md:rounded-3xl overflow-hidden transition-colors">

            <!-- BANDEAU BLEU SGDF (En haut sur mobile, à gauche sur PC) -->
            <div class="bg-[#004267] dark:bg-[#002a42] h-[35%] md:h-auto md:w-1/2 rounded-b-[40px] md:rounded-none shadow-lg md:shadow-none flex flex-col items-center justify-center p-8 relative overflow-hidden shrink-0 transition-colors">
                <!-- Décorations d'arrière-plan -->
                <div class="absolute -right-10 -top-10 w-40 h-40 bg-white opacity-5 rounded-full"></div>
                <div class="absolute -left-10 -bottom-10 w-32 h-32 bg-white opacity-10 rounded-full"></div>
                <div class="absolute hidden md:block top-1/2 -left-16 w-48 h-48 bg-white opacity-5 rounded-full blur-xl"></div>
                
                <h1 class="text-4xl md:text-5xl font-black text-white tracking-wider mb-3 relative z-10 text-center">PolyMaîtrise</h1>
                <p class="text-blue-100 font-medium text-center text-sm md:text-base relative z-10 px-4">L'outil compagnon de votre maîtrise</p>
            </div>

            <!-- FORMULAIRE (En bas sur mobile, à droite sur PC) -->
            <div class="flex-1 px-8 pt-10 pb-20 md:py-16 md:w-1/2 flex flex-col justify-center bg-white dark:bg-gray-900 md:bg-transparent md:dark:bg-transparent transition-colors">
                
                <!-- Wrapper pour limiter la largeur des champs même à l'intérieur de la demi-carte -->
                <div class="max-w-sm mx-auto w-full flex flex-col">
                    <h2 class="text-xl md:text-2xl font-extrabold text-gray-900 dark:text-white mb-8 text-center transition-colors">Connexion Intranet</h2>
                    
                    <div class="space-y-5">
                        <div>
                            <label class="block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 transition-colors">Identifiant / Mail</label>
                            <input 
                                v-model="username" 
                                type="text" 
                                placeholder="Ex: 12345678" 
                                class="w-full bg-gray-50 dark:bg-gray-800 md:bg-gray-100/50 md:dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#004267]/50 dark:focus:ring-blue-500/50 focus:bg-white dark:focus:bg-gray-900 transition-all"
                                :disabled="isLoggingIn"
                            >
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 transition-colors">Mot de passe</label>
                            <input 
                                v-model="password" 
                                type="password" 
                                placeholder="••••••••" 
                                class="w-full bg-gray-50 dark:bg-gray-800 md:bg-gray-100/50 md:dark:bg-gray-900/50 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#004267]/50 dark:focus:ring-blue-500/50 focus:bg-white dark:focus:bg-gray-900 transition-all"
                                @keyup.enter="handleLogin"
                                :disabled="isLoggingIn"
                            >
                        </div>
                    </div>

                    <!-- MESSAGE D'ERREUR -->
                    <div v-if="loginError" class="mt-5 p-3 bg-red-50 dark:bg-red-900/30 border border-red-100 dark:border-red-800/50 rounded-xl flex items-start gap-2 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-500 shrink-0 mt-0.5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>
                        <p class="text-sm font-semibold text-red-600 dark:text-red-400 transition-colors">{{ loginError }}</p>
                    </div>

                    <!-- BOUTON DE CONNEXION -->
                    <button 
                        @click="handleLogin" 
                        :disabled="isLoggingIn"
                        class="w-full mt-8 bg-[#004267] hover:bg-[#003B5C] dark:bg-blue-600 dark:hover:bg-blue-700 text-white font-bold text-lg py-4 rounded-xl transition-all shadow-md flex justify-center items-center gap-3 disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                        <span v-if="!isLoggingIn">Se connecter</span>
                        <span v-else class="flex items-center gap-3">
                            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            Connexion en cours...
                        </span>
                    </button>

                    <!-- SÉPARATEUR & BOUTON DÉMO -->
                    <div class="relative mt-5 mb-5">
                        <div class="absolute inset-0 flex items-center">
                            <div class="w-full border-t border-gray-200 dark:border-gray-700"></div>
                        </div>
                        <div class="relative flex justify-center text-sm">
                            <span class="px-2 bg-white dark:bg-gray-900 md:bg-gray-50 md:dark:bg-gray-800 text-gray-500 transition-colors">Ou</span>
                        </div>
                    </div>

                    <button 
                        @click="loginDemo" 
                        :disabled="isLoggingIn"
                        class="w-full bg-white dark:bg-gray-800 border-2 border-[#004267] dark:border-blue-500 text-[#004267] dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-gray-800 font-bold text-[15px] py-3 rounded-xl transition-all flex justify-center items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                        Essayer la version Démo
                    </button>

                    <!-- MESSAGES D'ATTENTE -->
                    <div class="h-16 mt-4">
                        <transition enter-active-class="transition-opacity duration-300" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition-opacity duration-300" leave-from-class="opacity-100" leave-to-class="opacity-0">
                            <div v-if="isLoggingIn && !isDemoMode">
                                <p class="text-center text-xs text-gray-400 dark:text-gray-500 italic animate-pulse transition-colors">
                                    Vérification auprès de l'intranet... (cela peut prendre quelques secondes) 
                                </p>
                                <p class="text-center text-[11px] text-gray-500 dark:text-gray-400 mt-2 italic transition-colors">
                                    Si vous trouvez ça long, aidez-moi à trouver le contact du DSI des SGDF. merciii 😁
                                </p>
                            </div>
                        </transition>
                    </div>

                </div>
            </div>
        </div>
    </div>
    
    <div class="absolute bottom-4 w-full text-center z-50">
      <router-link 
        to="/mentions-legales" 
        class="text-sm text-green-700 hover:text-green-500 transition-colors"
      >
        Mentions Légales & RGPD
      </router-link>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { userToken, loginToSGDF, loginDemo, isLoggingIn, loginError, isDemoMode } from '../stores/authStore.js'
import { API_BASE_URL } from '../api/config.js'

const username = ref('')
const password = ref('')

const handleLogin = () => {
    loginToSGDF(username.value, password.value)
}
</script>
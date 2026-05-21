<template>
    <div class="flex flex-col h-full bg-white pb-20 relative">
        
        <div class="bg-[#004267] h-[35%] rounded-b-[40px] shadow-lg flex flex-col items-center justify-center p-6 relative overflow-hidden shrink-0">
            <div class="absolute -right-10 -top-10 w-40 h-40 bg-white opacity-5 rounded-full"></div>
            <div class="absolute -left-10 -bottom-10 w-32 h-32 bg-white opacity-10 rounded-full"></div>
            
            <h1 class="text-4xl font-black text-white tracking-wider mb-2 relative z-10">PolyMaîtrise</h1>
            <p class="text-blue-100 font-medium text-center text-sm relative z-10">L'outil compagnon de votre maîtrise</p>
        </div>

        <div class="flex-1 px-8 pt-10 flex flex-col">
            <h2 class="text-xl font-extrabold text-gray-900 mb-6 text-center">Connexion Intranet</h2>
            
            <div class="space-y-5">
                <div>
                    <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Identifiant / Structure</label>
                    <input 
                        v-model="username" 
                        type="text" 
                        placeholder="Ex: 12345678" 
                        class="w-full bg-gray-50 border border-gray-200 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#004267]/50 focus:bg-white transition-all"
                        :disabled="isLoggingIn"
                    >
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">Mot de passe</label>
                    <input 
                        v-model="password" 
                        type="password" 
                        placeholder="••••••••" 
                        class="w-full bg-gray-50 border border-gray-200 text-gray-900 font-medium rounded-xl px-4 py-3.5 focus:outline-none focus:ring-2 focus:ring-[#004267]/50 focus:bg-white transition-all"
                        @keyup.enter="handleLogin"
                        :disabled="isLoggingIn"
                    >
                </div>
            </div>

            <div v-if="loginError" class="mt-4 p-3 bg-red-50 border border-red-100 rounded-xl flex items-start gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-red-500 shrink-0 mt-0.5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>
                <p class="text-sm font-semibold text-red-600">{{ loginError }}</p>
            </div>

            <button 
                @click="handleLogin" 
                :disabled="isLoggingIn"
                class="w-full mt-8 bg-[#004267] hover:bg-[#003B5C] text-white font-bold text-lg py-4 rounded-xl transition-all shadow-md flex justify-center items-center gap-3 disabled:opacity-70 disabled:cursor-not-allowed"
            >
                <span v-if="!isLoggingIn">Se connecter</span>
                <span v-else class="flex items-center gap-3">
                    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                    Connexion en cours...
                </span>
            </button>
            <p v-if="isLoggingIn" class="text-center text-xs text-gray-400 mt-3 italic animate-pulse">
                Vérification auprès de l'intranet... (cela peut prendre quelques secondes)
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { loginToSGDF, isLoggingIn, loginError } from '../store.js'

const username = ref('')
const password = ref('')

const handleLogin = () => {
    loginToSGDF(username.value, password.value)
}
</script>
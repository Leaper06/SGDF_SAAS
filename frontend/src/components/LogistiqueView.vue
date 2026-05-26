<template>
    <div class="h-full flex flex-col bg-gray-50">
        
        <div class="bg-[#004267] px-6 pt-8 pb-4 shrink-0 rounded-b-[30px] shadow-md z-10">
            <h2 class="text-2xl font-black text-white tracking-wider mb-6">Logistique</h2>
            
            <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                <button 
                    @click="activeTab = 'materiel'" 
                    :class="['flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap transition-colors', activeTab === 'materiel' ? 'bg-white text-[#004267] shadow-sm' : 'bg-[#003B5C] text-blue-100 hover:bg-[#003B5C]/80']"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 10l9-7 9 7v10a2 2 0 01-2 2H5a2 2 0 01-2-2V10z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 21V10l3-2 3 2v11" />
                    </svg>
                    Matériel
                </button>

                <button 
                    @click="activeTab = 'lieux'" 
                    :class="['flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap transition-colors', activeTab === 'lieux' ? 'bg-white text-[#004267] shadow-sm' : 'bg-[#003B5C] text-blue-100 hover:bg-[#003B5C]/80']"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    Lieux de camp
                </button>

                <button 
                    disabled
                    class="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap bg-[#003B5C]/50 text-blue-200/50 cursor-not-allowed border border-dashed border-[#003B5C]"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Trésorerie (Bientôt)
                </button>
            </div>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
            
            <div v-if="activeTab === 'materiel'" class="space-y-6">
                
                <div class="flex justify-between items-end">
                    <div>
                        <h3 class="text-lg font-extrabold text-gray-900">Parc matériel</h3>
                        <p class="text-xs font-medium text-gray-500 mt-1">Éléments nécessitant une intervention</p>
                    </div>
                    <span class="bg-red-100 text-red-600 px-3 py-1 rounded-lg text-xs font-black">{{ damagedTents.length }} incident(s)</span>
                </div>

                <div v-if="damagedTents.length === 0" class="text-center py-12 bg-white rounded-2xl border border-dashed border-gray-200">
                <div class="w-16 h-16 bg-blue-50 text-[#004267] rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
                    </svg>
                </div>
                <p class="text-gray-500 font-medium">Tout le matériel est en parfait état !</p>
            </div>

                <div v-else class="space-y-4">
                    <div v-for="tente in damagedTents" :key="tente.id" class="bg-white rounded-2xl p-5 border border-red-100 shadow-sm relative overflow-hidden">
                        <div class="absolute left-0 top-0 bottom-0 w-1.5 bg-red-500"></div>
                        
                        <div class="flex justify-between items-start mb-3 pl-2">
                            <div>
                                <h4 class="font-bold text-gray-900 text-lg">{{ tente.name }}</h4>
                                <p class="text-xs text-gray-500">{{ tente.capacity }} places</p>
                            </div>
                            <button @click="marquerReparee(tente.id)" class="text-xs font-bold bg-green-50 text-green-600 hover:bg-green-100 px-3 py-2 rounded-lg transition-colors flex items-center gap-2">
                                ✅ Marquer réparée
                            </button>
                        </div>
                        
                        <div class="bg-red-50 text-red-700 text-sm font-medium p-3 rounded-xl ml-2">
                            <span class="uppercase text-[10px] font-black tracking-wider block mb-1 opacity-70">Description de l'incident</span>
                            "{{ tente.notes_incident }}"
                        </div>
                    </div>
                </div>
            </div>

                    <div v-if="activeTab === 'lieux'">
                        <div class="text-center py-12">
                            <div class="w-16 h-16 bg-blue-50 text-[#004267] rounded-full flex items-center justify-center mx-auto mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                                </svg>
                            </div>
                            <h3 class="text-lg font-bold text-gray-900 mb-2">Carnet d'adresses</h3>
                            <button class="bg-[#004267] text-white px-6 py-3 rounded-xl font-bold text-sm shadow-md">
                        + Ajouter un lieu
                    </button>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
// On importe les fonctions qu'on a créées dans notre store logistique
import { damagedTents, fetchDamagedTents, marquerReparee } from '../stores/logistiqueStore.js'

// La variable qui gère l'onglet actuellement affiché
const activeTab = ref('materiel')

// Dès que la page s'affiche, on va chercher la liste des tentes cassées sur le serveur
onMounted(() => {
    fetchDamagedTents()
})
</script>
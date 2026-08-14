<template>
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
    <div v-if="showModal" class="fixed inset-0 pb-20 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
      <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="$emit('close')"></div>
      
      <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-2xl h-[85vh] md:max-h-[85vh] md:h-auto rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col z-10 overflow-hidden transition-colors">
        <div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/50 transition-colors">
          <div>
            <h3 class="font-extrabold text-lg text-gray-900 dark:text-white transition-colors">Matériel & Logistique</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400 font-medium transition-colors">Checklist de matériel et réservation de tentes</p>
          </div>
          <button @click="$emit('close')" class="p-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 rounded-full text-gray-600 dark:text-gray-300 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" /></svg>
          </button>
        </div>

        <!-- Onglets (Matériel vs Tentes) -->
        <div class="px-6 pt-3 bg-gray-50/50 dark:bg-gray-800/50 border-b border-gray-100 dark:border-gray-700 flex gap-2">
          <button @click="$emit('update:activeTab', 'materiel')" :class="['pb-2.5 px-4 text-xs font-bold border-b-2 transition-all flex items-center gap-2', activeTab === 'materiel' ? 'border-scoutBlue dark:border-blue-400 text-scoutBlue dark:text-blue-400' : 'border-transparent text-gray-400 dark:text-gray-500 hover:text-gray-600']">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>
            Matériel à emporter ({{ campMaterials.length }})
          </button>
          <button @click="$emit('update:activeTab', 'tentes')" :class="['pb-2.5 px-4 text-xs font-bold border-b-2 transition-all flex items-center gap-2', activeTab === 'tentes' ? 'border-scoutBlue dark:border-blue-400 text-scoutBlue dark:text-blue-400' : 'border-transparent text-gray-400 dark:text-gray-500 hover:text-gray-600']">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
            Tentes ({{ selectedTents.length }})
          </button>
        </div>
        
        <!-- CONTENU ONGLET 1 : MATÉRIEL -->
        <div v-if="activeTab === 'materiel'" class="flex-1 overflow-y-auto p-6 space-y-5 bg-gray-50/30 dark:bg-gray-900/30 transition-colors">
          <div class="bg-white dark:bg-gray-800 p-4 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm space-y-3">
            <div class="flex flex-col md:flex-row gap-2.5 items-stretch md:items-center justify-between">
              <div class="flex-1 flex gap-2">
                <select :value="selectedMaterialTemplateId" @change="$emit('update:selectedMaterialTemplateId', $event.target.value)" class="flex-1 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white text-xs font-medium rounded-xl px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="">-- Choisir un modèle de matériel --</option>
                  <option v-for="tmpl in materialTemplates" :key="tmpl.id" :value="tmpl.id">{{ tmpl.name }} ({{ tmpl.items?.length || 0 }} éléments)</option>
                </select>
                <button @click="$emit('applyTemplate')" :disabled="!selectedMaterialTemplateId" class="px-4 py-2.5 bg-scoutBlue dark:bg-blue-600 disabled:opacity-40 hover:bg-blue-700 text-white font-bold text-xs rounded-xl transition-colors shrink-0">
                  Appliquer
                </button>
              </div>
              <button @click="$emit('saveTemplate')" class="px-3 py-2.5 border border-scoutBlue/30 text-scoutBlue dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 font-bold text-xs rounded-xl transition-colors shrink-0 flex items-center justify-center gap-1.5">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>
                Sauvegarder comme modèle
              </button>
            </div>
          </div>

          <div class="flex gap-2">
            <input :value="newMaterialItemName" @input="$emit('update:newMaterialItemName', $event.target.value)" @keyup.enter="$emit('addMaterial')" type="text" placeholder="Ajouter du matériel (ex: Malle pharma, Bâche, Corde...)" class="flex-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white font-medium rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-colors">
            <button @click="$emit('addMaterial')" class="px-5 py-3 bg-[#e85d22] dark:bg-orange-600 hover:bg-orange-600 text-white font-bold text-sm rounded-xl transition-transform active:scale-95 shadow-sm shrink-0">
              + Ajouter
            </button>
          </div>

          <div v-if="campMaterials.length === 0" class="text-center py-10 bg-white dark:bg-gray-800 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700 p-6">
            <p class="text-sm font-medium text-gray-400 dark:text-gray-500">Aucun matériel dans la liste.</p>
            <p class="text-xs text-gray-300 dark:text-gray-600 mt-1">Ajoute du matériel ci-dessus ou choisis un modèle réutilisable !</p>
          </div>

          <div v-else class="space-y-2">
            <div v-for="(item, index) in campMaterials" :key="item.id || index" @click="$emit('toggleMaterial', index)" class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl p-3.5 flex items-center justify-between cursor-pointer hover:border-gray-300 dark:hover:border-gray-600 transition-all shadow-sm group">
              <div class="flex items-center gap-3">
                <div :class="['w-5 h-5 rounded border-2 flex items-center justify-center transition-colors', item.is_checked ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-gray-300 dark:border-gray-600']">
                  <svg v-if="item.is_checked" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                </div>
                <span :class="['text-sm font-bold transition-colors', item.is_checked ? 'text-gray-400 dark:text-gray-500 line-through' : 'text-gray-900 dark:text-white']">
                  {{ item.name }}
                </span>
              </div>
              <button @click.stop="$emit('deleteMaterial', index)" class="text-gray-300 dark:text-gray-600 hover:text-red-500 p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/30 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
          </div>
        </div>

        <!-- CONTENU ONGLET 2 : TENTES -->
        <template v-if="activeTab === 'tentes'">
          <div class="flex-1 overflow-y-auto p-6 space-y-3 bg-gray-50/30 dark:bg-gray-900/30 transition-colors">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div v-for="tente in allTents" :key="tente.id" 
                @click="(tente.status !== 'abimee' && tente.status !== 'deja_reservee') ? $emit('toggleTent', tente.id) : null"
                :class="[
                  'border-2 rounded-2xl p-4 transition-all',
                  (tente.status === 'abimee' || tente.status === 'deja_reservee') ? 'opacity-50 cursor-not-allowed border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800' : 'cursor-pointer hover:shadow-sm dark:hover:border-gray-600',
                  selectedTents.includes(tente.id) ? 'border-gray-800 dark:border-gray-500 bg-gray-900 dark:bg-gray-700 text-white shadow-md' : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
                ]">
              
                <div class="flex justify-between items-center">
                  <div>
                    <h4 :class="['font-bold flex items-center gap-2 transition-colors', selectedTents.includes(tente.id) ? 'text-white' : 'text-gray-900 dark:text-white']">
                      {{ tente.name }}
                      <span v-if="tente.status === 'abimee'" class="text-[9px] bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 px-2 py-0.5 rounded font-black uppercase tracking-wider transition-colors">Abîmée</span>
                      <span v-if="tente.status === 'deja_reservee'" class="text-[9px] bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400 px-2 py-0.5 rounded font-black uppercase tracking-wider transition-colors">Prise</span>
                    </h4>
                    <p :class="['text-xs mt-1 font-medium transition-colors', selectedTents.includes(tente.id) ? 'text-gray-300' : 'text-gray-500 dark:text-gray-400']">
                      {{ tente.capacity }} places
                    </p>
                    
                    <button 
                      v-if="selectedTents.includes(tente.id)" 
                      @click.stop="$emit('reportIncident', tente)" 
                      class="mt-2 text-[10px] uppercase font-bold text-orange-500 dark:text-orange-400 hover:text-orange-400 dark:hover:text-orange-300 flex items-center transition-colors gap-1"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      Signaler un problème
                    </button>
                  </div>
                  
                  <div :class="[
                    'w-6 h-6 rounded border-2 flex items-center justify-center transition-colors shrink-0', 
                    selectedTents.includes(tente.id) ? 'bg-white border-white text-gray-900' : 'border-gray-300 dark:border-gray-600 bg-transparent'
                  ]">
                    <svg v-if="selectedTents.includes(tente.id)" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" /></svg>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="p-6 border-t border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] transition-colors">
            <div class="flex justify-between items-center mb-4">
              <span class="text-sm font-bold text-gray-500 dark:text-gray-400 transition-colors">Capacité sélectionnée</span>
              <span class="text-xl font-black text-gray-900 dark:text-white transition-colors">{{ totalCapacity }} places</span>
            </div>
            <button @click="$emit('saveTents')" class="w-full bg-gray-900 dark:bg-blue-600 hover:bg-black dark:hover:bg-blue-700 text-white font-bold py-4 rounded-xl transition-transform active:scale-95 shadow-md flex justify-center items-center gap-2">
              Valider les tentes
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" /></svg>
            </button>
          </div>
        </template>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  showModal: Boolean,
  activeTab: String,
  campMaterials: { type: Array, default: () => [] },
  materialTemplates: { type: Array, default: () => [] },
  selectedMaterialTemplateId: String,
  newMaterialItemName: String,
  allTents: { type: Array, default: () => [] },
  selectedTents: { type: Array, default: () => [] }
})

defineEmits([
  'close', 'update:activeTab', 'update:selectedMaterialTemplateId', 'update:newMaterialItemName',
  'applyTemplate', 'saveTemplate', 'addMaterial', 'deleteMaterial', 'toggleMaterial',
  'toggleTent', 'reportIncident', 'saveTents'
])

const totalCapacity = computed(() => {
  return props.selectedTents.reduce((total, tentId) => {
    const tent = props.allTents.find(t => t.id === tentId)
    return total + (tent ? tent.capacity : 0)
  }, 0)
})
</script>

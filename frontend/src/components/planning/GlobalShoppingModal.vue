<template>
  <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
    <div v-if="showModal" class="fixed inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6 printable-modal">
      <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-colors no-print" @click="$emit('close')"></div>
      
      <div class="relative bg-gray-50 dark:bg-gray-900 w-full md:max-w-2xl h-[90%] md:h-auto md:max-h-[90vh] rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col z-10 overflow-hidden printable-content transition-colors">
        
        <div class="bg-[#004267] dark:bg-gray-800 text-white pt-5 pb-6 px-6 shrink-0 text-center rounded-t-3xl md:rounded-t-3xl border-b-4 border-[#003B5C] dark:border-gray-700 transition-colors">
          <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
          <p class="text-sm font-medium text-blue-100 dark:text-gray-300 mt-0.5 transition-colors">Bordereau d'achats</p>
        </div>

        <div class="bg-gray-50 dark:bg-gray-800 px-4 py-3 flex justify-between items-center shrink-0 shadow-sm border-b border-gray-100 dark:border-gray-700 z-10 transition-colors">
          <button @click="$emit('close')" class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 no-print transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" /></svg>
          </button>
          <div class="text-center">
            <h2 class="text-[15px] font-extrabold text-gray-900 dark:text-white transition-colors">Courses du Week-end</h2>
          </div>
          <button @click="$emit('exportPdf')" class="p-2 text-[#5b2b82] dark:text-purple-400 hover:bg-violet-50 dark:hover:bg-purple-900/30 rounded-full transition-colors no-print">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" /></svg>
          </button>
        </div>

        <div class="flex-1 overflow-y-auto p-4 pb-20">
          <div class="bg-[#5b2b82] dark:bg-purple-900/60 border border-transparent dark:border-purple-800 text-white rounded-xl p-4 mb-6 shadow-md flex justify-between items-center no-print transition-colors">
            <div>
              <h3 class="font-bold">Marge de sécurité (Rab)</h3>
              <p class="text-xs text-violet-200 dark:text-purple-300 mt-0.5 transition-colors">Quantités augmentées de +10%</p>
            </div>
            <div @click="$emit('toggleRab')" :class="['w-12 h-6 rounded-full p-1 cursor-pointer transition-colors duration-300 ease-in-out', rabEnabled ? 'bg-violet-400 dark:bg-purple-500' : 'bg-violet-900 dark:bg-gray-700']">
              <div :class="['w-4 h-4 bg-white rounded-full shadow-sm transform transition-transform duration-300 ease-in-out', rabEnabled ? 'translate-x-6' : 'translate-x-0']"></div>
            </div>
          </div>

          <div v-for="(items, category) in groupedShoppingList" :key="category" class="mb-6">
            <h3 class="flex items-center gap-2 text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-3 ml-1 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
              {{ category }}
            </h3>

            <div class="space-y-2 grid grid-cols-1 md:grid-cols-2 md:gap-2 md:space-y-0">
              <label v-for="(item, index) in items" :key="index" class="rounded-xl p-3 shadow-sm border flex items-center justify-between cursor-pointer transition-all hover:border-violet-200 dark:hover:border-purple-700 group" :class="item.isChecked ? 'border-violet-200 dark:border-purple-800 bg-violet-50/30 dark:bg-purple-900/20 opacity-75' : 'bg-white dark:bg-gray-800 border-gray-100 dark:border-gray-700'">
                <div class="flex items-center gap-3">
                  <div :class="['w-5 h-5 rounded border flex items-center justify-center transition-colors', item.isChecked ? 'bg-[#5b2b82] dark:bg-purple-600 border-[#5b2b82] dark:border-purple-600' : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 group-hover:border-[#5b2b82] dark:group-hover:border-purple-500']">
                    <input type="checkbox" v-model="item.isChecked" class="hidden">
                    <svg v-if="item.isChecked" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
                  </div>
                  <span :class="['text-[15px] font-bold transition-colors', item.isChecked ? 'text-gray-500 dark:text-gray-400 line-through' : 'text-[#001D2D] dark:text-white']">
                    {{ item.name }}
                  </span>
                </div>

                <div class="font-black text-[#5b2b82] dark:text-purple-300 bg-violet-50 dark:bg-purple-900/40 px-3 py-1.5 rounded-lg text-sm border border-violet-100 dark:border-purple-800/50 transition-colors">
                  {{ item.displayQty }} <span class="text-xs font-bold">{{ item.displayUnit }}</span>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  showModal: Boolean,
  groupedShoppingList: { type: Object, default: () => ({}) },
  rabEnabled: Boolean
})

defineEmits(['close', 'exportPdf', 'toggleRab'])
</script>

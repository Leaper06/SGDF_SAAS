<template>
    <nav class="absolute bottom-0 w-full bg-white border-t border-gray-200 px-6 py-3 flex justify-between items-center z-40 rounded-b-[2rem]">
      
      <div 
        @click="currentView = 'unite'" 
        :class="['flex flex-col items-center cursor-pointer transition-colors', currentView === 'unite' ? 'text-scoutViolet font-bold' : 'text-gray-400 hover:text-gray-600']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
        </svg>
        <span class="text-[10px] mt-1">Unité</span>
      </div>

      <div 
        @click="currentView = 'calendar'" 
        :class="['flex flex-col items-center cursor-pointer transition-colors', ['calendar', 'planning', 'activity_detail', 'menu_builder', 'recipe_catalog', 'recipe_builder'].includes(currentView) ? 'text-scoutViolet font-bold' : 'text-gray-400 hover:text-gray-600']"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
        </svg>
        <span class="text-[10px] mt-1">Camps</span>
      </div>

      <div class="flex flex-col items-center text-gray-400 hover:text-gray-600 cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
        </svg>
        <span class="text-[10px] font-medium mt-1">Matériel</span>
      </div>

      <div class="flex flex-col items-center text-gray-400 hover:text-gray-600 cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <span class="text-[10px] font-medium mt-1">Profil</span>
      </div>

    </nav>
</template>

<script setup>
import { currentView } from '../store.js'
</script>
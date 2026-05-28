<template>
    <nav class="w-full md:w-24 bg-white dark:bg-gray-900 border-t md:border-t-0 md:border-r border-gray-200 dark:border-gray-800 px-6 py-3 md:py-8 flex flex-row md:flex-col justify-between md:justify-start items-center md:gap-6 transition-colors duration-300 z-50">
      
      <!-- LOGO POLYMAÎTRISE (Visible uniquement sur ordinateur en haut à gauche) -->
      <div class="hidden md:flex flex-col items-center mb-4 text-[#004267] dark:text-blue-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
      </div>

      <!-- Onglet : Unité -->
      <router-link to="/unite" class="flex flex-col items-center cursor-pointer transition-colors text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 md:w-full md:py-3 md:rounded-xl" active-class="!text-scoutViolet dark:!text-purple-300 font-bold md:bg-violet-50 md:dark:bg-purple-900/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 md:h-7 md:w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" />
        </svg>
        <span class="text-[10px] md:text-xs mt-1 md:mt-2 font-medium">Unité</span>
      </router-link>

      <!-- Onglet : Camps -->
      <router-link to="/camps" :class="['flex flex-col items-center cursor-pointer transition-colors md:w-full md:py-3 md:rounded-xl', $route.path.includes('/camps') || $route.path.includes('/planning') || $route.path.includes('/activity') || $route.path.includes('/menu') || $route.path.includes('/recipe') ? '!text-scoutViolet dark:!text-purple-300 font-bold md:bg-violet-50 md:dark:bg-purple-900/30' : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300']">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 md:h-7 md:w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
        </svg>
        <span class="text-[10px] md:text-xs mt-1 md:mt-2 font-medium">Camps</span>
      </router-link>

      <!-- Onglet : Logistique -->
      <router-link to="/logistique" :class="['flex flex-col items-center cursor-pointer transition-colors md:w-full md:py-3 md:rounded-xl', $route.path.includes('/logistique') ? '!text-scoutViolet dark:!text-purple-300 font-bold md:bg-violet-50 md:dark:bg-purple-900/30' : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300']">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 md:h-7 md:w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
        </svg>
        <span class="text-[10px] md:text-xs font-medium mt-1 md:mt-2">Logistique</span>
      </router-link>

      <!-- Onglet : Profil (md:mt-auto le pousse tout en bas sur l'ordi !) -->
      <router-link to="/profile" :class="['flex flex-col items-center cursor-pointer transition-colors md:w-full md:py-3 md:rounded-xl md:mt-auto', $route.path.includes('/profile') ? '!text-scoutViolet dark:!text-purple-300 font-bold md:bg-violet-50 md:dark:bg-purple-900/30' : 'text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300']">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 md:h-7 md:w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
        </svg>
        <span class="text-[10px] md:text-xs font-medium mt-1 md:mt-2">Profil</span>
      </router-link>

    </nav>
</template>

<script setup>

</script>
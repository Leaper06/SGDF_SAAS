<template>
    <div class="flex flex-col h-full bg-gray-50 dark:bg-gray-900 relative transition-colors duration-300">
        
        <!-- HEADER UNITÉ -->
        <div class="bg-[#004267] dark:bg-gray-800 text-white pt-5 pb-4 px-6 rounded-b-[30px] shadow-lg z-30 flex-none relative shrink-0 transition-colors">
            <div class="flex justify-between items-center mb-3">
                <h1 class="text-xl font-bold tracking-wide">PolyMaîtrise</h1>
                <button @click="logout" class="text-xs bg-white/20 hover:bg-white/30 active:scale-95 px-3 py-1.5 rounded-lg transition-all font-medium flex items-center gap-1.5 border border-white/10">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                    <span>Déconnexion</span>
                </button>
            </div>
            
            <!-- SUB-NAV TABS UNITÉ -->
            <div class="flex gap-2 justify-center mt-2">
                <button 
                    @click="activeSubTab = 'membres'"
                    :class="['px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2', activeSubTab === 'membres' ? 'bg-white text-[#004267] shadow-md' : 'bg-[#003B5C] text-blue-100 hover:bg-[#003B5C]/80']"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                    <span>Membres ({{ jeunes.length + chefs.length }})</span>
                </button>

                <button 
                    @click="activeSubTab = 'equipages'"
                    :class="['px-4 py-2 rounded-xl text-xs font-extrabold transition-all flex items-center gap-2', activeSubTab === 'equipages' ? 'bg-white text-[#004267] shadow-md' : 'bg-[#003B5C] text-blue-100 hover:bg-[#003B5C]/80']"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                    <span>{{ nomRoleSelonBranche.unite }} ({{ equipages.length }})</span>
                </button>
            </div>
        </div>

        <!-- BANDEAU PREMIÈRE CONNEXION -->
        <div v-if="needsIdentification" class="bg-orange-50 dark:bg-orange-900/20 border-b border-orange-200 dark:border-orange-900/50 p-5 z-20 transition-colors">
            <h2 class="text-[#e85d22] dark:text-orange-400 font-black text-lg mb-2 transition-colors">Bienvenue À toi ! </h2>
            <p class="text-sm text-orange-800 dark:text-orange-300 font-medium mb-4 transition-colors">
                C'est ta première connexion. Pour que l'application fonctionne parfaitement, clique sur ton profil dans la liste des chefs ci-dessous :
            </p>
            <div class="grid grid-cols-1 gap-2">
                <button 
                    v-for="chef in chefs" 
                    :key="chef.id"
                    @click="confirmerIdentite(chef)"
                    class="bg-white dark:bg-gray-800 border border-orange-200 dark:border-orange-900/50 p-3 rounded-xl shadow-sm flex items-center justify-between hover:bg-orange-100 dark:hover:bg-orange-900/40 transition-colors"
                >
                    <span class="font-bold text-gray-800 dark:text-white transition-colors">{{ chef.prenom }} {{ chef.nom }}</span>
                    <span class="text-xs font-bold text-orange-500 dark:text-orange-400 bg-orange-100 dark:bg-orange-900/40 px-2 py-1 rounded transition-colors">C'est moi !</span>
                </button>
            </div>
        </div>

        <!-- SPINNER CHARGEMENT -->
        <div v-if="isLoadingAdherents" class="flex-1 flex flex-col items-center justify-center space-y-4">
            <svg class="animate-spin h-8 w-8 text-[#004267] dark:text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            <p class="text-sm font-bold text-gray-500 dark:text-gray-400 animate-pulse transition-colors">Récupération depuis l'intranet...</p>
        </div>

        <!-- CONTENU DE L'ONGLET UNITÉ -->
        <div v-else class="flex-1 overflow-y-auto p-4 pb-28 space-y-6">
            
            <!-- VUE 1 : REGISTRE DES MEMBRES -->
            <template v-if="activeSubTab === 'membres'">
                <!-- SECTION JEUNES -->
                <div>
                    <div class="flex items-center justify-between mb-3 ml-1 mr-1">
                        <h3 :class="[branchStyles.text, 'flex items-center gap-2 text-xs font-bold uppercase tracking-wider transition-colors']">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                            {{ unitName }} ({{ jeunes.length }})
                        </h3>
                        <button 
                            @click="syncAdherents()" 
                            :disabled="isSyncing"
                            class="flex items-center gap-1.5 text-xs font-semibold text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-all bg-gray-200/80 hover:bg-gray-300/80 dark:bg-gray-800 dark:hover:bg-gray-700 px-2.5 py-1 rounded-full border border-gray-300/60 dark:border-gray-700 shadow-sm cursor-pointer disabled:opacity-50"
                        >
                            <svg v-if="isSyncing" class="animate-spin h-3.5 w-3.5 text-blue-600 dark:text-blue-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                            <span>{{ isSyncing ? 'Synchro...' : 'Resynchroniser' }}</span>
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                        <div v-for="membre in jeunes" :key="membre.id" @click="ouvrirFiche(membre)" :class="['bg-white dark:bg-gray-800 rounded-2xl p-3 shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-4 cursor-pointer transition-colors', branchStyles.borderHover]">                        
                            <div class="w-12 h-12 rounded-full overflow-hidden bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center shrink-0 border-2 border-white dark:border-gray-800 shadow-sm transition-colors">
                                <img v-if="membre.photo" :src="membre.photo" class="w-full h-full object-cover">
                                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-[50%] w-[50%] opacity-50 text-gray-400 dark:text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                                </svg>
                            </div>
                            <div class="flex-1 min-w-0">
                                <h4 class="font-bold text-gray-900 dark:text-white truncate text-[15px] transition-colors">{{ membre.prenom }} {{ membre.nom }}</h4>
                                <div class="flex items-center gap-2 mt-1">
                                    <span v-if="membre.hasFiche" class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 transition-colors">Fiche Sanitaire</span>
                                    <span v-else class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-red-50 dark:bg-red-900/30 text-red-500 dark:text-red-400 transition-colors">Fiche Manquante</span>
                                    <span v-if="getEquipageJeune(membre.id)" class="text-[9px] font-bold px-2 py-0.5 rounded uppercase tracking-wider bg-blue-50 dark:bg-blue-900/30 text-[#004267] dark:text-blue-300">
                                        {{ getEquipageJeune(membre.id).name }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SECTION MAÎTRISE (CHEFS) -->
                <div class="pt-4">
                    <h3 class="flex items-center gap-2 text-xs font-bold text-[#5b2b82] dark:text-purple-400 uppercase tracking-wider mb-3 ml-1 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M12 14l9-5-9-5-9 5 9 5z" /><path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" /></svg>
                        La Maîtrise ({{ chefs.length }})
                    </h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div v-for="membre in chefs" :key="membre.id" @click="ouvrirFiche(membre)" class="bg-white dark:bg-gray-800 rounded-2xl p-3 shadow-sm border border-gray-100 dark:border-gray-700 flex items-center gap-4 cursor-pointer hover:border-violet-200 dark:hover:border-purple-500/50 transition-colors">
                            <div class="w-12 h-12 rounded-full overflow-hidden bg-violet-100 dark:bg-purple-900/30 flex items-center justify-center shrink-0 border-2 border-white dark:border-gray-800 shadow-sm transition-colors">
                                <img v-if="membre.photo" :src="membre.photo" class="w-full h-full object-cover">
                                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-[50%] w-[50%] opacity-50 text-gray-400 dark:text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                                </svg>
                            </div>
                            <div class="flex-1 min-w-0">
                                <h4 class="font-bold text-gray-900 dark:text-white truncate text-[15px] transition-colors">{{ membre.prenom }} {{ membre.nom }}</h4>
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <!-- VUE 2 : GESTION DES ÉQUIPAGES & SIXAINES -->
            <template v-else-if="activeSubTab === 'equipages'">
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-4 bg-white dark:bg-gray-800 p-5 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-xs">
                    <div>
                        <h3 class="text-lg font-black text-gray-900 dark:text-white">Gestion des {{ nomRoleSelonBranche.unite }}</h3>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5 font-medium">
                            {{ jeunesAffectesCount }} / {{ jeunes.length }} jeunes affectés dans {{ equipages.length }} {{ nomRoleSelonBranche.unite.toLowerCase() }}
                        </p>
                    </div>

                    <button 
                        @click="showCreateEquipageModal = true"
                        class="bg-[#e85d22] hover:bg-orange-600 text-white font-bold text-xs px-4 py-2.5 rounded-xl transition-all shadow-md flex items-center gap-1.5"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
                        <span>Créer un {{ nomRoleSelonBranche.single.toLowerCase() }}</span>
                    </button>
                </div>

                <!-- CARTE DES ÉQUIPAGES -->
                <div v-if="equipages.length === 0" class="text-center py-12 bg-white dark:bg-gray-800 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700">
                    <p class="text-gray-500 dark:text-gray-400 font-medium">Aucun {{ nomRoleSelonBranche.single.toLowerCase() }} créé.</p>
                    <button @click="showCreateEquipageModal = true" class="mt-3 px-4 py-2 bg-[#004267] text-white text-xs font-bold rounded-xl">
                        + Créer le 1er {{ nomRoleSelonBranche.single.toLowerCase() }}
                    </button>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div 
                        v-for="eq in equipages" 
                        :key="eq.id"
                        class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm overflow-hidden flex flex-col justify-between"
                    >
                        <!-- Bannière Équipage -->
                        <div class="p-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50/70 dark:bg-gray-900/40">
                            <div class="flex items-center gap-2">
                                <span class="w-3.5 h-3.5 rounded-full border border-white shadow-xs inline-block" :style="{ backgroundColor: eq.color || '#004267' }"></span>
                                <h4 class="font-extrabold text-base text-gray-900 dark:text-white">{{ eq.name }}</h4>
                            </div>
                            
                            <div class="flex items-center gap-2">
                                <span class="text-xs font-extrabold text-gray-400 px-2 py-0.5 rounded-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                                    {{ eq.member_ids?.length || 0 }} jeune(s)
                                </span>
                                <button @click="supprimerEquipage(eq.id)" class="text-gray-400 hover:text-red-500 p-1 text-xs">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                </button>
                            </div>
                        </div>

                        <!-- Membres de l'Équipage -->
                        <div class="p-4 space-y-3 flex-1">
                            <!-- Pilote / Sixainier -->
                            <div class="p-3 bg-purple-50/70 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800/40 rounded-xl flex items-center justify-between">
                                <div class="flex items-center gap-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-purple-600 dark:text-purple-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" /></svg>
                                    <span class="text-xs font-black text-purple-800 dark:text-purple-300 uppercase tracking-wider">{{ nomRoleSelonBranche.pilote }} :</span>
                                    <span v-if="getJeuneById(eq.pilote_id)" class="text-xs font-extrabold text-gray-900 dark:text-white">
                                        {{ getJeuneById(eq.pilote_id).prenom }} {{ getJeuneById(eq.pilote_id).nom }}
                                    </span>
                                    <span v-else class="text-xs text-purple-400 italic">Non désigné</span>
                                </div>
                                <select 
                                    :value="eq.pilote_id || ''"
                                    @change="e => setPiloteEquipage(eq.id, e.target.value)"
                                    class="text-[11px] font-semibold bg-white dark:bg-gray-800 border border-purple-200 dark:border-purple-700 rounded-lg px-2 py-1 text-purple-900 dark:text-purple-200 focus:outline-none"
                                >
                                    <option value="">-- Choisir --</option>
                                    <option v-for="j in getMembresEquipage(eq)" :key="j.id" :value="j.id">
                                        {{ j.prenom }} {{ j.nom }}
                                    </option>
                                </select>
                            </div>

                            <!-- Liste de tous les jeunes de l'équipage -->
                            <div class="space-y-1.5 pt-1">
                                <div 
                                    v-for="j in getMembresEquipage(eq)" 
                                    :key="j.id" 
                                    class="p-2 bg-gray-50 dark:bg-gray-900/50 rounded-xl flex items-center justify-between border border-gray-100 dark:border-gray-700/60"
                                >
                                    <span class="text-xs font-bold text-gray-800 dark:text-gray-200">{{ j.prenom }} {{ j.nom }}</span>
                                    <button @click="retirerJeuneDuneEquipage(j.id)" class="text-gray-400 hover:text-red-500 font-black text-xs px-2 py-0.5">
                                        ✕
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- Dropdown pour ajouter un jeune -->
                        <div class="p-3 bg-gray-50 dark:bg-gray-900/50 border-t border-gray-100 dark:border-gray-700">
                            <select 
                                @change="e => { if (e.target.value) { affecterJeuneAEquipage(e.target.value, eq.id); e.target.value = ''; } }"
                                class="w-full text-xs font-bold bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 text-gray-700 dark:text-gray-200 focus:outline-none"
                            >
                                <option value="">+ Ajouter un jeune à cet équipage...</option>
                                <option v-for="j in jeunes" :key="j.id" :value="j.id">
                                    {{ j.prenom }} {{ j.nom }} {{ getEquipageJeune(j.id) ? '(' + getEquipageJeune(j.id).name + ')' : '' }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- SECTION JEUNES NON AFFECTÉS -->
                <div v-if="jeunesNonAffectes.length > 0" class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
                    <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Jeunes non affectés ({{ jeunesNonAffectes.length }})</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                        <div v-for="j in jeunesNonAffectes" :key="j.id" class="p-3 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 flex justify-between items-center">
                            <span class="text-xs font-bold text-gray-800 dark:text-white">{{ j.prenom }} {{ j.nom }}</span>
                            <select 
                                @change="e => { if (e.target.value) affecterJeuneAEquipage(j.id, e.target.value) }"
                                class="text-[11px] font-bold bg-blue-50 dark:bg-blue-900/30 text-[#004267] dark:text-blue-300 border border-blue-200 dark:border-blue-800 rounded-lg px-2 py-1"
                            >
                                <option value="">Affecter à...</option>
                                <option v-for="eq in equipages" :key="eq.id" :value="eq.id">{{ eq.name }}</option>
                            </select>
                        </div>
                    </div>
                </div>
            </template>

        </div>

        <!-- MODALE DE FICHE MEMBRE COMPLÈTE -->
        <transition enter-active-class="transition-all duration-300 ease-out" enter-from-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95" enter-to-class="opacity-100 translate-y-0 md:scale-100" leave-active-class="transition-all duration-200 ease-in" leave-from-class="opacity-100 translate-y-0 md:scale-100" leave-to-class="opacity-0 translate-y-full md:translate-y-10 md:scale-95">
            
            <div v-if="selectedMember" class="fixed inset-0 z-50 flex flex-col justify-end md:justify-center md:items-center md:p-6">
                <div class="absolute inset-0 bg-gray-900/60 dark:bg-black/60 backdrop-blur-sm transition-opacity" @click="fermerFiche"></div>
                
                <div class="relative bg-white dark:bg-gray-800 w-full md:max-w-2xl rounded-t-3xl md:rounded-3xl shadow-2xl flex flex-col z-10 overflow-hidden pb-8 md:pb-0 transition-colors max-h-[90vh]">
                    
                    <div :class="['h-24 w-full relative shrink-0 transition-colors', selectedMember.isJeune ? branchStyles.bg : 'bg-[#5b2b82] dark:bg-purple-900/60']">
                        <div class="absolute -bottom-10 left-6 w-24 h-24 rounded-full overflow-hidden bg-white dark:bg-gray-800 border-4 border-white dark:border-gray-800 shadow-lg flex items-center justify-center cursor-pointer transition-colors" @click="triggerPhoto">
                            <img v-if="selectedMember.photo" :src="selectedMember.photo" class="w-full h-full object-cover">
                            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-[50%] w-[50%] opacity-50 text-gray-400 dark:text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <button @click="fermerFiche" class="absolute top-4 right-4 bg-black/20 hover:bg-black/30 p-2 rounded-full text-white transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>

                    <div class="px-6 pt-14 pb-6 space-y-6 flex-1 overflow-y-auto scrollbar-hide">
                        <div>
                            <h2 class="text-2xl font-black text-gray-900 dark:text-white transition-colors">{{ selectedMember.prenom }} <span class="uppercase">{{ selectedMember.nom }}</span></h2>
                            <p class="text-sm font-bold text-gray-400 dark:text-gray-500 mt-0.5 transition-colors">N° {{ selectedMember.id }}</p>
                        </div>

                        <!-- SECTION AFFECTATION ÉQUIPAGE DANS LA FICHE -->
                        <div v-if="selectedMember.isJeune" class="space-y-2">
                            <h3 class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider">{{ nomRoleSelonBranche.single }}</h3>
                            <div class="p-3 bg-blue-50/70 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 rounded-xl flex items-center justify-between">
                                <span class="text-xs font-bold text-gray-800 dark:text-white">
                                    {{ getEquipageJeune(selectedMember.id) ? getEquipageJeune(selectedMember.id).name : 'Aucun équipage' }}
                                </span>
                                <select 
                                    :value="getEquipageJeune(selectedMember.id) ? getEquipageJeune(selectedMember.id).id : ''"
                                    @change="e => { if (e.target.value) affecterJeuneAEquipage(selectedMember.id, e.target.value); else retirerJeuneDuneEquipage(selectedMember.id); }"
                                    class="text-xs font-semibold bg-white dark:bg-gray-800 border border-blue-200 dark:border-blue-700 rounded-lg px-2 py-1 text-[#004267] dark:text-blue-200 focus:outline-none"
                                >
                                    <option value="">Aucun</option>
                                    <option v-for="eq in equipages" :key="eq.id" :value="eq.id">{{ eq.name }}</option>
                                </select>
                            </div>
                        </div>

                        <div class="space-y-3">
                            <div class="space-y-3">
                                <h3 class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider transition-colors">Documents</h3>
                                
                                <div class="bg-gray-50 dark:bg-gray-900/50 border border-gray-100 dark:border-gray-700 rounded-xl p-4 flex flex-col gap-4 transition-colors">
                                    <div class="flex items-center gap-3">
                                        <div :class="['w-10 h-10 rounded-full flex items-center justify-center shrink-0 transition-colors', selectedMember.ficheUrl ? 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/30 text-red-500 dark:text-red-400']">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                            </svg>
                                        </div>
                                        <div>
                                            <p class="text-sm font-bold text-gray-900 dark:text-white transition-colors">Fiche Sanitaire</p>
                                            <p :class="['text-xs font-semibold mt-0.5 transition-colors', selectedMember.ficheUrl ? 'text-green-600 dark:text-green-400' : 'text-red-500 dark:text-red-400']">
                                                {{ selectedMember.ficheUrl ? 'À jour et stockée' : 'Document manquant' }}
                                            </p>
                                        </div>
                                    </div>
                                    
                                    <div :class="['p-3 rounded-xl border flex items-start gap-3 transition-colors', branchStyles.lightBg, branchStyles.lightBorder]">
                                        <input 
                                            v-model="rgpdAccepte" 
                                            type="checkbox" 
                                            id="rgpd-consent"
                                            class="mt-0.5 h-4 w-4 rounded border-gray-300 text-[#004267] dark:text-blue-500 focus:ring-[#004267]/20 dark:focus:ring-blue-500/30 transition-colors cursor-pointer"
                                        >
                                        <label for="rgpd-consent" class="text-[11px] font-semibold text-gray-600 dark:text-gray-400 leading-tight cursor-pointer select-none">
                                            Je confirme avoir l'autorité parentale et j'accepte que les données de santé de cet enfant soient traitées pour le camp, conformément aux <router-link to="/mentions-legales" class="underline font-bold" :class="branchStyles.text">Mentions Légales</router-link>.
                                        </label>
                                    </div>
                                    <div class="flex gap-2">
                                        <button v-if="selectedMember.ficheUrl" @click="consulterFiche" class="flex-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 text-xs font-bold py-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors shadow-sm">
                                            Consulter
                                        </button>
                                        
                                        <button 
                                        @click="triggerFiche" 
                                        :disabled="!rgpdAccepte"
                                        :class="[
                                            'flex-1 text-xs font-bold py-2.5 rounded-lg transition-colors shadow-sm', 
                                            !rgpdAccepte ? 'bg-gray-200 text-gray-400 dark:bg-gray-700 dark:text-gray-500 cursor-not-allowed' : 
                                            (selectedMember.ficheUrl ? 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700' : 'bg-[#004267] dark:bg-blue-600 text-white hover:bg-blue-900 dark:hover:bg-blue-700')
                                        ]"
                                        >
                                            {{ selectedMember.ficheUrl ? 'Remplacer' : 'Importer (PDF / IMG)' }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- PROGRESSION PERSONNELLE -->
                            <div class="space-y-3 pt-2">
                                <h3 class="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider transition-colors">Progression Personnelle</h3>
                                
                                <div :class="['border rounded-xl p-4 space-y-3 transition-colors', branchStyles.lightBg, branchStyles.lightBorder]">
                                    <div>
                                        <label :class="['block text-[10px] font-bold uppercase tracking-wider mb-1 transition-colors', branchStyles.text]">Étape / Insigne (Atout, Cap...)</label>
                                        <input 
                                            v-model="selectedMember.progressionSymbole"
                                            @blur="sauvegarderProgression"
                                            type="text"
                                            placeholder="Ex: Atout de la Rencontre"
                                            :class="['w-full bg-white dark:bg-gray-900 border text-gray-900 dark:text-white font-medium rounded-lg px-3 py-2 text-sm focus:outline-none transition-colors placeholder-gray-400 dark:placeholder-gray-600', branchStyles.lightBorder, branchStyles.focusBorder]"
                                        >
                                    </div>
                                    <div>
                                        <label :class="['block text-[10px] font-bold uppercase tracking-wider mb-1 transition-colors', branchStyles.text]">Défi / Action à réaliser</label>
                                        <textarea 
                                            v-model="selectedMember.progressionAction"
                                            @blur="sauvegarderProgression"
                                            rows="2"
                                            placeholder="Ex: Organiser un grand jeu..."
                                            :class="['w-full bg-white dark:bg-gray-900 border text-gray-900 dark:text-white font-medium rounded-lg px-3 py-2 text-sm focus:outline-none transition-colors resize-none placeholder-gray-400 dark:placeholder-gray-600', branchStyles.lightBorder, branchStyles.focusBorder]"
                                        ></textarea>
                                    </div>
                                    
                                    <div v-if="isSavingProgression" class="flex justify-end">
                                        <span class="text-[10px] font-bold text-green-500 animate-pulse">Sauvegarde...</span>
                                    </div>
                                </div>
                            </div>

                            <input type="file" id="ficheInput" accept="image/png, image/jpeg, application/pdf" ref="ficheInput" @change="handleFicheUpload" class="hidden">
                            <input type="file" id="photoInput" accept="image/*" ref="photoInput" @change="handlePhotoUpload" class="hidden">

                        </div>
                    </div>
                </div>
            </div>
        </transition>

        <!-- MODALE CRÉATION D'ÉQUIPAGE -->
        <div 
            v-if="showCreateEquipageModal" 
            @click="showCreateEquipageModal = false"
            class="fixed inset-0 bg-black/40 dark:bg-black/60 backdrop-blur-sm flex justify-center items-end sm:items-center z-50 p-0 sm:p-4 transition-colors"
        >
            <div 
                @click.stop
                class="bg-white dark:bg-gray-800 rounded-t-[30px] sm:rounded-3xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh] shadow-2xl transition-colors"
            >
                <div class="p-6 overflow-y-auto">
                    <div class="w-12 h-1 bg-gray-200 dark:bg-gray-700 rounded-full mx-auto mb-6"></div>

                    <div class="flex justify-between items-center mb-5">
                        <h3 class="text-xl font-black text-gray-900 dark:text-white">Créer un {{ nomRoleSelonBranche.single.toLowerCase() }}</h3>
                        <button @click="showCreateEquipageModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                            ✕
                        </button>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Nom du {{ nomRoleSelonBranche.single.toLowerCase() }}</label>
                            <input v-model="nouveauNomEquipage" type="text" placeholder="Ex: Équipage des Lynx ou Sixaine des Loups Blancs" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30">
                        </div>

                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Couleur du {{ nomRoleSelonBranche.single.toLowerCase() }}</label>
                            <div class="flex gap-2">
                                <button v-for="c in ['#004267', '#e85d22', '#059669', '#7c3aed', '#dc2626', '#d97706']" :key="c" @click="nouvelleCouleurEquipage = c" :class="['w-8 h-8 rounded-full border-2 transition-transform', nouvelleCouleurEquipage === c ? 'scale-110 border-gray-900 dark:border-white' : 'border-transparent']" :style="{ backgroundColor: c }"></button>
                            </div>
                        </div>

                        <div class="pt-4">
                            <button @click="validerCreationEquipage" class="w-full py-3.5 bg-[#e85d22] hover:bg-orange-600 text-white rounded-xl font-bold text-sm shadow-md transition-colors">
                                Enregistrer le {{ nomRoleSelonBranche.single.toLowerCase() }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <IntranetLoginModal />
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
    adherentsList, isLoadingAdherents, jeunes, chefs, fetchAdherents, isSyncing, syncAdherents,
    equipages, showCreateEquipageModal, initEquipages, creerEquipage, supprimerEquipage,
    affecterJeuneAEquipage, retirerJeuneDuneEquipage, nomRoleSelonBranche
} from '../stores/adherentsStore.js'
import { 
    userToken, loginToSGDF, isLoggingIn, loginError, userEmail, 
    needsIdentification, chefAdherentId, unitName, groupName, chefBranch, logout 
} from '../stores/authStore.js'
import { API_BASE_URL } from '../api/config.js'
import IntranetLoginModal from './IntranetLoginModal.vue'

const activeSubTab = ref('membres')
const selectedMember = ref(null)
const photoInput = ref(null)
const ficheInput = ref(null)
const rgpdAccepte = ref(false)
const isSavingProgression = ref(false)

const nouveauNomEquipage = ref('')
const nouvelleCouleurEquipage = ref('#004267')

const validerCreationEquipage = () => {
    if (!nouveauNomEquipage.value.trim()) return alert("Veuillez saisir un nom pour l'équipage.")
    creerEquipage({ name: nouveauNomEquipage.value.trim(), color: nouvelleCouleurEquipage.value })
    nouveauNomEquipage.value = ''
    showCreateEquipageModal.value = false
}

const jeunesAffectesCount = computed(() => {
    const set = new Set()
    equipages.value.forEach(e => {
        if (e.member_ids) e.member_ids.forEach(id => set.add(id))
    })
    return set.size
})

const jeunesNonAffectes = computed(() => {
    const affectes = new Set()
    equipages.value.forEach(e => {
        if (e.member_ids) e.member_ids.forEach(id => affectes.add(id))
    })
    return jeunes.value.filter(j => !affectes.has(j.id))
})

const getEquipageJeune = (jeuneId) => {
    return equipages.value.find(e => e.member_ids && e.member_ids.includes(jeuneId))
}

const getMembresEquipage = (eq) => {
    if (!eq.member_ids) return []
    return jeunes.value.filter(j => eq.member_ids.includes(j.id))
}

const getJeuneById = (jeuneId) => {
    if (!jeuneId) return null
    return jeunes.value.find(j => j.id === jeuneId)
}

const setPiloteEquipage = (equipageId, jeuneId) => {
    if (!jeuneId) return
    affecterJeuneAEquipage(jeuneId, equipageId, 'pilote')
}

const branchStyles = computed(() => {
    const branch = chefBranch.value || 'SG'
    if (branch === 'Louja') {
        return {
            text: 'text-orange-600 dark:text-orange-400',
            bg: 'bg-orange-500',
            lightBg: 'bg-orange-50 dark:bg-orange-950/30',
            lightBorder: 'border-orange-200 dark:border-orange-900/50',
            borderHover: 'hover:border-orange-400 dark:hover:border-orange-500',
            focusBorder: 'focus:border-orange-500'
        }
    }
    return {
        text: 'text-blue-700 dark:text-blue-400',
        bg: 'bg-[#004267]',
        lightBg: 'bg-blue-50 dark:bg-blue-950/30',
        lightBorder: 'border-blue-200 dark:border-blue-900/50',
        borderHover: 'hover:border-blue-400 dark:hover:border-blue-500',
        focusBorder: 'focus:border-blue-500'
    }
})

const ouvrirFiche = (membre) => {
    selectedMember.value = { ...membre }
    rgpdAccepte.value = !!membre.ficheUrl
}

const fermerFiche = () => {
    selectedMember.value = null
    rgpdAccepte.value = false
}

const triggerPhoto = () => {
    if (photoInput.value) photoInput.value.click()
}

const triggerFiche = () => {
    if (ficheInput.value) ficheInput.value.click()
}

const handleFicheUpload = async (event) => {
    const file = event.target.files[0]
    if (!file || !selectedMember.value) return
    const formData = new FormData()
    formData.append('file', file)
    try {
        const response = await fetch(`${API_BASE_URL}/adherents/${selectedMember.value.id}/upload`, {
            method: 'POST',
            body: formData
        })
        const json = await response.json()
        if (json.status === 'success') {
            selectedMember.value.ficheUrl = json.url
            selectedMember.value.hasFiche = true
            const index = adherentsList.value.findIndex(m => m.id === selectedMember.value.id)
            if (index !== -1) {
                adherentsList.value[index].ficheUrl = json.url
                adherentsList.value[index].hasFiche = true
            }
        }
    } catch (e) {
        console.error("Erreur upload fiche :", e)
    }
}

const handlePhotoUpload = async (event) => {
    const file = event.target.files[0]
    if (!file || !selectedMember.value) return
    const reader = new FileReader()
    reader.onload = (e) => {
        selectedMember.value.photo = e.target.result
        const index = adherentsList.value.findIndex(m => m.id === selectedMember.value.id)
        if (index !== -1) {
            adherentsList.value[index].photo = e.target.result
        }
    }
    reader.readAsDataURL(file)
}

const sauvegarderProgression = async () => {
    if (!selectedMember.value) return
    isSavingProgression.value = true
    try {
        await fetch(`${API_BASE_URL}/adherents/${selectedMember.value.id}/progression`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                progression_symbole: selectedMember.value.progressionSymbole,
                progression_action: selectedMember.value.progressionAction
            })
        })
        const index = adherentsList.value.findIndex(m => m.id === selectedMember.value.id)
        if (index !== -1) {
            adherentsList.value[index].progressionSymbole = selectedMember.value.progressionSymbole
            adherentsList.value[index].progressionAction = selectedMember.value.progressionAction
        }
    } catch (e) {
        console.error("Erreur sauvegarde progression :", e)
    } finally {
        isSavingProgression.value = false
    }
}

const confirmerIdentite = (chef) => {
    chefAdherentId.value = chef.id
    localStorage.setItem('sgdf_chef_id', chef.id)
}

onMounted(() => {
    fetchAdherents()
    initEquipages()
})
</script>
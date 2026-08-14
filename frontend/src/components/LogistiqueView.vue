<template>
    <div class="h-full flex flex-col bg-gray-50 dark:bg-gray-900 transition-colors duration-300 relative">
        
        <!-- HEADER LOGISTIQUE -->
        <div class="bg-[#004267] dark:bg-gray-800 px-6 pt-8 pb-4 shrink-0 rounded-b-[30px] shadow-md z-10 transition-colors">
            <div class="flex justify-between items-center mb-5">
                <h2 class="text-2xl font-black text-white tracking-wider transition-colors">Logistique</h2>
                
                <!-- Bouton rapide d'ajout dynamique selon l'onglet -->
                <button 
                    v-if="activeTab === 'tentes'" 
                    @click="ouvrirAjoutTente" 
                    class="bg-[#e85d22] hover:bg-orange-600 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all shadow-md flex items-center gap-1.5 cursor-pointer"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
                    <span>Ajouter une tente</span>
                </button>
                <button 
                    v-else-if="activeTab === 'lieux'" 
                    @click="ouvrirAjoutLieu" 
                    class="bg-[#e85d22] hover:bg-orange-600 text-white font-bold text-xs px-4 py-2 rounded-xl transition-all shadow-md flex items-center gap-1.5 cursor-pointer"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
                    <span>Ajouter un lieu</span>
                </button>
            </div>
            
            <!-- ONGLETS LOGISTIQUE -->
            <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                
                <!-- Onglet Lieux de Camp -->
                <button 
                    @click="activeTab = 'lieux'" 
                    :class="['flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap transition-colors', activeTab === 'lieux' ? 'bg-white dark:bg-gray-700 text-[#004267] dark:text-blue-300 shadow-sm' : 'bg-[#003B5C] dark:bg-gray-900 text-blue-100 dark:text-gray-400 hover:bg-[#003B5C]/80 dark:hover:bg-gray-900/80']"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span>Lieux de camp</span>
                </button>
                <!-- Onglet Tentes -->
                <button 
                    @click="activeTab = 'tentes'" 
                    :class="['flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap transition-colors', activeTab === 'tentes' ? 'bg-white dark:bg-gray-700 text-[#004267] dark:text-blue-300 shadow-sm' : 'bg-[#003B5C] dark:bg-gray-900 text-blue-100 dark:text-gray-400 hover:bg-[#003B5C]/80 dark:hover:bg-gray-900/80']"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M3 21h18M3 10l9-7 9 7v11H3V10z" />
                    </svg>
                    <span>Parc de Tentes</span>
                    <span class="ml-1 text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-blue-100 dark:bg-blue-900/50 text-[#004267] dark:text-blue-300">{{ allTents.length }}</span>
                </button>

            </div>
        </div>

        <div class="flex-1 overflow-y-auto p-4 md:p-6 pb-28">
            
            <!-- 1. ONGLET PARC DE TENTES -->
            <div v-if="activeTab === 'tentes'" class="space-y-6">
                <!-- En-tête statistiques -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white dark:bg-gray-800 p-5 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-xs transition-colors">
                    <div>
                        <h3 class="text-lg font-extrabold text-gray-900 dark:text-white transition-colors">Inventaire du Parc de Tentes</h3>
                        <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mt-0.5 transition-colors">
                            Capacité totale : <strong class="text-purple-700 dark:text-purple-300 font-extrabold">{{ capaciteTotaleTentes }} places</strong> d'hébergement
                        </p>
                    </div>

                    <div class="flex items-center gap-3">
                        <div class="flex items-center gap-1.5 px-3 py-1.5 bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-xl text-xs font-bold border border-green-200 dark:border-green-800/40">
                            <span class="w-2 h-2 rounded-full bg-green-500"></span>
                            <span>{{ tentesOperationnelles.length }} prête(s)</span>
                        </div>
                        <div class="flex items-center gap-1.5 px-3 py-1.5 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-xl text-xs font-bold border border-red-200 dark:border-red-800/40">
                            <span class="w-2 h-2 rounded-full bg-red-500"></span>
                            <span>{{ damagedTents.length }} à réparer</span>
                        </div>
                    </div>
                </div>

                <!-- GRILLE DE TOUTES LES TENTES -->
                <div v-if="allTents.length === 0" class="text-center py-12 bg-white dark:bg-gray-800 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700 transition-colors">
                    <p class="text-gray-500 dark:text-gray-400 font-medium">Aucune tente enregistrée dans le parc.</p>
                    <button @click="ouvrirAjoutTente" class="mt-3 px-4 py-2 bg-[#004267] text-white text-xs font-bold rounded-xl hover:bg-[#003B5C]">
                        + Enregistrer une 1ère tente
                    </button>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    <div 
                        v-for="tente in allTents" 
                        :key="tente.id" 
                        class="bg-white dark:bg-gray-800 rounded-2xl p-5 border border-gray-100 dark:border-gray-700 shadow-sm relative overflow-hidden transition-all flex flex-col justify-between"
                    >
                        <div :class="['absolute left-0 top-0 bottom-0 w-1.5', tente.status === 'abimee' ? 'bg-red-500' : 'bg-green-500']"></div>
                        
                        <div>
                            <div class="flex justify-between items-start mb-2 pl-2">
                                <h4 class="font-extrabold text-gray-900 dark:text-white text-base transition-colors">{{ tente.name }}</h4>
                                <span :class="['text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-md border', tente.status === 'abimee' ? 'bg-red-50 text-red-600 border-red-200 dark:bg-red-900/30 dark:text-red-300 dark:border-red-800' : 'bg-green-50 text-green-600 border-green-200 dark:bg-green-900/30 dark:text-green-300 dark:border-green-800']">
                                    {{ tente.status === 'abimee' ? 'À réparer' : 'Opérationnelle' }}
                                </span>
                            </div>
                            
                            <p class="text-xs font-semibold text-gray-500 dark:text-gray-400 pl-2 mb-3">
                                Capacité : <strong class="text-gray-900 dark:text-white">{{ tente.capacity }} personnes</strong>
                            </p>

                            <div v-if="tente.status === 'abimee' && tente.notes_incident" class="bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 text-xs font-medium p-3 rounded-xl ml-2 mb-3">
                                <span class="uppercase text-[9px] font-black tracking-wider block mb-0.5 opacity-70">Incident déclaré</span>
                                "{{ tente.notes_incident }}"
                            </div>
                        </div>

                        <div class="pt-2 border-t border-gray-100 dark:border-gray-700/60 ml-2 flex justify-between items-center">
                            <button 
                                v-if="tente.status === 'abimee'" 
                                @click="marquerReparee(tente.id)" 
                                class="text-xs font-bold text-green-600 dark:text-green-400 hover:underline flex items-center gap-1"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" /></svg>
                                <span>Marquer réparée</span>
                            </button>
                            <button 
                                v-else 
                                @click="ouvrirDeclarationIncident(tente)" 
                                class="text-xs font-bold text-red-500 dark:text-red-400 hover:underline flex items-center gap-1"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                                <span>Signaler incident</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 2. ONGLET LIEUX DE CAMP -->
            <div v-if="activeTab === 'lieux'" class="space-y-4 flex flex-col h-full">    
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-2">
                    <div>
                        <h3 class="text-lg font-extrabold text-gray-900 dark:text-white transition-colors">Carnet d'adresses</h3>
                        <p class="text-xs font-medium text-gray-500 dark:text-gray-400 mt-0.5 transition-colors">Lieux de camp enregistrés et partagés au réseau</p>
                    </div>

                    <div class="flex items-center gap-3 w-full sm:w-auto">
                        <div class="relative flex-1 sm:w-64">
                            <input 
                                v-model="rechercheLieu" 
                                type="text" 
                                placeholder="Rechercher un lieu, ville..." 
                                class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl px-3 py-2 text-xs font-medium text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30"
                            >
                        </div>

                        <div class="bg-gray-200 dark:bg-gray-800 p-1 rounded-xl flex items-center gap-1 shrink-0">
                            <button 
                                @click="switchMode('list')" 
                                :class="['px-3 py-1.5 rounded-lg text-[10px] uppercase tracking-wider font-bold transition-all flex items-center gap-1.5', displayMode === 'list' ? 'bg-white dark:bg-gray-700 text-[#004267] dark:text-white shadow-xs' : 'text-gray-500 dark:text-gray-400']"
                            >
                                Liste
                            </button>
                            <button 
                                @click="switchMode('map')" 
                                :class="['px-3 py-1.5 rounded-lg text-[10px] uppercase tracking-wider font-bold transition-all flex items-center gap-1.5', displayMode === 'map' ? 'bg-[#004267] dark:bg-blue-600 text-white shadow-xs' : 'text-gray-500 dark:text-gray-400']"
                            >
                                Carte
                            </button>
                        </div>
                    </div>
                </div>

                <!-- MODE LISTE -->
                <div v-if="displayMode === 'list'" class="space-y-8">
                    <div>
                        <h4 class="text-[11px] font-black text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-4 pl-1">Nos lieux de groupe ({{ mesLieuxFiltres.length }})</h4>
                        
                        <div v-if="mesLieuxFiltres.length === 0" class="text-sm text-gray-500 dark:text-gray-400 italic pl-1 mb-4">
                            Aucun lieu trouvé.
                        </div>

                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            <div 
                                v-for="lieu in mesLieuxFiltres" 
                                :key="lieu.id" 
                                @click="ouvrirDetailsLieu(lieu)"
                                class="bg-white dark:bg-gray-800 rounded-2xl p-5 border border-gray-100 dark:border-gray-700 shadow-xs flex flex-col justify-between cursor-pointer hover:shadow-md hover:border-gray-300 dark:hover:border-gray-500 transition-all active:scale-[0.99]"
                            >
                                <div>
                                    <div class="flex justify-between items-start">
                                        <h3 class="text-xl font-black text-gray-900 dark:text-white leading-tight">{{ lieu.name }}</h3>
                                        <span v-if="lieu.is_shared" class="shrink-0 text-[9px] bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 border border-green-200 dark:border-green-800 px-2 py-0.5 rounded font-black uppercase tracking-wider">
                                            Partagé
                                        </span>
                                    </div>
                                    
                                    <p class="text-xs text-gray-600 dark:text-gray-300 flex items-start gap-2 mt-2 leading-relaxed">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mt-0.5 shrink-0 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                                        {{ lieu.address }}
                                    </p>
                                </div>
                                
                                <p v-if="lieu.contact_info" class="text-xs text-gray-500 dark:text-gray-400 italic mt-3 pt-2 border-t border-gray-100 dark:border-gray-700/60">
                                    Contact : {{ lieu.contact_info }}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div v-if="lieuxPartagesFiltres.length > 0">
                        <h4 class="text-[11px] font-black text-[#004267] dark:text-blue-400 uppercase tracking-widest mb-4 pl-1 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                            Lieux partagés par d'autres groupes ({{ lieuxPartagesFiltres.length }})
                        </h4>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            <div 
                                v-for="lieu in lieuxPartagesFiltres" 
                                :key="lieu.id" 
                                @click="ouvrirDetailsLieu(lieu)"
                                class="bg-blue-50/40 dark:bg-blue-900/10 rounded-2xl p-5 border border-blue-100 dark:border-blue-900/30 shadow-xs flex flex-col justify-between cursor-pointer hover:shadow-md hover:border-blue-300 dark:hover:border-blue-700 transition-all active:scale-[0.99]"
                            >
                                <div>
                                    <h3 class="text-xl font-black text-[#004267] dark:text-blue-300 leading-tight">{{ lieu.name }}</h3>
                                    <p class="text-xs text-gray-600 dark:text-gray-300 mt-2">{{ lieu.address }}</p>
                                </div>
                                <p v-if="lieu.contact_info" class="text-xs text-gray-500 dark:text-gray-400 italic mt-3 pt-2 border-t border-blue-100 dark:border-blue-900/30">
                                    Contact : {{ lieu.contact_info }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- MODE CARTE -->
                <div v-if="displayMode === 'map'" class="w-full min-h-[500px] rounded-2xl overflow-hidden shadow-inner border border-gray-200 dark:border-gray-700 relative z-0 mt-2">
                    <div id="map" class="w-full h-full"></div>
                </div>
            </div>

        </div>

        <!-- MODALE : AJOUTER UNE TENTE -->
        <div 
            v-if="showAddTentModal" 
            @click="showAddTentModal = false"
            class="fixed inset-0 bg-black/40 dark:bg-black/60 backdrop-blur-sm flex justify-center items-end sm:items-center z-50 p-0 sm:p-4 transition-colors"
        >
            <div 
                @click.stop
                class="bg-white dark:bg-gray-800 rounded-t-[30px] sm:rounded-3xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh] shadow-2xl transition-colors"
            >
                <div class="p-6 overflow-y-auto">
                    <div class="w-12 h-1 bg-gray-200 dark:bg-gray-700 rounded-full mx-auto mb-6"></div>

                    <div class="flex justify-between items-center mb-5">
                        <h3 class="text-xl font-black text-gray-900 dark:text-white">Ajouter une tente</h3>
                        <button @click="showAddTentModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                            ✕
                        </button>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Nom / Numéro de la tente</label>
                            <input v-model="tentForm.name" type="text" placeholder="Ex: Canadienne N°6 ou Tente Mess 15m²" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30">
                        </div>

                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Capacité (nombre de places)</label>
                            <input v-model="tentForm.capacity" type="number" min="1" max="50" placeholder="Ex: 6" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30">
                        </div>

                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">État initial</label>
                            <select v-model="tentForm.status" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30">
                                <option value="operationnelle">Opérationnelle (Prête à camper)</option>
                                <option value="abimee">À réparer (Besoin de réparation)</option>
                            </select>
                        </div>

                        <div class="pt-4">
                            <button @click="soumettreTente" :disabled="isSavingTent" class="w-full py-3.5 bg-[#e85d22] hover:bg-orange-600 text-white rounded-xl font-bold text-sm shadow-md disabled:opacity-50 transition-colors">
                                {{ isSavingTent ? 'Enregistrement...' : 'Valider et ajouter la tente' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- MODALE : AJOUTER UN LIEU DE CAMP -->
        <div 
            v-if="showLocationModal" 
            @click="showLocationModal = false"
            class="fixed inset-0 bg-black/40 dark:bg-black/60 backdrop-blur-sm flex justify-center items-end sm:items-center z-50 p-0 sm:p-4 transition-colors"
        >                
            <div 
                @click.stop
                class="bg-white dark:bg-gray-800 rounded-t-[30px] sm:rounded-3xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh] shadow-2xl transition-colors"
            >                    
                <div class="p-6 overflow-y-auto">
                    <div class="w-12 h-1 bg-gray-200 dark:bg-gray-700 rounded-full mx-auto mb-6"></div>

                    <div class="flex justify-between items-center mb-5">
                        <h3 class="text-xl font-black text-gray-900 dark:text-white">Ajouter un lieu de camp</h3>
                        <button @click="showLocationModal = false" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200">
                            ✕
                        </button>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Nom du lieu</label>
                            <input v-model="locationForm.name" type="text" placeholder="Ex: Base Scoute de la Guiche" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30">
                        </div>
                        
                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Adresse complète</label>
                            <textarea v-model="locationForm.address" rows="2" placeholder="Ex: Lieu-dit La Guiche, 35350 Saint-Méloir" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30 resize-none"></textarea>
                        </div>
                        
                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Contact du propriétaire</label>
                            <input v-model="locationForm.contact_info" type="text" placeholder="Ex: M. Dupont : 06 12 34 56 78" class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30">
                        </div>
                        
                        <div>
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Description & Commodités</label>
                            <textarea v-model="locationForm.description" rows="2" placeholder="Ex: Eau potable, terrain plat, préau, douches..." class="w-full bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-xl px-4 py-3 text-sm font-semibold text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#004267]/30 resize-none"></textarea>
                        </div>

                        <div class="flex items-center justify-between pt-2 pb-2">
                            <div>
                                <span class="block text-sm font-bold text-gray-900 dark:text-white">Partager au réseau scout</span>
                                <span class="text-[10px] text-gray-500 dark:text-gray-400 font-medium">Rendre ce lieu visible par d'autres maitrises</span>
                            </div>
                            <button 
                                @click="locationForm.is_shared = !locationForm.is_shared"
                                :class="['w-12 h-6 flex items-center rounded-full p-1 transition-colors duration-300', locationForm.is_shared ? 'bg-[#004267] dark:bg-blue-600' : 'bg-gray-200 dark:bg-gray-600']"
                            >
                                <div :class="['bg-white w-4 h-4 rounded-full shadow-xs transform transition-transform duration-300', locationForm.is_shared ? 'translate-x-6' : 'translate-x-0']"></div>
                            </button>
                        </div>

                        <div class="pt-4">
                            <button @click="soumettreLieu" :disabled="isSavingLocation" class="w-full py-3.5 bg-[#004267] dark:bg-blue-600 text-white rounded-xl font-bold text-sm shadow-md disabled:opacity-50 transition-colors">
                                {{ isSavingLocation ? 'Enregistrement...' : 'Enregistrer ce lieu' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- MODALE : DÉTAILS DU LIEU -->
        <div 
            v-if="showLocationDetailsModal" 
            @click="fermerDetailsLieu" 
            class="fixed inset-0 bg-black/40 dark:bg-black/60 backdrop-blur-sm flex justify-center items-end sm:items-center z-50 p-0 sm:p-4 transition-colors"
        >
            <div 
                @click.stop 
                class="bg-white dark:bg-gray-800 rounded-t-[30px] sm:rounded-3xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh] shadow-2xl transition-colors"
            >
                <div class="p-6 overflow-y-auto">
                    <div class="w-12 h-1 bg-gray-200 dark:bg-gray-700 rounded-full mx-auto mb-6"></div>
                    
                    <div class="flex justify-between items-start mb-6">
                        <div>
                            <h3 class="text-2xl font-black text-gray-900 dark:text-white leading-tight">{{ selectedLocation?.name }}</h3>
                            <span v-if="selectedLocation?.is_shared" class="inline-block mt-2 text-[9px] bg-green-50 dark:bg-green-900/30 text-green-600 dark:text-green-400 border border-green-200 dark:border-green-800 px-2 py-0.5 rounded font-black uppercase tracking-wider">
                                Partagé au réseau scout
                            </span>
                        </div>
                        <button @click="fermerDetailsLieu" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 bg-gray-50 dark:bg-gray-700 rounded-full p-2">
                            ✕
                        </button>
                    </div>

                    <div class="space-y-5">
                        <div>
                            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Adresse</p>
                            <p class="text-sm text-gray-900 dark:text-gray-200 font-semibold">{{ selectedLocation?.address || 'Non renseignée' }}</p>
                        </div>

                        <div v-if="selectedLocation?.contact_info">
                            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Contact Propriétaire</p>
                            <p class="text-sm text-gray-900 dark:text-gray-200 font-semibold">{{ selectedLocation.contact_info }}</p>
                        </div>

                        <div v-if="selectedLocation?.description" class="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-xl border border-gray-100 dark:border-gray-700">
                            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Description & Commodités</p>
                            <p class="text-xs text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">{{ selectedLocation.description }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import { 
    damagedTents, fetchDamagedTents, marquerReparee, 
    allTents, showAddTentModal, tentForm, isSavingTent, fetchAllTents, ouvrirAjoutTente, soumettreTente, ouvrirDeclarationIncident,
    locations, showLocationModal, locationForm, isSavingLocation, 
    ouvrirAjoutLieu, soumettreLieu, fetchLocations, selectedLocation, showLocationDetailsModal, ouvrirDetailsLieu, fermerDetailsLieu
} from '../stores/logistiqueStore.js'
import { groupName } from '../stores/authStore.js'

const activeTab = ref('tentes')
const rechercheLieu = ref('')

const capaciteTotaleTentes = computed(() => {
    return allTents.value.reduce((sum, t) => sum + (parseInt(t.capacity) || 0), 0)
})

const tentesOperationnelles = computed(() => {
    return allTents.value.filter(t => t.status !== 'abimee')
})

const mesLieuxFiltres = computed(() => {
    const list = locations.value.filter(lieu => lieu.group_name === groupName.value)
    if (!rechercheLieu.value.trim()) return list
    const query = rechercheLieu.value.toLowerCase()
    return list.filter(l => l.name.toLowerCase().includes(query) || (l.address && l.address.toLowerCase().includes(query)))
})

const lieuxPartagesFiltres = computed(() => {
    const list = locations.value.filter(lieu => lieu.group_name !== groupName.value)
    if (!rechercheLieu.value.trim()) return list
    const query = rechercheLieu.value.toLowerCase()
    return list.filter(l => l.name.toLowerCase().includes(query) || (l.address && l.address.toLowerCase().includes(query)))
})

onMounted(() => {
    fetchAllTents()
    fetchDamagedTents()
    fetchLocations()
})

const displayMode = ref('list') 
let map = null

const initMap = async () => {
    await nextTick() 
    if (map) map.remove()

    map = L.map('map').setView([46.603354, 1.888334], 5)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map)

    const customIcon = L.divIcon({
        html: `<svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-[#004267] dark:text-blue-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" /></svg>`,
        className: 'bg-transparent',
        iconSize: [32, 32],
        iconAnchor: [16, 32]
    })

    locations.value.forEach(lieu => {
        if (lieu.latitude && lieu.longitude) {
            const marker = L.marker([lieu.latitude, lieu.longitude], { icon: customIcon }).addTo(map)
            marker.on('click', () => {
                ouvrirDetailsLieu(lieu)
            })
        }
    })
}

const switchMode = (mode) => {
    displayMode.value = mode
    if (mode === 'map') {
        initMap()
    }
}
</script>
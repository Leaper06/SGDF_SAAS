<template>
    <div class="h-full flex flex-col bg-gray-50">
        
        <div class="bg-[#004267] px-6 pt-8 pb-4 shrink-0 rounded-b-[30px] shadow-md z-10">
            <h2 class="text-2xl font-black text-white tracking-wider mb-6">Logistique</h2>
            
            <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">

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
            <div v-if="activeTab === 'lieux'" class="space-y-4 pb-24 flex flex-col h-full">    
                <div class="flex justify-between items-end mb-4 pr-1">
                    <div>
                        <h3 class="text-lg font-extrabold text-gray-900">Carnet d'adresses</h3>
                        <p class="text-xs font-medium text-gray-500 mt-1">Lieux de camp du groupe et partagés</p>
                    </div>

                    <div class="bg-gray-100 p-1 rounded-lg flex items-center gap-1 shrink-0">
                        <button 
                            @click="switchMode('list')" 
                            :class="['px-3 py-1.5 rounded-md text-[10px] uppercase tracking-wider font-bold transition-all flex items-center gap-1.5', displayMode === 'list' ? 'bg-white text-[#004267] shadow-sm' : 'text-gray-400']"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 10h16M4 14h16M4 18h16" /></svg>
                            Liste
                        </button>
                        <button 
                            @click="switchMode('map')" 
                            :class="['px-3 py-1.5 rounded-md text-[10px] uppercase tracking-wider font-bold transition-all flex items-center gap-1.5', displayMode === 'map' ? 'bg-[#004267] text-white shadow-sm' : 'text-gray-400']"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" /></svg>
                            Carte
                        </button>
                    </div>
                </div>

                <div v-if="displayMode === 'list'" class="space-y-8">
                    
                    <div>
                        <h4 class="text-[11px] font-black text-gray-400 uppercase tracking-widest mb-4 pl-2">Nos adresses</h4>
                        
                        <div v-if="mesLieux.length === 0" class="text-sm text-gray-500 italic pl-2 mb-4">
                            Vous n'avez pas encore enregistré de lieu.
                        </div>

                        <div class="space-y-4">
                            <div 
                                v-for="lieu in mesLieux" 
                                :key="lieu.id" 
                                @click="ouvrirDetailsLieu(lieu)"
                                class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm space-y-3 cursor-pointer hover:shadow-md hover:border-gray-200 transition-all active:scale-[0.98]"
                            >
                                <div class="pr-4">
                                    <h3 class="text-2xl font-black text-gray-900 leading-tight">{{ lieu.name }}</h3>
                                    <span v-if="lieu.is_shared" class="inline-flex items-center gap-1 mt-2 text-[9px] bg-green-50 text-green-600 border border-green-200 px-2 py-1 rounded font-black uppercase tracking-wider">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                                        Partagé au réseau
                                    </span>
                                </div>
                                
                                <p class="text-sm text-gray-600 flex items-start gap-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mt-0.5 shrink-0 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                                    {{ lieu.address }}
                                </p>
                                <p v-if="lieu.contact_info" class="text-xs text-gray-500 italic flex items-center gap-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                                    {{ lieu.contact_info }}
                                </p>
                            </div>
                        </div>
                    </div>

                    <div v-if="lieuxPartages.length > 0">
                        <h4 class="text-[11px] font-black text-[#004267] uppercase tracking-widest mb-4 pl-2 flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                            Réseau partagé
                        </h4>
                        
                        <div class="space-y-4">
                            <div 
                                v-for="lieu in lieuxPartages" 
                                :key="lieu.id" 
                                @click="ouvrirDetailsLieu(lieu)"
                                class="bg-blue-50/30 rounded-2xl p-5 border border-blue-100 shadow-sm space-y-3 cursor-pointer hover:shadow-md hover:border-blue-200 transition-all active:scale-[0.98]"
                            >
                                <div class="pr-4">
                                    <h3 class="text-2xl font-black text-[#004267] leading-tight">{{ lieu.name }}</h3>
                                    <span class="inline-flex items-center gap-1 mt-2 text-[9px] bg-blue-100 text-[#004267] border border-blue-200 px-2 py-1 rounded font-black uppercase tracking-wider">
                                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                                        Via {{ lieu.group_name }}
                                    </span>
                                </div>
                                
                                <p class="text-sm text-gray-600 flex items-start gap-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mt-0.5 shrink-0 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                                    {{ lieu.address }}
                                </p>
                                <p v-if="lieu.contact_info" class="text-xs text-gray-500 italic flex items-center gap-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                                    {{ lieu.contact_info }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <div v-if="displayMode === 'map'" class="w-full min-h-[500px] rounded-2xl overflow-hidden shadow-inner border border-gray-200 relative z-0 mt-2">
                    <div id="map" class="w-full h-full"></div>
                </div>
            </div>

                <div 
                    v-if="showLocationModal" 
                    @click="showLocationModal = false"
                    class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-end sm:items-center z-50 p-0 sm:p-4"
                >                
                    <div 
                            @click.stop
                            class="bg-white rounded-t-[30px] sm:rounded-3xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh] shadow-2xl"
                        >                    
                    <div class="p-6 overflow-y-auto">
                        <div class="w-12 h-1 bg-gray-200 rounded-full mx-auto mb-6"></div>

                        <div class="space-y-4">
                            <div>
                                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Nom du lieu</label>
                                <input v-model="locationForm.name" type="text" placeholder="Ex: Base de la Guiche" class="w-full bg-gray-50/50 border border-gray-100 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 focus:outline-none focus:ring-2 focus:ring-[#004267]/20 placeholder-gray-400">
                            </div>
                            
                            <div>
                                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Adresse complète</label>
                                <textarea v-model="locationForm.address" rows="2" placeholder="Ex: 12 chemin des bois..." class="w-full bg-gray-50/50 border border-gray-100 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 focus:outline-none focus:ring-2 focus:ring-[#004267]/20 resize-none placeholder-gray-400"></textarea>
                            </div>
                            
                            <div>
                                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Contact proprio</label>
                                <input v-model="locationForm.contact_info" type="text" placeholder="Tel ou nom du propriétaire" class="w-full bg-gray-50/50 border border-gray-100 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 focus:outline-none focus:ring-2 focus:ring-[#004267]/20 placeholder-gray-400">
                            </div>
                            
                            <div>
                                <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Infos complémentaires</label>
                                <textarea v-model="locationForm.description" rows="2" placeholder="Ex: Eau potable dispo, terrain plat..." class="w-full bg-gray-50/50 border border-gray-100 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 focus:outline-none focus:ring-2 focus:ring-[#004267]/20 resize-none placeholder-gray-400"></textarea>
                            </div>

                            <div class="flex items-center justify-between pt-2 pb-2">
                                <div>
                                    <span class="block text-sm font-bold text-gray-900">Partager le lieu</span>
                                    <span class="text-[10px] text-gray-500 font-medium">Le rendre visible aux autres groupes</span>
                                </div>
                                <button 
                                    @click="locationForm.is_shared = !locationForm.is_shared"
                                    :class="['w-12 h-6 flex items-center rounded-full p-1 transition-colors duration-300', locationForm.is_shared ? 'bg-[#004267]' : 'bg-gray-200']"
                                >
                                    <div :class="['bg-white w-4 h-4 rounded-full shadow-sm transform transition-transform duration-300', locationForm.is_shared ? 'translate-x-6' : 'translate-x-0']"></div>
                                </button>
                            </div>

                            <div class="pt-4">
                                <button @click="soumettreLieu" :disabled="isSavingLocation" class="w-full py-3.5 bg-[#004267] text-white rounded-xl font-bold text-sm shadow-md disabled:opacity-50 flex justify-center items-center gap-2 hover:bg-[#003B5C] transition-colors">
                                    {{ isSavingLocation ? 'Enregistrement...' : 'Enregistrer ce lieu' }}
                                    <svg v-if="!isSavingLocation" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                                    </svg>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
        <div 
            v-if="showLocationDetailsModal" 
            @click="fermerDetailsLieu" 
            class="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-end sm:items-center z-50 p-0 sm:p-4"
        >
            <div 
                @click.stop 
                class="bg-white rounded-t-[30px] sm:rounded-3xl w-full max-w-md overflow-hidden flex flex-col max-h-[90vh] shadow-2xl"
            >
                <div class="p-6 overflow-y-auto">
                    <div class="w-12 h-1 bg-gray-200 rounded-full mx-auto mb-6"></div>
                    
                    <div class="flex justify-between items-start mb-6">
                        <div class="pr-4">
                            <h3 class="text-2xl font-black text-gray-900 leading-tight">{{ selectedLocation?.name }}</h3>
                            
                            <span v-if="selectedLocation?.group_name === groupName && selectedLocation?.is_shared" class="inline-block mt-2 text-[9px] bg-green-50 text-green-600 border border-green-200 px-2 py-1 rounded font-black uppercase tracking-wider">
                                Ce lieu est visible par tous
                            </span>
                            
                            <span v-if="selectedLocation?.group_name !== groupName" class="inline-block mt-2 text-[9px] bg-blue-50 text-[#004267] border border-blue-200 px-2 py-1 rounded font-black uppercase tracking-wider">
                                Partagé par le groupe : {{ selectedLocation?.group_name }}
                            </span>
                        </div>
                        <button @click="fermerDetailsLieu" class="text-gray-400 hover:text-gray-600 transition-colors bg-gray-50 rounded-full p-2 shrink-0">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                        </button>
                    </div>

                    <div class="space-y-5">
                        <div class="flex gap-4">
                            <div class="mt-0.5 w-10 h-10 rounded-full bg-blue-50 text-[#004267] flex items-center justify-center shrink-0">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                            </div>
                            <div>
                                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Adresse</p>
                                <p class="text-sm text-gray-900 font-medium leading-relaxed">{{ selectedLocation?.address || 'Non renseignée' }}</p>
                            </div>
                        </div>

                        <div class="flex gap-4">
                            <div class="mt-0.5 w-10 h-10 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center shrink-0">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                            </div>
                            <div>
                                <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1">Contact</p>
                                <p class="text-sm text-gray-900 font-medium">{{ selectedLocation?.contact_info || 'Aucun contact' }}</p>
                            </div>
                        </div>

                        <div class="bg-gray-50/80 rounded-2xl p-5 border border-gray-100 mt-2">
                            <p class="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-3 flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                                Infos complémentaires
                            </p>
                            <p class="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">{{ selectedLocation?.description || 'Aucune information complémentaire pour ce lieu.' }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script setup>
import { ref, onMounted, computed,nextTick } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

import { 
    damagedTents, fetchDamagedTents, marquerReparee, 
    locations, showLocationModal, locationForm, isSavingLocation, 
    ouvrirAjoutLieu, soumettreLieu, fetchLocations, selectedLocation, showLocationDetailsModal, ouvrirDetailsLieu, fermerDetailsLieu
} from '../stores/logistiqueStore.js'

onMounted(() => {
    fetchDamagedTents()
    fetchLocations()
})
import { groupName } from '../stores/authStore.js'
// La variable qui gère l'onglet actuellement affiché
const activeTab = ref('lieux')

const mesLieux = computed(() => {
    return locations.value.filter(lieu => lieu.group_name === groupName.value)
})

const lieuxPartages = computed(() => {
    return locations.value.filter(lieu => lieu.group_name !== groupName.value)
})

// Dès que la page s'affiche, on va chercher la liste des tentes cassées sur le serveur
onMounted(() => {
    fetchDamagedTents()
    fetchLocations()
})
const displayMode = ref('list') 
let map = null

const initMap = async () => {
    // nextTick permet d'attendre que Vue ait fini de dessiner la balise <div id="map">
    await nextTick() 
    
    // Si la carte existe déjà, on la nettoie pour éviter les bugs d'affichage
    if (map) {
        map.remove()
    }

    // Initialisation de la carte (coordonnées par défaut : Centre de la France)
    map = L.map('map').setView([46.603354, 1.888334], 5)

    // Chargement du fond de carte OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(map)

    
    const customIcon = L.divIcon({
        html: `<svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-[#004267]" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" /></svg>`,
        className: 'bg-transparent',
        iconSize: [32, 32],
        iconAnchor: [16, 32] // Aligne la pointe du SVG exactement sur la coordonnée
    })

    // Ajout des marqueurs pour chaque lieu partagé
    locations.value.forEach(lieu => {
            if (lieu.latitude && lieu.longitude) {
                const marker = L.marker([lieu.latitude, lieu.longitude], { icon: customIcon }).addTo(map)
                
                // Le clic sur le marqueur ouvre la modale
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
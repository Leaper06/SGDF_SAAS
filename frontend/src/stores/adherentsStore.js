import { ref, computed } from 'vue'
import { API_BASE_URL } from '../api/config.js'
import { userToken, logout, unitName, chefAdherentId, chefBranch } from './authStore.js'
import { separerNomPrenom } from '../utils/helpers.js'

// --- VARIABLES (Mémoire) ---
export const adherentsList = ref([])
export const isLoadingAdherents = ref(false)

// --- COMPUTED (Calculs) ---
export const jeunes = computed(() => {
    return adherentsList.value
        .filter(m => m.isJeune)
        .sort((a, b) => a.nom.localeCompare(b.nom)); // Petit bonus pour les trier par ordre alphabétique
})

export const chefs = computed(() => {
    return adherentsList.value
        .filter(m => m.isChef)
        .sort((a, b) => a.nom.localeCompare(b.nom));
})

// --- ACTIONS (Fonctions) ---
export const fetchAdherents = async () => {
    if (adherentsList.value.length > 0) return 

    isLoadingAdherents.value = true
    try {
        const [intranextResponse, extrasResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/adherents`, {
                headers: { 'Authorization': `Bearer ${userToken.value}` }
            }),
            fetch(`${API_BASE_URL}/adherents/extras`)
        ])
        
        if (intranextResponse.status === 401) {
            logout()
            return
        }
        
        const json = await intranextResponse.json()
        const extrasJson = await extrasResponse.json()
        
        // Les extras viennent de Supabase, on récupère le dictionnaire
        const extraData = extrasJson.status === 'success' ? extrasJson.data : {}
        
        if (intranextResponse.ok && json.data) {
            // 1. Profil de l'unité
            unitName.value = json.unit_name || "Unité Inconnue"
            localStorage.setItem('sgdf_unit_name', unitName.value)
            
            if (json.adherent_id) {
                chefAdherentId.value = json.adherent_id
                localStorage.setItem('sgdf_chef_id', json.adherent_id)
            }

            // 2. Traitement du tableau HTML : on enlève la première ligne (les en-têtes)
            const rows = json.data.slice(1) 

            adherentsList.value = rows.map((row, index) => {
                // row est une liste de colonnes envoyée par Python
                const cols = row.filter(c => c.trim() !== '')
                const rowText = cols.join(" ")
                
                // Tes fameuses règles métier
                const isJeune = /\b1\d{2}\b/.test(rowText)
                const isChef = /\b2\d{2}\b/.test(rowText)
                const identite = separerNomPrenom(cols[0]) // Le nom est dans la colonne 0
                const numAdherent = cols[1] || `id-${index}` // L'ID est dans la colonne 1
                
                const matchCode = rowText.match(/\b([12]\d{2})\b/)
                const codeAffichage = matchCode ? matchCode[0] : "Code ???"
                const localInfo = extraData[numAdherent] || {}

                // On reconstruit l'objet propre pour Vue.js
                return {
                    id: numAdherent,
                    nom: identite.nom,
                    prenom: identite.prenom,
                    code: codeAffichage,
                    isJeune: isJeune,
                    isChef: isChef,
                    photo: localInfo.photo_url || null,
                    ficheUrl: localInfo.fiche_url || null,
                    hasFiche: !!localInfo.fiche_url,
                    progressionSymbole: localInfo.progression_symbole || '',
                    progressionAction: localInfo.progression_action || '',
                    regime_alimentaire: localInfo.regime_alimentaire || '',
                    observations_medicales: localInfo.observations_medicales || ''
                }
            })

            // 3. Détection de la branche
            if (chefAdherentId.value) {
                const idRecherche = String(chefAdherentId.value).trim()
                const monProfil = adherentsList.value.find(m => String(m.id).trim() === idRecherche)

                if (monProfil) {
                    if (['214', '215'].includes(monProfil.code)) chefBranch.value = 'Louja'
                    else if (['222', '223'].includes(monProfil.code)) chefBranch.value = 'SG'
                    else if (['224', '225'].includes(monProfil.code)) chefBranch.value = 'Piok'
                    else chefBranch.value = 'Autre'
                    localStorage.setItem('sgdf_chef_branch', chefBranch.value)
                }
            }
        }
    } catch (error) {
        console.error("Erreur API :", error)
    } finally {
        isLoadingAdherents.value = false
    }
}
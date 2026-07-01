import { ref, computed } from 'vue'
import { API_BASE_URL } from '../api/config.js'
import { userToken, logout, unitName, chefAdherentId, chefBranch, isDemoMode } from './authStore.js'
import { separerNomPrenom } from '../utils/helpers.js'

// --- VARIABLES (Mémoire) ---
export const adherentsList = ref([])
export const isLoadingAdherents = ref(false)

// --- COMPUTED (Calculs) ---
export const jeunes = computed(() => {
    return adherentsList.value
        .filter(m => m.isJeune)
        .sort((a, b) => a.nom.localeCompare(b.nom)); 
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

    // === INTERCEPTION MODE DÉMO ===
    if (isDemoMode.value) {
        setTimeout(() => {
            adherentsList.value = [
                // Faux profils de la maîtrise
                { id: 'demo-chef-loic', nom: 'Test', prenom: 'Utilisateur', code: '222', isJeune: false, isChef: true, photo: null, ficheUrl: 'demo_medical_file.pdf', hasFiche: true, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-chef-2', nom: 'DUPONT', prenom: 'Robert', code: '222', isJeune: false, isChef: true, photo: null, ficheUrl: null, hasFiche: false, progressionSymbole: '', progressionAction: '' },
                
                // Faux profils des jeunes (Jeunes avec des codes de Mousses 122)
                { id: 'demo-jeune-1', nom: 'BAILLY', prenom: 'Julien', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: 'demo.pdf', hasFiche: true, progressionSymbole: 'Brevet Équipage', progressionAction: 'Gérer la table à carte' },
                { id: 'demo-jeune-2', nom: 'Treard', prenom: 'Morgane', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: null, hasFiche: false, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-jeune-3', nom: 'Dupuis', prenom: 'THéo', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: null, hasFiche: false, progressionSymbole: '', progressionAction: '' },
            ]
            isLoadingAdherents.value = false
        }, 600) // Petit délai pour l'animation du spinner
        return
    }
    // =============================

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
        
        const extraData = extrasJson.status === 'success' ? extrasJson.data : {}
        
        if (intranextResponse.ok && json.data) {
            unitName.value = json.unit_name || "Unité Inconnue"
            localStorage.setItem('sgdf_unit_name', unitName.value)
            
            if (json.adherent_id) {
                chefAdherentId.value = json.adherent_id
                localStorage.setItem('sgdf_chef_id', json.adherent_id)
            }

            const rows = json.data.slice(1) 

            adherentsList.value = rows.map((row, index) => {
                const cols = row.filter(c => c.trim() !== '')
                const rowText = cols.join(" ")
                
                const isJeune = /\b1\d{2}\b/.test(rowText)
                const isChef = /\b2\d{2}\b/.test(rowText)
                const identite = separerNomPrenom(cols[0]) 
                const numAdherent = cols[1] || `id-${index}` 
                
                const matchCode = rowText.match(/\b([12]\d{2})\b/)
                const codeAffichage = matchCode ? matchCode[0] : "Code ???"
                const localInfo = extraData[numAdherent] || {}

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
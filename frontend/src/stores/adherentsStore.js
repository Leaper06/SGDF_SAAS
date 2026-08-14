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
                // Profils de la maîtrise
                { id: 'demo-chef-loic', nom: 'Test', prenom: 'Utilisateur', code: '222', isJeune: false, isChef: true, photo: null, ficheUrl: 'demo_medical_file.png', hasFiche: true, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-chef-2', nom: 'DUPONT', prenom: 'Robert', code: '222', isJeune: false, isChef: true, photo: null, ficheUrl: null, hasFiche: false, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-chef-3', nom: 'PETIT', prenom: 'Camille', code: '222', isJeune: false, isChef: true, photo: null, ficheUrl: 'demo_camille.png', hasFiche: true, progressionSymbole: '', progressionAction: '' },
                
                // Profils des jeunes de l'équipage
                { id: 'demo-jeune-1', nom: 'BAILLY', prenom: 'Julien', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: 'demo_julien.png', hasFiche: true, progressionSymbole: 'Brevet Équipage', progressionAction: 'Gérer la table à carte' },
                { id: 'demo-jeune-2', nom: 'TREARD', prenom: 'Morgane', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: null, hasFiche: false, progressionSymbole: 'Flèche Bleue', progressionAction: 'Animer la veillée' },
                { id: 'demo-jeune-3', nom: 'DUPUIS', prenom: 'Théo', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: 'demo_theo.png', hasFiche: true, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-jeune-4', nom: 'MARTIN', prenom: 'Lucas', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: 'demo_lucas.png', hasFiche: true, progressionSymbole: 'Pilote', progressionAction: 'Secourisme' },
                { id: 'demo-jeune-5', nom: 'BERNARD', prenom: 'Emma', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: null, hasFiche: false, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-jeune-6', nom: 'LEROY', prenom: 'Hugo', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: 'demo_hugo.png', hasFiche: true, progressionSymbole: 'Second d\'équipage', progressionAction: '' },
                { id: 'demo-jeune-7', nom: 'MOREAU', prenom: 'Chloé', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: 'demo_chloe.png', hasFiche: true, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-jeune-8', nom: 'SIMON', prenom: 'Gabriel', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: null, hasFiche: false, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-jeune-9', nom: 'LAURENT', prenom: 'Clara', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: 'demo_clara.png', hasFiche: true, progressionSymbole: '', progressionAction: '' },
                { id: 'demo-jeune-10', nom: 'DUBOIS', prenom: 'Antoine', code: '122', isJeune: true, isChef: false, photo: null, ficheUrl: null, hasFiche: false, progressionSymbole: '', progressionAction: '' }
            ]
            isLoadingAdherents.value = false
        }, 400)
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

// --- SYNCHRONISATION MANUELLE INTRANET ---
export const isSyncing = ref(false)
export const showSyncModal = ref(false)

export const syncAdherents = async (password = null) => {
    isSyncing.value = true
    try {
        const response = await fetch(`${API_BASE_URL}/adherents/sync`, {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${userToken.value}`,
                'Content-Type': 'application/json'
            },
            body: password ? JSON.stringify({ password }) : null
        })
        
        if (response.status === 401) {
            // Session Intranet expirée côté serveur, on demande le mot de passe
            showSyncModal.value = true
            return false
        }
        
        if (response.ok) {
            // Synchro réussie, on recharge les données depuis la base
            showSyncModal.value = false
            adherentsList.value = [] // Force le re-fetch
            await fetchAdherents()
            return true
        }
        
    } catch (error) {
        console.error("Erreur lors de la synchronisation :", error)
    } finally {
        isSyncing.value = false
    }
    return false
}

// ==========================================
// ÉQUIPAGES & SIXAINES MANAGEMENT
// ==========================================

export const equipages = ref([])
export const showCreateEquipageModal = ref(false)

export const initEquipages = () => {
    const saved = localStorage.getItem('sgdf_equipages')
    if (saved) {
        try {
            const parsed = JSON.parse(saved)
            // Purge automatique des anciens équipages démo (eq-1 et eq-2) du localStorage
            equipages.value = parsed.filter(e => e.id !== 'eq-1' && e.id !== 'eq-2')
            saveEquipages()
            return
        } catch (e) { console.error("Erreur lecture équipages :", e) }
    }
    
    // Par défaut : Aucun équipage pré-créé
    equipages.value = []
    saveEquipages()
}

export const saveEquipages = () => {
    localStorage.setItem('sgdf_equipages', JSON.stringify(equipages.value))
}

export const creerEquipage = ({ name, color = '#004267' }) => {
    if (!name || !name.trim()) return
    const newEq = {
        id: 'eq-' + Date.now(),
        name: name.trim(),
        color,
        pilote_id: null,
        member_ids: []
    }
    equipages.value.push(newEq)
    saveEquipages()
}

export const supprimerEquipage = (equipageId) => {
    if (!confirm("Voulez-vous vraiment supprimer cet équipage ?")) return
    equipages.value = equipages.value.filter(e => e.id !== equipageId)
    saveEquipages()
}

export const affecterJeuneAEquipage = (jeuneId, equipageId, role = 'membre') => {
    if (!jeuneId || !equipageId) return
    
    // 1. Retirer d'abord le jeune de tous les autres équipages
    retirerJeuneDuneEquipage(jeuneId)

    // 2. L'ajouter dans l'équipage cible
    const eq = equipages.value.find(e => e.id === equipageId)
    if (eq) {
        if (!eq.member_ids.includes(jeuneId)) {
            eq.member_ids.push(jeuneId)
        }
        if (role === 'pilote') {
            eq.pilote_id = jeuneId
        }
        saveEquipages()
    }
}

export const retirerJeuneDuneEquipage = (jeuneId) => {
    equipages.value.forEach(eq => {
        eq.member_ids = eq.member_ids.filter(id => id !== jeuneId)
        if (eq.pilote_id === jeuneId) eq.pilote_id = null
    })
    saveEquipages()
}

export const nomRoleSelonBranche = computed(() => {
    const branch = chefBranch.value || 'SG'
    if (branch === 'Louja') {
        return {
            unite: 'Sixaines',
            single: 'Sixaine',
            pilote: 'Sixainier'
        }
    }
    return {
        unite: 'Équipages',
        single: 'Équipage',
        pilote: 'Pilote'
    }
})
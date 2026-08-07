import { ref } from 'vue'
import { API_BASE_URL } from '../api/config.js'
import { groupName, isDemoMode } from './authStore.js'
import { supabase } from '../api/supabase.js'
// --- VARIABLES ---
export const damagedTents = ref([])
export const showIncidentModal = ref(false)
export const incidentForm = ref({ tent_id: null, nom: '', etat: 'Endommagée', notes_incident: '' })
export const locationForm = ref({
    name: '',
    address: '',
    contact_info: '',
    description: '',
    is_shared: false
})
export const isSavingLocation = ref(false)
export const locations = ref([])
export const showLocationModal = ref(false)

export const fetchLocations = async () => {
    // === INTERCEPTION MODE DÉMO ===
    if (isDemoMode.value) {
        locations.value = [
            // Lieux Partagés (is_shared: true)
            { id: 'demo-loc-1', name: 'Local Notre-Dame d\'Aleth', address: 'Place Saint-Pierre, 35400 Saint-Malo', contact_info: 'Clés dans la boîte à code.', description: 'Notre local habituel.', is_shared: true },
            { id: 'demo-loc-2', name: 'Base Scoute de la Guiche', address: 'La Guiche, 35350 Saint-Méloir-des-Ondes', contact_info: 'Équipe régionale', description: 'Grand terrain, accès eau potable et électricité.', is_shared: true },
            // Lieux Privés (is_shared: false)
            { id: 'demo-loc-3', name: 'Terrain de M. Martin', address: 'La Ville ès Nonais, 35430', contact_info: 'M. Martin : 06 12 34 56 78', description: 'Champ plat sans point d\'eau, demander avant.', is_shared: false },
            { id: 'demo-loc-4', name: 'Centre Nautique de Quelmer', address: 'Quelmer, 35400 Saint-Malo', contact_info: 'Accueil base nautique', description: 'Point de départ pour les activités en mer.', is_shared: false }
        ]
        return
    }
    // =============================
    try {
        // On récupère les lieux de notre groupe + les lieux partagés
        const response = await fetch(`${API_BASE_URL}/locations?group_name=${groupName.value}`)
        const json = await response.json()
        if (json.status === 'success') locations.value = json.data
    } catch (e) { console.error("Erreur lieux :", e) }
}

export const ouvrirAjoutLieu = () => {
    locationForm.value = { name: '', address: '', contact_info: '', description: '', is_shared: false }
    showLocationModal.value = true
}

export const soumettreLieu = async () => {
    if (!locationForm.value.name) return alert("Le nom est obligatoire")
    
    // === INTERCEPTION MODE DÉMO ===
    if (isDemoMode.value) {
        isSavingLocation.value = true
        setTimeout(() => {
            locations.value.push({
                id: 'demo-loc-new-' + Date.now(),
                name: locationForm.value.name,
                address: locationForm.value.address,
                contact_info: locationForm.value.contact_info,
                description: locationForm.value.description,
                is_shared: locationForm.value.is_shared
            })
            showLocationModal.value = false
            isSavingLocation.value = false
        }, 500)
        return
    }
    // =============================

    isSavingLocation.value = true
    if (!locationForm.value.name) return alert("Le nom est obligatoire")
    
    isSavingLocation.value = true
    try {
        const response = await fetch(`${API_BASE_URL}/locations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ...locationForm.value,
                group_name: groupName.value
                
            })
        })
        
        const json = await response.json()
        if (json.status === 'success') {
            showLocationModal.value = false
            await fetchLocations()
        }
    } catch (e) { 
        alert("Erreur lors de l'enregistrement") 
    } finally { 
        isSavingLocation.value = false 
    }
}

// --- VARIABLES POUR LES DÉTAILS D'UN LIEU ---
export const selectedLocation = ref(null)
export const showLocationDetailsModal = ref(false)

// --- FONCTIONS ---
export const ouvrirDetailsLieu = (lieu) => {
    selectedLocation.value = lieu
    showLocationDetailsModal.value = true
}

export const fermerDetailsLieu = () => {
    showLocationDetailsModal.value = false
    selectedLocation.value = null
}
// --- FONCTIONS ---

// 1. Récupérer toutes les tentes abîmées (pour l'onglet Logistique)
export const fetchDamagedTents = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/tents/damaged`)
        const json = await response.json()
        if (json.status === 'success') damagedTents.value = json.data
    } catch (e) { console.error("Erreur de chargement du matériel endommagé :", e) }
}

// 2. Ouvrir la modale d'incident depuis le planning
export const ouvrirDeclarationIncident = (tente) => {
    console.log("BOUTON CLIQUÉ ! Tente :", tente.name)
    incidentForm.value = { 
        tent_id: tente.id, 
        nom: tente.name, // Juste pour l'affichage dans la modale
        etat: tente.etat || 'Endommagée', 
        notes_incident: tente.notes_incident || '' 
    }
    showIncidentModal.value = true
}

export const fermerDeclarationIncident = () => {
    showIncidentModal.value = false
}

// 3. Envoyer l'incident au serveur
export const soumettreIncident = async () => {
    if (!incidentForm.value.notes_incident) return alert("Veuillez décrire le problème.")
    
    try {
        const response = await fetch(`${API_BASE_URL}/tents/${incidentForm.value.tent_id}/incident`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                etat: incidentForm.value.etat,
                notes_incident: incidentForm.value.notes_incident
            })
        })
        const json = await response.json()
        if (json.status === 'success') {
            fermerDeclarationIncident()
            alert("L'incident a bien été déclaré !")
            // Idéalement, ici on devrait rafraîchir la liste des tentes du camp
        }
    } catch (e) { 
        console.error("Erreur lors de la déclaration :", e) 
        alert("Impossible de joindre le serveur.")
    }
}

// 4. Marquer une tente comme réparée
export const marquerReparee = async (tenteId) => {
    if(!confirm("Confirmer que cette tente est réparée et complète ?")) return;

    try {
        const response = await fetch(`${API_BASE_URL}/tents/${tenteId}/incident`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ etat: 'OK', notes_incident: '' })
        })
        const json = await response.json()
        if (json.status === 'success') {
            await fetchDamagedTents() // On met à jour la liste visuelle
        }
    } catch (e) { console.error("Erreur lors de la réparation :", e) }
}

// ==========================================
// CHECKLIST MATÉRIEL DE CAMP & TEMPLATES
// ==========================================

export const campMaterials = ref([])
export const materialTemplates = ref([])
export const newMaterialItemName = ref('')
export const isSavingMaterials = ref(false)

// ==========================================
// ABONNEMENTS TEMPS RÉEL (Broadcast)
// ==========================================
let materialChannel = null

export const subscribeToMaterials = (campId) => {
    if (!campId || isDemoMode.value) return
    unsubscribeFromMaterials()
    materialChannel = supabase.channel(`materials-${campId}`, {
        config: { broadcast: { ack: false } }
    })
    
    materialChannel.on('broadcast', { event: 'materials_update' }, (payload) => {
        campMaterials.value = payload.payload.items
    }).subscribe()
}

export const unsubscribeFromMaterials = () => {
    if (materialChannel) {
        supabase.removeChannel(materialChannel)
        materialChannel = null
    }
}

export const broadcastMaterials = () => {
    if (materialChannel) {
        materialChannel.send({
            type: 'broadcast',
            event: 'materials_update',
            payload: { items: campMaterials.value }
        })
    }
}

export const fetchCampMaterials = async (campId) => {
    if (!campId) return
    if (isDemoMode.value) {
        campMaterials.value = [
            { id: 'm1', name: 'Malle Pharmacie', is_checked: true },
            { id: 'm2', name: 'Bâche de camp', is_checked: false },
            { id: 'm3', name: 'Jerrycans d\'eau (x2)', is_checked: true },
            { id: 'm4', name: 'Scie & Hachette', is_checked: false },
            { id: 'm5', name: 'Corde & Ficelle', is_checked: false }
        ]
        return
    }
    try {
        const response = await fetch(`${API_BASE_URL}/camps/${campId}/materials`)
        const json = await response.json()
        if (json.status === 'success') campMaterials.value = json.data
    } catch (e) {
        console.error("Erreur chargement matériel camp :", e)
    }
}

export const sauvegarderMaterielCamp = async (campId) => {
    if (!campId) return
    if (isDemoMode.value) return
    isSavingMaterials.value = true
    try {
        await fetch(`${API_BASE_URL}/camps/${campId}/materials`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items: campMaterials.value })
        })
    } catch (e) {
        console.error("Erreur sauvegarde matériel :", e)
    } finally {
        isSavingMaterials.value = false
    }
}

export const ajouterMaterielCamp = (campId) => {
    const nom = newMaterialItemName.value.trim()
    if (!nom) return
    campMaterials.value.push({
        id: 'tmp-' + Date.now(),
        name: nom,
        is_checked: false
    })
    newMaterialItemName.value = ''
    if (campId) { 
        sauvegarderMaterielCamp(campId)
        broadcastMaterials() 
    }
}

export const supprimerMaterielCamp = (index, campId) => {
    campMaterials.value.splice(index, 1)
    if (campId) { 
        sauvegarderMaterielCamp(campId)
        broadcastMaterials()
    }
}

export const toggleMaterielCamp = (index, campId) => {
    campMaterials.value[index].is_checked = !campMaterials.value[index].is_checked
    if (campId) { 
        sauvegarderMaterielCamp(campId)
        broadcastMaterials()
    }
}

export const fetchMaterialTemplates = async () => {
    if (isDemoMode.value) {
        materialTemplates.value = [
            { id: 'tmpl-1', name: 'Matériel WE classique', items: ['Malle Pharmacie', 'Bâche de camp', 'Jerrycans d\'eau (x2)', 'Scie & Hachette', 'Corde & Ficelle'] },
            { id: 'tmpl-2', name: 'Matériel Camp d\'été', items: ['Malle Pharmacie', 'Bâches de camp (x3)', 'Jerrycans d\'eau (x4)', 'Sies & Hachettes', 'Trousse à outils', 'Table pliante'] }
        ]
        return
    }
    try {
        const response = await fetch(`${API_BASE_URL}/material_templates`)
        const json = await response.json()
        if (json.status === 'success') materialTemplates.value = json.data
    } catch (e) {
        console.error("Erreur chargement modèles matériel :", e)
    }
}

export const appliquerTemplateMateriel = async (campId, templateId) => {
    if (!templateId || !campId) return
    if (isDemoMode.value) {
        const tmpl = materialTemplates.value.find(t => t.id === templateId)
        if (tmpl && tmpl.items) {
            tmpl.items.forEach(name => {
                if (!campMaterials.value.some(m => m.name === name)) {
                    campMaterials.value.push({ id: 'demo-' + Date.now() + Math.random(), name, is_checked: false })
                }
            })
        }
        return
    }
    try {
        const response = await fetch(`${API_BASE_URL}/camps/${campId}/materials/apply-template`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ template_id: templateId })
        })
        const json = await response.json()
        if (json.status === 'success') campMaterials.value = json.data
    } catch (e) {
        console.error("Erreur application modèle matériel :", e)
    }
}

export const creerTemplateMateriel = async (nomTemplate) => {
    if (!nomTemplate || nomTemplate.trim() === '') return
    const items = campMaterials.value.map(m => m.name)
    if (items.length === 0) return alert("Ajoutez au moins un matériel dans la liste avant de créer un modèle.")

    if (isDemoMode.value) {
        materialTemplates.value.push({
            id: 'demo-tmpl-' + Date.now(),
            name: nomTemplate,
            items: items
        })
        alert("Modèle de matériel créé avec succès !")
        return
    }

    try {
        const response = await fetch(`${API_BASE_URL}/material_templates`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: nomTemplate, items })
        })
        const json = await response.json()
        if (json.status === 'success') {
            alert("Modèle de matériel enregistré avec succès !")
            await fetchMaterialTemplates()
        }
    } catch (e) {
        console.error("Erreur création modèle matériel :", e)
    }
}

export const supprimerTemplateMateriel = async (templateId) => {
    if (!confirm("Supprimer ce modèle de matériel ?")) return
    if (isDemoMode.value) {
        materialTemplates.value = materialTemplates.value.filter(t => t.id !== templateId)
        return
    }
    try {
        const response = await fetch(`${API_BASE_URL}/material_templates/${templateId}`, { method: 'DELETE' })
        const json = await response.json()
        if (json.status === 'success') {
            await fetchMaterialTemplates()
        } else {
            alert("Erreur lors de la suppression")
        }
    } catch (e) {
        console.error("Erreur suppression modèle matériel :", e)
    }
}
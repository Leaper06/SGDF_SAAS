import { ref } from 'vue'
import { API_BASE_URL } from '../api/config.js'
import { groupName, isDemoMode } from './authStore.js'
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
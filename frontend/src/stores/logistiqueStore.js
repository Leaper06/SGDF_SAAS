import { ref } from 'vue'
import { API_BASE_URL } from '../api/config.js'

// --- VARIABLES ---
export const damagedTents = ref([])
export const showIncidentModal = ref(false)
export const incidentForm = ref({ tent_id: null, nom: '', etat: 'Endommagée', notes_incident: '' })

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
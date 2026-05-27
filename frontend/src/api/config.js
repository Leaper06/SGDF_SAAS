// src/api/config.js

export const API_BASE_URL = 'http://localhost:5001/api'

// ==========================================
// INTERCEPTEUR GLOBAL DE REQUÊTES
// ==========================================
const originalFetch = window.fetch

window.fetch = async (...args) => {
    const [resource] = args

    // On ne surveille QUE les requêtes vers notre API (pour ne pas bloquer OpenStreetMap)
    if (typeof resource === 'string' && resource.startsWith(API_BASE_URL)) {
        const response = await originalFetch(...args)
        
        // Si le serveur refuse l'accès (Token expiré ou invalide)
        if (response.status === 401) {
            // On lance un signal d'alarme global dans toute l'application
            window.dispatchEvent(new CustomEvent('session-expired'))
        }
        return response
    }
    
    // Pour toutes les autres requêtes, on laisse faire normalement
    return originalFetch(...args)
}
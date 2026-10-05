// src/api/config.js

export const API_BASE_URL = '/api'

// ==========================================
// INTERCEPTEUR GLOBAL DE REQUÊTES
// ==========================================
const originalFetch = window.fetch

window.fetch = async (...args) => {
    const [resource] = args

    // On ne surveille QUE les requêtes vers notre API (pour ne pas bloquer OpenStreetMap)
    if (typeof resource === 'string' && resource.startsWith(API_BASE_URL)) {
        // Ajout automatique du token de session sur toutes les requêtes vers l'API
        const token = localStorage.getItem('sgdf_token')
        if (token) {
            const options = args[1] || {}
            const headers = new Headers(options.headers || {})
            if (!headers.has('Authorization')) {
                headers.set('Authorization', `Bearer ${token}`)
            }
            args[1] = { ...options, headers }
        }

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

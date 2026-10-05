// src/api/config.js

export const API_BASE_URL = '/api'

// ==========================================
// INTERCEPTEUR GLOBAL DE REQUÊTES
// ==========================================
// Toutes les requêtes vers notre API passent par ici. On y gère en un seul endroit
// ce qui rend l'application utilisable sur un réseau faible (camp, forêt, 3G) :
//   - ajout automatique du token de session
//   - délai maximal par requête (sinon un chargement peut tourner indéfiniment)
//   - nouvel essai automatique des lectures (GET) en cas de coupure ou de serveur indisponible
//   - réponses d'erreur toujours en JSON (Nginx renvoie du HTML en cas de panne)
//   - message visible pour l'utilisateur quand une requête échoue

const DEFAULT_TIMEOUT_MS = 15000
// Connexion (navigateur headless vers l'intranet), upload, export PDF et synchronisation sont longs
const LONG_TIMEOUT_MS = 90000
const LONG_REQUEST_PATTERNS = ['/login', '/upload', '/export-dossier', '/sync']
// Nombre de nouveaux essais pour une lecture (donc 3 tentatives au total)
const MAX_READ_RETRIES = 2

const originalFetch = window.fetch.bind(window)

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms))

const getTimeout = (url) =>
    LONG_REQUEST_PATTERNS.some(pattern => url.includes(pattern)) ? LONG_TIMEOUT_MS : DEFAULT_TIMEOUT_MS

// Prévient l'interface (composant ApiErrorToast) qu'une requête a échoué
const notifyProblem = (message) => {
    window.dispatchEvent(new CustomEvent('api-problem', { detail: { message } }))
}

const jsonErrorResponse = (status, message) => new Response(
    JSON.stringify({ status: 'error', error: message, message }),
    { status, headers: { 'Content-Type': 'application/json' } }
)

// Si le serveur répond autre chose que du JSON (ex : page HTML "504 Gateway Time-out"),
// on la remplace par une erreur JSON pour que les appels à response.json() ne plantent pas
const ensureJsonResponse = (response) => {
    const contentType = response.headers.get('content-type') || ''
    if (response.ok || contentType.includes('application/json')) return response
    let message = 'La requête n\'a pas pu aboutir.'
    if (response.status === 429) message = 'Trop de tentatives de connexion. Réessayez dans une minute.'
    else if (response.status >= 500) message = 'Le serveur est momentanément indisponible. Réessayez dans un instant.'
    return jsonErrorResponse(response.status, message)
}

const apiFetch = async (url, options = {}) => {
    const method = (options.method || 'GET').toUpperCase()
    const isRead = method === 'GET'
    const isLogin = url.startsWith(`${API_BASE_URL}/login`)
    const maxAttempts = isRead ? MAX_READ_RETRIES + 1 : 1

    const headers = new Headers(options.headers || {})
    const token = localStorage.getItem('sgdf_token')
    if (token && !headers.has('Authorization')) {
        headers.set('Authorization', `Bearer ${token}`)
    }

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        const controller = new AbortController()
        const timer = setTimeout(() => controller.abort(), getTimeout(url))

        try {
            const response = await originalFetch(url, { ...options, headers, signal: controller.signal })
            clearTimeout(timer)

            // Serveur momentanément indisponible (502, 503, 504) : on retente les lectures
            if (isRead && response.status >= 502 && attempt < maxAttempts) {
                await wait(1000 * attempt)
                continue
            }

            if (response.status === 401) {
                // Token expiré ou invalide : signal global (voir App.vue)
                window.dispatchEvent(new CustomEvent('session-expired'))
            } else if (response.status >= 500 && !isLogin) {
                notifyProblem(isRead
                    ? 'Le serveur rencontre un problème : certaines données n\'ont pas pu être chargées.'
                    : 'Le serveur rencontre un problème : la modification n\'a pas été enregistrée.')
            }
            return ensureJsonResponse(response)

        } catch (error) {
            clearTimeout(timer)
            // Après un délai dépassé, on ne retente pas : l'utilisateur a déjà attendu 15 s
            const timedOut = error.name === 'AbortError'
            if (attempt < maxAttempts && !timedOut) {
                await wait(1000 * attempt)
                continue
            }
            if (!isLogin) {
                notifyProblem(isRead
                    ? 'Connexion instable : impossible de charger les dernières données.'
                    : 'Connexion impossible : la modification n\'a pas été enregistrée. Réessayez quand le réseau revient.')
            }
            // On relance l'erreur comme avant : le code appelant garde ses données affichées
            throw error
        }
    }
}

window.fetch = (resource, options) => {
    // On ne surveille QUE les requêtes vers notre API (pour ne pas bloquer OpenStreetMap)
    if (typeof resource === 'string' && resource.startsWith(API_BASE_URL)) {
        return apiFetch(resource, options)
    }
    return originalFetch(resource, options)
}

// src/api/supabase.js

// Le temps réel Supabase est désactivé : il utilisait la clé secrète du projet,
// qui donne un accès total à la base et ne doit jamais être envoyée au navigateur
// (Supabase refuse d'ailleurs cette clé côté navigateur).
// Ce client inactif garde les mêmes méthodes pour que les stores fonctionnent sans changement.
const createDisabledChannel = () => ({
    on() { return this },
    subscribe() { return this },
    send() { return Promise.resolve('disabled') }
})

export const supabase = {
    channel: () => createDisabledChannel(),
    removeChannel: () => {}
}

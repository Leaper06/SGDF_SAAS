// src/stores/themeStore.js
import { ref } from 'vue'

// On regarde si un choix a déjà été fait dans le téléphone, sinon on met "false" (clair)
export const isDarkMode = ref(localStorage.getItem('sgdf_dark_mode') === 'true')

// Fonction pour initialiser l'affichage au chargement de l'application
export const initTheme = () => {
    if (isDarkMode.value) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }
}

// Fonction pour le bouton de la page Profil
export const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('sgdf_dark_mode', isDarkMode.value)
    initTheme()
}
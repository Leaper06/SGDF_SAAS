// src/stores/themeStore.js
import { ref } from 'vue'

const storedTheme = localStorage.getItem('polymaitrise_theme')
const initialDark = storedTheme === 'dark'

export const isDarkMode = ref(initialDark)

export const initTheme = () => {
    const stored = localStorage.getItem('polymaitrise_theme')
    const isDark = stored === 'dark'
    isDarkMode.value = isDark
    if (isDark) {
        document.documentElement.classList.add('dark')
    } else {
        document.documentElement.classList.remove('dark')
    }
}

// Initialisation globale automatique
initTheme()

// Fonction pour le bouton de la page Profil
export const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
    
    if (isDarkMode.value) {
        document.documentElement.classList.add('dark')
        localStorage.setItem('polymaitrise_theme', 'dark')
    } else {
        document.documentElement.classList.remove('dark')
        localStorage.setItem('polymaitrise_theme', 'light')
    }
}
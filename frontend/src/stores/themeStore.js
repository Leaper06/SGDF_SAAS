// src/stores/themeStore.js
import { ref } from 'vue'

const storedTheme = localStorage.getItem('polymaitrise_theme')
const initialDark = storedTheme === 'dark'

export const isDarkMode = ref(initialDark)

if (initialDark) {
    document.documentElement.classList.add('dark')
} else {
    document.documentElement.classList.remove('dark')
}

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
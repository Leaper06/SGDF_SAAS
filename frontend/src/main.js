import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router.js' 
import { initTheme } from './stores/themeStore.js'

// Restauration immédiate du thème (mode sombre/clair) au démarrage de l'application
initTheme()

const app = createApp(App)

app.use(router)

app.mount('#app')
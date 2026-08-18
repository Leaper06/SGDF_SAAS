import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import './style.css'
import App from './App.vue'
import router from './router.js' 
import { initTheme } from './stores/themeStore.js'

import { registerSW } from 'virtual:pwa-register'

// Enregistrement immédiat du Service Worker PWA
registerSW({ immediate: true })

// Restauration immédiate du thème (mode sombre/clair) au démarrage
initTheme()

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)

app.mount('#app')
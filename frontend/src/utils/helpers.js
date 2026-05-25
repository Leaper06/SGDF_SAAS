// src/utils/helpers.js

export const separerNomPrenom = (nomComplet) => {
    if (!nomComplet) return { nom: "Inconnu", prenom: "" }
    const textPropre = nomComplet.trim().replace(/\s+/g, ' ')
    const mots = textPropre.split(' ')
    if (mots.length === 1) return { nom: mots[0], prenom: "" }
    const premierMot = mots.shift()
    const resteDuNom = mots.join(' ')
    return { nom: premierMot, prenom: resteDuNom }
}

export const getTheme = (type) => {
  switch (type) {
    case 'jeu': return { border: 'border-[#e85d22]', textTime: 'text-[#e85d22]', bgBadge: 'bg-orange-50 text-[#e85d22]' }
    case 'repas': return { border: 'border-scoutBlue', textTime: 'text-scoutBlue', bgBadge: 'bg-blue-50 text-scoutBlue' }
    case 'spi': return { border: 'border-[#009ee0]', textTime: 'text-[#009ee0]', bgBadge: 'bg-cyan-50 text-[#009ee0]' }
    default: return { border: 'border-gray-400', textTime: 'text-gray-700', bgBadge: 'bg-gray-100 text-gray-500' }
  }
}

export const formatTypeLabel = (type) => {
  const labels = { 'jeu': 'Jeu / Anim', 'repas': 'Intendance', 'spi': 'Temps Spi', 'logistique': 'Logistique' }
  return labels[type] || 'Activité'
}

export const formatHeure = (dateTimeStr) => {
    return new Date(dateTimeStr).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

export const formatCourt = (d) => {
  const date = new Date(d)
  return `${date.toLocaleDateString('fr-FR', { weekday: 'short' }).replace('.', '')} ${date.getDate()}`
}

export const formatDay = (d) => new Date(d).toLocaleDateString('fr-FR', { day: '2-digit' })

export const formatWeekday = (d) => new Date(d).toLocaleDateString('fr-FR', { weekday: 'short' }).replace('.', '')

export const getRecipeIcon = (type) => {
  const t = (type || '').toLowerCase()
  if (t.includes('entrée')) return { emoji: '🥗', bg: 'bg-green-100', text: 'text-green-600' }
  if (t.includes('plat')) return { emoji: '🍝', bg: 'bg-orange-100', text: 'text-[#e45a27]' }
  if (t.includes('dessert') || t.includes('fruit')) return { emoji: '🍏', bg: 'bg-blue-100', text: 'text-blue-500' }
  return { emoji: '🧀', bg: 'bg-yellow-50', text: 'text-yellow-600' }
}
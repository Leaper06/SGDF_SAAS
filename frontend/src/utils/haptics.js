/**
 * Utilitaire de retour haptique (vibrations tactiles sur mobile)
 */
export function triggerHaptic(type = 'light') {
  if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
    try {
      if (type === 'light') {
        navigator.vibrate(12)
      } else if (type === 'medium') {
        navigator.vibrate(25)
      } else if (type === 'success') {
        navigator.vibrate([15, 50, 20])
      }
    } catch (e) {
      // Ignore si la vibration n'est pas autorisée/supportée sur l'appareil
    }
  }
}

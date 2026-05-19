/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: { 
        scoutViolet: '#5b2b82', 
        scoutOrange: '#e45a27',
        spiBlue: '#0284c7',
        lifeGray: '#f3f4f6',
        scoutBlue: '#004267',
        bgLight: '#f8fafc',
        ecoGreen: '#16a34a'
      }
    },
  },
  plugins: [],
}
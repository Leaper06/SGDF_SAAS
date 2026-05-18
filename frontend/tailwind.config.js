/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        scoutViolet: '#5b2b82',
        scoutOrange: '#e45a27',
      }
    },
  },
  plugins: [],
}
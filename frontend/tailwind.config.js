/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#0f1117',
          secondary: '#1a1d27',
          tertiary: '#252836'
        },
        accent: {
          teal: '#1D9E75',
          blue: '#378ADD',
          amber: '#BA7517',
          red: '#E24B4A',
          green: '#9FE1CB'
        }
      }
    },
  },
  plugins: [],
}

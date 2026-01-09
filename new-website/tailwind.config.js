/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bitcoin: {
          orange: '#F7931A',
          gold: '#FFD700',
          darkGold: '#B8860B',
          lightGold: '#FFF8DC',
        },
        historical: {
          parchment: '#F4ECD8',
          sepia: '#704214',
          antique: '#8B7355',
        }
      },
      fontFamily: {
        'serif': ['Georgia', 'Cambria', 'Times New Roman', 'serif'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'book-texture': "url('/textures/paper.jpg')",
        'gold-gradient': 'linear-gradient(135deg, #FFD700 0%, #F7931A 100%)',
        'warm-gradient': 'linear-gradient(135deg, #F4ECD8 0%, #FFF8DC 100%)',
      },
      boxShadow: {
        'book': '0 10px 40px rgba(0, 0, 0, 0.2), 0 2px 8px rgba(0, 0, 0, 0.1)',
        'page': '0 4px 6px rgba(0, 0, 0, 0.1)',
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}",
    "./src/app/**/*.{js,ts,jsx,tsx}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        xbox: {
          primary: '#107C10',
          background: '#0E0E0E',
          accent: '#1F1F1F'
        },
        playstation: {
          primary: '#003791',
          background: '#F2F2F2',
          accent: '#E5E5E5'
        },
        powderblue: {
          light: '#B0E0E6',
          dark: '#4682B4'
        }
      },
      borderRadius: {
        '2xl': '1rem',
      },
      boxShadow: {
        'soft': '0 4px 6px rgba(0, 0, 0, 0.1)'
      },
      animation: {
        marquee: 'marquee 15s linear infinite'
      },
      keyframes: {
        marquee: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(-100%)' }
        }
      }
    }
  },
  plugins: [],
}

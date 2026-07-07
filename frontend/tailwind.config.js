/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B0B0F',
        surface: '#1A1B23',
        primary: '#6366F1',
        secondary: '#EC4899',
        textMain: '#F8FAFC',
        textMuted: '#94A3B8',
        accent: '#8B5CF6'
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'hero-glow': 'conic-gradient(from 180deg at 50% 50%, #6366F133 0deg, #EC489933 180deg, #8B5CF633 360deg)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'glow': '0 0 20px rgba(99, 102, 241, 0.3)',
      }
    },
  },
  plugins: [],
}

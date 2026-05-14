/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './*.html',
    './services/*.html',
    './blog/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Manrope', 'system-ui', 'sans-serif'],
        display: ['Raleway', 'system-ui', 'sans-serif'],
      },
      colors: {
        ink: {
          900: '#ffffff',
          800: '#f8fafc',
          700: '#f1f5f9',
          600: '#e2e8f0',
          500: '#cbd5e1',
        },
        gold: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#4ade80',
          400: '#22c55e',
          500: '#16a34a',
          600: '#15803d',
          700: '#166534',
        },
        warm: {
          50: '#ffffff',
          100: '#f0ede8',
        },
      },
    },
  },
  plugins: [],
}

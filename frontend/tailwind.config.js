/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        indigo: {
          50: '#f0f9ff',
          600: '#4f46e5',
          700: '#4338ca',
        }
      },
    },
  },
  plugins: [],
}

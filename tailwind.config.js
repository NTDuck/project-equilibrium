/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  purge: ['./app/templates/*.{html, js}'],
  content: ['./app/templates/*.{html, js}'],
  theme: {
    extend: {},
  },
  plugins: [],
}

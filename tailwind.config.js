/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    './app/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        // monkeytype's serika_dark theme: https://github.com/monkeytypegame/monkeytype/blob/27ff20da5152f9c9a90a409a2f9e8d4bdd689187/frontend/static/themes/serika_dark.css#L4
        'bg-color': '#323437',
        'main-color': '#e2b714',
        'caret-color': '#e2b714',
        'sub-color': '#646669',
        'sub-alt-color': '#2c2e31',
        'text-color': '#d1d0c5',
        'error-color': '#ca4754',
        'error-extra-color': '#7e2a33',
        'colorful-error-color': '#ca4754',
        'colorful-error-extra-color': '#7e2a33',
      },
      fontFamily: {
        'Lexend-Deca': 'Lexend Deca'
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}

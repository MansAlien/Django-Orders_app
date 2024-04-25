/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'media',
  content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js',

  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('flowbite/plugin')
  ]
}



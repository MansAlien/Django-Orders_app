/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js',

  ],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
        rubik: ['Rubik', 'sans-serif'],
      },
    },
  },
  plugins: [
      require('flowbite/plugin')
  ]
}



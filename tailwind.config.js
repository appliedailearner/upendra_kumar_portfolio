/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./*.html", "./blog/**/*.html", "./js/**/*.js"],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: '#0078D4',
                secondary: '#7c3aed',
                dark: '#0a0a0f',
                navy: '#0f0f23',
            }
        }
    },
    plugins: [],
}

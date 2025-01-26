/** @type {import('tailwindcss').Config} */
const config = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'custom-purple-gradient': `
          linear-gradient(180deg, #000 0%, rgba(0, 0, 0, 0.1) 45%),
          radial-gradient(51% 51% at -11% 9%, #a657ffb3 1%, #a657ff00 100%),
          radial-gradient(51% 67% at 115% 96%, #a657ffb3 0%, #a657ff00 100%),
          radial-gradient(50% 66% at 50% 50%, #f2a6ffa3 0%, #f2a6ff00 100%),
          radial-gradient(22% 117% at 2% 87%, #b300f400 20%, #b300f494 100%),
          linear-gradient(0deg, #7c61ffa3, #7c61ffa3)
        `,
      },
    },
  },
  plugins: [],
}

export default config;
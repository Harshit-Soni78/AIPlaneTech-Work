/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#000000",
        primary: "#3B82F6", 
        textPrimary: "#E5E7EB",
        accent: "#2563EB",
      },
      borderRadius: {
        button: "0.75rem",
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
// #3B82F6
// #A3E635
// #000000
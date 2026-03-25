import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "#070c11",
        surface: "#111922",
        panel: "#16222f",
        border: "#233448",
        accent: "#7dc0ff",
        success: "#7ff0b0",
        warning: "#f0c36d",
        danger: "#ff7a7a",
        text: "#e7eef7",
        muted: "#8ca2ba"
      },
      fontFamily: {
        sans: ["var(--font-sans)", "Segoe UI", "sans-serif"],
        mono: ["var(--font-mono)", "Consolas", "monospace"]
      },
      backgroundImage: {
        grid: "linear-gradient(rgba(125,192,255,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(125,192,255,0.06) 1px, transparent 1px)"
      },
      backgroundSize: {
        grid: "32px 32px"
      },
      boxShadow: {
        panel: "0 30px 80px rgba(4, 9, 17, 0.45)"
      }
    }
  },
  plugins: []
};

export default config;


import type { Config } from "tailwindcss";

export default {
  content: ["./frontend/app/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: "#192c3d",
        muted: "#667788",
        line: "#e6ebef",
        canvas: "#f5f7f8",
        navy: "#173b5e",
        teal: "#2d7f79",
      },
    },
  },
  plugins: [],
} satisfies Config;

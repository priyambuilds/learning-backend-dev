import { FlatCompat } from "@eslint/eslintrc";
import js from "@eslint/js";
import unicorn from "eslint-plugin-unicorn";
import betterTailwind from "eslint-plugin-better-tailwindcss";

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
});

export default [
  // Baseline recommended JS rules
  js.configs.recommended,

  // Next.js & TypeScript best practices and Prettier harmony
  ...compat.extends("next/core-web-vitals", "next/typescript", "prettier"),

  // unicorn: modern JS/TS best practices
  {
    plugins: { unicorn },
    rules: {
      "unicorn/prevent-abbreviations": "off", // less strict for framework naming
      "unicorn/filename-case": [
        "error",
        {
          cases: {
            camelCase: true,
            pascalCase: true,
          },
        },
      ],
    },
  },

  // Tailwind v4 compatible linting
  betterTailwind.configs.recommended,

  // Ignores, project rules, settings
  {
    ignores: ["components/ui/**", "node_modules/**", ".next/**"],
    rules: {
      "no-undef": "off",
      // add further global overrides as desired
    },
  },

  // TypeScript-specific tweaks
  {
    files: ["**/*.ts", "**/*.tsx"],
    rules: {
      "no-undef": "off",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
    },
  },
];

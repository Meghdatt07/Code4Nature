import type { Config } from 'tailwindcss';
const config: Config = {
  content:['./app/**/*.{ts,tsx}','./components/**/*.{ts,tsx}','./lib/**/*.{ts,tsx}'],
  theme:{extend:{fontFamily:{sans:['Inter','ui-sans-serif','system-ui']},boxShadow:{glow:'0 0 0 1px rgba(165, 214, 186, .12), 0 16px 60px rgba(0,0,0,.24)'}}},
  plugins:[]
}; export default config;

import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { site } from './src/site.config.ts';

// Les liens internes sont relatifs (boutique.html, contact.html...) :
// le site fonctionne a la racine d'un domaine comme dans un sous-dossier.
export default defineConfig({
  site: site.url,
  markdown: { smartypants: false },
  build: {
    format: 'file',
    inlineStylesheets: 'always',
  },
  integrations: [
    sitemap({
      filter: (page) => site.salonDeThe || !page.includes('salon-de-the'),
    }),
  ],
});

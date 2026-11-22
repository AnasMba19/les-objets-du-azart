# Les objets du Az'art

Site vitrine de la boutique Les objets du Az'art, a Alencon : brocante,
creations faites main et friperie. Les clients voient les pieces et
contactent la boutique sur WhatsApp.

## Technique

- [Astro](https://astro.build), site statique, aucune base de donnees.
- Le catalogue est un dossier de fiches Markdown : `src/content/objets/`.
- Hebergement gratuit sur GitHub Pages, publication automatique a chaque
  modification de la branche `main` (`.github/workflows/deploy.yml`).
- Les liens internes sont relatifs : le site marche sur `*.github.io` comme
  sur un nom de domaine.

## Pages

Accueil, La Boutique (filtres par univers, une fiche par objet), Nos Services,
Nous chez Vous, Flaneries a Alencon, Contact. La page Salon de The est
construite mais masquee (`salonDeThe` dans `src/site.config.ts`).

## Travailler en local

```bash
npm install
npm run dev     # http://localhost:4321
npm run build   # genere dist/
```

## Mettre a jour le contenu

Voir [AGENTS.md](AGENTS.md) : c'est aussi le guide suivi par l'assistant IA
qui fait les mises a jour a la demande de la boutique.

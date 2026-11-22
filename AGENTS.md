# Guide pour l'assistant qui met a jour le site

Ce depot contient le site de la boutique Les objets du Az'art (Alencon).
Mouna, la gerante, te demande des modifications en langage courant.
Chaque modification poussee sur la branche `main` publie le site automatiquement
en une a deux minutes.

## Ce que tu peux modifier sans demander

| Demande de Mouna | Fichier a toucher |
|---|---|
| Ajouter, modifier, retirer un objet | `src/content/objets/<nom-court>.md` |
| Marquer un objet reserve ou vendu | champ `statut` du fichier de l'objet |
| Ajouter une photo client (Nous chez Vous) | `src/content/nous-chez-vous.json` + photo dans `public/images/nous-chez-vous/` |
| Changer telephone, adresse, horaires, liens | `src/site.config.ts` |
| Activer la page Salon de The | `salonDeThe: true` dans `src/site.config.ts` |

Ne touche ni a `src/layouts`, ni a `src/components`, ni a `src/styles`, ni a
`.github` sans l'accord explicite de Batall.

## Ajouter un objet

1. Enregistre les photos dans `public/images/objets/`, en JPG ou WebP,
   1600 px de large au maximum, nommees `<nom-court>-1.jpg`, `<nom-court>-2.jpg`...
2. Cree `src/content/objets/<nom-court>.md` (minuscules, tirets, sans accents) :

```md
---
titre: Commode en merisier
categorie: brocante        # brocante | tresors | atelier | friperie
statut: disponible         # disponible | reserve | vendu
prix: 240                  # en euros, a supprimer pour "Prix sur demande"
dimensions: "L 110 x P 50 x H 85 cm"
epoque: "Fin XIXe"
photos:
  - images/objets/commode-merisier-1.jpg
  - images/objets/commode-merisier-2.jpg
emballageCadeau: false     # true pour les creations de l'atelier
ajoute: 2026-11-22
---
Deux ou trois phrases simples et chaleureuses qui donnent envie.
```

3. Verifie avec `npm run build` que le site se construit, puis pousse sur `main`.

## Regles de contenu

- Ton : chaleureux, simple, vouvoiement. Pas de superlatifs en cascade.
- Pas de tiret long, pas de guillemets typographiques : apostrophe droite `'`.
- Les photos d'objets a vendre doivent montrer l'objet reel. L'IA peut
  ameliorer une vraie photo (lumiere, fond, recadrage), jamais inventer l'objet.
- Un objet vendu reste en ligne avec `statut: vendu` quelques semaines,
  puis on supprime son fichier et ses photos.
- Quand tous les objets d'exemple (`exemple: true`) ont ete remplaces,
  supprime-les et passe `bandeauExemples: false` dans `src/site.config.ts`.

## Photos libres de droits

Pour une photo d'ambiance ou d'illustration, ajoute une ligne dans
`scripts/images.json` avec l'identifiant d'une photo Unsplash (fin de l'adresse
de la photo), le chemin de sortie et le format (`1:1` objets, `4:3` galerie,
`4:5` accueil). A la publication, le serveur la telecharge, la retouche
(tons chauds, recadrage) et l'enregistre dans `public/images/`.
Une photo d'illustration sur une fiche objet garde `exemple: true` :
le site affiche alors la mention "Photo d'illustration".

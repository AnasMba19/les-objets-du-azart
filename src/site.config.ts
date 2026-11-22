// Reglages generaux du site. C'est le seul fichier a modifier pour
// changer les coordonnees, les horaires ou activer une page.

export const site = {
  nom: "Les objets du Az'art",
  accroche: 'Brocante, créations et friperie à Alençon',
  url: 'https://anasmba19.github.io/les-objets-du-azart',

  ville: 'Alençon',
  codePostal: '61000',
  adresse: '', // a completer, ex. '12 rue ..., 61000 Alençon'

  telephone: '06 73 48 73 05',
  whatsapp: '33673487305', // format international, sans le +
  email: 'lesobjetsduazart@gmail.com',

  // Laisser vide tant que les horaires ne sont pas confirmes.
  horaires: [] as { jours: string; heures: string }[],

  // Lien vers la fiche Google de la boutique (pour les avis).
  avisGoogle: 'https://www.google.com/search?q=Les+objets+du+Az%27art+Alen%C3%A7on',
  instagram: '',
  facebook: '',

  // Page Salon de the : construite mais masquee. Passer a true pour l'activer.
  salonDeThe: false,

  // Affiche un bandeau tant que le catalogue contient des objets d'exemple.
  bandeauExemples: true,
};

export const categories = {
  brocante: {
    nom: 'La Brocante',
    court: 'Brocante',
    texte: 'Mobilier, vaisselle ancienne, luminaires, miroirs, lustres et objets de curiosité.',
    illustration: 'lustre',
  },
  tresors: {
    nom: 'Les Trésors de Mouna',
    court: 'Trésors',
    texte: "Les pièces coup de cœur : plus rares, d'exception ou chargées d'une histoire particulière.",
    illustration: 'malle',
  },
  atelier: {
    nom: "L'Atelier Créatif",
    court: 'Atelier',
    texte: 'Les créations faites main : bougies, luminaires et abat-jours sur mesure, plâtre et céramique.',
    illustration: 'bougie',
  },
  friperie: {
    nom: 'Friperie & Accessoires',
    court: 'Friperie',
    texte: "Le coin mode éco-responsable : vêtements vintage, pièces rétro et accessoires d'époque.",
    illustration: 'robe',
  },
} as const;

export type CategorieId = keyof typeof categories;

export const wa = (texte: string) =>
  `https://wa.me/${site.whatsapp}?text=${encodeURIComponent(texte)}`;

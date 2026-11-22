import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

const objets = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/objets' }),
  schema: z.object({
    titre: z.string(),
    categorie: z.enum(['brocante', 'tresors', 'atelier', 'friperie']),
    statut: z.enum(['disponible', 'reserve', 'vendu']).default('disponible'),
    prix: z.number().optional(), // en euros ; vide = prix sur demande
    dimensions: z.string().optional(),
    epoque: z.string().optional(),
    photos: z.array(z.string()).default([]), // chemins depuis public/, ex. images/objets/buffet-1.jpg
    illustration: z.string().optional(), // dessin affiche si pas de photo
    emballageCadeau: z.boolean().default(false),
    ajoute: z.coerce.date(),
    exemple: z.boolean().default(false),
  }),
});

const chezVous = defineCollection({
  loader: file('./src/content/nous-chez-vous.json'),
  schema: z.object({
    photo: z.string().optional(),
    illustration: z.string().optional(),
    legende: z.string(),
    prenom: z.string().optional(),
    ville: z.string().optional(),
    exemple: z.boolean().default(false),
  }),
});

const evenements = defineCollection({
  loader: file('./src/content/evenements.json'),
  schema: z.object({
    date: z.string(),
    titre: z.string(),
    lieu: z.string().optional(),
    texte: z.string().optional(),
    aConfirmer: z.boolean().default(false),
  }),
});

export const collections = { objets, chezVous, evenements };

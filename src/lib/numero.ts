import type { CollectionEntry } from 'astro:content';

// Numero de lot stable : ordre d'arrivee dans le catalogue.
export function numeros(tous: CollectionEntry<'objets'>[]) {
  const tri = [...tous].sort((a, b) => a.data.ajoute.getTime() - b.data.ajoute.getTime() || a.id.localeCompare(b.id));
  return new Map(tri.map((o, i) => [o.id, String(i + 1).padStart(2, '0')]));
}

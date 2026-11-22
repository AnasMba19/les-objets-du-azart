import { existsSync } from 'node:fs';
import { join } from 'node:path';

// Garde seulement les photos presentes dans public/ : tant qu'une photo
// n'est pas encore telechargee, le dessin prend le relais.
export const dispo = (p?: string) => !!p && existsSync(join(process.cwd(), 'public', p));
export const photosDispo = (ps: string[] = []) => ps.filter(dispo);

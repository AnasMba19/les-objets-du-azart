"""Telecharge les photos libres de droits (licence Unsplash) listees dans
scripts/images.json et les retouche pour l'ambiance de la boutique :
recadrage, tons chauds, contraste doux, leger vignettage, format WebP.
Ne retelecharge pas une image deja presente."""
import io, json, sys, urllib.request
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
LARGEUR = {"1:1": 1200, "4:5": 1200, "4:3": 1400}

def recadre(img, ratio):
    w, h = (int(x) for x in ratio.split(":"))
    return ImageOps.fit(img, (LARGEUR[ratio], round(LARGEUR[ratio] * h / w)), Image.LANCZOS, centering=(0.5, 0.45))

def chaud(img):
    r, g, b = img.split()
    r = r.point(lambda v: min(255, int(v * 1.04 + 4)))
    b = b.point(lambda v: int(v * 0.92))
    img = Image.merge("RGB", (r, g, b))
    img = ImageEnhance.Color(img).enhance(0.88)
    img = ImageEnhance.Contrast(img).enhance(1.06)
    return img

def vignette(img, force=0.28):
    w, h = img.size
    masque = Image.new("L", (w, h), 0)
    interieur = Image.new("L", (int(w * 0.8), int(h * 0.8)), 255)
    masque.paste(interieur, (int(w * 0.1), int(h * 0.1)))
    masque = masque.filter(ImageFilter.GaussianBlur(min(w, h) // 5))
    sombre = ImageEnhance.Brightness(img).enhance(1 - force)
    return Image.composite(img, sombre, masque)

def main():
    items = json.loads((ROOT / "scripts" / "images.json").read_text())
    fait = 0
    for it in items:
        cible = PUBLIC / it["out"]
        if cible.exists():
            continue
        url = f"https://unsplash.com/photos/{it['id']}/download?force=true&w=2000"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            data = urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:
            print(f"ECHEC {it['id']}: {e}", file=sys.stderr)
            continue
        img = Image.open(io.BytesIO(data)).convert("RGB")
        img = vignette(chaud(recadre(img, it["ratio"])))
        cible.parent.mkdir(parents=True, exist_ok=True)
        img.save(cible, "WEBP", quality=80, method=6)
        print(f"ok {it['out']} ({cible.stat().st_size // 1024} Ko)")
        fait += 1
    print(f"{fait} image(s) traitee(s)")

if __name__ == "__main__":
    main()

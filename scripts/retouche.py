"""Cherche des photos libres sur Wikimedia Commons (domaine public, CC0,
CC BY, CC BY-SA) d'apres scripts/images.json, puis les retouche pour
l'ambiance de la boutique : recadrage, tons chauds, contraste doux,
leger vignettage, format WebP. Les credits sont ecrits dans
src/content/credits.json. Une image deja presente n'est pas refaite."""
import io, json, re, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
CREDITS = ROOT / "src" / "content" / "credits.json"
UA = "LesObjetsDuAzart-site/1.0 (https://github.com/AnasMba19/les-objets-du-azart)"
LARGEUR = {"1:1": 1200, "4:5": 1200, "4:3": 1400}
LICENCES = ("cc0", "public domain", "pd", "cc by", "cc-by")
JOURNAL = []

def log(m):
    print(m)
    JOURNAL.append(m)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def texte(v):
    return re.sub(r"<[^>]+>", "", v or "").strip()

def candidats(recherche):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": f"{recherche} filetype:bitmap", "gsrnamespace": "6", "gsrlimit": "30",
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiurlwidth": "2000",
    }
    data = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)))
    pages = sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata", {})
        lic = texte(meta.get("LicenseShortName", {}).get("value", "")).lower()
        if ii.get("mime") != "image/jpeg" or ii.get("width", 0) < 1200 or ii.get("height", 0) < 900:
            continue
        if not lic.startswith(LICENCES) or "nc" in lic or "nd" in lic:
            continue
        cat = texte(meta.get("Categories", {}).get("value", "")).lower()
        if any(m in cat for m in ("paintings", "drawings", "engravings", "logos")):
            continue
        yield {
            "url": ii.get("thumburl") or ii["url"],
            "page": ii.get("descriptionurl"),
            "titre": p["title"].removeprefix("File:"),
            "auteur": texte(meta.get("Artist", {}).get("value", "")) or "Auteur inconnu",
            "licence": texte(meta.get("LicenseShortName", {}).get("value", "")),
        }

def recadre(img, ratio):
    w, h = (int(x) for x in ratio.split(":"))
    return ImageOps.fit(img, (LARGEUR[ratio], round(LARGEUR[ratio] * h / w)), Image.LANCZOS, centering=(0.5, 0.45))

def chaud(img):
    r, g, b = img.split()
    r = r.point(lambda v: min(255, int(v * 1.04 + 4)))
    b = b.point(lambda v: int(v * 0.92))
    img = Image.merge("RGB", (r, g, b))
    img = ImageEnhance.Color(img).enhance(0.88)
    return ImageEnhance.Contrast(img).enhance(1.06)

def vignette(img, force=0.28):
    w, h = img.size
    masque = Image.new("L", (w, h), 0)
    masque.paste(Image.new("L", (int(w * 0.8), int(h * 0.8)), 255), (int(w * 0.1), int(h * 0.1)))
    masque = masque.filter(ImageFilter.GaussianBlur(min(w, h) // 5))
    return Image.composite(img, ImageEnhance.Brightness(img).enhance(1 - force), masque)

def apercu(it, liste):
    """Planche des 8 premiers candidats, pour choisir le rang."""
    from PIL import ImageDraw
    W = 360
    planche = Image.new("RGB", (4 * W, 2 * (W + 26)), (20, 20, 20))
    d = ImageDraw.Draw(planche)
    for i, c in enumerate(liste[:8]):
        try:
            im = Image.open(io.BytesIO(get(c["url"].replace("/2000px-", "/400px-")))).convert("RGB")
        except Exception:
            continue
        im.thumbnail((W, W))
        x, y = (i % 4) * W, (i // 4) * (W + 26)
        planche.paste(im, (x, y))
        d.text((x + 6, y + W + 6), f"{i} {c['titre'][:40]}", fill=(230, 220, 200))
    out = PUBLIC / "apercus" / (Path(it["out"]).stem + ".jpg")
    out.parent.mkdir(parents=True, exist_ok=True)
    planche.save(out, quality=80)
    log(f"apercu {out.name} ({len(liste)} candidats)")

def main():
    items = json.loads((ROOT / "scripts" / "images.json").read_text())
    credits = json.loads(CREDITS.read_text()) if CREDITS.exists() else []
    connus = {c["id"] for c in credits}
    fait = 0
    for it in items:
        cible = PUBLIC / it["out"]
        if cible.exists():
            continue
        try:
            liste = list(candidats(it["recherche"]))
        except Exception as e:
            log(f"ECHEC recherche {it['recherche']}: {e}")
            continue
        if it.get("apercu"):
            apercu(it, liste)
            continue
        if not it.get("fichier") and len(liste) <= it.get("rang", 0):
            log(f"AUCUN resultat pour {it['recherche']} ({len(liste)})")
            continue
        c = liste[it.get("rang", 0)]
        if it.get("fichier"):
            c = next((x for x in liste if x["titre"] == it["fichier"]), None)
            if not c:
                log(f"AUCUN fichier {it['fichier']}")
                continue
        try:
            img = Image.open(io.BytesIO(get(c["url"]))).convert("RGB")
        except Exception as e:
            log(f"ECHEC telechargement {c['url']}: {e}")
            continue
        img = vignette(chaud(recadre(img, it["ratio"])))
        cible.parent.mkdir(parents=True, exist_ok=True)
        img.save(cible, "WEBP", quality=80, method=6)
        credits = [x for x in credits if x["id"] != it["out"]]
        credits.append({"id": it["out"], "sujet": it["sujet"], "titre": c["titre"], "auteur": c["auteur"], "licence": c["licence"], "source": c["page"]})
        log(f"ok {it['out']} <- {c['titre']} ({c['licence']})")
        fait += 1
    CREDITS.write_text(json.dumps(sorted(credits, key=lambda x: x["id"]), ensure_ascii=False, indent=1) + "\n")
    log(f"{fait} image(s) traitee(s)")
    (PUBLIC / "journal-photos.txt").write_text("\n".join(JOURNAL) + "\n")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Baut die Website aus pages/ + partials/ + static/ nach dist/.

- Kopf, Navigation, Footer und Kontakt-Button kommen aus partials/ und
  werden in jede Seite eingesetzt.
- Firmendaten (Telefon, Adresse, ...) stehen nur in BUSINESS unten und
  ersetzen Platzhalter wie {{PHONE}} überall.
- Strukturierte Daten (Google), sitemap.xml und eine Prüfung aller
  internen Links werden automatisch erzeugt.

Aufruf:  python3 build.py
"""
import html
import json
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
PAGES, PARTIALS, STATIC, DIST = ROOT / "pages", ROOT / "partials", ROOT / "static", ROOT / "dist"

SITE = "https://canex-studio.de"

# ---------- Firmendaten: nur hier ändern ----------
BUSINESS = {
    "NAME": "CANEX Hair Studio",
    "OWNER": "Caner Kahriman",
    "STREET": "Kaiserstraße 52",
    "ZIP": "45468",
    "CITY": "Mülheim an der Ruhr",
    "PHONE": "0208 38582992",          # Salon (Festnetz) – wie im Google-Profil
    "PHONE_TEL": "+4920838582992",
    "PHONE_INTL": "+49 208 38582992",
    "MOBILE": "0157 37147882",         # Handy / WhatsApp
    "MOBILE_TEL": "+4915737147882",
    "EMAIL": "info@canex-studio.de",
    "WHATSAPP": "https://wa.me/4915737147882",
    "INSTAGRAM": "https://www.instagram.com/canexstudio_/",
    "TIKTOK": "https://www.tiktok.com/@canex_studio",
    "SITE": SITE,
}
OPENING_HOURS = [
    (["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "09:00", "19:00"),
    (["Saturday"], "09:00", "16:00"),
]


def business_jsonld():
    b = BUSINESS
    return {
        "@context": "https://schema.org",
        "@type": "HairSalon",
        "@id": SITE + "/#salon",
        "name": b["NAME"],
        "url": SITE + "/",
        "image": SITE + "/assets/img/og-image.jpg",
        "logo": SITE + "/assets/img/canex-logo-dark.png",
        "telephone": b["PHONE_INTL"],
        "email": b["EMAIL"],
        "priceRange": "€",
        "sameAs": [b["INSTAGRAM"], b["TIKTOK"]],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": b["STREET"],
            "postalCode": b["ZIP"],
            "addressLocality": b["CITY"],
            "addressCountry": "DE",
        },
        "areaServed": {"@type": "City", "name": b["CITY"]},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c}
            for d, o, c in OPENING_HOURS
        ],
    }


META_RE = re.compile(r"\A\s*<!--(.*?)-->", re.S)
FAQ_RE = re.compile(r'<details class="faq-item">\s*<summary>(.*?)</summary>(.*?)</details>', re.S)
TAG_RE = re.compile(r"<[^>]+>")


def parse_page(path):
    text = path.read_text(encoding="utf-8")
    m = META_RE.match(text)
    if not m:
        sys.exit(f"Fehler: {path.name} hat keinen Meta-Block am Anfang.")
    meta = {}
    for line in m.group(1).strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    for key in ("title", "description", "path"):
        if key not in meta:
            sys.exit(f"Fehler: {path.name} – '{key}' fehlt im Meta-Block.")
    return meta, text[m.end():].lstrip("\n")


def plain(s):
    return re.sub(r"\s+", " ", html.unescape(TAG_RE.sub(" ", s))).strip()


def build_jsonld(meta, body):
    blocks = []
    url = SITE + meta["path"]
    if meta["path"] == "/":
        blocks.append(business_jsonld())
    else:
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Start", "item": SITE + "/"}]
        crumbs.append({"@type": "ListItem", "position": 2, "name": meta.get("breadcrumb", meta["title"]), "item": url})
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs})
    if meta.get("service"):
        svc = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": meta["service"],
            "serviceType": meta.get("service_type", meta["service"]),
            "url": url,
            "areaServed": {"@type": "City", "name": BUSINESS["CITY"]},
            "provider": {"@id": SITE + "/#salon", "@type": "HairSalon", "name": BUSINESS["NAME"],
                         "telephone": BUSINESS["PHONE_INTL"],
                         "address": business_jsonld()["address"]},
        }
        if meta.get("price"):
            svc["offers"] = {"@type": "Offer", "priceCurrency": "EUR",
                             "priceSpecification": {"@type": "PriceSpecification",
                                                    "minPrice": meta["price"], "priceCurrency": "EUR"}}
        blocks.append(svc)
    faqs = FAQ_RE.findall(body)
    if faqs:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": plain(q),
                 "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                for q, a in faqs
            ],
        })
    return "\n".join(
        '  <script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False, indent=2) + "\n  </script>"
        for b in blocks
    )


def fill(text, values):
    def rep(m):
        key = m.group(1)
        if key not in values:
            sys.exit(f"Fehler: unbekannter Platzhalter {{{{{key}}}}}")
        return values[key]
    return re.sub(r"\{\{([A-Za-z_]+)\}\}", rep, text)


def out_file(path):
    if path == "/":
        return DIST / "index.html"
    if path.endswith(".html"):
        return DIST / path.lstrip("/")
    return DIST / path.strip("/") / "index.html"


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(STATIC, DIST)

    head, header, footer = ((PARTIALS / f).read_text(encoding="utf-8") for f in ("head.html", "header.html", "footer.html"))
    version = time.strftime("%Y%m%d%H%M")
    sitemap = []

    for page in sorted(PAGES.glob("*.html")):
        meta, body = parse_page(page)
        robots = meta.get("robots", "index, follow")
        values = dict(BUSINESS)
        values.update({
            "title": html.escape(meta["title"], quote=True),
            "description": html.escape(meta["description"], quote=True),
            "canonical": SITE + meta["path"],
            "robots": robots,
            "version": version,
            "preload": f'<link rel="preload" href="{meta["preload"]}" as="image">' if meta.get("preload") else "",
            "jsonld": "",
        })
        layout = meta.get("layout", "default")
        if layout == "bare":
            doc = head + body + "</body>\n</html>\n"
        else:
            doc = head + header + body + footer
        values["jsonld"] = fill(build_jsonld(meta, body), values)
        doc = fill(doc, values)
        if "{{" in doc:
            sys.exit(f"Fehler: nicht ersetzter Platzhalter in pages/{page.name}")
        target = out_file(meta["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(doc, encoding="utf-8")
        if robots.startswith("index"):
            sitemap.append((meta["path"], meta.get("priority", "0.8")))
        print(f"  {meta['path']:45} ← pages/{page.name}")

    today = time.strftime("%Y-%m-%d")
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, prio in sitemap:
        xml.append(f"  <url><loc>{SITE}{p}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    xml.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(xml) + "\n", encoding="utf-8")

    # Interne Links prüfen
    broken = []
    for f in DIST.rglob("*.html"):
        for href in re.findall(r'(?:href|src)="(/[^"#?]*)', f.read_text(encoding="utf-8")):
            t = DIST / href.lstrip("/")
            if href.endswith("/"):
                t = t / "index.html"
            if not t.exists():
                broken.append(f"{f.relative_to(DIST)} → {href}")
    fonts_missing = [b for b in broken if "/assets/fonts/" in b]
    broken = [b for b in broken if "/assets/fonts/" not in b]
    if broken:
        print("\nFehlerhafte interne Links:\n  " + "\n  ".join(sorted(set(broken))))
        sys.exit(1)
    if fonts_missing:
        print("  (Hinweis: Schriften fehlen lokal – werden beim Upload ergänzt)")
    print(f"\nFertig: {len(sitemap)} Seiten in der Sitemap, keine defekten Links.")


if __name__ == "__main__":
    main()

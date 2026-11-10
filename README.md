# CANEX Hair Studio – Website (canex-studio.de)

Statische Website (HTML/CSS/JS) für CANEX Hair Studio, Friseur & Barber in
Mülheim an der Ruhr. Jede Änderung auf `main` wird automatisch gebaut und per
SFTP zu IONOS hochgeladen (`.github/workflows/deploy.yml`).

## Aufbau

```
pages/       Inhalte der einzelnen Seiten (Meta-Block oben: Titel, Beschreibung, URL)
partials/    head.html, header.html (Menü), footer.html (Footer + Kontakt-Button)
static/      Bilder, CSS, JS, favicon, robots.txt, .htaccess – wird 1:1 kopiert
build.py     setzt alles zu dist/ zusammen, erzeugt sitemap.xml und Google-Daten,
             prüft interne Links. Firmendaten (Telefon, Adresse …) stehen NUR hier.
```

Lokal bauen: `python3 build.py` → Ergebnis in `dist/`.

## Seiten und Keywords

| Seite | URL | Hauptkeyword |
|---|---|---|
| Startseite | `/` | Friseur / Barber Mülheim an der Ruhr |
| Herrenhaarschnitt | `/herrenhaarschnitt-muelheim/` | haarschnitt männer, herren haarschnitt |
| Fade & Übergang | `/fade-haarschnitt-muelheim/` | männer haarschnitt mit übergang, fade |
| Bart & Rasur | `/bart-muelheim/` | bart schneiden, bart rasur |
| Kinder & Jungs | `/kinderhaarschnitt-muelheim/` | haarschnitt jungs, kinderhaarschnitt |
| Lange Haare & Locken | `/lange-haare-locken-maenner-muelheim/` | männer haarschnitt lang, locken schneiden mann |
| Preise | `/preise/` | haarschnitt preis, haare schneiden preise |

## Upload-Secrets (GitHub → Settings → Secrets and variables → Actions)

`SFTP_USER` (su967145, auf /public beschränkt) und `SFTP_PASSWORD`.

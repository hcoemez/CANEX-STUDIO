# CANEX Hair Studio – Website (canex-studio.de)

Neu aufgebaute Fassung der früheren Lovable-Seite: reines HTML/CSS/JavaScript,
kein Baukasten, kein Build-Schritt. Jede Änderung auf dem Branch `main` wird
automatisch per SFTP in den IONOS-Ordner `/public` hochgeladen.

## Aufbau

```
site/                    ← alles hier drin geht 1:1 online
  index.html             Startseite (alle Abschnitte)
  impressum/index.html   Impressum
  datenschutz/index.html Datenschutzerklärung
  404.html               Fehlerseite
  assets/css/style.css   Design (Farben/Schriften oben in :root)
  assets/js/main.js      Menü, Galerie, Karte, Animationen
  assets/img/            Bilder
  .htaccess, robots.txt, sitemap.xml, favicon.ico
.github/workflows/deploy.yml   automatischer Upload zu IONOS
```

## Einmalige Einrichtung des Uploads

In GitHub unter **Settings → Secrets and variables → Actions → New repository secret**:

| Name            | Wert                                   |
|-----------------|----------------------------------------|
| `SFTP_USER`     | SFTP-Benutzername aus IONOS (Hosting → SFTP) |
| `SFTP_PASSWORD` | Passwort dieses SFTP-Benutzers         |

Danach unter **Actions → „Website zu IONOS hochladen“ → Run workflow** einmal
manuell starten. Achtung: Der Upload ersetzt den kompletten Inhalt von
`/public` (alte Lovable-Dateien werden entfernt).

## Hinweise

- Schriften (Playfair Display, Raleway) werden beim Upload automatisch
  heruntergeladen und lokal ausgeliefert – keine Verbindung zu Google Fonts.
- Google Maps wird erst nach Klick geladen (Einwilligung).
- Der Abschnitt „Bewertungen“ ist in `index.html` auskommentiert, bis echte
  Bewertungen vorliegen.

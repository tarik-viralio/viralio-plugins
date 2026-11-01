---
name: thumbnail-video
description: Gestaltet das Reel-Cover (erster Frame des Videos, alles Wichtige im 1:1-Quadrat, das im Profil-Raster gelesen wird) und YouTube-Thumbnails in 16:9 mit drei Ideen – in Größen, die auf dem Handy lesbar sind. Use when user says "mach ein Cover", "Reel-Cover", "Titelbild fürs Reel", "Thumbnail", "YouTube-Thumbnail", "Vorschaubild", "das Cover ist nicht lesbar", or after any finished video. Not for carousel covers.
---

# Cover und Thumbnail – lesbar auf dem Handy

**Die Engine wird mit dem Reel-Skill geteilt.** Alle `scripts/` und `references/` liegen hier:
`${CLAUDE_SKILL_DIR}/../video-ad-editor`

**Zuerst lesen:** `references/thumbnails.md` – Mindestgrößen und ihre Quellen. Das Raster verkleinert das Cover auf 12 %; was unter der Grenze liegt, ist nicht lesbar.

## Bevor du startest – eine Frage
**„Soll ich dein Foto aus dem Video nehmen, oder hast du Fotos für mich?“**
- **Aus dem Video:** Das Skript wählt den klarsten Frame mit großem Gesicht und stellt dich auf cremefarbenem Hintergrund frei (`--cut` fürs Cover · `--video` fürs Thumbnail – braucht einen Mac).
- **Deine Fotos:** freigestelltes Bild mit transparentem Hintergrund (`--photo`) – am besten fürs Thumbnail: klare Emotion (großes Lächeln, Staunen).
- Keine Antwort: aus dem Video.

**Das Design entsteht jedes Mal aus dem Thema des Videos – keine Vorlage:** Der Titel kommt aus seinen Worten, Logos und Elemente aus dem, worüber er spricht (Tool, Firma, Zahl). Die Struktur bleibt fest, der Inhalt wechselt.
**Der Hintergrund ist cremefarben wie bei Claude** (`#F0EEE6`, oder `bg` aus dem Theme, falls hell) – `--bg` ändert ihn, `--bg video` übernimmt die Hintergrundfarbe des Videos.

## Reel-Cover (9:16) – wird zum ersten Frame des Videos

```bash
python3 scripts/28_cover.py <work> "Zeile|*Hervorgehobenes Wort*" [--photo me.png | --cut] [--x alt.png --ok neu.png] [--first ad-master.mp4]
python3 scripts/34_phone_preview.py <work>/cover.jpg
```

- Alles Wichtige liegt im 1:1-Quadrat in der Mitte – unsichtbar, ohne Rahmen.
- Titel: höchstens 5 Wörter, zwei Zeilen, ≈ 9 Zeichen pro Zeile (das Skript warnt dich).
- ✕ und ✓ sind **keine Pflicht** – nur wenn das Video „von so zu so“ erzählt. Logos als Reihe über dem Kopf im Quadrat, Text darunter auf Brusthöhe.
- `--first` setzt das Cover als ersten Frame → `<Name>-cover.mp4`.
- Zeig `cover_phone.jpg` (in echter Handygröße) – wenn du es dort nicht lesen kannst, ist es nicht lesbar.

## YouTube-Thumbnail (16:9) – drei Ideen

```bash
python3 scripts/33_thumb.py <work> "Zeile|*Hervorgehobenes Wort*" [--photo me.png | --video src.mov] [--logo etwas.png] [--x alt.png --ok neu.png]
python3 scripts/34_phone_preview.py <work>/thumb_A_1280.jpg --youtube
```

- Liefert je Idee 3840×2160 (empfohlen) + 1280×720 (fürs Handy, unter 2 MB) und ein Übersichtsblatt `thumbs_sheet.jpg` – zeig es und lass ihn wählen.
- Großes Gesicht mit klarer Emotion · unten rechts frei (Videodauer) · 3–5 Wörter.

## ⛔ Dein Stil

- Der Titel kommt aus dem Inhalt des Videos – kurzer Hook, nichts erfinden, was nicht gesagt wurde.
- Kein Wort über dem Gesicht. Schrift: Inter (oder die Schrift aus dem Theme).
- Zeig das Bild vor jedem Upload oder jeder Veröffentlichung – kein Veröffentlichen, kein Planen.

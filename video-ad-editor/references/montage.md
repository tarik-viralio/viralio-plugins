<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Montage-Modus – Clips ohne Sprache

Ein Ordner mit vielen Clips (Café · Tisch · Produkt · Ort · Event), gewünscht ist ein Video mit Rhythmus.
⛔ **Keine Transkription, keine Untertitel, keine gezeichneten Szenen.** Die ganze Auswahl liegt an der Szene selbst.
Du brauchst vom Nutzer nur eins: **den Clip-Ordner.** Frag nicht nach Farben, Logo oder Account – es gibt ja keinen Text.

**Wie die Engine auswählt:** Jeder Moment in jedem Clip wird nach vier Kriterien bewertet – Bildschärfe · Bewegung in Maßen · Licht · Farbe.
Schärfe ist **relativ** (sie vergleicht deine Clips untereinander), Bewegung und Licht sind **absolut**.
Eingefrorene, dunkle und verwackelte Momente werden **multipliziert**, nicht subtrahiert: Es hilft ihnen nicht, dass ihre übrigen Eigenschaften gut sind.
Und die ersten und letzten Drittelsekunden jedes Clips werden abgeschnitten – der Moment, in dem die Hand am Gerät ist.

### 1) Scan
```bash
python3 scripts/12_montage.py <work> scan <Clip_Ordner> --shot 1.5
```
Prüft vier Clips gleichzeitig. Unsere Messung: **30 Sekunden Video ≈ 15 Sekunden Scan** – also 30 Clips
à 10 Sekunden ≈ zweieinhalb Minuten. Starte es im Hintergrund und sag ihm, wie lange es dauert.
Gibt jeden Clip mit seiner Bewertung und seinem besten Moment aus und schreibt `montage.json`.

### 2) Zeig ihm die Einstellungen – ein nummeriertes Blatt
```bash
python3 scripts/12_montage.py <work> sheet          # 4 Spalten · Einstellungshöhe 180
```
Jede Einstellung trägt die Nummer ihres Clips. **Lies das Blatt als Ganzes – nicht die Einzelbilder.**
Und zeig es ihm: „Das ist der beste Moment jedes Clips – was soll raus?“

**Sucht er eine bestimmte Szene?** („Ich will die Einstellung, in der der Kaffee zubereitet wird, am Anfang“) – such nach Bedeutung, statt das Blatt zu durchsuchen:
```bash
python3 scripts/26_find_shots.py <work> index <Clip_Ordner>        # einmalig
python3 scripts/26_find_shots.py <work> where "coffee being poured into a cup" --sheet
```
Gibt für jedes Ergebnis die Montage-Clipnummer aus – nutze sie mit `keep`. Details: `references/find-shots.md`.

### 3) Entferne, was ihm nicht gefällt
```bash
python3 scripts/12_montage.py <work> drop 4 11      # entfernt
python3 scripts/12_montage.py <work> keep 1 2 5 9   # behält nur diese
python3 scripts/12_montage.py <work> undo           # rückgängig
```

### 4) Reihenfolge und Rhythmus
```bash
python3 scripts/12_montage.py <work> plan --dur 30 --shot 1.5
```
| | |
|---|---|
| `--order energy` (Standard) | wechselt bewegt/ruhig, stärkste Einstellung am Anfang |
| `--order best` \| `folder` | nach Bewertung · in Ordnerreihenfolge |
| `--bpm 96` | Einstellungslängen auf dem Beat – der Schnitt fällt auf den Ton |
| `--dur 0` | alle Clips ohne Obergrenze |

Die Einstellungslängen wechseln in einem wiederkehrenden Muster (1,0 · 0,82 · 1,24 · 0,94 von `--shot`), damit es nicht eintönig wird.

🥁 **Auf den tatsächlichen Beats des Songs (genauer als `--bpm`):** `python3 scripts/beat.py <work>/bg-audio.mp3 --out <work>/beats.json`
dann `plan … --beats <work>/beats.json [--on beats|accents|onsets]` – jeder Schnitt landet genau auf dem Beat-Frame, und nach `build`
laufen Effekte und Übergänge auf den Schlägen mit `node scripts/23_beatfx_render.js`. Details → `references/beat-fx.md`.

### 5) Zusammenbau
```bash
python3 scripts/12_montage.py <work> build <work>/montage.mp4
```
| | |
|---|---|
| `--ar 9:16` | Format: `9:16` · `4:5` · `1:1` · `16:9` (Beschnitt aus der Mitte) |
| `--xfade 0.25` | Überblendung zwischen den Einstellungen statt hartem Schnitt |
| `--zoom 0` | schaltet den leichten Zoom nach innen ab |
| `--amb 0.3` | behält die Atmosphäre der Clips leise (setzt voraus, dass alle Clips Ton haben, und keine Überblendung) |

**Der Zoom funktioniert nur, wenn die Quelle mindestens anderthalbmal größer ist als die Ausgabe** (z. B. 4K), sonst schaltet
die Engine ihn selbst ab und sagt es dir – denn ein Beschnitt auf einer Quelle in Ausgabegröße lässt den Zoom ruckeln.

### 6) Ton und Lieferung – gleiche Linie wie im Sprech-Modus
```bash
bash scripts/06b_master.sh <work> <work>/montage.mp4 <work>/montage-master.mp4
```
Lege seine Audiodatei `<work>/bg-audio.mp3` vorher in den Arbeitsordner. Die Montage kommt mit stummer Spur heraus, wenn du
die Atmosphäre nicht verlangt hast – die Hintergrund-Audiodatei ist hier also keine Zierde, ohne sie ist das Video stumm.

### ⛔ Regeln des Modus
1. **Nicht transkribieren und keine Untertitel machen.** Enthalten die Clips wichtige Sprache, ist das der Sprech-Modus, nicht die Montage.
2. **Zeig ihm das Blatt vor dem Zusammenbau** – er entfernt, was ihm nicht gefällt, nicht du.
3. **Kein Theme, keine Farben, kein Verlauf** – das Bild kommt in seinen Originalfarben (gleiche Regel 4).
4. Die vernünftige Dauer ist **20–40 Sekunden**; darüber wird es dem Zuschauer langweilig.
5. **Kein Veröffentlichen, kein Planen** – geliefert wird nur eine Datei.

---

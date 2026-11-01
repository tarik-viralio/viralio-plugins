<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Podcast-Modus – zwei oder mehr Kameras (v2.7)

Zwei (oder mehr) Kameras derselben Session → ein 9:16-Reel. Nur Mac (Gesichter und Personen-Freistellung über die Vision-Bibliothek). **Nur zwei Befehle** – alles dazwischen läuft automatisch:

```bash
python3 scripts/15_podcast.py prep <work> <Kameraordner | Datei1 Datei2 …>
#  synchronisiert die Kameras über den Ton · prüft jede Kamera auf Defekte (z. B. halbes schwarzes Bild) und schließt sie selbst aus
#  erkennt Gesichter und Mund → wer spricht wann · sind beide Kameras dieselbe Person? · transkribiert und gibt den Text nummeriert aus
#  (extrahiert Frames parallel – 3–5 Minuten für ein Video von einer Minute)
#  ← Text mit fixes.json korrigieren (gleiches Format wie im Sprech-Modus: Wortzahl muss gleich sein, gestrichenes Wort = "")
python3 scripts/15_podcast.py make <work>
#  Untertitel · Szenenplan · Beschnitt über dem Kopf · Rendern · Zusammenbau · Lautheit · srt · Kontaktblatt sheet.jpg
```

## Die vier Modi (das Skript plant sie selbst, mit ruhigem Rhythmus)

| Modus | Wann | Form |
|---|---|---|
| `FULL` | der Sprecher spricht | seine Kamera im Vollbild (und leichter Zoom 1,08 bei Wiederholung) |
| `FULL` für den zweiten | er antwortet | seine Kamera im Vollbild |
| `SPLIT` | schneller Dialog, oder bei jedem dritten Wechsel | Sprecher oben, der andere unten, mit einer Linie in der Akzentfarbe |
| `HEAD` | Satz mit einer Zahl oder einem „heißen“ Wort (ein- oder zweimal) | kleine Karte unten, sein Kopf ragt über ihren Rand, und der Text sind Collage-Schnipsel darüber – ohne Untertitel |

**Dieselbe Person aus zwei Winkeln?** (erkennt es an der übereinstimmenden Mundbewegung) → wechselt den Winkel: Nahaufnahme (größtes Gesicht) beim Hook, dann abwechselnd nah/geteilt/weit/Zoom.
**Rhythmusregeln:** Der Hook ist Vollbild in der Nahaufnahme · kein Wechsel vor 4 Sekunden · kein Halten über 9 · eine `HEAD`-Szene dauert 3–8 Sekunden, und zwischen zwei gibt es mindestens 8.

## Das Theme
`theme.json` im Arbeitsordner (oder im Kameraordner, von dort wird kopiert) – gleiche Schlüssel wie im Sprech-Modus + `capStyle: "shadow"` (weißer Text mit Schatten ohne Hintergrund, zwei bis drei Wörter, das gesprochene Wort in der Akzentfarbe) oder `"card"` · `fontFiles` für eine lokale Schrift (`[{src, weight}]`) · `logo` · `site`. **Die Farben kommen von der Person selbst (Schritt 1) – es gibt kein Standard-Theme.** Normale Ziffern.

## 🪝 Der geschriebene Hook (v3.8.1 – Pflicht für jedes Reel)
Jedes Reel beginnt mit einem **geschriebenen** Hooksatz auf dem Bildschirm, 1,5–3 s (nicht sein erster Satz – aus der stärksten Zeile des Clips), der Clip läuft darunter weiter, dann blendet er aus und die Untertitel kehren zurück.
```bash
python3 scripts/22_hook.py suggest <work>                       # stärkste Zeilen + erlaubte Zahlen
python3 scripts/22_hook.py check <work> "Hook 1" "Hook 2" "Hook 3"  # 3–8 Wörter · Spannungsmittel · Zahl aus seinem Text
python3 scripts/22_hook.py apply <work> "Der Hook" [--kicker "Name des Podcasts"] [--style card]
python3 scripts/22_hook.py preview <work>                       # hook_sheet.jpg – vor dem Gesamtrender ansehen
```
`16_render_pod.js` baut ihn selbst ein, wenn `theme.json ← hook` vorhanden ist – bei `SPLIT` auf die Trennlinie, bei `HEAD` oben auf das Blatt, und er schaltet „die große Frage“ und die Sprach-Collage für seine Zeit ab. Wende den Hook **vor** `plan` an, damit die große Frage eine danach liegende Frage wählt. Regeln und Formeln: `references/podcast-hook.md`.

## Nach `make`
- Lies nur `sheet.jpg` und zeig es ihm.
- Szene ändern? `plan.json` bearbeiten, dann `node scripts/16_render_pod.js <work> range <von> <bis>` und den Zusammenbau ab `make` wiederholen (macht weiter, ohne neu zu schneiden).
- Text ändern? `fixes.json`, dann `make`.
- **Pausen werden nicht entfernt** (ein natürlicher Dialog hat Pausen) – auf Wunsch entfernt `10_script_edit.py drop` ganze Sätze.
- **Ausgabedateien:** `pod-master.mp4` · `pod-master.srt` · `pod-master.txt` · `sheet.jpg`.
- Lieferung: Nenne Zahl der Kameras, Synchronisationsunterschied und jede ausgeschlossene defekte Kamera.

Dateien: `15_podcast.py` · `16_render_pod.js` · `compose.PODCAST.html` · `facetrack.swift` · `22_hook.py` + `hook-card.js`.

## 📺 Ganze Folge im Querformat 16:9 (YouTube) – keine Reels
Gleiche Eingabe (Ordner mit den rohen Kameradateien, dazu die Mikrofondatei, falls getrennt, mit audio/mic/zoom/rode im Namen); Ergebnis ist eine ganze Folge in 1920×1080, die je nach Sprecher zwischen den Kameras wechselt:
```bash
python3 scripts/24_podcast_wide.py prep   <work> <Kameraordner>     # Synchronisation über den Ton + Hauptton + Gesichter und Mund (eine Stunde ≈ Minuten)
python3 scripts/24_podcast_wide.py plan   <work>                      # edl.json + Zusammenfassungszeile (Zahl der Einstellungen, Anteil jeder Kamera)
python3 scripts/24_podcast_wide.py render <work> --preview 90         # Vorschau der ersten anderthalb Minuten – zeig sie ihm vor dem Gesamtrender
python3 scripts/24_podcast_wide.py render <work>                      # episode-wide.mp4 mit –14 LUFS
```
- **Die Kameras:** Eine mit zwei oder mehr Personen = „weit“ (Eröffnung, Pausen und Überlappung der Rede, und eine Einstellung von 4 s alle 45 s in langen Redeabschnitten). Die übrigen sind „nah“ und wechseln zu dem, der spricht, nachdem seine Rede eine Sekunde anhält (kein Springen bei „äh“ und „ja“); die kürzeste Einstellung ist 2 s (`--min`, `--wide-every`).
- **Hochkant-Handykamera?** Wird in der Bildmitte auf einem unscharfen Hintergrund aus ihr selbst gezeigt – ohne Dehnung.
- **Erkennt nicht, wer spricht** (dieselbe Person auf allen Kameras oder unklare Gesichter) → gibt einen Hinweis aus und wechselt bei Pausen alle 6–12 s.
- **Standardmäßig keine Pausenentfernung und keine Untertitel** – die Folge bleibt, wie sie gesprochen wurde. Soll ein Stück raus? Bearbeite `edl.json` (Einstellung löschen und verschieben) oder schneide das Ergebnis mit ffmpeg.
- **Reels aus derselben Folge:** `cams.json` und `master` sind fertig – weiter mit dem Abschnitt „Ganze Folge → mehrere Reels“ in `references/landscape.md`.
- Am 2. Oktober an 3 künstlichen Kameras aus einer Folge getestet (eine 2,3 s verspätet, eine hochkant): Die Synchronisation stimmte genau (+2,30 / –1,00), und 29 Einstellungen in 3 Minuten. **Nicht an einem echten Dreh mit zwei Kameras und zwei Personen getestet** – bei der ersten Folge die Vorschau selbst ansehen.

---
name: video-ad-editor
description: Schneidet ein Talking-Head-Video zu einem 9:16-Reel oder einer Anzeige – entfernt Pausen, setzt deutsche Untertitel wortgenau und baut Motion Graphics in den Markenfarben. Use when user says "schneid dieses Video", "mach aus dem Video eine Anzeige", "entferne die Pausen", "mach ein Reel daraus", "setz deutsche Untertitel", "schneid die Stille raus", or sends a talking-head video. Not for carousels or video covers.
---

# Reel aus einem Sprechvideo – ohne Schnittprogramm

Der ganze Schnitt ist Code:
- ffmpeg schneidet.
- Whisper transkribiert wortgenau.
- Eine Render-Engine setzt Untertitel und Motion Graphics über das Video.

Ergebnis: eine fertige MP4-Datei.

**Pfade:** `scripts/`, `references/` und `motion/` liegen im Ordner dieses Skills:
`${CLAUDE_SKILL_DIR}`

**Sprache:** Standard ist Deutsch. Andere Sprache → Umgebungsvariable `VIDEO_LANG` setzen (z. B. `VIDEO_LANG=en`) und bei Whisper `--language` anpassen.

---

## Kein Sprechvideo? Dann zum richtigen Modus

| Material | Modus | Lesen |
|---|---|---|
| Ordner mit Clips ohne Sprache (Café, Tisch, Produkt) | Montage auf den Beat | `references/montage.md` |
| Zwei oder mehr Kameras derselben Session | Podcast → Reels | `references/podcast.md` |
| Ganze Folge „im Querformat“ oder „für YouTube“ | Podcast 16:9 | `references/podcast.md` (Abschnitt „Ganze Folge im Querformat“) |
| Einstündige Folge → mehrere Reels | Reels aus einer Folge | `references/landscape.md` (Abschnitt „Ganze Folge“) |
| Text oder Idee, ohne Person | Motion-Erklärvideo | `references/motion-mode.md` |
| Link zu einer Website oder „erklär die App“ | Website-/App-Erklärung | `references/motion-mode.md` |

Ist für den Modus ein eigener Skill installiert (`motion-video`, `podcast-video` oder `montage-video`), hat der Vorrang.

⛔ **Frag nicht „Welchen Modus willst du?“** – sag in einem Satz, was du verstanden hast, und mach weiter.

**Engine:** immer die leichte (`04_render_frames.js`), und erwähne das Wort „Engine“ nicht.
- Will er selbst nachbearbeiten? Öffne ihm das Studio → `references/studio.md`
- Remotion nur, wenn er es ausdrücklich nennt → `references/remotion.md`

**🎞️ CapCut-Modus:** Sagt er „mach es in CapCut“ oder „ich will selbst in CapCut nachbearbeiten“? Statt einer MP4 entsteht ein bearbeitbares CapCut-Projekt (Zoom-Clips, CapCut-Untertitel und -Texte, Voice, Effekte, Hintergrund-Audio, transparentes Motion) → `references/capcut.md` (ein Skript: `scripts/40_capcut.py`).

**🎬 DaVinci Resolve:** Ist in dieser Version nicht enthalten. Wünscht er es, sag ihm in einem Satz, dass es dafür ein separates Add-on braucht, und biete den normalen Weg (MP4 oder CapCut-Projekt) an.

---

## ⛔ Dein Umgang mit dem Nutzer

**Du bereitest vor, nicht er.** Gib ihm niemals eine Liste mit Befehlen zum Ausführen.

- **Frag nicht „Hast du das installiert?“** – prüf es selbst.
  Fehlt etwas? „Mir fehlen zwei Tools, die richte ich dir jetzt ein, dauert zwei Minuten – soll ich starten?“
- **Keine Fachbegriffe:** „ein Tool, das die Folien zeichnet“, nicht „Puppeteer“; „Videoqualität“, nicht „Codec“.
- **Sag bei jedem Schritt, wo ihr steht,** und schätze die Zeit:
  „Pausen entfernt – das halbe Video ist weg. Jetzt transkribiere ich deine Sprache, 3 Minuten.“
- **Immer nur eine Sache.**
- **Liefere nichts, ohne es zu zeigen:** nach jeder wichtigen Phase ein Frame oder eine Zusammenfassung.

## ✅ Wo läuft das? Überall – Handy · Cloud · Mac · Windows · Linux · Codex

Der lokale Rechner (Mac + Claude Code) ist am schnellsten und stärksten, **aber nicht Pflicht**. Sag dem Nutzer nie „das geht auf deinem Handy oder in der Cloud nicht“. Fällt ein Tool in der Umgebung aus, nimm die Alternative und nenn ihm in einer Zeile, was du genutzt hast.
**Lies `references/any-environment.md`** – die Leiter der Alternativen (Transkription, Personen-Freistellung, Motion-Rendering …) und der Handy-Ablauf. Die erprobten Rezepte im Detail (ruhiger Schnitt ohne Wackeln, Papier-Cutout-Motion, Zusammenbau) stehen in `references/phone-cloud-playbook.md`.

- Auf dem Handy: Video an den Chat anhängen, die Cloud-Umgebung übernimmt, das Handy darf gesperrt werden.
- Windows: `python` statt `python3`, Pfade wie `C:/…` → `references/windows.md`.

---

## Schritte 0, 0.5 und 1 – Tools, Geschmack, Identität

Lies `references/start.md` und setze es um – gleicher Start für alle Modi.

---

## Schritt 2 – Das Video holen

| Weg | Wie |
|---|---|
| **Datei auf seinem Rechner** (am besten) | nach `<work>/src.mov` kopieren |
| **Google-Drive-Link** | Freigabe „Jeder mit dem Link“, dann der Befehl unten |
| **Google-Drive-Connector** | wenn die Datei privat ist – Connector-Tools der Sitzung |

Drive-Link (die ID steht zwischen `/d/` und `/view`):

```bash
curl -sL "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t" -o <work>/src.mov
```

- 4K ist besser (der Zoom verliert weniger Qualität). 1080p funktioniert aber – **nicht ablehnen und keinen Neudreh verlangen.**
- **Querformat-Video** (Interview, Podcast, TV-Folge)? Gleiche Schritte.
  Schritt 6 schneidet pro Einstellung hochkant um das Gesicht, statt zu strecken → `references/landscape.md`
- **🪝 Reel aus einer Folge oder einem Interview = geschriebener Hook, Pflicht.** Nach `02_captions.py`:
  1. `python3 scripts/22_hook.py suggest <work>`
  2. Schreib 3 Hooks aus der stärksten Aussage (nicht dem ersten Satz) → `check` → er wählt → `apply`
  3. `preview` und `hook_sheet.jpg` ansehen, bevor du komplett renderst.
  - Reel kommt von außerhalb unserer Engines (fertige MP4)? `22_hook.py overlay` → transparentes `hook.mov`.
  - Regeln und Formeln → `references/podcast-hook.md`

Dauer prüfen:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 <work>/src.mov
```

### 🎞️ Verlorene Frames?

Browser-Aufnahme oder nicht-native Kamera-App (iPhone im Browser verliert 13–54 %). Lücken vor dem Schnitt prüfen:

```bash
ffprobe -v error -select_streams v -show_entries frame=pts_time -of csv=p=0 <work>/src.mov | python3 -c "import sys;t=[float(x) for x in sys.stdin if x.strip()];g=[(round(a,2),round(b-a,2)) for a,b in zip(t,t[1:]) if b-a>0.07];print(len(g),'Lücken',g[:8])"
```

Lücken gefunden? Vor Schritt 3 reparieren:

```bash
ffmpeg -i src.mov -vf "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" -c:a copy src_fixed.mov
```

Und sag ihm: „Die Aufnahme hatte verlorene Frames – ich habe sie repariert.“ Beim nächsten Mal Kamera-App empfehlen.

### 🔬 Licht- und Farbcheck (Sekunden, still)

```bash
python3 scripts/25_scopes.py <work>
```

- „In Ordnung“ → nicht erwähnen.
- Problem (dunkel, gelbstichig, flau) → ein Satz: „Das Video ist etwas dunkel und gelbstichig – soll ich es korrigieren?“
  - Zeig Vorher/Nachher in einem Frame.
  - Zustimmung → `theme.json` → `"grade":"auto"` (korrigiert nur die Belichtung).
  - Ablehnung oder Schweigen → nicht anfassen (Regel 4).

---

## Schritte 3–11 – Produktion

### 3) Schnittplan

```bash
python3 scripts/01_cut_plan.py <work>
```

Sag ihm, wie viel wegfällt: „52 Sekunden Stille entfernt – das Video ist jetzt 46 statt 98 Sekunden lang.“

**3.5) Ton verbessern (optional):** Hall oder Rauschen, oder er sagt „verbessere den Ton“?
→ `references/audio-enhance.md`

```bash
bash scripts/02b_enhance_audio.sh <work> --local
```

### 4) Wortgenaue Transkription

```bash
ffmpeg -v error -i <work>/src.mov -vn -ac 1 -ar 16000 -y <work>/a.wav
python3 -m whisper <work>/a.wav --language de --model medium --word_timestamps True \
  --output_format json --output_dir <work> --fp16 False --verbose False > <work>/whisper.log 2>&1
```

- Dauert Minuten – im Hintergrund starten und sagen, wie lange es etwa dauert.
- Fehlgeschlagen? `tail -5 <work>/whisper.log`

**4.1) ⛔ Transkription prüfen, bevor du korrigierst – Pflicht** (Whisper `medium` kann in den letzten Sekunden denselben Satz wiederholt ausgeben, statt das Gesagte zu transkribieren, und verschluckt dabei Sekunden in der Mitte, ohne Spur):

```bash
python3 scripts/02a_whisper_check.py <work>          # 0 = sauber · 3 = listet die verdächtigen Fenster
python3 scripts/02a_whisper_check.py <work> --fix    # transkribiert nur die Fenster neu und führt sie in a.json zusammen (Original bleibt a_orig.json)
```

- Erkennt: denselben Satz 3× hintereinander · bekannte Halluzinationssätze · ein Wort ×4 · jede Lücke, in der Ton ist, aber keine Transkription.
- `--fix`: Das Fenster (mit dem Satz davor und danach – oft abgeschnitten) wird an Pausen in Stücke ≤ 25 s geteilt und **ohne Kontext** neu transkribiert (`condition_on_previous_text=False`): Halluzinationen ziehen sich selbst aus dem Vortext, das einzelne Stück löst sich auf. Der Stückanfang wird auf jeden Zeitstempel addiert, danach wird erneut geprüft. Dauert etwa eine Minute.
- Manuell, falls nötig: `ffmpeg -ss <von> -to <bis> -i a.wav p.wav` → `python3 -m whisper p.wav … --condition_on_previous_text False`
  → `<von>` auf `start`/`end` des Satzes und seiner Wörter addieren → die Sätze des Fensters in `a.json` ersetzen.
- Bleibt etwas übrig? In Schritt 5 korrigieren: ein Text statt der Liste für den halluzinierten Satz.

### 5) Korrektur und Untertitel

Lies `a.json` und korrigiere jeden Satz – Whisper macht Fehler bei Eigennamen, Fachwörtern, Anglizismen und Dialekt. Schreib `<work>/fixes.json`:

```json
{ "fix": [["Alles","was","du","siehst"], ["Der","Untertitel","Zoom"]], "hot": ["siehst","Zoom"], "fx": {"Schluss":"drop"} }
```

- `hot` = Wörter, die beim Sprechen mit der Hervorhebung markiert werden.
- `fx` optional → `references/word-fx.md`
- ⛔ **Wortzahl pro Satz = Wortzahl von Whisper für denselben Satz.** Sonst verrutschen die Zeiten (das Skript bricht ab).

```bash
python3 scripts/02_captions.py <work>
```

### 5.5) Zeig ihm den Text und entferne, was er nicht will → Pflicht

Vor dem Gestalten jeder Szene:

```bash
python3 scripts/10_script_edit.py <work> show
```

- Gibt seinen Text nummeriert mit Zeit aus und schreibt `script.txt`.
- Zeigt gleichzeitig wiederholte Sätze und einen Löschvorschlag – danach nicht noch `dupes` starten.
- ⛔ **Gib das ganze Skript im Chat aus** und frag: „Was soll raus?“ – nicht nur auf die Datei verweisen.

**Wiederholter Satz:** Der erste ist falsch, der zweite die Korrektur.
„Du hast den Satz zweimal gesagt – ‚Wir konnten die Ursache lösen‘ und dann ‚Wir konnten die Ursache erkennen‘. Soll ich den ersten entfernen?“

```bash
python3 scripts/10_script_edit.py <work> drop 6 8       # entfernt die beiden Sätze aus Video und Ton
python3 scripts/10_script_edit.py <work> keep 1 2 5 9   # behält nur diese
python3 scripts/10_script_edit.py <work> undo
```

- Alles danach rückt nach; `cut.json`, `caps.json` und `sfx.json` werden aktualisiert.
- **Mach das hier.** Löschen nach dem Szenendesign verschiebt alle Zeiten.
- Nach jedem Löschen: Schritt 6 wiederholen und mit `--force` neu rendern.

### 6) Schnitt und Zoom

```bash
python3 scripts/03_cut_zoom.py <work>
mkdir -p <work>/vfr && ffmpeg -v error -i <work>/cutz.mp4 -vf fps=30 -q:v 3 -y <work>/vfr/%05d.jpg
```

- **Zoom ist pro Clip fixiert (6.0):** Der erste Lauf schreibt in `cut.json` → `"zooms": {"25.05": 1.06, …}` (Schlüssel = Clipanfang in Sekunden des Originals).
  Entfernst, ergänzt oder teilst du einen Clip, verrutscht der Zoom der übrigen nicht – die Koordinaten deiner Szenen bleiben richtig. Zoom eines Clips ändern = seine Zahl anpassen. Die Reihenfolge in `keep` ist frei (ein Clip vom Ende vor dem vorherigen ist erlaubt).

**6.1) ⛔ Beschnitt über dem Kopf – Pflicht bei jedem Video mit Karte** (Bildschirmtext, `R_DOWN`, `R_LOWER`):

```bash
python3 scripts/23_headcrop.py <work> --from <Beginn der ersten Karte>
```

- Schreibt `studio.json` → `cardTop`.
- Beschnitt ist **konstant über das ganze Video** – kein Tracking, keine Kamera, die folgt.
- Beginnt über dem höchsten Punkt, den sein Kopf erreicht, mit kleinem Rand (1,5 %).
- Der Kopf wird nicht abgeschnitten, es bleibt aber auch keine leere Decke – „viel Platz über dem Kopf“ ist genauso falsch.
- Der Nutzer hat das mehrfach angemahnt und war verärgert.
- Prüf mit eigenen Augen an einem Frame, der nah an die Kamera heranzoomt.
- Eingebrannter Text unter dem Körper? Näher heran mit `theme.json` → `cardZoom` (Standard 1).

### 7) Szenen gestalten → der wichtigste Schritt

**Vor jeder Szene lesen:**
1. `references/motion-rules.md` – Identität, Faktenliste `facts.md`, Verbote.
2. `references/scenes.md` – wie man eine Szene schreibt, Motion-Paket, Ideen, B-Roll.
3. `references/moves.md` – **Bewegungsbank:** `python3 scripts/35_moves.py plan --title "…" --cues …` → Palette des Videos (3 Kernbewegungen, um die es sich dreht + Akzente). Du entscheidest bewusst, der Nutzer muss nicht wählen.
   + `references/styles.md` – **Stilbank (17):** Die Palette liefert einen `style` (Kinetic, Papier-Cutout, Doku, Zeitungs-Erklärer …) = die Form des ganzen Videos (Fläche, Textur, Schrift, Karten). Eine Sprache, keine Vorlage: kombiniere `a+b`, nimm einen Teil oder erfinde aus dem Sinn des Satzes.

**🎯 Von der ersten Fassung an auf Spitzenniveau (6.0 – das Reel, das die Bank durchgesetzt hat und viral ging):** Steck die Mühe in Performance und Motion – reich, tief, überraschend, nicht brav.
- Plane vor dem Rendern **2–3 Tiefenmomente** und nenn sie dem Nutzer in einer Zeile: ein Element, das **hinter seinem Kopf** vorbeizieht (`11_behind_text.js person` + `MV.person`),
  eine **Welle seiner Stimme** (`37_env.py` → `MV.env`), eine Punktkarte hinter dem Kopf, eine **3D-Umlaufbahn**, eine **Form aus der Kundenidentität**, die zur Bewegung wird (Logobogen = Zähler und Wisch), ein **One-Take-Einstieg** (die Kamera taucht ins Logo und kommt im nächsten Shot heraus).
- Das sind die ersten Griffe, nicht die einzigen: Karten, Stempel und Badges sind **nicht verboten** – nutz sie, wenn das Thema es verdient.
- Der Satz, den das Motion selbst ausschreibt, bekommt `nocap` (kein Zerreißen zwischen oben und unten). Text über dem Kopf ist besser, wenn Platz ist.
- **⛔ Ein Element verschwindet nicht mit dem letzten Wort (6.1):** Es bleibt 0,3–0,6 s danach und blendet ruhig über 0,4 s aus, das nächste am selben Ort kommt überlappend herein – `e = letztes Wort + 0,45` (`references/motion-rules.md` §3).
- Rezepte in Code → `references/moves.md` §3e.

**⛔ Layoutregel (vom Nutzer abgenommen):**

| Moment | Rechteck | Form |
|---|---|---|
| Sprache ohne Grafik | `R_FULL` | sein Gesicht füllt den Bildschirm, Untertitel unten bei 1460 |
| Jede Grafik oder Motion | `R_DOWN` | Grafik oben (y 280–520) → Untertitel → sein Gesicht unten in Bildschirmbreite |
| B-Roll oder große Tafel | `R_LOWER` | große Karte oben → Untertitel → sein Gesicht klein unten |
| Komplette Erklärung (Zahlen, Listen) | `R_OFF` | ohne Gesicht, seine Stimme trägt weiter → `references/explainer-and-pace.md` |

- ⛔ **Untertitel stehen niemals auf dem Gesicht des Sprechers.**
  In jedem Modus mit Videokarte liegen alle Untertitel über der Karte, der Fortschrittsbalken mit ihnen.
- **Die Moduswahl ist deine Entscheidung aus dem Sinn des Gesagten** – Gesicht wichtiger oder die Grafik? (Details in `scenes.md`)

**⛔ Sichere Zone** (Instagram-Buttons – `08_safe_check.js` prüft sie):

| Zone | kein Text hier |
|---|---|
| oben | y 0–150 |
| unten | y 1620–1920 (und Warnstreifen 1500–1620) |
| rechts | x 950–1080 zwischen y 1100 und 1750 (Like, Kommentar, Teilen) |

Die Engine ist schon eingestellt: Unterkante der Untertitel 1460, Fortschrittsbalken 1492 in voller Breite.
**Und der erste Untertitel erscheint in der ersten halben Sekunde.**

**Vorschau vor dem Gesamtrender – ein Blatt mit 6 Frames:**

```bash
node scripts/04_render_frames.js <work> preview 1.2 4.6 12.3 27.6 31.0 48.4
bash scripts/07_contact_sheet.sh <work> <work>/sheet.jpg 1.2 4.6 12.3 27.6 31.0 48.4
```

- Das Blatt hat 3 Spalten × 2 Reihen in 1080 Breite, jeder Frame mit seiner Zeit.
- **Lies nur `sheet.jpg`** – nicht die Einzelbilder, nicht viele Blätter.
- Zeig es ihm vor dem Gesamtrender.

### 7.x) Extras – jedes mit eigener Referenz, nur öffnen, wenn nötig

| Extra | Referenz |
|---|---|
| Bildschirmaufnahme vom Handy (im gezeichneten Handyrahmen) | `references/screen-recording.md` |
| Schnittstile: Sprache hinter der Person, vor der Tafel, dein Kopf außerhalb des Rechtecks (Mac) | `references/cut-styles.md` |
| „Ebenen“ für den Hook: ein Wort über dem Kopf, zwei hinter dem Kopf, der Rest davor (Mac) | `references/cut-styles.md` |
| Effekte auf dem Beat (Schnitt, Zoom, Shake auf dem Beat) | `references/beat-fx.md` |
| Wortbewegungen, Untertitelstile, Dehnung | `references/word-fx.md` |
| Komplette Erklärung ohne Gesicht + ruhiges Tempo | `references/explainer-and-pace.md` |
| Verblasster Hintergrund | `references/backdrop.md` |
| Collage (Bildschirm als Blatt, er als Ausschnitt) | `references/collage.md` |
| Element, das der Hand folgt – ein Logo kommt aus der Handfläche (Mac) | unten ↓ |
| Szene nach Bedeutung in der B-Roll suchen | `references/find-shots.md` |
| KI-generierte Szenen (braucht `FAL_KEY`) | `references/gen-scenes.md` |
| Du bist woanders und sprichst mit deiner Stimme (Avatar) | `references/talking-avatar.md` – ⛔ lies „Ausprobiert und gescheitert“, bevor du Geld ausgibst |
| Studio – er bearbeitet die Timeline selbst | `references/studio.md` |

**„Ebenen“ für den Hook:**

```bash
node scripts/11_behind_text.js <work> stack 1
node scripts/04_render_frames.js <work> preview
```

Einen Satz daraus entfernen: `drop <Nummer>`.

**Element, das der Hand folgt:**

```bash
python3 scripts/29_handtrack.py <work> <von> <bis>
```

- Erzeugt `palm.js` (geglätteter Pfad der Handfläche).
- In `compose.html` einbinden: `<script src="palm.js"></script>` und `palmAt(t)` in der Szene nutzen.
- Die Koordinaten gelten für das Vollbild-Video. Ist die Szene eine Karte (`R_DOWN` …)? Mit demselben Kartenmaßstab umrechnen.

### 8) Soundeffekte

```json
{ "outro": 5.2, "whoosh_up": [3.1,11.25], "whoosh_down": [7.85], "thud": [27.27,29.47], "tap": [23.08,24.06] }
```
- `outro` = Dauer der Schlusskarte. Fehlt es = 0 (keine Karte) – und `04_render_frames.js` bricht mit Fehler ab, wenn die Dauer keine Zahl oder 0 ist (vor 6.0 gab es „0 Frames“ und lief still durch).

```bash
python3 scripts/05_sfx.py <work>
```

### 9) Endrender und Zusammenbau

```bash
node scripts/04_render_frames.js <work> all
bash scripts/06_encode.sh <work> <work>/ad-final.mp4
```

- Das Rendern macht dort weiter, wo es aufgehört hat – fertige Frames werden nicht wiederholt.
- Szene nach dem Rendern geändert? Nur ihr Fenster neu rendern, dann zusammenbauen:
  `node scripts/04_render_frames.js <work> range 26.4 31.2`
- `--force` mit `all` rendert alles neu. Das Skript warnt, wenn ein Frame fehlt.
- **📦 Größe (6.1):** Ein Reel über anderthalb Minuten liegt hier meist über 30 MB (124 s → 59 MB) – normal, das ist die hochwertige Fassung.
  Das Cover (`28_cover.py --first`) erzeugt darunter die Lieferdatei selbst (zweistufige Kodierung mit aus der Dauer berechneter Bitrate).
  Ohne Cover? `FIT=1 bash scripts/06_encode.sh <work> <work>/ad-final.mp4` (Ziel `MAXMB`, Standard 29). Nicht beides – sonst wird doppelt komprimiert.

### 10) Lautheit

```bash
bash scripts/06b_master.sh <work> <work>/ad-final.mp4 <work>/ad-master.mp4
```

- Hebt den Ton auf –14 LUFS (gleiche Lautheit wie im Feed) und druckt eine Zeile mit Lautheit und Spitze.
- Liegt `<work>/bg-audio.mp3` bereit? Wird beigemischt und senkt sich automatisch, sobald gesprochen wird.
- Das Bild wird ohne Neukodierung kopiert.

### 11) Untertiteldatei

```bash
python3 scripts/09_srt.py <work> ad-master
```

- `.srt` für YouTube und LinkedIn.
- `.txt` = sein kompletter Text für die Post-Caption.

---

## ⛔ Feste Regeln

1. **Soundeffekt nur an einem bedeutsamen Moment** (eine Zahl fällt, etwas zerbricht, die Szene wechselt) – nicht auf jedes Wort streuen.
   Höchstens 15 Ereignisse pro Minute, Spitze unter –18 dBFS, und zeig ihm vor dem Export, wo du sie gesetzt hast.
2. **Normale Ziffern (0–9), deutsche Schreibweise** (1.000 € · 3,5 %).
3. **Farben ausschließlich aus `theme.json`** – keine festen Farben im Code.
4. **Null Farbbearbeitung an seinem Bild:** kein Verlauf, keine Tönung, kein LUT, kein Blur (`grade:false`) – außer auf ausdrücklichen Wunsch.
   Farben nur für Karten und Texte. Einzige Ausnahme: `"grade":"auto"`, nachdem er dem Lichtcheck zugestimmt hat.
5. **iPhone-HDR → Apple-Konverter ist Pflicht.** `03_cut_zoom.py` erkennt es und baut `hdr2sdr.swift`.
   Eine naive Umwandlung macht das Bild flau und wirkt wie eine „Farbbearbeitung“.
6. **Whisper-Transkription korrigieren**, bevor die Untertitel entstehen, und **nichts erfinden, was er nicht gesagt hat** – weißt du es nicht, schreib allgemein statt zu raten.
7. **Kein Veröffentlichen, kein Planen** – geliefert wird nur eine Datei.
8. **„Hinter der Person“, „Ebenen“ und Schnittstile ein- bis zweimal pro Video** – mehr verliert die Wirkung. (Tiefenmomente mit `MV.person` sind etwas anderes – 2–3 pro Reel.)
   Jedes `build` oder `stack` = die vollständige Liste seiner Art (was du nicht nennst, fällt weg). Und der vordere Text steht nie auf dem Gesicht.
9. **Nenn es „Hintergrund-Audiodatei“, nicht „Musik“.** Der Inhalt ist seine Wahl; du legst sie unverändert als `bg-audio.mp3` ab.
10. **Erfinde jedes Mal neue Szenen.** Die Beispiele sind eine Musterbibliothek, keine Vorlage.
11. **Jedes Bild, jede Bildschirmaufnahme, jedes Logo im Originalseitenverhältnis** – nur proportional verkleinern oder vergrößern. Nicht stauchen, nicht beschneiden, außer auf Wunsch.
12. **Zitate (Gesetzestexte, Studien, Bücher) wörtlich aus der Quelle – kein Buchstabe von Hand:**
    - Automatisch kopieren oder aus der offiziellen Quelle übernehmen.
    - Vor dem Rendern gegen eine zweite Quelle vergleichen.
    - Alles, was kein Zitat ist (Quellenangabe, Autor), in der normalen Theme-Schrift.
13. **Zoom-out = nur Rückkehr aus einem Zoom-in.** Verwandelt den Ausschnitt nicht in eine Karte und wird nicht kleiner als das Original.
14. **Der Hook hat in der ersten Sekunde Bewegung** – ein schneller, weicher Zoom-in oder Icons, die hinter ihm hervorkommen. Ein statischer erster Frame = Weiterscrollen.
15. **Ein eingeblendetes Wort bleibt, bis sein Satz zu Ende ist** – kein halbsekündiges Aufblitzen (mindestens 0,6 s, besser bis zum Satzende).
16. **Standardmäßig verboten** – außer er verlangt es beim Namen:
    - Buchstabe-für-Buchstabe-Tippen (zerreißt die Wörter – animiere Wort für Wort).
    - Glow, Bounce, Verlauf auf Text, Lila→Blau-Hintergrund.
    - Glow verlangt? Auf dem ganzen Bildschirm (`fillRect(0,0,W,H)`) – ein begrenztes Rechteck erzeugt harte Kanten.
    - Details → `references/motion-rules.md`
17. **Sprecher mit bewusst ruhigem Stil** (Predigt, Meditation, Vorlesung): Frag „Soll ich die Pausen so lassen?“
    Zustimmung → `cut.json` → `"keep":[[0,Dauer]]`. Schnitte würden hier wie Sprünge wirken.
18. **Immer ein Element, und zeig es ihm.** Neue Szene oder neuer Effekt: einzeln einbauen, ein Frame-Blatt, dann das nächste.
    Kleine Anfrage? Ändere nur den betroffenen Teil, fang den Skill nicht von vorn an.

---

## ✅ Prüfung vor der Lieferung (Pflicht)

**Vor dem Gesamtrender** – ein Frame aus der **Mitte jeder Szene** (nicht 6 zufällige):

```bash
python3 scripts/32_midframes.py <work>
```

Such nach: abgeschnittenem Text, Überlappungen, einer Zahl, die nicht aus `facts.md` stammt, Schnittkanten um die Person, Reihenfolge „hinter der Person“.
Beheben, erneut prüfen, erst dann rendern.

**0. Sichere Zone und Hook** – automatisch, dein Auge ist nicht nötig:

```bash
node scripts/08_safe_check.js <work> --shot
```

- Zeichnet jeden Moment zweimal in zwei Farben an die Stelle des Videos; was sich nicht ändert, ist deine Grafik.
- Zählt deine Texte in den Button-Zonen und prüft, dass der erste Untertitel vor einer halben Sekunde erscheint.
- Beendet sich mit Code 3 bei einem Verstoß. `--shot` erzeugt `safe.jpg` **nur bei Fehlschlag**.
- Der eingefrorene Frame in Übergängen (`MV.frameAt`) zählt als Video, nicht als Text (6.0) – vorher gab es Fehlalarme.
- Die Grenzen lassen sich über `<work>/safe.json` anpassen.

**1. Synchronität** – Ergebnis transkribieren und Satzanfänge mit `caps.json` vergleichen. Abweichung unter 0,1 Sekunde:

```bash
ffmpeg -v error -i <work>/ad-final.mp4 -vn -ac 1 -ar 16000 -y <work>/fa.wav
python3 -m whisper <work>/fa.wav --language de --model small --output_format json --output_dir <work> --fp16 False --verbose False > <work>/whisper.log 2>&1
```

**2. Ton** – letzte Zeile von `06b_master.sh`: etwa –14 LUFS und Spitze –1,5 dBTP oder niedriger.

**3. Das Auge** – ein Blatt mit 6 Frames aus `ad-final.mp4`, wirklich angesehen.
Beat-Effekte vorhanden? Dann auch `beatfx-sheet.jpg` (Montage: `--sheet` · Sprache: `--check`).

**4. Größe** – Lieferdatei unter 30 MB. Das Cover regelt es: länger als 90 s (oder größer als `MAXMB`) → zweistufig mit berechneter Bitrate
(Reel „1000 € an einem Tag“, 124 s: 1,72 M → 27,9 MB, Text bleibt klar).

---

## 💰 Token sparen

Messung vom 10. September: Ein 36-Sekunden-Video kostete 3,1 Mio. Token.
41 % verstreute Terminal-Befehle, und 8 Vorschaubilder fraßen rund 900.000 Zeichen.

1. **Ein Befehl pro Phase** – bündle unabhängige Schritte in einem Hintergrundbefehl und warte auf die Meldung.
2. **Ein Frame-Blatt pro Vorschau** (6 Frames). Jede weitere Prüfung über Zahlen, nicht übers Auge.
3. **Lies keine ganzen Dateien:** `grep -n` für die Funktion, `tail -5` für Logs.
4. **Referenzen nur bei Bedarf** – öffne `references/` erst, wenn der Einstieg dich dorthin führt.
5. **`theme.json` wird für den Kunden gespeichert** – das zweite Video startet damit. Speichere auch `caps.json` und `cut.json`.
6. **Kurze Antworten:** zwei Zeilen und ein Bild. ⛔ Zeig ein Bild nur bei einer visuellen Frage, die anders nicht zu beantworten ist.

---

## Lieferung

Zeig die Datei mit: Dauer, wie viel Stille entfernt wurde, Anzahl der Szenen und finale Lautheit.
Liefer `.srt` und `.txt` mit und erwähne, dass du nichts veröffentlicht hast.

**🖼️ Das Cover = erster Frame jedes Videos – Pflicht:**

```bash
python3 scripts/28_cover.py <work> "Erste Zeile|*Zweite Zeile farbig*" "Kleine Zeile" \
  [--photo me.png] [--x alt.png] [--ok neu.png] --first <work>/ad-master.mp4
```

- **Regel des sicheren Quadrats:** Das Reel ist 9:16, Instagram zeigt es im Profil aber in 4:5 (manchmal 1:1).
  Alles Wichtige – Gesicht, Text, Logos – liegt im 1080×1080-Quadrat in der Bildmitte (y 420–1500).
  Das Quadrat ist unsichtbar: kein Rahmen, keine Linie.
- **Der Text ist ein kurzer Hook:** zwei Zeilen, höchstens 5 Wörter, ≈ 9 Zeichen pro Zeile – auf der Brust oder knapp darunter. `|` = neue Zeile, `*…*` = Akzentfarbe.
- **📏 Größen, die auf dem Handy lesbar sind:** Das Raster verkleinert das Cover auf 12 % → Titel ≥ 170 px, jeder Text ≥ 110, Logo ≥ 200, ohne Berechnung. Details → `references/thumbnails.md`
- **Foto der Person:** Hat er ein freigestelltes Bild (transparenter Hintergrund)? `--photo` – es kommt auf einen Hintergrund in der Farbe des Videos (oder `--bg`), und die Person darf ruhig abgeschnitten sein. Ohne: ein Frame aus der Quelle.
- **🙂 Gesicht (6.0):** Ohne `--t` wählt es den Frame mit dem größten, klarsten **Gesicht des Sprechers** (Gesichtserkennung auf dem Mac – nicht eine B-Roll-Szene mit einer anderen Person).
  Der Text deckt das Gesicht nie ab: Es erkennt das Gesicht und verkleinert das freigestellte Bild (`--cut`/`--photo`) oder schiebt den Frame hoch, bis das Kinn 30 px über dem Text liegt.
  Ohne Mac: Es nimmt den klarsten Frame und warnt – prüfen, dass er es ist, oder `--t` setzen.
- **Zwei Logos für eine Vergleichsgeschichte – keine Regel:** nur wenn das Video „von so zu so“ erzählt. `--x` = was er verlassen hat (✕), `--ok` = die Alternative (✓). Sie stehen als Reihe oben im Quadrat, der Kopf darunter.
- `--first` setzt das Cover in die ersten 0,1 s des Videos → `ad-master-cover.mp4` – das ist die Lieferdatei. (Länger als 90 s? Es kodiert zweistufig unter 29 MB von selbst – 6.1)
- Zeig `cover_grid.jpg` (9:16 · 4:5 · 1:1 nebeneinander) – prüf, dass im 1:1 nichts abgeschnitten ist.
- Danach `python3 scripts/34_phone_preview.py <work>/cover.jpg` – in echter Handygröße. Kannst du es dort nicht lesen? Größer oder kürzer.
- Will er danach noch ein YouTube-Thumbnail? → Skill `thumbnail-video` (oder `scripts/33_thumb.py`).
- Instagram: ersten Frame als Cover wählen. TikTok: genauso.

Skript- und Dateiübersicht → `references/script-map.md`

<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen -->

# Eine Website oder App im Motion-Stil erklären (v3.9)

Der Nutzer gibt dir einen **Website-Link** oder den **Namen einer App / eines Ablaufs, den er erklären will** → ein Video, das ihn erklärt: echte Aufnahmen von der Website/App in einem gezeichneten Handy- oder Computerrahmen, und Bewegung und Texte darüber.

## 1) Das Material – woher die Aufnahmen kommen
| Eingabe | Wie du sie bekommst | Ergebnis |
|---|---|---|
| **Website-Link** | `node scripts/27_web_capture.js <url> <work>/web [--desktop] [--scroll 7]` | `mobile_01..N.png` (jeder Handybildschirm) · `mobile_full.png` · `scroll_mobile.mp4` (weiches Scrollen) · `desktop_*.png` · `site.json` |
| **Ein Ablauf in einer Website** (Registrierung, Kauf, Einrichtung) | der eingebaute Browser der Sitzung: Mach die Schritte und nimm nach jedem Schritt einen Screenshot auf (`screenshot`) – ⛔ gib keine echten Daten, keine Passwörter und keine Zahlung ein. Nur ein Testkonto oder öffentliche Seiten | ein Frame pro Schritt = eine Szene |
| **Eine iPhone-App, die er am Handy hat** | Er nimmt den Bildschirm auf (Kontrollzentrum → Bildschirmaufnahme) und schickt die Datei | Video ca. 1080×2346 → `references/screen-recording.md` |
| **Eine App, die er selbst baut (Xcode)** | iOS-Simulator: `xcrun simctl io booted recordVideo --codec=h264 <work>/app.mov` (Ctrl+C stoppt) – oder `screenshot` pro Schritt | eine saubere Aufnahme ohne Benachrichtigungen |

`site.json` enthält Titel, Beschreibung, Überschriften, Buttons und die Farben der Website: **Baue das Skript daraus** (erfinde keine Funktionen, die nicht auf der Website stehen), und **das Theme aus ihren Farben**, wenn das Video für die Website selbst ist (oder aus ihren Aufnahmen: `00_theme_refs.py <work> web/mobile_01.png web/mobile_02.png`).

## 2) Die Form des Videos – wähle nach dem Wunsch
- **Eine Person spricht** (er erklärt die Website) → Modus der Sprech-Anzeige: Die Aufnahmen als B-Roll in einem Handyrahmen mit `R_OFF` oder `R_LOWER` – Code und Regeln stehen bereit in `references/screen-recording.md` (das Verhältnis ist heilig, harter Schnitt, Tippmarkierung in Quellkoordinaten).
- **Ohne Person** → Motion-Erklärmodus (`motion/`): Füge die Aufnahmen in `project.json ← "images"` ein und zeichne das Gerät selbst:
  - **Handy:** ein abgerundetes Rechteck (Radius ≈ 16 % der Breite), dunkel + ein feiner heller Rand + das Bild darin `contain` (kein Beschnitt und keine Dehnung). In 3D: ein schlankes `RoundedBoxGeometry` mit dem Bild als Textur auf seiner Vorderseite und einer leichten Neigung (8–14°), die sich langsam dreht.
  - **Computer:** ein Browserfenster (drei Punkte + eine Adressleiste mit der Domain) und das Bild darunter.
  - **Scrollen:** `scroll_mobile.mp4` als Frames im Rahmen, oder bewege `mobile_full.png` innerhalb der Bildschirmmaske nach oben (weicher und leichter).
  - **Fokus:** Zoom auf den Teil, der erklärt wird (Knopf, Preis, Feld) + ein Ring/Pfeil, der sich darauf zeichnet + das Schlüsselwort erscheint daneben. Ein Schritt = eine Szene.
- **Ein Ablauf Schritt für Schritt:** eine große Schrittnummer (1 · 2 · 3) + ihr Frame + eine pulsierende Tippmarkierung an der Stelle des Knopfs, und ein Übergang schiebt den Bildschirm zum nächsten Schritt.

## 2.5) Ein fertiges Kino-Demo (ohne Szenen zu bauen) – `30_demo.js`
Der schnellste Weg, eine Website/App zu erklären: Rahmen, Hintergrund, Zoom und Neigung sind fertig, und du schreibst nur `demo.json`:
```json
{"src":"web/scroll_mobile.mp4","size":[1080,1920],"device":"phone","tilt":8,
 "zooms":[{"s":1.2,"e":3.4,"x":0.45,"y":0.32,"scale":2.0}],
 "taps":[{"t":2.4,"x":0.4,"y":0.32}],
 "title":[{"s":0.2,"e":1.6,"text":"Öffne die Einstellungen"}]}
```
```bash
node scripts/30_demo.js <work>/demo.json preview 1 2.4 4     # Frames demo_*.jpg – sieh sie dir an
node scripts/30_demo.js <work>/demo.json                     # demo.mp4 (5 s ≈ 13 s Rendern)
```
- **3D-iPhone** (`device:"phone"`): Dicke, Metallrahmen, Insel, seitliche Tasten und Glanz auf dem Glas. **`moves`** = eine Kamera auf dem Gerät selbst mit Zeitpunkten: Drehung (`rx`/`ry`/`rz` in Grad), Annäherung (`s`) und Zoom auf eine Stelle des Bildschirms (`fx`,`fy` als Anteil 0–1) – Beispiel: kommt schräg –30° herein → richtet sich auf → nähert sich ×2 an den Knopf, wenn er erwähnt wird → dreht sich zum Schluss nach rechts:
  `"moves":[{"t":0,"ry":-32,"rx":14,"s":0.8},{"t":1.4,"ry":-6,"s":1},{"t":2.4,"s":2,"fx":0.45,"fy":0.18},{"t":3.8,"s":2,"fx":0.45,"fy":0.18},{"t":5,"ry":18,"s":0.95}]`
  Die Bildschirmaufnahme eines iPhones hat die Statusleiste oben, die Insel sitzt also natürlich an ihrem Platz. Bei Website-Aufnahmen (ohne Statusleiste) verdeckt die Insel etwas vom oberen Rand – in Ordnung, oder schneide den Rand der Aufnahme ab.
- **MacBook** (`device:"laptop"`): ein Bildschirm mit schwarzem Rahmen und Notch + eine Aluminiumbasis mit Tastatur und Trackpad, nach vorn gestreckt. Am schönsten für Erklärungen: Er beginnt **gerade** (`rx:0,ry:0`) → neigt sich → nähert sich dem Knopf → kehrt zurück → nähert sich dem zweiten Schritt. Website-Aufnahmen in Breite 1440 (`27_web_capture.js --desktop`), und `holds` ist die Dauer jeder einzelnen Aufnahme. Der Titel steht oben auf dunklem Hintergrund, damit er lesbar bleibt, auch wenn das Gerät darunter herangezoomt ist.
- `src`: eine Bildschirmaufnahme (mp4/mov) oder Bilder (`["web/mobile_01.png",…]` + `hold` Sekunden pro Bild). `device`: `phone` · `browser` (mit `url`) · `none`. `size`: `[1080,1920]` Reel oder `[1920,1080]` YouTube.
- **Zoom:** `x,y` ist der Interessenpunkt als Anteil des aufgenommenen Bildschirms (0–1) – nimm ihn aus der Aufnahme mit eigenen Augen oder von der Stelle des Knopfs. Er geht weich hinein und hinaus, und das Gerät neigt sich die ganze Zeit leicht (`tilt`, 0 = flach).
- **Der Rhythmus kommt aus der Rede:** Gibt es Ton (seine Stimme oder eine generierte), lass jeden `zoom`/`title`/`tap` mit seinem Wort beginnen (Whisper-Zeit) und mische den Ton danach mit ffmpeg dazu.
- Der Hintergrund kommt aus `theme.json` (bg + acc), falls im selben Ordner vorhanden, sonst `bg` in der Datei.
- Die Idee ist von OpenVid inspiriert (Zoom auf einen Punkt + Neigung + Geräterahmen) – der Code ist von Grund auf geschrieben (ihre Lizenz verbietet kommerzielle Nutzung, kopiere also nichts daraus).

## 2.6) Echte 3D-Geräte – `31_device3d.js` (das stärkste)
Genau dieselbe `demo.json`, aber das Gerät ist ein echtes Modell mit three.js: ein iPhone mit einem Titanrahmen, der das Licht spiegelt, Glas, Insel, Tasten und Kameras hinten · ein MacBook mit Aluminiumbasis und Tastatur mit plastischen Tasten, Trackpad und einem Deckel an einem Scharnier · weicher Schatten und leichter Glow auf den Glanzlichtern.
```bash
node scripts/31_device3d.js <work>/demo.json preview 0.5 2.6 4.6   # d3_*.jpg
node scripts/31_device3d.js <work>/demo.json                       # 9 s ≈ 16 s Rendern auf einem Mac M1
```
- `moves` hier: `rx/ry/rz` Drehung des Geräts, `s` Annäherung der Kamera (2–3 = Zoom auf den Knopf), `fx/fy` der Punkt. Die Kamera dreht sich, bis sie vor dem Bildschirm steht, wenn sie näher kommt.
- `metal` ist die Metallfarbe (`"#8f9196"` Titan · `"#b9bbc0"` Aluminium · jede Farbe der Identität), `fit:"cover"` füllt den Bildschirm, wenn die Aufnahme kürzer ist als er.
- `30_demo.js` bleibt für das Flache und Schnelle (braucht keine Grafikkarte).

## 3) Regeln
- Die Aufnahmen sind echt von der Website selbst – zeichne keine erfundene Oberfläche und behaupte nicht, sie sei die Website.
- Ist der Text im Bild klein? Verlass dich nicht darauf, dass er lesbar ist: Vergrößere den Teil oder schreib das wichtige Wort darüber in der Theme-Schrift.
- Ist die Website englisch und das Video deutsch: Die Aufnahme bleibt, wie sie ist, und die Erklärung darüber steht auf Deutsch.
- Persönliche Daten in der Aufnahme (E-Mail, Name, Nummer)? Verwische sie vor der Nutzung.
- Am 2. Oktober an anthropic.com erprobt: 8 Handyscreens + 5 s Scrollen in 43 Sekunden.

<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# 👋 Die Kennenlern-Seite – das Erste, was der Nutzer sieht (v3.8)

> ⚠️ **Stand der deutschen Fassung:** Die Seite selbst (`onboarding/index.html`) ist noch in der Sprache des Originals (Oberfläche, Schriftwahl, Stimmenliste). Diese Anleitung beschreibt die Logik; ohne eine deutsche Fassung der Seite nutze den Weg „Ohne Browser“: eine Frage im Chat zu den Farben (siehe `references/start.md`, Schritt 1).

Eine Seite (`onboarding/index.html`) öffnet sich in seinem Browser: Er wählt Farben, Schrift, Untertitelform, Rhythmus … oder **überspringt alles und schreibt in einer Zeile, was er will**. Jeder Abschnitt steht standardmäßig auf „automatisch“, und was er nicht anfasst, entscheidest du. Sie dauert höchstens zwei Minuten.

## Wann öffnest du sie?
| Der Fall | Was du tust |
|---|---|
| Erstes Mal (`00_onboard.py show` gibt `{}` aus) **und es gibt kein** `.auto-memory/creator-profile.md` | Öffne sie **vor Schritt 1**, nach `00_setup.sh` |
| Erstes Mal, aber er hat `.auto-memory/creator-profile.md` (vom Content-Skill) | ⛔ Nicht öffnen – seine Identität ist bekannt. Weiter mit Schritt 1 (nimm Farben, Schrift und Account aus der Datei). Will er Untertitel und Rhythmus wählen, öffne sie auf seinen Wunsch |
| Sagt „ändere meine Einstellungen“ / „ändere meine Farben“ / „ich will neu wählen“ | Öffne sie – sie öffnet sich mit seinen alten Auswahlen ausgefüllt |
| Er hat eine gespeicherte Datei | ⛔ Nicht öffnen. Lies die Datei still und sag in einer Zeile: „Ich arbeite mit deinen Einstellungen: Farben so, Untertitel so“ |
| Der Arbeitsordner hat eine `theme.json` von einem früheren Video | Das Theme hat Vorrang – nicht anfassen (Regel von Schritt 1) |
| Cloud-Sitzung / kein Browser | Nicht öffnen – eine einzige Frage im Chat zu den Farben wie zuvor |

## Starten
```bash
python3 scripts/00_onboard.py --work <work>     # Windows: python
```
- **Starte es im Hintergrund** (`run_in_background`) – es wartet, bis er „Speichern“ oder „Überspringen“ drückt (höchstens 30 Minuten), beendet sich dann und gibt das JSON aus.
- Die erste Zeile `URL: http://127.0.0.1:…/` – der Browser öffnet sich selbst; öffnet er sich nicht, gib ihm den Link.
- Sag ihm in einer Zeile: „Ich habe dir eine kleine Seite geöffnet, auf der du deinen Geschmack wählst – oder schreib, was du willst, und überspring sie. Ich warte.“
- Der Code: `0` gespeichert · `2` Zeit abgelaufen ohne etwas (mach automatisch weiter und sag es ihm) · `1` Fehler.
- Gespeichert wird in `~/.video-ad-editor/profile.json` (bleibt für alle seine Projekte und wird von einem Update des Skills nicht gelöscht) + `<work>/profile.json`. Das Logo: `~/.video-ad-editor/logo.<ext>`.
- Weitere Befehle: `show` (gibt die Datei aus) · `path` · `theme <work> [--force]` (unten) · `onacc <work>` (Textfarbe auf der Akzentfarbe, nachdem du Farben von Hand geschrieben hast). `VAE_HOME=<Ordner>` ändert den Speicherort zum Testen.

## „Überspringen“
- Erstes Mal: Es wird `{"skip":true,"note":"…"}` gespeichert – **lies `note` und arbeite danach**, der Rest ist automatisch (und frag nach den Farben mit einer einzigen Frage, wenn er sie nicht nannte).
- Ein wiederkehrender Nutzer mit Auswahlen: „Überspringen“ lässt seine alten Auswahlen, wie sie sind, und aktualisiert nur `note` (`keptPrevious: true`).
- **`note` hat Vorrang vor jeder Auswahl** – schreibt er „großer Untertitel“ und wählt „Karte“, folge seinen Worten.

## Die Bewegungen
Abschnitt 11 der Seite ist optional: Standardmäßig wählst du die Palette jedes Videos aus der Bank (`references/moves.md`). Schaltet er „Ich will die Bewegungen selbst wählen“ ein, öffnet sich die Bank von der Seite aus (`/moves/`) und speichert „will ich/nicht“ in `moves` in der Datei. Fragt er danach „Welche Bewegungen hast du?“ → `python3 scripts/35_moves.py`.

## Von der Datei zur Arbeit
```bash
python3 scripts/00_onboard.py theme <work>      # schreibt <work>/theme.json + kopiert das Logo – berührt kein vorhandenes Theme
```
| In der Datei | Wohin es geht | Hinweis |
|---|---|---|
| `identity.colors` {bg,ink,acc,clay,mut} | `theme.json` + `theme.onAcc` | eine fertige Palette oder seine Farben; `clay`/`mut` werden aus seinen Farben berechnet, wenn er sie von Hand wählte. `onAcc` = die Textfarbe auf der Akzentfarbe (unten) |
| `identity.mode:"url"` + `url` | du leitest sie ab (unten), dann `theme.json` | `theme` schreibt den Rest und warnt, wenn die Farben fehlen. Nachdem du sie geschrieben hast: `00_onboard.py onacc <work>` |
| `identity.logo` | `<work>/logo.<ext>` + `theme.logo` | |
| `font` | `theme.font` | Die Auswahl kommt aus Google Fonts und wird von der Engine gezeichnet (Prüfung vom 28. September). Lädt eine Schrift nicht, gibt das Rendern „⚠️ Die Schrift … wurde nicht vollständig geladen“ aus |
| `capStyle` | `theme.capStyle` | dieselben Namen wie in der Engine: `card` · `shadow` · `big` · `underline` · `bar` · `type` · `chunk` (`references/word-fx.md`) |
| `pace:"calm"` | `theme.pace:"calm"` | läuft in der Engine (`03_cut_zoom.py`) |
| `pace:"fast"` | nichts | = der normale Rhythmus |
| `pace:"hyper"` | **du, in den Szenen** | Es gibt keinen Schlüssel dafür in der Engine: `hookZoom` + Moduswechsel alle 1,5–2 s + mehr Wortbewegungen (`slam`/`drop`). Effekte bleiben unter 15 pro Minute (Regel 1) |
| `digits` | – | Im Deutschen ohne Bedeutung (normale Ziffern) |
| `content.type` | Moduswahl | `talking`/`review`/`news` = Sprech-Anzeige · `podcast` = `references/podcast.md` · `montage` = `references/montage.md` · `explainer` = ohne Person – **experimentell** (unten) · `auto` = aus dem Material |
| `content.person:"without"` | ohne Gesicht | Stimme + Motion (`R_OFF` und das Motion-Paket) |
| `orientation` | Format | ⚠️ Die Sprech-Engine ist nur 1080×1920. Querformat und Quadrat **nur für die Montage** (`12_montage.py` → `9:16`/`1:1`/`16:9`/`4:5`). Wählt er Querformat für ein Sprechvideo, sag es ihm offen: „Querformat gibt es noch nur für die Montage – soll ich es dir hochkant machen?“ |
| `platforms` | die sichere Zone | Die aktuellen Grenzen gelten für Instagram; die Buttons von TikTok und Shorts liegen nah daran – wählt er sie, prüf `safe.jpg` einmal mit eigenen Augen |
| `length` | Löschvorschlag | `30`/`60`/`90` = Ziel für Schritt 5.5 (`10_script_edit.py keep`) · `full` = schneide aus seiner Rede nichts außer den Pausen |
| `voice.mode:"own"` | er spricht selbst | bitte ihn um den Tonclip, und er läuft wie `a.wav` |
| `voice.mode:"tts"` + `voice.lang` + `voice.gender` + `voice.tts` | kostenlose generierte Stimme (unten) | `tts:null` = ⛔ keine Standardstimme: Probiere alle Stimmen des gewünschten Geschlechts an 3 Sätzen aus seinem Text, bewerte sie mit Whisper (Fehlerquote) und wähle die deutlichste, und lass ihn die Probe hören, bevor das ganze Video entsteht |
| `bgAudio` | `bg-audio.mp3` | `none` = ohne · `own` = bitte um seine Datei · `auto` = **frag ihn dann** – ⛔ wähle den Inhalt nicht selbst (Regel 9) |
| `sfx` | Schritt 8 | `off` = `sfx.json` enthält nur `outro` · `on`/`auto` = normal |
| `endCard.on:false` | `sfx.json` → `"outro": 0` | Die Vorschau der Engine mit 0 lief; das vollständige Rendern und der Zusammenbau wurden noch nicht erprobt – prüf die letzte Sekunde |
| `endCard` handle/cta/word | `theme.handle` + `theme.outro` | `theme` schreibt die Karte **vollständig** – weil der Standard der Engine die Anzeige des Skills selbst ist. Ihre Form: sein Satz (wenn 16 Zeichen oder kürzer) = **die große Zeile**; längere fallen als zwei graue Zeilen darüber (`l1`/`l2`), und die große Zeile ist „Kommentiere mit“ oder „Folge mir“. Die farbige Scheibe = das Kommentarwort, oder sein Account, wenn es kein Wort gibt (mit dem Zeichen `U+200E` umschlossen, sonst kippt `my.brand@`). Der Account wird nach einer kleinen Zeile darunter geschrieben |
| `note` | alles | hat Vorrang vor den Auswahlen |

## Die Identität aus einem Link (seine Website oder sein Instagram)
1. **Website:** Hol die Startseite (WebFetch oder `curl -sL`) und such: `<meta name="theme-color">`, die wiederkehrenden CSS-Farben (`--primary`, die Buttons, die Links), `font-family` und das Logo (`<link rel="icon" sizes=…>` das größte, `og:image`, ein `<img>` mit logo). Lade das Logo als PNG/SVG herunter.
2. **Instagram:** Die Seite blockiert meist das automatische Lesen – versuch `og:image` (das Profilbild = meist das Logo). Kommt nichts, bitte ihn um einen Screenshot seines Accounts und leite die Farben aus dem Bild ab (die 5 häufigsten Farben ohne Weiß, Schwarz und Grau).
3. Ordne sie: die dominierende dunklere oder hellere = `bg`, ihr Gegenteil = `ink`, die gesättigtste = `acc`, `acc` um 20 % dunkler = `clay`, eine Mischung aus `bg`/`ink` = `mut`. Die Schrift: Ist seine Schrift in Google Fonts, nimm sie, sonst die nächste aus der Auswahl.
4. **Zeig sie ihm vor dem Rendern:** „Ich habe von deiner Website abgeleitet: Hintergrund so, Akzent so, und das ist dein Logo – passt das?“ Dann schreib `theme.json` und aktualisiere `profile.json` (`identity.colors`), damit du sie nicht nochmals ableiten musst.
5. `python3 scripts/00_onboard.py onacc <work>` – schreibt `theme.onAcc` (die Textfarbe auf der Akzentfarbe). Gibt es „⚠️ Auf der Akzentfarbe … ist keine klare Schrift möglich“ aus (z. B. hellgelb auf Weiß), sag es ihm und schlag ein dunkleres `acc` vor – ändere es nicht still.

## Die generierte Stimme (edge-tts – kostenlos, braucht Internet)
```bash
python3 -m edge_tts --voice <die gewählte Stimme> --text "…" --write-media <work>/vo.mp3
```
- Es gehört nicht zu den Tools von `00_setup.sh` – fehlt es: „Ich brauche ein kleines kostenloses Stimmen-Tool, soll ich es installieren?“ Dann `pip3 install edge-tts`.
- Für Deutsch gibt es mehrere Stimmen (z. B. `de-DE-…Neural`, `de-AT-…Neural`, `de-CH-…Neural`, männlich und weiblich). Liste mit `python3 -m edge_tts --list-voices | grep de-`.
- **Immer erst eine Probe an 3 Sätzen** aus seinem Text, mit Whisper `medium` gegengeprüft, und ihn die Probe hören lassen, bevor du weitermachst.
- Schreib Zahlen, Einheiten und Abkürzungen für die Stimme aus („3,5 Prozent“, „zwanzig Euro“), und auf dem Bildschirm steht die Schreibweise mit Ziffern.
- **Versuche mit bezahlten Stimmen (30. September):** Die Klonung der Stimme des Nutzers mit ElevenLabs (`eleven_v4` kam seiner Stimmlage am nächsten; v3 klang anders). Für ein gutes Ergebnis braucht es ein professionelles Klonen (30 Min.+ seiner Rede in derselben Energie).
- **Ohne Person = experimentell.** Was erprobt wurde (28. September, eine Stimme von 11 s): Ein Video in der Hintergrundfarbe in der Länge des Tons wird zu `src.mov`, und die Schritte 3–9 laufen darauf unverändert:
  ```bash
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 <work>/vo.mp3)
  ffmpeg -v error -f lavfi -i "color=c=0x<Farbe bg ohne #>:s=1080x1920:r=30:d=$D" -i <work>/vo.mp3 \
    -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest -y <work>/src.mov
  ```
  Und in den Szenen `studio.json` → `{"scenes":[{"s":0,"e":99,"m":"R_OFF"}]}` (es gibt kein Gesicht, zu dem es zurückkehrt). Es kam eine komplette MP4 mit seiner Stimme und seinen Untertiteln heraus – **aber der Bildschirm ist bis auf die Untertitel leer**: Der ganze visuelle Inhalt sind Szenen, die du in Schritt 7 für jeden Satz entwirfst, und das wurde an einem ganzen Video nicht erprobt.
- ⚠️ Schritt 3 entfernt Pausen aus dem generierten Ton selbst (im Test fielen 20 % weg) – normal, aber wird die Rede zu eng, lass die Pausen.
- Der Text ist vorher bekannt (du hast ihn geschrieben), also ist `fixes.json` = dieselben Wörter mit der Wortzahl von Whisper.
- Sag ihm offen, bevor du anfängst: „Ein Video ohne Person ist noch experimentell – Stimme und Untertitel kommen korrekt heraus, und die Zeichnungen baue ich dir Szene für Szene. Soll ich weitermachen?“

## Was Aufmerksamkeit braucht
- **Die Textfarbe auf der Akzentfarbe** (`theme.onAcc`): Ohne sie wählt die Engine Weiß oder `ink` nach einer alten Regel, die bei dunklen Themes **weiß auf zitronengelb/golden** ergibt (Kontrast 1,2–1,7, nicht lesbar). `theme`/`onacc` schreiben sie mit derselben Regel wie die Vorschau der Seite (die klarere aus `ink`/`bg`, wenn ihr Kontrast 4,5+ ist, sonst Weiß und Schwarz), also ist, was er auf der Seite sieht, das, was herauskommt. Die Engine (`compose.REFERENCE.html` · `compose.PODCAST.html` · `studio.html`) liest `onAcc`, wenn vorhanden, sonst bleibt es beim Alten – Themes ohne `onAcc` ändern ihr Aussehen nicht.
- Ein `compose.html`, das vor dem 28. September kopiert wurde, kennt `onAcc` nicht – `theme` warnt dich; kopiere die Referenz neu, wenn du keine Szenen darin gestaltet hast.
- **Die Schriften** (repariert am 28. September): `04_render_frames.js` wartete auf die Schrift, bevor ihr eingespeister Stil fertig war, sodass jede Schrift außer der Standardschrift ohne Warnung in einer Ersatzschrift erschien. Jetzt wartet es auf den Stil und prüft, dass die Schrift bekannt ist (Test: Alle der Auswahl wurden in ihrer Schrift gezeichnet, und ein falscher Schriftname gab die Warnung aus). `16_render_pod.js` und `08_safe_check.js` wurden auf dasselbe Problem nicht geprüft.
- Die Sprech-Engine ist nur 1080×1920 – Querformat und Quadrat sind für die Montage.
- Die Farben der Seite selbst sind neutral (indigo-violett) – keine der fertigen Paletten ist die Identität von irgendjemandem.

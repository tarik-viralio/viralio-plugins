<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# 🪝 Der geschriebene Hook – die ersten 1,5–3 Sekunden jedes Podcast-/Interview-Reels (v3.8.1)

**Die Regel:** Jedes Reel aus einer Folge beginnt mit einem **geschriebenen** Hooksatz auf dem Bildschirm, der vom ersten Frame an lesbar ist, und der Clip läuft darunter mit seiner Stimme weiter. Danach geht er nach oben weg, und die Untertitel kehren zurück.
Der Hook ist **nicht sein erster Satz** – du schreibst ihn aus der stärksten Zeile des Clips (Zahl, Widerspruch, Frage, Geschichte).
Der gesprochene Hook (das erste Stück aus der Mitte der Rede in `spec.json`) bleibt, wie er ist – der geschriebene liegt darüber, und beide arbeiten zusammen.

## Die Befehle (Arbeitsordner des Reels – nach `02_captions.py`)
```bash
python3 scripts/22_hook.py suggest <work>                         # die stärksten 8 Zeilen mit Bewertung und Mitteln + die Zahlen, die er wirklich gesagt hat (Wiederholtes einmal mit allen Zeiten)
python3 scripts/22_hook.py check <work> "Hook 1" "Hook 2" "Hook 3"    # Regelprüfer (❌ stoppt · ⚠️ Hinweis)
python3 scripts/22_hook.py apply <work> "Der Hook" [--kicker "Name deiner Sendung"] [--style card] [--pos top] [--em "10 Minuten"] [--dur 2.4]
python3 scripts/22_hook.py preview <work>                         # hook_sheet.jpg: 0 · 0,3 · 70 % · danach – vor dem Gesamtrender ansehen
```
- In `<work>` muss `caps.json` oder `a.json` liegen – sonst bricht `check` ab (❌), weil es nicht prüfen kann, ob die Zahlen aus seinem Text stammen. Sein Text liegt in einer anderen Datei? `--words <Whisper-Datei oder caps>`. `--no-words` überspringt die Prüfung bewusst (sag das dem Nutzer).
- `apply` schreibt `theme.json ← hook`, kopiert `hook-card.js` in den Ordner und baut es ans Ende von `compose.html` ein. Wurde `compose.html` gelöscht oder neu aus der Referenz kopiert: `04_render_frames.js` und `08_safe_check.js` bauen ihn selbst ein und geben eine 🪝-Zeile aus (er verschwindet nicht still). Im Kamera-Modus baut `16_render_pod.js` ihn selbst ein.
- Kamera-Modus: Liegt in `plan.json` eine „große Frage“ (QUOTE) unter dem Hook, warnt `apply` ⚠️ – wiederhole `15_podcast.py plan`: Mit einem Hook im Theme wählt es eine Frage, die nach dem Hook beginnt.
- Reel schon gerendert? Nicht komplett neu rendern: `node scripts/04_render_frames.js <work> range 0 <dur+0.5>` (oder `16_render_pod.js … range`), dann wie gewohnt zusammenbauen.
- `08_safe_check.js` prüft den Hook mit dem Rest in seinen allgemeinen Zonen (unterer Rand 1500+ · oben 0–150 · Button-Spalte rechts x ≥ 950). Die Grenzen des Hooks selbst (x 140–940 · y 230–1480) setzt `hook-card.js` beim Zeichnen, nicht 08.
- `preview` zeichnet das Blatt mit Pillow, falls vorhanden (mit Zeitmarke), sonst mit ffmpeg ohne Marke (die Reihenfolge wird gedruckt) – es muss nichts installiert werden.
- Zeig dem Nutzer **3 Hooks** für das erste Reel, und er wählt – danach geh bei den übrigen im selben Stil vor.

## Ein Reel, das nicht von unseren Engines kommt (Interview-Linie in DaVinci/Lottie · fertige mp4)
```bash
python3 scripts/22_hook.py overlay <Ausgabeordner> "Der Hook" --theme theme.json --words <Reel>.json [--video <Reel>.mp4] [--pos mid] [--style bold]
```
- Erzeugt `hook.mov` (ProRes 4444 **mit Alpha**, mit denselben Frames wie das Video, wenn du es mit `--video` angibst): Leg es auf die oberste Spur bei 0, **und verzögere den ersten Untertitel**, bis der Hook weg ist (zwei Texte zusammen sind nicht lesbar).
- Mit `--video`: brennt ihn über das fertige Reel → `<Name>_hook.mp4` + `hook_sheet.jpg`. ⚠️ Die in das Original eingebrannten Untertitel **lassen sich nicht entfernen** – deshalb ist der Standard `mid` (zwischen Gesicht und Untertitel) mit kürzerem Schatten (`--pad 150`). Das ist eine schnelle Lösung; sauberer ist DaVinci.
- `--words` = die Whisper-Datei des Reels selbst (z. B. `reels/R4_….json`) – damit die Prüfung „die Zahl stammt aus seinem Text“ funktioniert.

## So schreibst du ihn – 6 Formeln (alle aus seinen eigenen Worten)
| Die Formel | Die Form | Beispiel (aus einer echten Folge) |
|---|---|---|
| **Zahl + Widerspruch** (die stärkste) | eine Zahl … dann das Gegenteil des Erwarteten | „38 Flüge … und kein einziges Ticket bezahlt“ |
| **Die peinliche Frage** | eine Frage mit zwei Zahlen, die kollidieren | „6 Stunden am Handy … und keine 10 Minuten?“ |
| **Scheitern vor dem Erfolg** | ein Verlust in Zahlen … dann der Sieg offen | „8 Bilder im Finale … und nie gewonnen“ |
| **Geschichte im halben Satz** | eine Szene + ein seltsames Ergebnis | „Seit 10 Jahren folgt er mir … jetzt hat er ein Studio“ |
| **Der gegenläufige Befehl** | nicht + etwas, das alle tun | „Kündige nicht, bevor du das weißt“ |
| **Neugierlücke** | der Grund/der Fehler/was niemand sagt | „Der Grund, warum ich Platz eins gewonnen habe“ |

**Die Bedingungen (der Prüfer setzt sie durch):**
1. **3–8 Wörter.** Höchstens zwei Zeilen. „…“ bricht die Zeile: oben die Idee, unten die Wendung.
2. **Mindestens ein Spannungsmittel** (Zahl · Widerspruch · Frage · Neugier · Befehl · Geschichte) – und am stärksten zwei.
3. **Natürliches Deutsch, so wie er spricht:** kurz, direkt, ohne Amtsdeutsch. Kein Füllwort-Anfang („also“, „halt“, „naja“).
4. **Nichts erfinden:** Jede Zahl im Hook muss in der Rede des Clips vorkommen (als Ziffer oder ausgeschrieben – „sechs“ = 6). Schreib ihm nichts zu, was er nicht gesagt hat, und das Versprechen im Hook muss im Clip eingelöst werden.
5. **Nicht der erste Satz** – stammen 75 % seiner Wörter aus den ersten zwei Zeilen = ❌.
6. Normale Ziffern (1 2 3) · keine Emojis (die Flamme ist komplett verboten) · keine Namen, die das Publikum nicht kennt · kein Punkt am Ende (? und … sind erlaubt).

**Das Mittel „Neugier“ = ein Wort, das eine Lücke öffnet** (Geheimnis · Grund · Fehler · niemand · Wahrheit · einzige · Unterschied · Problem) – „das/der/die“ zählt nicht: „Das ist sehr wichtig“ ❌.

**Häufige Fehler:** eine beschreibende Überschrift statt Hook („Tipps zum Zeitmanagement“) · ein Hook, der die Antwort verbrennt („Das Geheimnis: 20 Minuten am Tag“) · Übertreibung, die er nicht gesagt hat („Hat mein Leben um 180 Grad gedreht“) · Amtsdeutsch („Wie Sie Ihre Zeit organisieren können“).

## Das Design (hook-card.js – nicht ändern, die Einstellung kommt aus theme.json)
- **bold** (Standard): riesiger Text 900 (schrumpft, bis jeder Teil in einer Zeile steht, mindestens 68; muss er brechen, wird er wieder größer und **ausgewogen** geteilt, ohne verwaistes Wort). **Über dem Video:** weiß auf einem dunklen neutralen Schatten in Bildschirmbreite. **Über dem Papier** (`R_DOWN` über der Karte · `R_OFF` · HEAD bei Kameras): in Tintenfarbe ohne Schatten (das Papier selbst ist der Hintergrund). Die Zahl und ihre Einheit (oder `--em` oder `*Wort*`) liegen unter einem Balken in der Akzentfarbe, der von links wischt.
- **card**: eine Karte in der Hintergrundfarbe des Themes mit Text in Tintenfarbe und einer Akzentlinie links – für helle Identität oder wenn er „dieselbe Form wie die Untertitel“ will. Gleiche ausgewogene Teilung (erprobt an „38 Flüge … und kein einziges Ticket bezahlt“ und an einem Hook mit 10 Wörtern in einem Teil: 3 ausgewogene Zeilen).
- `--kicker`: eine kleine Zeile darüber (Name der Sendung/des Gasts – vom Nutzer, nicht erfinden).
- **Alles ist vom ersten Frame an sichtbar** (taugt als Cover und liest sich sofort) – die Bewegung ist nur das „Setzen“ der Wörter im Abstand von 0,045 s, und der Balken wischt 0,1–0,35 s.
- **Der Platz (`pos: auto`):**
  - Folge → Reel: Vollbild und das Gesicht oben (`faceAnchor ≤ 0.45`) → auf der Brust (y≈1180) · Gesicht unten → oben (y≈470) · Karte unten (`R_DOWN`/`R_LOWER`) → über der Karte auf dem Papier · `R_OFF` → mittig auf dem Papier.
  - Kameras: FULL/QUOTE → auf der Brust (das Gesicht bei 42 % ≈ y 806, der Hook steht also nicht über y≈1000) · **SPLIT → auf der Trennlinie zwischen den beiden Kameras (y≈975, der Platz ihrer Untertitel) mit kürzerem Schatten** · HEAD → oben auf dem Papier (y≈640, der Platz der Sprach-Collage).
  - Verdeckt er die Hand oder etwas Wichtiges: `--pos top|mid|low` (die Art des Hintergrunds – Video/Papier – ergibt sich selbst aus dem, was dahinter liegt).
- **Die Dauer:** 0,9 + 0,28 × Wortzahl (1,6–3,0 s). In dieser Zeit verschwindet **jeder andere Text**: die Untertitel, „die große Frage“ (QUOTE – ihr Video bleibt) und die Sprach-Collage (HEAD). `--keep-caps` bringt die Untertitel zurück. Alle kehren mit dem Abgang des Hooks ohne Lücke zurück.
- `studio.json ← "sceneFx": false` entfernt den Hook nicht (der Hook ist kein Szeneneffekt – er kehrt nach `init` in die Liste zurück).
- Alle Farben kommen aus `theme.json` (acc/bg/ink/font). Fehlt etwas davon, nimmt er die Farben der Engine selbst (wie die Untertitel) und gibt ⚠️ aus – und keine feste Identitätsfarbe im Code; das einzig Feste ist der neutrale schwarze Schatten.

## Prüfen vor der Lieferung
- `hook_sheet.jpg`: Der Hook ist im ersten Frame (0,00) lesbar, deckt das Gesicht nicht ab, und die Untertitel sind im letzten Frame zurück.
- `08_safe_check.js` ✅ · und der Hook wird bei der Lieferung als Text genannt, damit er leicht geändert werden kann.

<!-- Referenz für den Skill video-ad-editor – Motion-Erklärmodus (ohne Person und ohne Video) -->

# Motion-Erklärvideo – ein Film aus Text

Eingabe: Text, Idee oder Skript.
Weg: Stimme (seine eigene oder eine kostenlos generierte) → 3D-Motion-Film mit 60 fps.

Schritte und Befehle → `motion/README.md`, dann der Leitfaden für Szenen-Autoren `motion/ENGINE-API.md`.

---

## ⛔ Ein Agent baut den ganzen Film

- Ein Prompt, kein Team, keine Juroren und keine Kritiker – außer er verlangt „poliere es“.
- Erfahrung vom 28. September: ein Agent, 22 Minuten → „krass“. Ein Team aus 13 Bauern + Kritikern → 6 Stunden.

## Qualitätsdecke

Der Prompt des Nutzers wörtlich:

> Craft a high-energy motion graphics piece that flexes your top-tier animation skills
> like a killer portfolio reel. Pull out all the stops, like the creative work on Dribbble, fps 60

Das heißt: dreidimensional, Linienzeichnung und bewegte Typografie. Ein Auge, das nicht blinzelt.

## One-Take und Beispiele

- Ein Video, das komplett eine Einstellung ist, ohne Schnitt (Oberflächen, Schritte, Ideen mit verschachtelten Szenen): `references/one-take.md`.
- Beispiele und Techniken anderer (Inspiration, kein Kopieren): `references/examples.md`.

## Eine Einstellung mit festem Rahmen – nur auf Wunsch des Nutzers

⛔ **Nicht Standard und nicht für jeden Film.** Nutze es, wenn der Nutzer es verlangt („fester Rahmen“, „fester Titel, darunter wechselt es“, „Folienwand“, „3D“ …). Ohne Wunsch: Der Film läuft wie üblich über Brainstorming und die Idee aus dem Sinn des Skripts.
Wenn verlangt, sind das die Werkzeuge:
- **Fester Rahmen** (`MOTION.stage`): ein Titel oben, der sich nicht bewegt, darunter ein Feld, das wechselt und den Satz fortsetzt (`ctx.text.slot`), und das Inhaltsfenster in der Mitte. Szenen und Übergänge passieren nur im Fenster.
- **Eine Akzentfarbe** auf dunklem Hintergrund, und dieselbe Kartenform in allen Szenen.
- **3D-Folienwand** (`ctx.slideWall`): Die Kamera fliegt darüber und endet bei einer Karte, die ohne Schnitt zur ersten Szene wird. Der erste Frame zeigt die Wand (kein leerer Bildschirm), denn er ist das Cover.
- **Motion-Blur** (`motionBlur`): Das passt als Einziges zu jedem Film mit schneller Bewegung – es ist keine Form, sondern macht die Bewegung weich.
- Alle Farben kommen aus dem Theme (`project.palette`) – das Beispiel ist hell und läuft dunkel oder in den Farben jedes Kunden ohne Änderung.
- Das laufende Beispiel: `motion/examples/stage-wall/` – lies es für die Methode, die Idee selbst kommt aus dem Sinn deines Skripts.

## Keine Vorlage

- Sammle 3 Ideen selbst, kritisiere sie und entwickle die stärkste weiter.
- Jeder Satz wird in dem Moment sichtbar, in dem er gesagt wird.

## Tempo

- Ein Satz ≈ eine Szene.
- Ein Schlag oder Wechsel alle 0,5–1 s.
- Aber jedes Wort auf dem Bildschirm bleibt mindestens 0,6 s, damit es lesbar ist.
- Schneide Leerräume nicht, bis es atemlos wird.

## Generierte Stimme

- Wähle eine natürliche deutsche Stimme (z. B. `de-DE-…Neural`); ⛔ keine Standardstimme – der Nutzer wählt. Teste mehrere Stimmen an 3 Sätzen und lass ihn hören.
- Schreib Zahlen, Einheiten und Abkürzungen für die Stimme aus („3,5 Prozent“, „zwanzig Euro“, „und so weiter“) – Symbole liest die Stimme falsch.
- Englische Namen in ihrer Schreibweise (Opus) – sie werden meist richtig gesprochen; prüf es.
- Prüf jede Zeile mit eigenen Augen und mit Whisper `medium` **vor** dem Rendern.
- Schick ihm die Stimme zum Anhören.

## Ton im Film

- Nur Sprache + Soundeffekte.
- ⛔ Standardmäßig keine Hintergrund-Audiodatei – wer eine will, fügt sie selbst hinzu:

```bash
python3 motion/audio.py <Projekt> --no-bed
```

## Liefere früh einen Entwurf

Ein Frame-Blatt oder der Qualitätstext – vor dem Gesamtrender.

---

## Website oder App erklären

Er gibt dir einen Website-Link oder sagt „erklär den Leuten, wie sie das in der App machen“.
Ergebnis: echte Aufnahmen in einem gezeichneten Handy- oder Computerrahmen.

Die Website aufnehmen (Screens + Scrollen + ihre Texte und Farben):

```bash
node scripts/27_web_capture.js <url>
```

Demo mit iPhone oder MacBook in **echtem 3D** (Metall, Glas, Schatten, dreht sich und zoomt auf die Taste):

```bash
node scripts/31_device3d.js
```

Die schnelle flache Fassung: `scripts/30_demo.js`

Alle Details → `references/web-app-explainer.md`

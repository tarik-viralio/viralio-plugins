<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# 🔤 Wortbewegungen + Untertitelstile (v3.1)

## Wortbewegungen
Eine Bewegung auf jedem Wort im Moment seiner Aussprache. Festgelegt in `fixes.json` vor `02_captions.py`:
```json
{ "fix": [...], "hot": [...], "fx": { "Schluss": "drop", "getippt": "type", "kaputt": "crack", "bewegt": "slam" } }
```
| Die Bewegung | Der Name | Wie sie aussieht | Im Rhythmus-Skript |
|---|---|---|---|
| Fall | `drop` | fällt von oben mit Schwerkraft und federt leicht, und der Rahmen schiebt sich im Moment des Aufpralls nach unten | `[Fall: „Schluss“]` |
| Wackeln | `shake` | wackelt, und der Rahmen zittert leicht mit | `[Wackeln: „wackelt“]` |
| Bruch | `crack` | Wackeln + weiße Risse auf dem Bildschirm | `[Bruch: „kaputt“]` |
| Tippen | `type` | wird von links enthüllt, als würde es geschrieben | `[Tippen: „getippt“]` |
| Puls | `pulse` | wird größer und kehrt zurück | `[Puls: „Schluss“]` |
| Schlag | `slam` | landet riesig aus der Mitte, schlägt ein und schrumpft an seinen Platz | `[Schlag: „kostenlos“]` |

Die Bewegungen laufen mit den Stilen ohne Karte (`shadow` und Verwandte). Die Risse (`crack`) und das Wackeln zeichnet die Engine selbst aus `fx` – du brauchst keine Szene.
⚠️ Die Bewegung `stretch` (Dehnung eines Worts per Kashida) ist für arabische Schrift gebaut und hat im Deutschen keine Wirkung – nicht verwenden.

## Untertitelstile (`theme.json` → `capStyle`)
`card` (Karte in der Identitätsfarbe, Standard) · `shadow` (groß, weiß, mit Schatten, ohne Karte) · `big` (ein riesiges Wort) · `underline` (eine Linie unter dem gesprochenen Wort) · `bar` (ein Balken in der Akzentfarbe dahinter) · `type` (Schreibmaschine mit Cursor) · `chunk` (Stücke bis zu 4 Wörtern in einer Kapsel – unten ↓).
In allen Stilen: Die Zahl und ihre Einheit stehen in einer Zeile, ein langer Satz verkleinert seine Schrift, damit er in zwei Zeilen passt, statt Seiten umzublättern, und **die Untertitel erscheinen in jedem Modus mit Videokarte über der Karte** – sie stehen nie auf dem Gesicht.

### Untertitel ohne Bewegung (`theme.json` → `"capStill": true`)
Für ruhige Premium-Anzeigen (Wunsch des Nutzers vom 17. Oktober: Das Wort steigt und fällt nicht, aber seine Farbänderung bleibt). Läuft mit jedem `capStyle`:
- Die Karte (oder der Satz ohne Karte) kommt herein und geht **nur über Transparenz** – ohne Aufstieg und ohne Vergrößerung.
- Das gesprochene Wort **springt nicht**, das hervorgehobene (`hot`) **pulsiert und wächst nicht**, und bei `big` erscheint das Wort ohne Vergrößerung.
- Es bleiben: das Einfärben des gesprochenen Worts, die Kapsel hinter dem hervorgehobenen (`card`), der Balken hinter dem Wort (`bar`), die Linie, die sich zeichnet (`underline`), und der Cursor von `type`.
- Wortbewegungen (`fx` oben) sind eine ausdrückliche Wahl für jedes Wort und werden dadurch nicht abgeschaltet – setz sie in einem `capStill`-Video nicht.
- Ohne den Schlüssel = die Bewegung wie gehabt.

### 🆕 6.1 `chunk` – kurze Stücke in einer Kapsel (Reel „1000 $ an einem Tag“ – Rückmeldung: „das ist auf einem anderen Level“)
Für ruhigen Rhythmus und lockeres Sprechen in die Kamera: Es liest sich mit einem Blick und zieht das Auge nicht vom Gesicht.
- **Stücke bis zu 4 Wörtern in einer Zeile** – keine Seiten und keine zwei Zeilen. Ein langes Stück verkleinert seine Schrift, bis es passt (Kapselbreite ≤ 800).
- **Eine Kapsel in der Hintergrundfarbe** (`bg`) mit weichem Schatten, der Text in der Tintenfarbe (`ink`): Das jetzt gesprochene Wort ist **in der Akzentfarbe** (`acc`), das bereits gesagte in Tinte, und das kommende blass.
- **Ohne Springen:** Das Wort färbt sich nur an seinem Platz, und die Kapsel kommt und geht über Transparenz – sie steigt und wächst nicht (`capStill` ist damit unnötig).
- **Wo getrennt wird:** 4 Wörter · eine Pause länger als 0,45 s · das Stück dauert länger als 2 s · nach einem Satzzeichen (, . ? !).
- **Manueller Umbruch** in `compose.html`, wenn der Sinn falsch geteilt wird (z. B. „2026 und wer kann das“ → „und wer kann das“ allein):
  ```js
  window.CHUNK_BREAK = { 48: [3] };   // Satz 48 (ab null – Reihenfolge in caps.json) beginnt bei seinem Wort 3 (ab null) ein neues Stück
  ```
- Die Kapsel bleibt bis zum nächsten Stück, wenn dazwischen weniger als 0,8 s liegen – der Bildschirm wird nicht bei jedem Atemzug leer. Und kommt danach eine Pause? Sie bleibt 0,45 s nach dem letzten Wort (0,6 beim letzten Stück) – die Regel „nicht mit dem letzten Wort verschwinden“ (`motion-rules.md` §3).
- **Ihr Platz:** Mitte y 1395 im Vollbild · über der Videokarte im Kartenmodus · über seinem Kopf in den Schnittstilen (`headout`/`cutout`).
  Du willst einen Moment an anderer Stelle? `window.CAP_Y_AT = t => (t>=12 && t<15) ? 600 : 0` (null = der normale Platz).
- Alles, was die Untertitel ausschaltet, schaltet sie ab: `nocap` in der Szene · `MV.hideCaption(s,e)` · „hinter dem Kopf“/„Ebenen“ (Wörter, die durch den Effekt erschienen sind, werden nicht wiederholt).
  ⛔ Der Satz, den das Motion selbst ausschreibt = keine Untertitel (`MV.hideCaption`) – im Reel „1000 $“ waren die Untertitel in 17 Fenstern aus.
- `hot` und `fx` wirken hier nicht – die Betonung ist das gesprochene Wort selbst.

### Zahlen und Englisches in Untertiteln und Szenen
Im Deutschen entfällt der alte Sonderfall: Zahlen, Bereiche („25–30“) und englische Wörter stehen in derselben Leserichtung wie der Satz und brauchen keine Behandlung. Die Engine setzt Wörter von links nach rechts.

## Sprache hinter dem Kopf
`11_behind_text.js build <Satznummern ab 1>`: pixelgenau und mit strengen Regeln – die Buchstaben liegen immer außerhalb des Kopfes, das ganze Wort bleibt im Bild, sonst schrumpft die Schrift, und ein Wort ohne geeignete Stelle fällt als Karte auf die Brust. Höchstens drei Wörter hinter dem Kopf. Details in `references/cut-styles.md`.

## „Ebenen“ (der Hook)
`11_behind_text.js stack 1`: ein Wort über dem Kopf in Bildschirmbreite → ein oder zwei Wörter hinter dem Kopf → der Rest vor seinem Körper, weiß, schwer, mit Rand und Schatten. Die Aufteilung ergibt sich automatisch aus den Grenzen seines Körpers. Details in `references/cut-styles.md` (7.5.1).

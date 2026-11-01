<!-- Referenz für den Skill video-ad-editor – Schritt 7: Szenendesign. Lesen, bevor du eine Szene schreibst -->

# Szenendesign – Schritt 7 im Detail

Vorher lesen: `references/motion-rules.md`
(Identitätsdatei, Faktenliste `facts.md`, Verbote, Bewegungsregeln).
⛔ Keine Zahl und kein Name auf dem Bildschirm, die nicht in `facts.md` stehen.

---

## Die Struktur steht – nicht anfassen

`compose.html` enthält alles Grundlegende:
- Das Video in den Modi, mit weichem Übergang.
- Untertitel und Hervorhebung des gesprochenen Worts.
- Hinter dem Kopf, B-Roll, generierte Szenen, Sticker.
- Fortschrittsbalken, Schlusskarte und Farbableitung.

**Standardmäßig zeichnet es keine eigene Szene:** Vollbild-Video + Untertitel + Schlusskarte.

---

## Wie du deine Szene schreibst

Deine Szenen stehen am Ende von `compose.html`, in einem zweiten Skript unter dem Engine-Skript:

```html
<script>
SCENES=[{s:0,e:4.1,m:R_FULL},{s:4.1,e:9.8,m:R_DOWN,gb:480},{s:9.8,e:99,m:R_FULL}];
/* 9.8 = letztes Wort des Satzes + 0,45: Die Tafel bleibt nach seiner Stimme und geht ruhig über 0,4 s (references/motion-rules.md §3) */
function listPanel(t){
  if(t<4.1||t>9.8) return;
  panelIn(t,4.1,9.8,()=>{ /* Zeichnung in Koordinaten 130..950 × 278..458 */ });
}
SCENE_LIST.push(['listPanel',listPanel]);   // ohne Registrierung wird nichts gezeichnet
</script>
```

- `SCENES` kannst du statt im Code auch in `studio.json` schreiben.
- Jede Szene bekommt `t` und hängt an der Wortzeit aus `caps.json` – nicht an einer ungefähren Zeit.
  - `wordsOf(i)` = Wörter des Satzes Nummer i (Zählung ab null).
- Eine Szene, die auf dem Videobild selbst arbeitet (z. B. ein Glitch), wird in der Videoebene gezeichnet:
  `SCENE_LIST.push(['myFx',myFx,'video'])`
- Aus dem Studio: `studio.json` → `"sceneFx":["listPanel"]` registriert sie per Name.
- Eine Szene, die abstürzt, wird im Terminal als `[compose] ⚠️ Szene übersprungen` gemeldet – behebe sie, ignoriere sie nicht.
- Beispiele zum Lesen: `scripts/compose.EXAMPLES.js` (der Kopf erklärt, wie man sie lädt).

### Motion-Paket – in jedem Video mit Zahlen oder Erklärung

`scripts/motion-kit.js` enthält:
- Zählwerk mit Walzen, aufpoppende Zahlenkarten, eine Kurve, die sich zeichnet, Vergleichsbalken.
- Wörter, die aus einer Maske kommen, Timeline, Kommentarfeld, Stempel, technischer Rahmen.

Alles passt auf `R_DOWN`, `R_LOWER` und `R_OFF`.
Die Boxen, Regeln und das Beispiel → `references/motion-kit.md` (vor dem Design lesen).

---

## Die Idee – eine visuelle Metapher, keine Zierde

Sammle 3–4 Ideen pro Satz. Die Idee **verkörpert, was er sagt**:

| Er sagt | Die Szene |
|---|---|
| zählt Dinge auf | Karten kommen mit jedem Wort herein, dann kippen sie mit einem Häkchen um |
| Zahl oder Preis | ein Zähler dreht und landet mit einem Schlag auf der Zahl |
| „kaputt“ oder „Fehler“ | ein Glitch verschiebt Bildstreifen + Risse |
| Problem, dann Lösung | die Karte wird schwarz mit einer Warnung → Fortschrittsbalken + Liste wird abgehakt |
| „eine Datei“ | eine Dateikarte, Karten fliegen herein und verschmelzen damit |
| Aufruf zum Kommentar | ein Kommentarfeld, das Wort wird Wort für Wort getippt |

Die Tabelle sind Beispiele, keine Vorlage. **Erfinde jedes Mal etwas Neues.**

---

## Layoutdetails

- `R_DOWN` ist **eine flexible Karte:** Sie schrumpft je nach Unterkante der Grafik (`gb`) und Zahl der Untertitelzeilen.
  So konkurrieren Grafik und Untertitel nicht. Tafeln in `panelIn()` werden automatisch um 1,2 vergrößert.
- „Vollbild“ wird über die Fläche erkannt (`isFull()`) – nicht über die Ecken.
- `{s,e,m,nocap:true}` = Szene ohne Untertitel (wenn die Tafel denselben Text enthält).
- **Regel des Nutzers (17. Oktober, Reel mit vielen Zahlen):** Jeder Satz, den das Motion auf dem Bildschirm ausschreibt (Titel, Karten, Zähler mit derselben Zahl), bekommt `nocap` für denselben Satz.
  Untertitel unten + Text oben = der Zuschauer ist abgelenkt („Lese ich oben oder unten?“). Untertitel bleiben nur für Sätze ohne Text im Motion.
- Schriftliches Motion bevorzugt den freien Platz **über dem Kopf**, wenn er da ist – eine Vorliebe, keine Regel; an den Schultern ist es in Ordnung, wenn es funktioniert.
  Und das Wort in der Karte berührt das Icon nicht (Ausrichtung mit Rand, nicht mittig).
- **Von der ersten Fassung an auf Spitzenniveau (gleiches Reel):** Steck die Mühe in Performance und Motion – reich, tief, überraschend, nicht brav.
  Zuerst greifst du zu: Tiefe durch die Freistellung der Person (das Element zieht hinter seinem Kopf vorbei – `11_behind_text.js person` + `MV.person`), eine Welle aus seiner eigenen Stimme (`MV.env`),
  eine Punktkarte hinter dem Kopf, eine 3D-Umlaufbahn, eine Form aus der Kundenidentität, die zur Bewegung wird (der Logobogen = Zähler und Wisch), und ein One-Take-Einstieg.
  Weiße Karten, Stempel und Badges sind **nicht verboten** – nutz sie, wenn das Thema es verdient oder es läuft. Der Nutzer: „Ich will jedes Mal Motion bis zum Schluss.“
  Rezepte in Code → `references/moves.md` §3e „Tiefenmomente“.
- **Text, der vor der freigestellten Person erscheinen muss** (Modus `cutout` oder nach `MV.person`)? Normale Szenen werden im Cutout-Modus **unter** der Person gezeichnet.
  Setz die Funktion in `window.AFTER_PERSON=[fn]` oder registriere sie in der Ebene `'afterPerson'` (`MV.scene('x',fn,'afterPerson')`) – sie wird danach gezeichnet (6.0).
- Ein leichtes Raster im Hintergrund alle 60 px. Ausschalten mit `theme.json` → `grid:false`.

### Moduswahl – deine Entscheidung aus dem Sinn des Gesagten

Anweisung des Nutzers (28. September): „Halt dich nicht an eine Regel … studiere das Skript und entscheide: kleine Karte, verschwinden oder Text in Text.“

Lies das ganze Skript und frag bei jedem Satz: **Ist das Gesicht wichtiger oder die Zeichnung?**
- Emotion, Frage, Versprechen → das Gesicht wird größer.
- Zahlen und Erklärung → die Zeichnung bekommt die Fläche (`R_LOWER` oder `R_OFF`).
- Kommentar zu einer Zeichnung → `R_DOWN`.

Tipps, keine Vorschriften: Der Hook ist oft mit Gesicht am stärksten, und Abwechslung zwischen den Modi hält die Spannung.
Fest sind nur: Untertitel stehen nicht auf dem Gesicht, und die sichere Zone.

---

## B-Roll (optional)

Ein zweites Video von der Firma?
1. Extrahiere das Nützliche als Frames: `<work>/broll/<name>_%04d.jpg`
2. Lege seinen Bereich mit `BR_NEED` fest.
3. Zeig es mit `brCard()` zusammen mit `R_LOWER`.
4. `BRCROP` schneidet eingebrannte Untertitel ab.

3–4 Einstellungen im Video reichen.
`R_LOWER` reicht bewusst in den Instagram-Streifen – erlaubt, weil das Verdeckte ein Bild ist, kein Text.

## Echtes 3D-Logo im Sprechvideo-Reel – nur auf Wunsch
⛔ Nicht Standard. Wenn er „3D“ oder „Logo mit Dicke“ verlangt: `node scripts/41_logo3d.js <work> <spec.json> [preview t…]` rendert Logo-Kacheln mit three.js (Dicke, Glanz, Schatten) als transparente PNG-Frames in `three/<name>/`, und in der Szene setzt `MV.overlay(name, X, t, R)` sie ein. Die Logofläche behält ihre echte Farbe (ohne Beleuchtung), der Glanz ist eine eigene Ebene. Nimm ein hochaufgelöstes Logo (kein 64-Pixel-Icon).

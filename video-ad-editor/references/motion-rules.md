<!-- Referenz für den Skill video-ad-editor – lesen vor Schritt 7 (Szenendesign) und vor der Lieferung -->

# Bewegungsregeln + Faktenliste + Prüfung vor dem Export (v3.9.3)
Übernommen und für unsere Reels angepasst aus offenen Skills unter MIT-Lizenz: `charlie947/motion-graphics-skills` und `emilkowalski/skills`.

## 0) Identitätsdatei – wird vor jeder Bewegung gelesen
`<work>/theme.json` ist die Identitätsdatei (Farben, Schrift, Untertitelstil, Logo, Account). Du kannst einen Bewegungsabschnitt ergänzen:
```json
"motion": { "bounce": false }      // true = bringt das Nachschwingen in die Engine zurück (seit 3.9.3 standardmäßig aus)
```
Keine `theme.json`? Animiere nichts – zuerst Schritt 1 (seine Farben, seine Referenzbilder oder der Link zu seinem Account). Und sag nicht „in deiner Identität“, wenn es keine gibt.

## 1) Faktenliste – keine Zahl aus dem Kopf
- Bevor du eine Szene mit **Zahl, Name, Datum oder Prozentwert** gestaltest, schreib `<work>/facts.md` – jede Tatsache in eine Zeile und woher sie kommt (aus seinen Worten im Video bei Sekunde X oder aus der Quelle seines Links):
  ```
  - 37 Billionen Zellen — gesagt bei Sekunde 21,4
  - Opus 5.5 = 5,74 $ — Bericht von claude -p
  ```
- Zeig sie ihm in einer Zeile: „Das sind die Zahlen, die auf dem Bildschirm erscheinen – stimmt das?“ Keine Zahl und kein Name erscheint auf dem Bildschirm, die nicht auf dieser Liste steht.
- Logos und Aufnahmen aus seinen Dateien oder von der offiziellen Website – zeichne kein Logo aus dem Gedächtnis.

## 2) Standardmäßig verboten (außer er verlangt es beim Namen)
1. **Buchstabe-für-Buchstabe-Tippen** – es zerreißt Wörter. Animiere **Wort für Wort**. (Der Effekt `type` der Engine ist erlaubt: Er enthüllt das Wort mit einer Maske, die Buchstaben bleiben zusammen.)
2. **Glow** auf Text und Elementen (glow/bloom). (Wenn verlangt: auf dem ganzen Bildschirm, Regel 16 in SKILL.md.)
3. **Bounce** (bounce / overshoot / elastic) – die Engine selbst ist standardmäßig ohne Nachschwingen (`back()` = weiches Hereingleiten).
4. **Farbverlauf auf Text.**
5. **Lila→Blau-Hintergrund** (der abgenutzte „KI-Look“).
6. Leerer erster Frame – der Hook liegt in den ersten 3 Sekunden und hat in der ersten Sekunde Bewegung.

## 3) Bewegungsregeln
- **Jede Bewegung hat einen Grund:** Sie lenkt das Auge, betont ein Wort oder erklärt. Reine Zierbewegung an einem wiederkehrenden Element fliegt raus.
- **Eingang:** ease-out oder eine kräftige Kurve (`cubic-bezier(.2,.8,.2,1)`). Kein ease-in beim Eingang.
- **Dauer:** 0,15–0,30 s für Elemente. Länger nur für Heldenmomente (Hook, Schluss).
- **Nicht aus null skalieren:** Starte bei 0,92–0,97 mit Transparenz.
- **Gruppen** kommen gestaffelt mit 30–80 Millisekunden Abstand, nicht alle auf einmal.
- **Der Eingang ist langsamer als der Ausgang** bei bewussten Momenten; Reaktionen sind schnell. (Der Ausgang am Satzende hat unten seine eigene Regel ↓)
- **⛔ Ein Element verschwindet nicht mit dem letzten Wort** (6.1 – Rückmeldung zu einem Reel: „Das Motion Graphic endet mit meiner Stimme und verschwindet sofort … ich erwarte, dass es noch etwas nachklingt, und wenn nur Bruchteile einer Sekunde.“):
  - Es bleibt **0,3–0,6 s nach dem letzten Wort seines Satzes** und geht ruhig über **0,4 s** hinaus (`eio`) – nicht mit dem letzten Buchstaben und nicht davor.
  - **Das nächste am selben Ort kommt mit weicher Überlappung herein** mit dem Ausgang des vorigen (es kommt 0,1–0,3 s nach Beginn seines Satzes, das alte geht bis +0,3) – warte nicht, bis es verschwunden ist, sonst wird der Bildschirm leer.
  - **Untertitel genauso:** Sie bleiben 0,45 s nach dem letzten Wort, wenn danach eine Pause kommt; ist das nächste nah (unter 0,8 s), bleiben sie bis dahin – `02_captions.py` und der Stil `chunk` machen das selbst.
  - **Im Code:** Das Ende `e` = der Zeitpunkt, an dem das Element **verschwunden** ist – setz es auf `MV.lineSpan(n).e + 0.45` (oder Beginn des nächsten Satzes + 0,3, wenn das nächste am selben Ort steht), nicht auf das nackte `lineSpan(n).e`:
    ```js
    const e = MV.lineSpan(4).e + 0.45;                    // bleibt nach seiner Stimme
    if (t < s || t > e) return;
    const a = ease(pr(t, s, s + 0.5)) * (1 - eio(pr(t, e - 0.4, e)));   // geht ruhig über 0,4
    ```
    Der Ausgang von `panelIn(t,s,e)` und `MK.*` (`o.e`) dauert jetzt 0,4 s und endet bei `e` (6.1) – gleiche Regel: `e` = letztes Wort + 0,45.
    Sticker (Studio) und generierte Szenen (`"e":"w:Wort+"`) enden mit dem letzten Wort, und die Engine lässt sie danach selbst 0,4 s stehen und ausblenden.
    Bewegungen aus der Bank: `out` (Beginn des Ausgangs) = letztes Wort, und +0,3, wenn ihr Ausgang schneller als 0,4 s ist – und das Szenenfenster reicht bis `out + 0.7`. Schneide das Fenster nicht am letzten Wort ab.
- Animiere `transform` und Transparenz – animiere nicht Breite, Höhe und Position in Pixeln, wenn du es vermeiden kannst.
- **Zähler** mit Ziffern fester Breite (tabellarisch), damit die Zahl nicht zittert.
- „Handgezeichnete“ Note (Sticker, Geste): animiere sie „auf Zweien“ – jede Pose hält zwei Frames.

## 4) Prüfung vor dem Export (Pflicht)
```bash
python3 scripts/32_midframes.py <work>          # ein Frame aus der Mitte jeder Szene → mid_1.jpg, mid_2.jpg… (6 pro Blatt)
```
Prüfe in jedem Frame: abgeschnittener Text · Elemente übereinander · Zahl/Name nicht aus `facts.md` · **Schnittkanten** (Halo oder raue Kante um die Person bei „hinter der Person“/„Ebenen“/Collage) · Tiefenreihenfolge (Text, der hinter der Person sein soll, ist es wirklich).
Beheben → `32_midframes.py` wiederholen → erst dann komplett rendern.
**Bewegungs-Audit:** Schreib dir eine Liste jeder Bewegung, die Abschnitt 2 und 3 verletzt (die schlimmste zuerst), und behebe sie vor der Lieferung.

## 5) Lieferung
Sag ihm in zwei Zeilen, was du geprüft hast und was nicht.

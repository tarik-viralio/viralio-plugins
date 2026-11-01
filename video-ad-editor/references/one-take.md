<!-- Referenz für den Skill video-ad-editor / motion-video – One-Take-Modus (das ganze Video als eine Einstellung, ohne Schnitt) -->

# One-Take-Modus – eine Einstellung vom ersten bis zum letzten Frame

**Die Idee:** Ein einziges Element verwandelt sich für jede Szene. Kein Schnitt, keine Blende, kein Übergang. Die Kamera zoomt heran, bis jeder Zustand den Bildschirm füllt, und ein Mauszeiger (Cursor) macht jede Änderung mit Klicks und Ziehen. Letzter Frame = erster Frame, also eine Schleife.

**Wann du ihn nutzt:** Werbung für eine App oder ein Tool (jede Funktion ein Zustand), Installations- oder Nutzungsschritte, die Erklärung einer Idee mit ineinander verschachtelten Szenen. **Nicht**, wenn der Inhalt lange Rede oder echte Aufnahmen sind – das hier ist für Oberflächen und Ideen.

**Das laufende Beispiel:** `motion/examples/one-take/` – eine Marketplace-Seite für Plugins: Seite mit den Plugins → Klick auf den schwarzen Knopf → **Zoom nach innen, bis der Knopf den Bildschirm verschluckt (schwarz)** → wir tippen die Adresse → Enter öffnet einen orangefarbenen Kreis → zwei Plugins werden hinzugefügt → Schalter „automatische Aktualisierung“ → **Zoom nach außen: Alles, was wir sahen, war ein Handybildschirm neben einem Laptop** → das Handy kehrt zur Seite zurück → Zoom nach innen, bis es den Rahmen füllt = erster Frame. 16 Sekunden, eine Szene (`scenes/s1.js`), mit echter Bewegungsunschärfe (Mittel aus 7 Zeitproben während des Zooms auf einem Hilfs-Canvas) – übernimm die Methode, wenn du sie brauchst. **Kopiere es nicht** – lies es, um die Methode zu sehen, und baue deine Zustände aus dem Sinn des Skripts (es gibt keine Vorlagen).
⚠️ Der Text im Beispielprojekt ist noch in der Sprache des Originals und nennt dessen Marke – ersetze ihn vollständig durch deine eigenen Inhalte, bevor du irgendetwas aus dem Beispiel auslieferst.

## Drei Formen

| Form | Die Bewegung | Beispiel |
|---|---|---|
| **Eine Form, die nie verschwindet** | dieselbe Form ändert Größe, Rundung und Farbe, und der Inhalt wechselt in ihr | Knopf → Lader → Häkchen → Feld → Player → Schalter → Diagramm → Knopf |
| **Jede Szene kommt aus der vorigen** | eine schwarze Form flutet den Rahmen und schrumpft zu einer neuen Szene; Text kommt aus einer Maskenlinie; Balken zeichnen sich | eine Anzeige im Stil einer Apple-Keynote |
| **Endloser Zoom** | die Kamera fliegt in etwas hinein (Uhr, Linse, Spiegel) und öffnet eine neue Welt, und die Schleife kehrt zum Anfang zurück | Welten in Welten |

## Die Regeln (verbindlich)

1. **Eine lange Szene** in der Datei `scenes/s1.js` mit einer einzigen Funktion `draw(t)`. Alles wird nur aus der Zeit `t` berechnet – keine Timer, keine Akkumulation (`x += v`), kein `Math.random`. Die Engine arbeitet ohnehin so (ENGINE-API.md).
2. **Jeder Zustand = dasselbe Element.** Größe, Rundung und Farbe ändern sich, und der Inhalt wechselt, nachdem der Container begonnen hat, sich zu verwandeln, und verschwindet vor der nächsten Verwandlung. Text überlagert sich nicht.
3. **Der Cursor macht jede Änderung:** klicken, ziehen, echtes Tippen. Der Klick hat einen Ring und ein kleines Eindrücken. Der Cursor wächst mit der Kamera.
4. **Die Kamera zoomt heran,** damit der Zustand den Rahmen füllt (ein kleiner Zustand wird vergrößert, ein breiter bleibt bei 1,0). Sie bewegt sich mit der Verwandlung, nicht danach.
5. **Rhythmus:** ein Pulsraster (z. B. 120 BPM = eine halbe Sekunde). Etwas passiert auf jedem Schlag oder jedem zweiten. Federn mit sehr geringem Überschwingen (`E.springK`). Ändert ein Wert mehrfach sein Ziel, summiere eine Feder pro Änderung.
6. **Farbe:** Verwandle Schwarz nicht direkt in die Identitätsfarbe. Bewege ein Farbelement (Kreis, Tab-Indikator) zwischen den Zuständen. Beim Tab-Indikator gib jeder Kante eine andere Feder, dann dehnt er sich.
7. **Schleife:** Der letzte Frame entspricht genau dem ersten (gleiche Größe, gleicher Inhalt, gleicher Puls).
8. **Verboten:** Crossfade, Eintrittsunschärfe, 3D-Flip, Partikel, Glow, länger als eine Sekunde stehen, alles, was nach fertiger Vorlage aussieht, und übertriebenes Bounce.

## Für Deutsch und unsere Identität

- **Richtung:** Text läuft von links nach rechts. Der Schalter (Toggle) bewegt sich in die Richtung, in der man den Satz liest. Links verankerte Karten, Zähler wachsen nach rechts.
- Die Farben ausschließlich aus `theme.json`/`project.json`. Normale Ziffern, deutsche Schreibweise. Keine Flamme 🔥, keine Frauenbilder.
- Jedes Wort auf dem Bildschirm mindestens 0,6 s, damit es lesbar ist. Sichere Zone: prüf mit `--safe`.
- **Ton:** nur Effekte. Keine Hintergrund-Audiodatei, außer auf Wunsch (`audio.py --no-bed`). Gibt es Skript und Stimme, hänge die Verwandlungen mit `ctx.wordTime('l3', 0).s` an die Wörter statt an feste Zeiten.

## Vorbereitung und Aufbau

1. **Lies das Skript und leite die Zustände ab:** 6–12 Zustände, jeder mit Bedeutung (keine Zierde). Schreib sie in einem Satz: „Zustand 3: ein Feld, in das die Adresse getippt wird“.
2. **Fehlt Material?** Was du selbst beschaffen kannst (Logo, Zahlen, Text), beschaffe. Frag den Nutzer nur nach dem, was du nicht finden kannst (echte Bilder, unbekannte Zahlen). Jede Zahl und jeder Name auf dem Bildschirm kommt aus `facts.md` – nichts erfinden.
3. **Zustandstabelle:** zwei Arrays: `TS` (Startzeit jeder Verwandlung) und `G` (Breite, Höhe, Rundung, Zoom). Und eine Cursor-Liste `[Zeit, x, y]` in Koordinaten der Formmitte. Das ist das Gerüst im Beispiel.
4. **Ein Vorschaublatt vor dem Gesamtrender:** ein Frame am Anfang jedes Zustands und in der Mitte jeder Verwandlung: `node render.js <Projekt> preview 0.3 1.0 1.6 … --safe`. Sieh dir die Verwandlungen mit eigenen Augen an und behebe, was gedrängt oder abgeschnitten ist.
5. **Rendern:** `node render.js <Projekt> all --scale 0.5` für den Entwurf (Sekunden), dann `all` für die Endfassung, und `python3 audio.py <Projekt> --no-bed`.
6. **Liefere es** mit dem ersten und dem letzten Frame (sie stimmen überein).

## Echte Bewegungsunschärfe (jetzt in der Engine)
`"motionBlur": {"samples": 8, "shutter": 0.6, "ranges": [[a, b]]}` in `project.json`, oder `blur: [[lt0, lt1]]` in der Szene. Setz es nur auf Zooms und schnelle Züge (es kostet ×8 auf diesen Frames). Details: `ENGINE-API.md` §2b.

## Verweise
- Beispiele anderer (Anstöße und Tipps zu ihrem Aufbau): `references/examples.md`
- Die Engine: `motion/ENGINE-API.md` · der allgemeine Modus: `references/motion-mode.md` · die Regeln: `references/motion-rules.md`

<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

### 7.8) Stil „Collage“ (v2.6) – echte Papierschnipsel kommen zu seiner Rede herein

Statt Untertiteln und gezeichneten Szenen: **Der Bildschirm ist ein Blatt, er ist ein Ausschnitt mit weißem Rand, und jeder Satz bringt sein Element mit** (ein Codefenster fällt herein, ein zerrissenes Archivfoto, eine Uhr, ein Kalender, ein Diagramm, ein Preisschild, eine riesige Zahl mit Kritzelei, Wurzeln, Domino …). Die Zeitleiste baut der Planer selbst aus `caps.json`: Er fasst kurze Sätze zu Schlägen von ≥ 2,4 Sekunden zusammen, wählt für jeden Schlag ein Muster aus seinen Wörtern und ein Heldenwort, verteilt die Seiten und legt bei Namen und Zahlen ganze Farbseiten fest, dazu den Auftrittsplan des Sprechers.

```bash
node scripts/13_collage.js <work> collage all [--logos <Ordner mit Logo-PNGs>]   # alles mit einem Befehl → ad-collage.mp4
node scripts/13_collage.js <work> collage preview 2 8 15 27 40              # Frames zur Prüfung vor dem Gesamtrender
node scripts/13_collage.js <work> collage range 20 26                       # rendert ein Fenster nach einer Änderung neu
node scripts/13_collage.js <work> accents all                                # „Collage-Akzente“: normaler Schnitt + Collage nur bei Zahlen und Namen
```
Braucht einen Mac (Freistellung des Sprechers mit der eingebauten Vision-Bibliothek). Macht dort weiter, wo es aufgehört hat. Der Plan steht in `collage_plan.json`, der Ton in `collage_sfx.json`.

**⛔ Regeln des Stils (vom Nutzer am 4. September abgenommen – nicht verletzen):**
1. **Absolut keine Untertitel:** Das Heldenwort ist der Text. Untertitel wären hier Wiederholung und Konkurrenz.
2. **Der Text liegt immer über allem:** über den Bildern und über dem Sprecher. Kein Wort versteckt sich hinter seinem Rücken.
3. **Auftritt des Sprechers ≥ 3 Sekunden** jedes Mal und nicht mehr als 55 % des Videos. Eine Sekunde, in der er auftaucht und verschwindet, nervt.
4. **Jedes Element lebt ≥ 1,6 Sekunden;** ein kurzer Satz verlängert sein Element in den nächsten hinein.
5. **Elemente kommen von außerhalb des Bildes herein und gehen hinaus** (Feder) – kein plötzlicher Schnitt. Die ganze Farbseite ist der einzige akzeptable Schnitt, und sie kommt nicht vor Sekunde 6 und nicht öfter als alle 9 Sekunden.
6. **70 Pixel Rand** um jedes Wort, und ein langer Titel schrumpft selbst. Kein Text in den letzten 300 Pixeln und nicht im rechten Streifen (1100–1750).
7. **Kein orangefarbener Text auf einem orangefarbenen Block** – auf Blöcken ist es schwarz auf Papier.
8. **Die dunkle Seite** hat ein leichtes beiges Raster (7 %) für Tiefe.
9. **Die Schrift kommt aus `theme.json`** für jeden Text, und wir warten, bis alle ihre Gewichte geladen sind, vor dem ersten Frame (sonst erscheinen die ersten Frames in der Systemschrift).
10. **Das Skript macht die Collage:** Ein Satz mit etwas Greifbarem (Code, Ingenieure, Million, Kalender) wird zu einem starken Schnipsel; ein abstrakter Satz wird nur ein Wort und ein Block. Schreibt der Nutzer ein neues Skript, sag ihm das.

Die mitgelieferten Bilder (`scripts/collage-assets/`) sind alle gemeinfrei, ihre Quellen stehen in `LICENSES.md`. Kommerzielle Logos werden nicht mitgeliefert: Der Nutzer stellt sie im Ordner `--logos` bereit.

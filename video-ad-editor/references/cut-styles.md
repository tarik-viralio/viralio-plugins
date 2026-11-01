<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

> ⚠️ **Wichtig für Deutsch:** Die Stile „Sprache hinter der Person“ und „Ebenen“ wurden für arabische Schrift gebaut: Das Wort wird mit **Kashida** (Dehnstrich) so breit gezogen, dass nur die Dehnung hinter dem Kopf verläuft und die Buchstaben an den Seiten sichtbar bleiben. Lateinische Schrift kennt diese Dehnung nicht. Im Deutschen gilt deshalb: Ein Wort, das nicht gedehnt werden kann, fällt als Karte **vor** den Körper (siehe unten „Die Wörter, die nicht hinter den Kopf passen“). Der Effekt „hinter dem Kopf“ ist bei deutschem Text **noch nicht getestet** und sollte vor dem Einsatz an einem Beispiel geprüft werden. Die Schnittstile **„Karte vor der Tafel“ und „dein Kopf außerhalb des Rechtecks“ (`cutout`/`headout`)** sind sprachunabhängig und laufen normal.

### 7.5) Sprache läuft hinter der Person (optional – aber stark)

Das Wort wird groß geschrieben und über die Breite des Körpers des Sprechers gezogen, sodass nur der Dehnstrich hinter seinem Kopf verläuft
und die Buchstaben an beiden Seiten hervorstehen. Läuft mit der eingebauten Mac-Bibliothek (Vision) – null Download und null Kosten.

```bash
node scripts/11_behind_text.js <work> plan        # schlägt passende Sätze vor
node scripts/11_behind_text.js <work> build 8     # schneidet die Person in den Frames dieses Satzes frei
node scripts/04_render_frames.js <work> all --force
node scripts/11_behind_text.js <work> drop 9      # entfernt einen Satz und lässt den Rest
node scripts/11_behind_text.js <work> off         # alles aufheben
```

**⛔ Wann du es nutzt – die Regel:**
1. **Ein- bis zweimal im ganzen Video.** Kommt es in jedem Satz vor, wird aus „wow“ Lärm.
2. **Am besten beim Hook** (erster Satz) oder am Höhepunkt der Idee – der Satz, den er sich merken soll.
3. Die Bedingungen, die das Skript prüft: Der Satz hat **ein bis vier Wörter** · seine Dauer ≥ 0,85 Sekunden.
4. Und es funktioniert **nur in Vollbild-Momenten** – steckt das Video in diesem Moment in einer kleinen Karte, überspringt es ihn selbst.
5. Die normale Untertitelkarte **verschwindet in diesem Moment automatisch**, damit der Text nicht doppelt steht.
6. Ist der Satz lang oder steht die Person am Bildrand, verkleinert sich die Schrift selbst – und bleibt kein Platz für die Buchstaben, bestehe nicht darauf.

**Kosten:** ~0,15 Sekunden pro Frame für die Freistellung (ein Satz von zwei Sekunden ≈ 10 Sekunden Arbeit). Braucht einen Mac + Xcode-Tools (`xcode-select --install`);
fehlen sie, sagt es das Skript in einem Satz, und der Rest der Linie läuft normal.

### 7.5.1) „Ebenen“ – ein Satz in drei Ebenen um die Person (28. September 2026, aus einer Referenz des Nutzers)

Die stärkste Form für den Hook. Der Satz teilt sich **selbst** aus den Grenzen seines Körpers und Gesichts:
1. **Ein Wort über dem Kopf** – riesig, mit Dehnstrich **auf die volle Bildschirmbreite** gezogen.
2. **Ein oder zwei Wörter hinter Kopf/Hals** – die Buchstaben an den Seiten, und nur der Dehnstrich verläuft hinter seinem Kopf.
3. **Der Rest des Satzes vor seinem Körper** – kleiner, ohne Dehnstrich, Wort für Wort im Moment der Aussprache.

Eine schwere weiße Schrift + ein feiner dunkler Rand + ein harter Schatten nach unten + ein weicher Schatten ← lesbar auf jedem Hintergrund. Erprobt an: einem orangefarbenen und einem türkisen Hintergrund (halbnah) und an zwei Nahaufnahmen in einem Auto (die Kopfstütze hinter dem Kopf + sich bewegende Hände).

```bash
node scripts/11_behind_text.js <work> plan          # gibt die Kandidaten für „Ebenen“ aus (2–8 Wörter, ≥ 1,2 s)
node scripts/11_behind_text.js <work> stack 1       # der Hook
node scripts/11_behind_text.js <work> stack 3:1-5   # bestimmte Wörter aus einem langen Satz
node scripts/04_render_frames.js <work> preview 1.0 2.3   # vor dem Gesamtrender ansehen
```

**Wie es selbst entscheidet:**
- `stack` baut eine „Summenmaske“ für jeden Satz (`bt/umask_<n>.png` = Mittel der Masken seiner Frames). Die Engine berechnet daraus die Grenzen seines Körpers Zeile für Zeile **einmal** pro Satz, das Layout ist also fest und zittert nicht, und die Buchstaben kommen nicht an eine Stelle, an der er stand – auch nicht in 5 % der Frames.
- Die erste Zeile hinter dem Kopf beginnt an der Kopfspitze, und das obere Wort steht direkt darüber (unter dem oberen Instagram-Streifen y 170) und ein Drittel größer als die Zeilen „dahinter“.
- Die Dehnposition wird für jedes Wort nach dem Ort der Person gewählt (die breitere der beiden Seiten), und die Schrift schrumpft (bis 64 px), bis die Buchstaben außerhalb des Kopfes liegen. In der Nahaufnahme (das Gesicht halb so groß wie der Bildschirm) werden die Zeilen „dahinter“ kleiner – normal, der Platz an den Seiten ist gering.
- **🪑 Die Kopfsäule:** Der Vision-Beschnitt umfasst die Kopfstütze (im Auto) und alles, was am Kopf klebt, sodass „der Kopf“ 550–750 px breit wird und kein Wort hineinpasst. Jetzt gilt von über dem Kopf bis zum Hals als Grenze der Person die Säule der Gesichtsrahmen in allen Frames des Satzes (+6 %), und die Personenebene wird um dieselbe Säule gekürzt – die Kopfstütze wird also **unter** den Buchstaben gezeichnet. Der Preis: Eine Hand, die neben dem Gesicht erhoben ist, steht hinter den Buchstaben.
- **Ein Wort, das nicht hinter den Kopf passt, fällt nach vorn – es wird nicht gekürzt und nicht abgeschnitten:** ein Wort ohne Dehnposition oder ein lateinisches Wort/eine Zahl. Die Leserichtung bleibt: oben → hinten → vorn.
- Kein Platz über dem Kopf? Das erste Wort wird zum Wort hinter dem Kopf statt darüber.
- **⛔ Das Vordere steht nicht auf dem Gesicht:** Die erste Zeile beginnt immer unter dem Kinn (bevorzugt auf der Brust). Kein Platz bis 1490? Die Schrift schrumpft, dann erlaubt es bis 1600 (vor der verbotenen Zone 1620). Und ist die Einstellung zu nah, gibt es eine Warnung: kürze den Satz `stack 1:1-3`.
- Lateinische Wörter und Zahlen in der vorderen Zeile stehen in der richtigen Reihenfolge („iPhone 17“, nicht „17 iPhone“) – der Browser ordnet die Richtung selbst.
- Die Button-Spalte von Instagram (y 1100–1750): Jede Zeile, die dorthin fällt, ist auf x ≤ 940 begrenzt, und das Vordere hat Breite 820 in der Mitte.
- Der Hook-Zoom (`hookZoom`) hält im Moment von „hinter dem Kopf/Ebenen“ an – er hatte den Text gelöscht; die Ebenen selbst sind der Schlag des Hooks.

**Die Form aus dem Theme (optional)** – `theme.json`:
```json
"stack": { "fill": "#FFFFFF", "shade": "#000000", "accent": false, "font": null, "weight": 900, "maxBehind": 2 }
```
- Der Standard ist weiß/schwarz neutral – nicht die Identität von irgendjemandem. `accent:true` färbt das obere Wort mit der Akzentfarbe (`acc`) seiner Identität.
- `font:null` = die Schrift des Themes (900). **Für eine Form, die einer Referenz mit schwererer Schrift nahe kommt:** eine breite Display-Schrift aus Google Fonts mit hohem Gewicht – die Engine wartet vor dem ersten Frame darauf. Sehr breite Schriften schicken Wörter „dahinter“ nach vorn, weil sie nicht hineinpassen.
- `maxBehind` (oder `behind`): wie viele Wörter hinter dem Kopf (2 wie in der Referenz, höchstens 3).
- 🆕 6.0 `above`: wie viele Wörter **über** dem Kopf (Standard 1). `"stack":{"above":2,"behind":1}` = die ersten zwei Wörter über dem Kopf übereinander
  und in Bildschirmbreite, und das dritte hinter dem Kopf beginnt an seiner Spitze (nur der Dehnstrich verläuft dahinter).
  Kein Platz oben? Alles schrumpft, bis die oberste Zeile unter den Instagram-Streifen passt (y 170).

**🆕 6.0 Die Untertitel nach teilweisen „Ebenen“** (`stack 21:1-3`): Vorher schrieben die Untertitel nach dem Effekt den ganzen Satz erneut – dasselbe wurde zweimal gelesen.
Jetzt schreiben die Untertitel nur die Wörter, die nicht im Effekt vorkamen: vor dem Effekt = die Wörter davor, danach = der Rest kommt ab dem Ende des Effekts herein.
Der ganze Satz im Effekt = keine Untertitel. Und wurde der Effekt nicht gezeichnet (kein Vollbild zu seiner Zeit, oder im Studio aus), bleiben die Untertitel vollständig. Dasselbe für „hinter dem Kopf“ (`build 2:3-5`).

**⛔ Ihre Regeln:** einmal im Video (der Hook) – höchstens zweimal. Ein Satz von 2–8 Wörtern; kürze Längere mit `stack 3:1-5`. Braucht einen Mac (derselbe Vision-Beschnitt). Kosten: Beschnitt ~0,15 s/Frame + Rendern ~0,05 s/Frame zusätzlich über die Dauer des Satzes.
**Die Befehle und behind.json:** Jedes `build` oder `stack` = **die vollständige Liste seiner Art** – `build 1 9` und dann `build 1` lässt nur 1 (und sagt dir, was es entfernt hat), und die Sätze der anderen Art und `cutout`/`headout` bleiben unberührt. Einen Satz entfernen: `drop 9`. `off` löscht alles. `ranges` werden jedes Mal neu berechnet (ohne Wiederholung), und derselbe `cutout`-Bereich zweimal = einmal. Ein Satz ohne Summenmaske kehrt von selbst zum normalen Stil zurück.
**Die Schrift:** Die Engine (`init`) wartet vor dem ersten Zeichnen auf die Glyphen der Theme-Schrift – vor dem 28. September lud sie nur den lateinischen Teil, die Messung lief also mit einer Ersatzschrift, ca. 20 % schmaler, und das Layout in der Vorschau unterschied sich von dem mit der echten Schrift.
**Die Prüfung:** `08_safe_check.js` sieht jetzt „Ebenen“ und „hinter dem Kopf“ (vorher prüfte es ohne die Personenebene, sie wurden nicht gezeichnet).

### 7.6) Die drei Schnittstile (optional – brauchen einen Mac)

Dieselbe Technik der Personen-Freistellung in drei Anwendungen. Alle mit einem Befehl und dann nur das Fenster neu rendern:

| Der Stil | Seine Form | Der Befehl |
|---|---|---|
| **Sprache hinter der Person** | das Wort wird mit Dehnstrich gezogen und läuft hinter seinem Kopf | `build 2:6-8` |
| **Er steht vor der Tafel** | ohne Karte – er ist freigestellt und steht vor dem Design | `cutout 23.8-26.6` |
| **Dein Kopf außerhalb des Rechtecks** | das Video in einer kleinen Karte unten, und sein Kopf ragt über ihren Rand | `headout 23.8-26.6` |

```bash
node scripts/11_behind_text.js <work> headout 23.8-26.6
node scripts/04_render_frames.js <work> range 23.6 26.8
```

**⛔ Eine vom Nutzer abgenommene Regel (8. September):** Wenn du den Sprecher unter eine Tafel setzt, **nutze nicht `R_DOWN` mit freigestelltem Gesicht** – nimm die kleine Karte `R_LOWER` mit „dein Kopf außerhalb des Rechtecks“ (headout) und blende die Untertitel in diesen Szenen aus (`nocap:true` in der Szene), weil der Text oben genügt und die Untertitel stören. Und verteile die Elemente der Tafel über ihre ganze Höhe nach der Menge der Informationen, stapele sie nicht oben und lass unten nichts.

**Wann nutzt du „Dein Kopf außerhalb des Rechtecks“ oder „Er steht vor der Tafel“?**
Wenn du **eine Erklärung, Zeichnung oder Infografik hast, die Platz braucht** – die Karte rückt klein nach unten (`R_LOWER`) und lässt **zwei Drittel des Bildschirms** für das Design.
Und in diesem Modus **darfst du den Instagram-Streifen verletzen** – das Verdeckte ist ein Bild, kein Text.

**Die Engine stellt es automatisch ein:** Die Untertitel erscheinen über seinem Kopf · der Fortschrittsbalken verschwindet · Größe und Position werden in jedem Frame aus den Grenzen seines Körpers berechnet, sie tanzen also nicht.
**Die festen Grenzen (`headbox`):** `headout` schreibt sie selbst in `behind.json` (druckt `📐 headbox`) – ohne sie folgt die Karte dem Körper in jedem Frame, und der Hintergrund wackelt.
Vor 6.1 scheiterte es immer still („braucht PIL“, obwohl installiert): Die Berechnung war ein `python3 -c` über die Shell, und die Zeilen kamen als wörtliches `\n` an. Jetzt ffmpeg + node.

**🆕 6.1 Die saubere Rückkehr ins Vollbild** (Reel „1000 € an einem Tag“ – Rückmeldung: „auf einem anderen Level“):
Der normale Übergang (0,42 s) von der kleinen Karte ins Vollbild zeigt, wie die Karte wächst und der freigestellte Kopf mittendrin abgeschnitten wird.
Das Rezept: Ein Element aus der Tafel selbst (das Handy, das die Anzeige zeigt) **wächst, bis es den Bildschirm bedeckt** → darunter kehrt das Video **sofort** ins Vollbild zurück → das Element verschwindet, und das Gesicht ist vor dir.

```js
SCENES=[ {s:0,e:H1s,m:R_FULL},
  {s:H1s,e:H1e,m:R_LOWER,nocap:true},     // headout H1s-H1e – mit genau demselben Ende
  {s:H1e,e:99,m:R_FULL,tr:0.001} ];       // tr = Übergangsdauer dieser Szene in Sekunden (ohne: 0,42) – 0,001 ist ein sofortiger Schnitt
/* In der Szene der Tafel: In den letzten 0,32 s vor H1e wächst das Element, bis es bedeckt, und nach H1e verschwindet es in 0,32 s */
const cov = window.__SAFE_FLAT ? 0 : eio(pr(t, H1e-0.32, H1e-0.02)), fade = eio(pr(t, H1e, H1e+0.32));
x = lerp(x, 540, cov); y = lerp(y, 960, cov); w = lerp(w, 1080*1.06, cov);   // ein 9:16-Handy mit Breite 1145 = Höhe 2035 → bedeckt 1920
X.globalAlpha *= 1 - fade;
```

- `tr` läuft auch im Studio (`studio.json` → `scenes`). Und „dein Kopf außerhalb des Rechtecks“ blendet mit demselben `tr` der Szene über.
- Der sofortige Schnitt **muss verdeckt werden** – `tr:0.001` ohne bedeckendes Element = ein Sprung. Und die Bedeckung ist vollständig (≥ 1080×1920), nicht 90 %.
- `window.__SAFE_FLAT ? 0 :` – die Prüfung der sicheren Zone zählt die Vergrößerung als Text, der den ganzen Bildschirm bedeckt (100 % Fehlalarm im Moment der Bedeckung). Diese Bedingung schaltet es nur während der Prüfung ab.
- Dieselbe Sprache bei jeder Rückkehr im Reel (zweimal in einem Reel von zwei Minuten) – die feste Sprache ist Teil des Niveaus.

## ⛔ Strenge Regeln für Sprache hinter dem Kopf (17. September 2026 – nach Fehlern in einem Reel)
1. **Der Dehnstrich wird nur nach einem Buchstaben eingefügt, der sich mit dem folgenden verbindet.** Die arabischen Buchstaben `ا أ إ آ د ذ ر ز و ؤ ة ء ى` bekommen nie einen Dehnstrich. Die Position = die letzte gültige Verbindung im Wort (`_pts`). Ein Wort ohne gültige Verbindung = **keine Dehnung**, es wird normal gezeichnet. Das gilt für arabische Schrift; im Deutschen gibt es keine Dehnung (siehe Hinweis oben).
   (28. September) **Diakritika sind kein Buchstabe:** `_pts` rechnet vom Grundbuchstaben und setzt den Dehnstrich nach seinem Diakritikum.
2. **Die Buchstaben gehen nie hinter den Kopf.** Der Dehnstrich allein bedeckt die Kopfbreite + einen Rand von 36 px, und der Anfang des Wortes liegt auf der einen Seite des Kopfes, das Ende auf der anderen.
3. **Das ganze Wort bleibt im Bild mit 40 px Rand auf beiden Seiten.** Die Schrift schrumpft (bis 44 px), bis es passt – und passt es nicht, wird der Satz als normaler Untertitel gezeichnet, statt freigestellt zu werden.
4. **Die Dehnung geschieht in Pixeln, nicht in Zeichen** (ein Streifen aus der Mitte des Dehnstrichs verändert sich weich) – jede Änderung der Zeichenzahl lässt es zittern.
5. Ein Satz hinter dem Kopf: ein bis drei Wörter, und nicht öfter als zweimal im Video.
Diese Regeln sind in der Engine umgesetzt (`_stretchCache` · `behindText`), und wenn du die Engine änderst, brich sie nicht.


## ⛔ Die Untertitel stehen nicht auf seinem Gesicht (Regel des Nutzers – 23. September)
Im Kartenmodus (`R_DOWN` / `R_LOWER`) erscheinen die Untertitel **vollständig über der Videokarte**, sie überlappen nicht ihren Rand und kommen nicht ins Bild.
- Stil `card`: `SEAM=0` – die Karte steht 60 Pixel über dem Videorand.
- Stile ohne Karte (`shadow` · `big` · `underline` · `bar` · `type`): Sie waren bei 1400 fixiert, egal wie der Videomodus war, und fielen deshalb auf sein Gesicht. Jetzt wird `by2` aus `vtarget(t)` berechnet: über der Karte, wenn das Video unten ist, und 1400 im Vollbild.
Der Grund: „Was werden die Leute sagen“ – Text über dem Gesicht liest sich schlecht und verdeckt den Ausdruck, und der Platz über dem Kopf ist ohnehin leer.

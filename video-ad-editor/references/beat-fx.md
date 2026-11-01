<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Effekte auf dem Beat – `beat.py` + `beat-fx.js` + `23_beatfx_render.js`

Die Idee (Referenz von celina): **Der Effekt schlägt genau mit dem Ton ein** – auf dem Beat, oder auf einem Einstellungswechsel, der selbst auf dem Beat liegt.
Nicht „ungefähr“: Der Frame, der dem Schlag am nächsten liegt, ist der Spitzenframe, und der größte Fehler ist ein halber Frame (17 ms bei 30 Frames).

> 🔎 **Was die Analyse der Referenz ergab:** Der Clip war eine Bildschirmaufnahme aus CapCut (Vlog + Soundeffekte auf der Timeline). Die Schnitte darin
> sind harte Schnitte, und **rund 70 % der Schnitte (13–14 von 19–20) fallen innerhalb von 40 ms auf einen hörbaren Schlag** (zufällige Zeiten ergeben 39–46 %)
> – der Editor schneidet also auf den Schlagton selbst, nicht auf ein festes Raster. Deshalb gibt es unten den Modus `--on onsets`.

## 1) Die Beats – `beat.py`
```bash
python3 scripts/beat.py <der Song oder das Video> --out <work>/beats.json [--click]
```
Gibt Tempo, Beats und starke Schläge aus. **`--click`** erzeugt eine Datei mit dem Song + einem Klick auf jedem Beat (lauter auf
den starken Schlägen) – sagt der Nutzer „das sitzt nicht“, lass ihn zuerst das hören.

| Die Option | Wann |
|---|---|
| `--bpm 128` | Die Erkennung lieferte das halbe oder doppelte Tempo. Es warnt selbst, wenn das doppelte Raster fast gleich stark passt (z. B. ein Song mit 174 wird als 87 erkannt) oder das Tempo außerhalb von 80–150 liegt |
| `--offset 1.2` | Der Song beginnt im Video nach 1,2 s (alle Zeiten verschieben sich) |
| `--start 30 --end 45` | Du willst einen Ausschnitt des Songs – die Zeiten beginnen bei `--start` mit null |
| `--grid` | Ein elektronischer Song mit festem Raster – sauberer als das elastische Tracking |

Die Ausgabe: `bpm` · `beats` (jeder Beat) · `accents` (starke Schläge: Taktbeginn + die stärksten 15 % + Explosionen) ·
`downbeats` · `drops` (der nächste Takt ist 4,5 dB oder mehr lauter – der größte Moment) · `onsets` (jeder hörbare Schlag mit seiner Stärke) ·
`energy` pro Beat = **Energie des Abschnitts** (Mittel eines ganzen Takts: 1 = der lauteste Abschnitt, und je 15 dB leiser = 0 – es schwankt nicht zwischen Kick/Snare) ·
`strength` = die Stärke des Beats selbst.

**Genauigkeit (gemessen an künstlichen Drums mit bekanntem Timing 76–128 BPM, mit Swing und Jitter):** alle Beats ohne Fehlen und ohne Überschuss,
mittlerer Fehler 0,4–3,4 ms und im schlimmsten Fall 11 ms. Ein Sprung von +7 dB (die Trommel ×4) wurde als Explosion auf demselben Beat erkannt, und ein gleichmäßiger Song ohne Sprung
ergab keine Explosion. Ein Song mit 174 wird als 87 erkannt (halbes Tempo) mit Warnung → `--bpm 174`, wenn du schnellere Schnitte willst.
Nur numpy + scipy, ohne librosa – ein Song von 3 Minuten in unter zwei Sekunden.

## 2) Die Bibliothek – `scripts/beat-fx.js`
Jeder Effekt ist eine reine Funktion der Zeit (derselbe Frame = dieselbe Zeichnung) – Fortsetzen und teilweises Rendern sind sicher.
**Die Farben kommen aus dem Theme des Videobesitzers** (`acc`/`clay`/`ink`/`font`); Weiß und Schwarz nur für Blitz und Balken.
⛔ **Ohne Theme = neutraler Modus** (die Montage fragt nicht nach Farben, also gibt es meist keine `theme.json`): Der Wisch ist schwarz mit grauem Rand, das Wort
ist weiß mit schwarzem Rand, die Glitch-Linien sind weiß, und das Leck nimmt seine Farbe aus der Einstellung selbst (und der automatische Planer wählt es nicht). Es gibt keine
„Standardfarbe“ aus der Identität von irgendjemandem.

| Der Effekt | Die Ebene | Was er tut | Passt zu |
|---|---|---|---|
| `zoomPunch` | Video | ein Zoom, der plötzlich hereinkommt und zurückgeht (0,32 s) | jeden Schlag – die Grundlage |
| `shake` | Video | ein Kamerawackeln, das abklingt | Kick/schwerer Schlag |
| `rgbSplit` | Video | die drei Kanäle trennen sich und kehren zurück | scharfer Schlag |
| `glitch` | Video | verschobene Streifen + Zerlegung + Linien in der Akzentfarbe (weiß ohne Theme) | Technik/Nachrichten |
| `whip` | Video | Whip-Pan: vor dem Schnitt zieht es unscharf weg, danach kommt die neue herein | **Übergang auf dem Schnitt** |
| `echo` | Video | Spuren früherer Frames **aus derselben Einstellung** (Gefühl von Zeitlupe/Zeitraffer) | starker Schlag – ⛔ kein Schnittübergang |
| `invert` | Video | ein kurzes Invertieren der Farben (3 Frames) | starker Schlag |
| `strobe` | Video | Wechsel invertiert/weiß in jedem Frame | ⛔ nur auf ausdrücklichen Wunsch |
| `flash` | oben | ein weißer Blitz, der abklingt | Schlag/Schnitt |
| `letterbox` | oben | Kinobalken, die einschlagen und zwei Beats stehen | dramatischer Moment |
| `leak` | oben | ein Lichtleck in der Akzentfarbe (ohne Theme: in der Farbe der Einstellung) zieht durch – auf dunklen Einstellungen deutlicher | Eröffnung/Ruhe |
| `wipeCircle` | oben | ein Kreis in der Akzentfarbe (ohne Theme: schwarz) bedeckt, darunter der Schnitt, dann öffnet er sich | **Übergang auf dem Schnitt** |
| `wipeDiag` | oben | ein schräger Streifen in zwei Farben (ohne Theme: schwarz/grau) zieht durch, darunter der Schnitt | **Übergang auf dem Schnitt** |
| `textSlam` | oben | ein riesiges Wort fällt und schlägt ein (von links nach rechts gesetzt, unter dem Gesicht bei 0,68). Auf dem Schlagframe vollständig im Bild | Wörter mit `--words` |

**Der automatische Planer** `BFX.plan(beats, {density, style, cuts, words, avoid, safe})`:
- Schnitte (Montage): Der starke Schlag bekommt meist einen echten Übergang (Whip/Wisch), der Rest ist leicht (Zoom/Blitz/Zerlegung).
  Ein Schnitt, der **außerhalb** des Rhythmus fiel (nicht nahe an einem Beat/hörbaren Schlag), bekommt keinen Übergang – ein harter Schnitt ist besser als ein Effekt, der ihn betont.
- Starke Schläge: ein großer Effekt – **nicht derselbe Effekt hintereinander und nicht dieselbe Familie**, und es gibt Mindestabstände (Balken alle 4 s, Leck 3 s).
  (Einzige Ausnahme: Die Explosion hat eine feste Zusammensetzung und kann nach einem Schlag mit einem ihrer Effekte kommen.)
- Normale Beats: leichter Zoom/Wackeln (`high` jeder Beat · `mid` Beat 1 und 3 im Takt · `low` nichts), und in ruhigen Abschnitten schweigen sie.
- **Die Intensität folgt der Energie des Abschnitts** (0,35 + 0,65 × `energy`) – ein ruhiger Clip ist insgesamt leichter, ein lauter Abschnitt insgesamt stärker. Die Explosion = Blitz + großer Zoom + Zerlegung zusammen.
- **Wörter (`words`) werden zuerst reserviert:** über die Länge des Clips verteilt, jedes auf dem stärksten Schlag in der Nähe seiner Position (ein starker Schlag ohne
  Schnitt ist besser, sonst ein Schnitt auf einem Schlag mit leichtem Zoom), und dazwischen mindestens ~1 s. Das Wort läuft über den nächsten Schnitt ganz normal weiter. Findet es keinen Platz
  (ein kurzer Clip und viele Wörter), **wird eine Warnung mit seinem Namen gedruckt** – es wird nicht still verschluckt.
- ⛔ `safe` (Standard): kein Strobe, und die Blitze (Flash/Invertieren) **≤ 3 pro Sekunde** (Blitzkriterium WCAG 2.3.1).
- Ein Effekt, der sich zieht (außer Wort, Balken und Leck), überquert den nächsten Schnitt nicht.
- `style:'clean'` (nur Zoom/Wackeln/Blitz/Balken/Whip) für Sprache · `'hype'` alles – für die Montage.
- `loop: <Länge des Videos>` – ist der Song kürzer und die Audiodatei wiederholt sich, wiederholen sich die Beats mit.

## a) Montage auf dem Beat (die häufigste Nutzung)
```bash
python3 scripts/beat.py <work>/bg-audio.mp3 --out <work>/beats.json
python3 scripts/12_montage.py <work> plan --dur 20 --shot 1.0 --beats <work>/beats.json   # [--on onsets|accents]
python3 scripts/12_montage.py <work> build <work>/montage.mp4          # die Schnitte genau auf dem Beat-Frame
node scripts/23_beatfx_render.js <work> <work>/montage.mp4 --audio <work>/bg-audio.mp3 --sheet
```
- `--on beats` (Standard) auf den Beats · `accents` nur auf den starken Schlägen (langsamer und prunkvoller) · `onsets` auf jedem
  hörbaren Schlag (wie in der Referenz – für Songs ohne festes Raster oder mit Soundeffekten).
- Bei `accents`: Liegt der nächste starke Schlag viel weiter weg als `--shot`, verlängert sich die Einstellung bis dorthin (wenn der Clip reicht), sonst
  landet der Schnitt auf einem normalen Beat – und es wird gedruckt, wie viele das betrifft. Ein Schnitt **außerhalb** des Rhythmus passiert nur, wenn der Clip selbst kürzer ist als der Abstand zum nächsten
  Beat, und die Warnung nennt diese Clips (entferne sie mit `drop` oder gib einen längeren).
- Der Plan wählt den Beat, der der gewünschten Länge am nächsten ist, und der starke Schlag hat Vorrang. Die Einstellungslängen sind **ganze Frames** –
  es sammelt sich keine Verschiebung an (vor der Korrektur fiel der letzte Schnitt 4 Frames hinter den Beat).
- `--xfade` stoppt von selbst bei Beats (es verschiebt den Schnitt) – die Übergänge kommen aus `23_beatfx_render.js`.
- `--sheet` → `<work>/beatfx-sheet.jpg`: für jeden Schlag 4 Frames (davor · **darauf in Rot** · +1 · +3). **Lies es** –
  der Effekt muss auf dem roten Frame selbst erscheinen, und der davor ist sauber (außer Wisch und Whip: Sie beginnen absichtlich 4–5 Frames vor dem Schnitt, und der Schnitt selbst liegt auf dem roten Frame).
- Der Plan wird in `<work>/beatfx.json` geschrieben – ändere `fx`/`k`/`t` von Hand und starte neu (ohne `--replan` bleiben deine Änderungen erhalten).
- `--words "los,schau"` Wörter, die auf verteilten Schlägen einschlagen (druckt, wo jedes landete, und warnt, wenn eines keinen Platz fand) ·
  `--density high` · `--unsafe` nur auf ausdrücklichen Wunsch.
- Das Farbtheme: `<work>/theme.json` (dieselbe Datei wie im Sprech-Modus), wenn der Videobesitzer dir seine Farben gab. Ohne sie = der neutrale Modus (oben).
  ⛔ Kopiere nicht das Theme einer anderen Person und erfinde keine Farben, „damit es schöner wird“.

## b) Ein Sprechvideo mit Schlägen auf der Audiodatei
Die Hintergrund-Audiodatei (`bg-audio.mp3`) beginnt mit `06b_master.sh` bei null **und wiederholt sich bis zum Ende des Videos**, ihre Beats = die Zeit des
fertigen Videos (und `--loop` wiederholt die Beats mit der Wiederholung der Datei).
```bash
python3 scripts/beat.py <work>/bg-audio.mp3 --out <work>/beats.json
node scripts/23_beatfx_render.js <work> - --plan-only --style clean --density low --avoid 0:3.2 --loop
cp scripts/beat-fx.js <work>/
```
`--plan-only` schreibt nur `<work>/beatfx.json` (die Länge aus `caps.json` + dem Schluss). Und in `compose.html` unter dem Engine-Skript:
```html
<script src="beat-fx.js"></script>
<script>BFX.attach({events:'beatfx.json'});</script>
```
Und nach dem Rendern und Kodieren das **Prüfblatt aus dem fertigen Video** (es rendert nichts, es liest denselben Plan):
```bash
node scripts/23_beatfx_render.js <work> <das_fertige_Video.mp4> --check    # → <work>/beatfx-sheet.jpg
```
(`BFX.attach({beats:'beats.json', density:'low', avoid:[[0,3.2]]})` ohne Plan läuft auch – es plant innerhalb der Seite und wiederholt die
Beats selbst, wenn das Video länger ist als der Song – aber ohne `beatfx.json` gibt es kein Prüfblatt.)
- Es registriert `beatFxVideo` (die Videoebene – nur innerhalb der Videokarte, wenn der Modus `R_DOWN`/`R_LOWER` ist, und es folgt dem Wackeln/Fallen des Worts
  `videoShift`) und `beatFxTop` (über der Zeichnung, **unter den Untertiteln** – der Blitz löscht die Rede nicht). Der Standard hier ist `style:'clean'`.
- ⛔ Bei Sprache **`density:'low'`** und halte dich zurück: Der Effekt dient der Rede und konkurriert nicht mit ihr. `avoid` für den Hook und für die Zahlenmomente.
- Ein einzelner manueller Effekt auf einem Wort (innerhalb der Videokarte):
  `SCENE_LIST.push(['hit',t=>BFX.applyLayer(X,t,[{t:wordsOf(3)[1].s,fx:'zoomPunch',k:0.7}],'video',{region:vrect(t)}),'video'])`
- Erprobt: ein Blitz auf dem Beat über dem Video bei intakten Untertiteln, Balken im Vollbild, der Zoom in einer `R_LOWER`-Karte (mit dem Wackeln
  des Worts `crack` – der Bereich folgt dem Versatz), und ein Song von 2 s auf einem Video von 4 s: Die Schläge liefen nach der Wiederholung weiter.

## c) Motion-Modus / jeder Canvas
```js
const ev = BFX.plan(beatsJson, {density:'mid'});   // oder deine Liste: [{t, fx, k, …}]
BFX.apply(ctx, t, ev);                              // nachdem du den Frame gezeichnet hast
BFX.at(ctx, 'zoomPunch', t, beatsJson.beats, {k:0.6});   // ein Effekt auf jedem Beat
```
`BFX.theme = {acc, clay, ink, bg, font}`, wenn die Engine `ACC/INK/…` nicht definiert. Im Browser und in node (`require` nur für die Planung).

## ⛔ Regeln
1. **Hör zu, bevor du urteilst:** Fühlt es sich „nicht passend“ an, zuerst `--click`. Das falsche Tempo (halb/doppelt) ist die häufigste Ursache → `--bpm`.
2. **Das Blatt vor der Lieferung** – der rote Frame trägt den Effekt, der davor ist sauber. Montage: `--sheet` · Sprache: `--check` am fertigen Video.
3. Strobe und schnelle Blitze sind standardmäßig aus – schalte sie nur auf ausdrücklichen Wunsch ein.
4. Das einschlagende Wort wird nicht auf das Gesicht gesetzt (Standard 0,68 der Höhe) und nicht in die Button-Zone von Instagram.
5. Montage auf dem Beat **mit einem Song** – der Song ist die Datei und die Entscheidung des Nutzers (sag „Hintergrund-Audiodatei“).
6. Kein Veröffentlichen, kein Planen – geliefert wird nur eine Datei.

## Bekannte Lücken
- `leak` ist auf hellen Einstellungen schwach (Screen-Mischung) – deutlich auf dunklen. Im neutralen Modus (Farbe der Einstellung) noch schwächer.
- Zoom/Wackeln innerhalb der Videokarte (`R_DOWN`/`R_LOWER`) zeichnet ein Rechteck – die abgerundeten Ecken der Karte werden im Moment des Effekts scharf.
- Windows: Die Skripte finden Chrome/Edge unter Windows, wurden dort aber nicht wirklich getestet.
- Die `sfx`-Tipps zu jedem Ereignis (`whoosh`/`thud`/`tap`) stehen nur im Plan – es gibt noch keine automatische Tonmischung dafür.
- Das elastische Tracking folgt einem Song, dessen Tempo sich etwas ändert, aber ein Song, der mitten drin sein Tempo wechselt, braucht `--start/--end` für jeden Abschnitt.

# Bewegungsbank – jedes Video hat eine Bewegungspalette, und du wählst bewusst

Eine nummerierte Bewegungsbank, die mit der Zeit wächst (`motion/moves/catalog.json` – 100 Bewegungen, Stand 17. Oktober). Jede Bewegung: eine fertige Funktion in `motion/moves.js` + eine Vorschau von 4 s + ihre Quelle.
**Entscheidung des Nutzers (13. Oktober):** „Ich will, dass du reich an Bewegungen bist … und bewusst.“ Er wählt nicht Bewegung für Bewegung. Du wählst für jedes Video.

> ⚠️ **Hinweis für Deutsch:** Einige Bewegungen sind ausdrücklich für **arabische Schrift** gebaut (Abschnitt 3c: Buchstabenbewegungen 62, 63, 66, 67, `pageTurnRTL`, `nuqtaCurtain`, `girihBloom`, und `ayahCalm` für Koranverse). Nutze sie bei deutschem Text **nicht**. Die Namen und Beschreibungen im Katalog (`catalog.json`) sind noch in der Sprache des Originals; die Funktionsnamen (`FX.<id>`) sind unverändert.

| Die Datei | Was darin steht |
|---|---|
| `motion/moves/catalog.json` | die Nummer · `id` · der Name · `role` · `energy` 1–3 · `families` · `cues` · die Quelle · die Vorschau |
| `motion/moves.js` | die Funktionen: `ctx.FX.<id>(ctx, t, o)` – alle Optionen stehen über jeder Funktion |
| `motion/moves/index.html` | die Galerie (wird von `scripts/35_moves.py` geöffnet) – zum Anschauen, oder wenn er etwas verbieten will |
| `motion/moves/CREDITS.md` | Quellen und Lizenzen |

## 1) Die Palette des Videos (Pflicht vor der ersten Szene)

```bash
python3 scripts/35_moves.py plan --title "<Titel des Videos>" --family auto --cues number,cta
```
Gibt die **Palette** des Videos aus:
- **Die Familie** (`family`): die Farbe der Bewegung für das ganze Video. `calm` ruhig · `punch` Energie · `onetake` eine durchgehende Kamera ohne Schnitt · `editorial` redaktionell/Erklärung.
  `auto` = die am längsten nicht genutzte. Wähle selbst, wenn das Video klar ist: ein ruhiger Tipp = `calm`, Hook und Zahlen = `punch`, eine einzige Idee, die sich entwickelt = `onetake`, Erklärung und Schritte = `editorial`.
- **3 Grundlagen** (`core`): Wortbewegung + Übergang + Kamera oder Karte. **Das ganze Video dreht sich darum**, wie im One-Take: dieselbe visuelle Sprache von Anfang bis Ende.
- **Akzente** (`accents`, höchstens 2): eine besondere Bewegung nur für einen besonderen Moment. `--cues` = die Momente im Skript:
  `number` eine starke Zahl · `list` Punkte · `price`/`cta` Preis oder Aufforderung · `contrast` Vergleich · `emphasis` Schlüsselwort · `reveal` Enthüllung · `tech` Technik · `hit` Schlag.
- **Regeln** (`rules`): laufen immer über die Zeit (z. B. J-Cut).
- **Stil** (`style`): die Form des ganzen Videos – Fläche, Textur, Schrift und Karten (17 Stile, oder die Mischung `a+b`). Details und Code: `references/styles.md`. Und `moments` = ein Momentstil (VHS/Brutal) nur für Hook oder Aufruf.
- Es wird in `moves-history.json` gespeichert, die Grundlagen wechseln also von Video zu Video. Sag dem Nutzer in einer Zeile: „Die Palette dieses Videos: Energie – gestaffelter Aufstieg + Zug + Benachrichtigungen.“

## 2) Der Rhythmus im Video

1. **Alle 2–4 s passiert etwas** (nach `pace` im Profil). Nicht jeder Satz braucht eine Bewegung: Normale Sätze laufen nur mit den Untertiteln.
2. **Die Wortbewegung der Grundlagen** auf den wichtigen Sätzen. **Der Übergang der Grundlagen** nur bei einem Szenen- oder Ideenwechsel. **Die Kamera der Grundlagen** höchstens einmal pro Szene.
3. **Der Akzent** nur in seinem Moment (die Zahl, der Preis, der Schlag), und er wiederholt sich nicht.
4. ⛔ Nicht dieselbe Bewegung zweimal hintereinander. Und hol keine Bewegung von außerhalb der Palette, außer der Satz wird von nichts aus der Palette bedient – und sag es in einer Zeile.
5. **Die Bewegung kommt aus dem Sinn des Satzes:** Die Palette legt die Sprache fest, der Satz bestimmt wo und wann. Zum Beispiel „von 0 auf 1000“ = der Zähler, nicht irgendeine Bewegung. **Und die Bank begrenzt dich nicht:** Die stärksten Momente eines Kunden waren eine Erfindung aus dem Satz – „kopieren“ → 3 Kopien von ihm, „Ideen gab es schon“ → eine Kartenwand hinter seinem Rücken. Verdient der Satz etwas, das nicht in der Bank ist, erfinde es.
6. `off` im Profil (wenn er etwas aus der Galerie verboten hat) ist endgültig verboten. `on` bevorzugt sie bei der Wahl. Beides ist optional: Standard ist, dass er nicht wählt.

## 1b) Die Galerie (optional)
`python3 scripts/35_moves.py` öffnet die Galerie zum Anschauen oder Verbieten. Und aus dem Chat: `set "3 7" --off "5"` · `show` · `list`.

## 3) Nutzung im Code

**In der Motion-Engine** (`motion/` – der Motion-Film, der One-Take, jede mit `render.js` gezeichnete Szene): ruf die Funktion direkt auf.
```js
draw(t, lt, ctx) {
  const { X, P, FX } = ctx;
  X.fillStyle = P.bg; X.fillRect(0, 0, ctx.W, ctx.H);
  FX.riseUp(ctx, t, { text: 'Die Idee ist wichtiger als das Tool', s: ctx.wordTime('l2', 0).s, accent: [1] });    // 3 gestaffelter Aufstieg
  FX.whip(ctx, t, { s: 4.2, A: Y => drawIntro(Y), B: Y => drawStats(Y) });                         // 11 Whip
  const tau = FX.ramp(t, { hit: ctx.wordTime('l3', 2).s });                                          // 20 Zeitlupe am Schlag: nimm tau statt t
}
```
- Die Farben kommen automatisch aus `ctx.P` (das Theme des Nutzers). Gib keine festen Farben mit.
- `o.s` muss die Zeit eines echten Worts sein (`ctx.wordTime`). `FX.caption` nimmt `line: 'l2'` und läuft Wort für Wort mit dem Ton.
- Die Übergänge (`crossZoom softWipe iris whip zoomWipe dotZoom dipFade slideOver clockWipe slices glitch flip lightLeak` und `compare`) nehmen `A` und `B` als Funktionen, die den ganzen Rahmen zeichnen. Setz sie in eine einzige Szene an die Stelle des Engine-Übergangs.
  `glitch` und `flip` zeichnen A/B auf denselben Rahmen und nehmen einen Schnappschuss davon, also läuft jeder FX in A/B (z. B. `MV.panel(Y, () => FX.ringStat(MV, t, …))`) richtig.
- Die Kamera (`pushIn pullOut handheld kenBurns snapZoom shake`) wickelt `draw`; `rackFocus` und `dollyZoom` nehmen `back` und `front`; `parallax` nimmt `layers:[{draw, depth}]`. Im Sprech-Reel setz sie in die Ebene `'video'`.
- `lowerThird` unten rechts innerhalb der sicheren Zone (y ≤ 1500 und x ≤ 920) – schieb es nicht in die Ecke der Buttons.
- `jcut` und `matchCut` sind Zeitregeln, keine Zeichnung: J-Cut = der Ton der nächsten Einstellung geht ihrem Bild um 4–12 Frames voraus. Match-Cut = dieselbe Form am selben Ort und in derselben Größe auf dem Schnittframe.

**Das Sprech-Reel** (`compose.html`): dieselben Funktionen, nur heißt das ctx `MV` (aus `scripts/moves-compose.js`: Text- und Zeitwerkzeuge und die Farben und Schrift von `theme.json` über dem Canvas der Engine).
`compose.REFERENCE.html` lädt `moves.js` und `moves-compose.js` aus dem Arbeitsordner, und `04_render_frames.js`/`08_safe_check.js` kopieren sie selbst, wenn sie fehlen.
Deine Szenen am Ende von `compose.html` (nach der Ladezeile):
```js
MV.ready(() => {                                   // caps.json kommt mit init an – jedes wordTime/lineSpan außerhalb des Zeichnens gehört in ready
  MV.hideCaption(MV.lineSpan(0).s, MV.lineSpan(2).e + 0.5);                 // FX.caption statt der Untertitel der Engine
  MV.scene('cap', t => { const n = [2,1,0].find(i => t >= MV.lineSpan(i).s);   // der zuletzt begonnene Satz – der nächste nimmt seinen Platz
    if (n !== undefined && t < MV.lineSpan(n).e + 0.5) FX.caption(MV, t, { line: n, y: 1280, out: MV.lineSpan(n).e }); });   // 1 · bleibt nach seiner Stimme und geht (6.1)
  const s = MV.wordTime(3, 0).s;
  MV.scene('push', t => { if (t >= s && t < MV.lineSpan(4).e)
    FX.pushIn(MV, t, { s, to: 1.18, focus: [540, 560], blur: false, draw: Y => MV.video(Y) }); }, 'video');   // 12 Videoebene
  const w = MV.wordTime(5, 0).s - 0.3;
  MV.scene('whip', t => { if (t >= w && t < MV.lineSpan(5).e)
    FX.whip(MV, t, { s: w, A: Y => MV.video(Y), B: Y => MV.panel(Y, () => FX.riseUp(MV, t, { text: 'Die Idee', s: w + 0.35 })) }); });   // 11
});
```
- Die Zeile = die Nummer des Satzes in `caps.json` (`MV.wordTime(3, 0)` = das erste Wort in Satz 3). `line: 0` funktioniert.
- `MV.video(Y, R?)` zeichnet den aktuellen Videoframe (standardmäßig Vollbild) – er ist die Szene A/B für die Übergänge und das `draw` für die Kamerabewegungen.
- `MV.panel(Y, fn)` = der Hintergrund des Themes + deine Zeichnung: ein ganzer Bildschirm zwischen zwei Einstellungen. Die Untertitel der Engine bleiben darüber.
- `MV.scene(name, fn, 'video')` für eine Bewegung, die auf dem Video selbst läuft (pushIn/pullOut), sodass die Untertitel darüber bleiben; ohne Ebene = über dem Video und unter den Untertiteln.
- ⛔ 6.1 **Ein Element verschwindet nicht mit dem letzten Wort:** `out` (Beginn des Ausgangs) = letztes Wort – und +0,3, wenn der Ausgang der Bewegung schneller als 0,4 s ist (wie `speechBubble`) – und das Szenenfenster reicht bis `out + 0.7`. Schneide das Fenster nicht bei `lineSpan(n).e` ab (`motion-rules.md` §3).
- ⚠ `FX.caption` mit dunklem Theme: Der Rand um die Wörter wird automatisch das Dunklere aus `ink`/`bg`, und das aktuelle Wort steht in `onAcc` auf der Kapsel.

## 3b) Bewegungen des freigestellten Sprechers (51–61)

`orbit couchWall uiWorld frameBreak headlineWall doodleBoil coverStory glassType phoneMockup greenScreen paperCut`
- Sie nehmen `person` (der Sprecher freigestellt, ganzer Rahmen) und `video` (das ganze Video). `glassType` nimmt `draw` statt der beiden, und `phoneMockup` nimmt nur `video`.
- **Die Freistellung gibt es nur am Mac** (`mask: required` und `mac: true` im Katalog). Bereite sie für den Bereich vor dem Rendern vor: `node scripts/11_behind_text.js <work> person 12.4-15.8`
  (nur Freistellung, ohne anderen Effekt). In der Szene gib `person: MV.person` **unverändert** mit – FX fragt `MV.person.ok()`.
- Ohne Freistellung (kein Mac, oder der Frame liegt außerhalb des Bereichs) fällt jede Bewegung selbst auf ihre Alternative zurück: das Video in einer Karte (die Umlaufbahn dreht sich um die Karte, das Cover liegt über dem Video, der Klon ist ein Bildschirm mit deinem Gesicht in einer Blase). `uiWorld` und `doodleBoil` (`mask: optional`) sind mit Freistellung schöner und laufen auch ohne.
- `o.out` = die Zeit des Ausgangs (kehrt mit derselben Bewegung rückwärts zum Video zurück).
```js
MV.ready(() => { const s = MV.wordTime(4, 0).s;
  MV.scene('cover', t => { if (t >= s && t < s + 3) FX.coverStory(MV, t, { s, out: s + 2.5, person: MV.person, video: Y => MV.video(Y), title: 'Maschine' }); }); });
```

## 3c) Die Charge 62–73 (arabische Buchstaben · Sticker · Verbindung · Kapitel)

`ijamDrop qalamWrite videoText joinSnap kufiGrid redact` (Rede) · `pageTurnRTL` (Übergang) · `tilt3D` (Kamera) · `stickerFreeze beamConnect lightRays dynamicIsland` (Karten und Ebenen).
- ⚠️ **Für Deutsch:** `ijamDrop` (62), `qalamWrite` (63), `joinSnap` (66), `kufiGrid` (67) und `pageTurnRTL` bauen auf arabischer Schrift auf (verbundene Buchstaben, Punkte, Kalligrafie, Lesen von rechts nach links) – **nicht für deutschen Text verwenden**. Sprachunabhängig sind `videoText`, `redact`, `tilt3D`, `stickerFreeze`, `beamConnect`, `lightRays` und `dynamicIsland`.
- `videoText` zeichnet den ganzen Rahmen bis `out`; danach kehrst du selbst zu `MV.video` zurück (der Schnitt passt). `tilt3D`, `lightRays` und `stickerFreeze` zeichnen das Video selbst (gib `video` mit).
- `tilt3D` = dieselbe Bewegung für jedes Kapitel im Video (eine Regel) – ändere nur `title` und `num`.
- **`stickerFreeze` braucht einen Frame zu einer anderen Zeit** – eine Ergänzung der Engine (17. Oktober) in `moves-compose.js`:
  `MV.frameAt(Y, t, R?)` der Videoframe bei t (`vfr/`), und `MV.personAt(Y, t, R?)` die Freistellung bei t (`bt/person/`). Die erste Anfrage lädt das Bild, und `04_render_frames.js` wartet auf `MV.settle()` und zeichnet den Frame vor der Aufnahme neu, das Ergebnis ist also deterministisch.
  Die Freistellung muss den Moment des Einfrierens abdecken: `node scripts/11_behind_text.js <work> person <von-bis>` und der Bereich enthält `s`. Ohne Freistellung fällt es auf ein Polaroid des ganzen Frames zurück (`videoAt: MV.frameAt`).
```js
MV.ready(() => { const s = MV.wordTime(6, 0).s;
  MV.scene('freeze', t => { if (t >= s && t < s + 2.4) FX.stickerFreeze(MV, t, { s, out: s + 2, person: MV.person, personAt: MV.personAt, video: Y => MV.video(Y), videoAt: MV.frameAt, text: 'Stopp!' }); }); });
```

## 3d) Die Charge 75–87 (Kopie · Karte · Kran · Terminal · Glas · Gesicht)

`morphWord` (Rede) · `nuqtaCurtain glassLens scanLine` (Übergänge, nehmen `A` und `B`) · `craneUp punchCut` (Kamera) · `cloneTrio dotMap rimOutline terminalType lineChartDraw girihBloom speechBubble` (Karten und Ebenen).
- ⚠️ Für Deutsch ungeeignet: `nuqtaCurtain` (Vorhang aus arabischen Punkten) und `girihBloom` (arabische Geometrie) – sie sind dekorativ und laufen auch ohne Text, passen aber zur arabischen Bildsprache; nutze sie nur, wenn sie zur Marke passen.
- **Die Freistellung (Mac):** `cloneTrio` und `rimOutline` (`mask: required`) – ohne sie: 3 Videokarten / ein Strahl auf dem Rand der Karte. `girihBloom` (`optional`) hinter der Person mit Freistellung, über dem Video ohne.
  `cloneTrio` nimmt `personAt: MV.personAt` (die Kopien um 0,2/0,4 s verspätet) und `videoAt: MV.frameAt` für die Alternative – dieselbe Bedingung der Freistellung wie in 3c.
- **Das Gesicht (Mac, `face: optional` im Katalog)** – `speechBubble` und `punchCut`: eine Ergänzung der Engine (17. Oktober):
  `python3 scripts/36_facetrack.py <work> <von> <bis>` erzeugt `face.js` (derselbe `facetrack.swift` wie im Podcast, geglättet σ=5 Frames). Setz es in compose.html: `<script src="face.js"></script>`, und gib `face: MV.faceAt` mit.
  `MV.faceAt(t)` = `{x,y,w,h,mx,my}` in Canvas-Koordinaten (im selben Ausschnitt wie `MV.video`) oder `null` – dann kehrt die Bewegung an einen Standardort zurück.
  `punchCut` fixiert das Gesicht auf dem ersten Frame jeder Einstellung (die echte Kamera folgt nicht), und die Grenze ×2.
- `glassLens` Die Linse trägt die neue Szene mit sich (`carry`), also bleibt alles in der Mitte von B vollständig darin – halte den Titel von B auf ein oder zwei Wörter (am breitesten ~400 px), damit kein Wort an ihrem Rand abgeschnitten wird.
- `scanLine` nimmt `Aat: MV.frameAt` (das Alte ist unter der Linie eingefroren). `craneUp` nimmt `A` (das Video) und `B` (die nächste Karte) – nach `at + 0.5` zeichne `B` selbst. Die Karten sind Standbilder (`cards`).
- `dotMap` hat ihre Karte eingebaut (eine vereinfachte Landmasse, vom Atlantik bis Japan) – Städte außerhalb dieses Bereichs erscheinen nicht. In `terminalType` sind Befehl und Ausgabe englisch (Menlo/monospace), und der Kommentar steht in seiner Zeile.
```js
MV.ready(() => { const s = MV.wordTime(5, 0).s;
  MV.scene('bubble', t => { if (t >= s && t < MV.lineSpan(5).e + 1) FX.speechBubble(MV, t, { s, out: MV.lineSpan(5).e + 0.3, line: 5, face: MV.faceAt }); });   // bleibt nach seiner Stimme (6.1)
  const p = MV.wordTime(7, 0).s;
  MV.scene('cam2', t => { if (t >= p && t < MV.lineSpan(7).e) FX.punchCut(MV, t, { s: p, out: MV.lineSpan(7).e, video: Y => MV.video(Y), face: MV.faceAt }); }, 'video'); });
```

## 3e) Die Charge C: 74 und 88–100 (Vers · Post · Rechnung · Suche · Tür · Echo)

`ayahCalm echoStack warpWave` (Rede) · `bentoCut doorway lumaMelt` (Übergänge, nehmen `A` und `B`) · `bodyFollow swishSettle motionEcho` (Kamera) · `postCard palmHold receiptPrint searchBar pointerCursor` (Karten und Ebenen).

**74 `ayahCalm` ist ausschließlich für Koranverse in arabischer Schrift** und für deutschen Text nicht relevant. Falls ein Kunde doch einen heiligen Text zeigt: nur wörtlich aus einer verlässlichen Quelle kopieren, nie von Hand schreiben oder ändern, und nicht mit Buchstabenbewegungen oder Glitch kombinieren.

**Der Rest:**
- `bodyFollow` (89) braucht das Gesicht (`face: MV.faceAt` aus `36_facetrack.py` – Mac); ohne fällt es auf `handheld` (31) zurück. In der Ebene `'video'`.
- `motionEcho` (100) braucht einen Frame zu einer anderen Zeit: `videoAt: MV.frameAt`, und mit Freistellung (`mask: optional`) `person: MV.person, personAt: MV.personAt`, sodass das Echo nur auf deinem Körper liegt. Ohne beide wird es übersprungen. Setz es zusammen mit `FX.ramp` (20) auf denselben Schlag.
- `palmHold` (91) braucht die Handfläche (`hand: optional`): `python3 scripts/29_handtrack.py <work> <von> <bis>` erzeugt `palm.js` – setz es in compose.html und gib `palm: MV.palmAt` mit. Ohne sie bleibt das Element fest unten links.
- `postCard` (88): ⚠ Mach keinen gefälschten Post für eine echte Person – entweder eine echte Aufnahme oder die Worte des Kontoinhabers selbst. Ohne das Logo irgendeiner Plattform.
- `receiptPrint` (93) Die Preise mit normalen Ziffern und die Währung aus `currency` (z. B. `'€'`). `searchBar` (94) und `pointerCursor` (98) ein Mauspfeil in der Tintenfarbe des Themes; `pointerCursor` nimmt `steps` (mehrere Klicks) und `targets` (Knöpfe, die er zeichnet).
- `swishSettle` (95) ist ein Szenenbeginn (wickelt `draw`), er wächst selbst, bis der Rand des Rahmens nicht mehr sichtbar ist. `doorway` (97) und `lumaMelt` (99) zeichnen `A` auf ein Hilfs-Canvas.
```js
MV.ready(() => { const h = MV.wordTime(3, 2).s;
  MV.scene('echo', t => { if (t >= h - 0.1 && t < h + 0.7) FX.motionEcho(MV, t, { s: h, video: Y => MV.video(Y), videoAt: MV.frameAt, person: MV.person, personAt: MV.personAt }); }, 'video'); });
```

## 3f) Tiefenmomente – Spitzenniveau von der ersten Fassung an (6.0, aus einem Reel für einen Bankkunden)

Das Reel (von der Bank abgenommen und viral gegangen) gelang, weil das Motion **von der ersten Fassung an tief** war. Das Prinzip: Steck die Mühe in Performance und Motion – nicht in brave Sachen.
Karten, Stempel und Badges sind nicht verboten; nutz sie, wenn das Thema es verdient. Aber bevor du zeichnest, **plane 2–3 Tiefenmomente** für das Reel und nenn sie in einer Zeile:
„Tiefenmomente: die Welle deiner Stimme hinter deinem Kopf bei (Interview mit Stimme) · die Karte von Deutschland bei (erstes Mal) · eine Umlaufbahn um dich bei (Kunde/Arbeit/Mitarbeiter).“

| Das Werkzeug | Wann | Wie |
|---|---|---|
| **Hinter der Person** | jedes Element (Welle, Karte, Umlaufbahn), das hinter seinem Kopf vorbeizieht | schneide den Bereich frei: `node scripts/11_behind_text.js <work> person 5.8-7.7` · zeichne in der Ebene `'video'` und dann `MV.person(X)` darüber |
| **Die Welle seiner Stimme** | „Stimme“, „spricht“, „Interview“, KI antwortet | `python3 scripts/37_env.py <work>` → `env.js` · `<script src="env.js">` · die Höhe = `MV.env(t)` |
| **Punktkarte** | ein Ort, „zum ersten Mal in Deutschland“, Verbreitung | `FX.dotMap` mit `cities:[]` und hellen Farben, wächst langsam hinter seinem Kopf |
| **3D-Umlaufbahn** | 3 Dinge (Kunde · Arbeit · Mitarbeiter) | ein ovaler Ring: Der Text dahinter wird vor `MV.person` gezeichnet und der davor danach |
| **Eine Form aus der Kundenidentität** | eine Zahl, ein Übergang | sein Logobogen zeichnet sich = ein Zähler (`k` von 0 bis 1) oder ein Wisch, der den Bildschirm verschluckt, mit der nächsten Einstellung darin |
| **Ein One-Take-Einstieg** | ein Einstellungswechsel | Die Kamera taucht in das Logo/Tablet (Zoom 1→10 + Unschärfe) und kommt mit der nächsten Einstellung heraus – `MV.frameAt` für den eingefrorenen Frame |
| 🆕 6.1 **Licht in der Kundenfarbe hinter der Person** | der Name des Kunden, „sie haben es freigegeben“, ein Markenmoment | Die Wand dahinter färbt sich in seiner Identität (`multiply` + ein `screen`-Schein), dann `MV.person(X)` darüber – **sein Gesicht ohne jede Farbänderung**. Es leuchtet wie eine Glühbirne auf (Flackern in den ersten 0,3 s) |
| 🆕 6.1 **Spark-Übergang** | jeder Orts-/Einstellungswechsel – dieselbe Sprache im ganzen Reel | Die nächste Einstellung enthüllt sich **innerhalb einer Form aus seiner Identität** (Icon/Zeichen), die sich dreht und wächst, bis sie den Bildschirm bedeckt, mit einem Rand in der Akzentfarbe – `sparkReveal` unten |

```js
/* Die Welle seiner Stimme hinter seinem Kopf – die Videoebene, und die Person darüber */
MV.scene('wave', t => { if (t < 5.86 || t > 7.62) return;
  const n = 43, cx = 540, cy = 790; X.save(); X.fillStyle = '#fff';
  for (let i = 0; i < n; i++) { const x = 40 + i * (1000 / (n - 1)), d = Math.abs(x - cx) / 500;
    const h = 18 + 420 * MV.env(t - d * 0.22) * (1 - d * 0.3); X.fillRect(x - 7, cy - h / 2, 14, h); }
  X.restore(); MV.person(X); }, 'video');

/* Punktkarte hinter seinem Kopf – helle Farben, ohne Städte */
const MAPC = Object.assign({}, MV, { P: Object.assign({}, MV.P, { mut: '#FFFFFF', bg: '#FFFFFF', ink: '#FFFFFF' }) });
MV.scene('map', t => { if (t < 11.8 || t > 14.4) return;
  FX.dotMap(MAPC, t, { s: 11.8, y: 140, cities: [], total: null, title: null }); MV.person(X); }, 'video');

/* Umlaufbahn: das Hintere vor der Person, das Vordere danach (orbitDraw ist deine Funktion: front=false zeichnet die hintere Hälfte des Rings) */
MV.scene('orbit', t => { if (t < 31 || t > 38) return; orbitDraw(t, false); MV.person(X); orbitDraw(t, true); }, 'video');

/* Ein One-Take-Einstieg mit einem Punkt (px,py) am Schnitt tc */
function dive(t, tc, px, py) { if (t < tc - 0.38 || t > tc + 0.36) return;
  if (t < tc) { const k = Math.pow(2, 10 * ((t - tc + 0.38) / 0.38) - 10), s = 1 + 9 * k;
    X.save(); X.filter = `blur(${(k * 14).toFixed(1)}px)`; X.translate(px, py); X.scale(s, s); X.translate(-px, -py); MV.video(X); X.restore(); }
  else { const k = 1 - Math.pow(2, -10 * ((t - tc) / 0.36)), s = 1.45 - 0.45 * k;
    X.save(); X.filter = `blur(${((1 - k) * 12).toFixed(1)}px)`; X.translate(540, 900); X.scale(s, s); X.translate(-540, -900); MV.video(X); X.restore(); } }
```

**🆕 6.1 Aus dem Reel „1000 € an einem Tag“ (Rückmeldung: „auf einem anderen Level“) – die beiden gelobten Rezepte:**
```js
/* Licht in der Kundenfarbe hinter der Person: Die Wand färbt sich, das Gesicht wird nicht angefasst. Zuerst den Bereich freistellen (Mac):
   node scripts/11_behind_text.js <work> person 32.3-36.3   ← deckt on-0.05 bis off+0.45 ab
   Die Farben = die offizielle Identität des Kunden aus facts.md (Beispiel: #C8102E · #961428) – der Moment seiner Identität, nicht das Theme des Reels */
MV.ready(() => { const RL = { on: MV.wordTime(19, 4).s - 0.06, off: MV.lineSpan(20).e + 0.05 };   // „… Kundenname“ → Ende von Satz 20
MV.scene('brandLight', t => {
  if (t < RL.on - 0.05 || t > RL.off + 0.45 || !MV.person.ok()) return;            // ⛔ ohne Freistellung für diesen Frame nicht färben – es würde sein Gesicht färben
  const fl = t < RL.on + 0.32 ? [1, 0.25, 0.95, 0.4, 1][Math.min(4, Math.floor((t - RL.on) / 0.065))] : 1;   // leuchtet wie eine Glühbirne auf
  const a = pr(t, RL.on, RL.on + 0.05) * fl * (1 - eio(pr(t, RL.off, RL.off + 0.45))); if (a <= 0) return;
  X.save(); X.globalAlpha = a; X.globalCompositeOperation = 'multiply';              // die helle Wand nimmt die Farbe (auf der dunklen sieht man sie nicht)
  const g = X.createRadialGradient(560, 820, 60, 560, 900, 1250); g.addColorStop(0, '#FF4D5E'); g.addColorStop(0.45, '#C8102E'); g.addColorStop(1, '#961428');
  X.fillStyle = g; X.fillRect(0, 0, 1080, 1920); X.restore();
  X.save(); X.globalAlpha = a * 0.55; X.globalCompositeOperation = 'screen';         // ein weicher Schein hinter dem Kopf
  const g2 = X.createRadialGradient(560, 760, 20, 560, 760, 620); g2.addColorStop(0, 'rgba(255,90,100,.85)'); g2.addColorStop(1, 'rgba(255,90,100,0)');
  X.fillStyle = g2; X.fillRect(0, 0, 1080, 1920); X.restore();
  MV.person(X);                                                                      // er steht über der Färbung, wie er ist – null Farbbearbeitung an seinem Bild
}, 'video'); });

/* Spark-Übergang: tc = erster Frame der nächsten Einstellung · shape(Y,x,y,size,rot,col) zeichnet die Form seiner Identität, gefüllt mit col.
   Vor dem Schnitt: A = das Live-Video und B = der erste Frame der nächsten Einstellung eingefroren · danach: A = der letzte Frame eingefroren und B = live */
let SPARK_CV = null;   // ⚠️ Nenne deine Konstanten nicht AR oder MARK – die Engine definiert sie (der Fehler „already declared“ bricht dein ganzes Szenenskript ab)
function sparkReveal(Y, t, tc, shape, o = {}) {
  const d0 = o.d0 || 0.34, d1 = o.d1 || 0.42; if (t < tc - d0 || t > tc + d1) return false;
  const FR = 1 / 30, A = Z => (t < tc ? MV.video(Z) : MV.frameAt(Z, tc - FR)), B = Z => (t >= tc ? MV.video(Z) : MV.frameAt(Z, tc + FR));
  const xi = u => u <= 0 ? 0 : Math.pow(2, 10 * u - 10), xo = u => u >= 1 ? 1 : 1 - Math.pow(2, -10 * u), k = pr(t, tc - d0, tc + d1);
  const g = k < 0.5 ? 0.5 * xi(k * 2) * 0.85 + 0.5 * (k * 2) * 0.15 : 0.5 + 0.5 * xo((k - 0.5) * 2);   // bremst → schießt am Schnitt los → beruhigt sich
  const S = lerp(10, 12500, g), rot = -0.9 + 1.6 * eio(k), cx = o.cx || 540, cy = o.cy || 900;
  if (!SPARK_CV) { SPARK_CV = document.createElement('canvas'); SPARK_CV.width = 1080; SPARK_CV.height = 1920; }
  const G = SPARK_CV.getContext('2d');
  A(Y);
  Y.save(); Y.globalAlpha = 1 - pr(k, 0.75, 1); shape(Y, cx, cy, S * 1.045, rot, o.edge || MV.P.acc); Y.restore();   // der Akzentrand hinter der Maske
  G.setTransform(1, 0, 0, 1, 0, 0); G.globalCompositeOperation = 'source-over'; G.clearRect(0, 0, 1080, 1920); B(G);
  G.globalCompositeOperation = 'destination-in'; shape(G, cx, cy, S, rot, '#000'); G.globalCompositeOperation = 'source-over';
  Y.drawImage(SPARK_CV, 0, 0); return true;
}
/* Die Identitätsform als Path2D (scharf in jeder Größe, ohne Laden): Der Pfad aus dem SVG seines Logos mit viewBox 0 0 100 100 */
const BRAND_PATH = new Path2D('M50 0 L61 39 L100 50 L61 61 L50 100 L39 61 L0 50 L39 39 Z');   // Beispiel: ein Stern – setz den Pfad seines Zeichens
const brandMark = (Y, x, y, s, r, col) => { Y.save(); Y.translate(x, y); Y.rotate(r); Y.scale(s / 100, s / 100); Y.translate(-50, -50); Y.fillStyle = col; Y.fill(BRAND_PATH); Y.restore(); };
MV.scene('sparks', t => { for (const [tc, cx, cy] of [[262 / 30, 760, 905], [1639 / 30, 540, 440]]) sparkReveal(X, t, tc, brandMark, { cx, cy }); }, 'video');
```
- **Die Mitte der Form** = etwas in der Einstellung, das es verdient (das Logo im Hintergrund, das Handy, der Kopf) – im Reel „1000 €“ einmal auf dem Handy (760, 905) und zweimal über dem Kopf (540, 440).
- Ist die Form ein Bild (ein PNG-Icon)? Färbe es mit `source-in` auf einem Hilfs-Canvas und lass das Bild vor dem Zeichnen laden (`MV.settle` muss darauf warten) – Path2D ist einfacher und schärfer.
- Die Schnitte `tc` kommen aus den Schnitten in `cut.json` (der erste Frame der neuen Einstellung), und `MV.frameAt` braucht `vfr/` (liegt seit Schritt 6 vor). `08_safe_check.js` zählt den eingefrorenen Frame als Video.
- Beide im Vollbild (`R_FULL`) – `MV.video` und `MV.person` zeichnen den ganzen Rahmen; im Kartenmodus zerstören sie das Layout.
- Derselbe Übergang bei jedem Ortswechsel (3-mal in einem Reel von zwei Minuten) – die feste Sprache ist Teil des Niveaus. Und „Licht des Kunden“ ist einer der 2–3 Tiefenmomente, nicht in jedem Satz.
- Das sind Ideen, keine Vorlagen: Jedes Reel erfindet seine Momente aus seiner Rede und der Identität seines Kunden (Beispiel: der Logobogen als 90-Sekunden-Zähler, ein Rennen „einer der ersten“, eine rote Stufenkarte).
- Jeder Satz, dessen Worte das Motion selbst schreibt = `nocap` für diesen Satz (`references/scenes.md`).
- Text, der vor der Person erscheinen muss (Modus `cutout`) = die Ebene `'afterPerson'` oder `window.AFTER_PERSON`.
- `08_safe_check.js` zählt den eingefrorenen Frame (`MV.frameAt`) als Video, nicht als Text – die Übergänge geben keinen Fehlalarm (6.0).

## 4) Eine neue Bewegung hinzufügen (die Bank hat 100 – jede Ergänzung bekommt eine neue Nummer am Ende)

0. Gib ihr im Katalog `role`, `energy`, `families` und `cues`. **Zuerst die schwachen Familien**: `plan --dry` für jede Familie, und sieh, wo die Auswahl klein ist.
1. Eine neue Funktion in `moves.js` in derselben Form `FX.<id>(ctx, t, o)`, und die Farben aus `ctx.P`.
2. Eine Zeile im Katalog **mit einer neuen Nummer am Ende**. ⛔ Nummeriere das Alte nicht neu: Die Leute kennen die Nummern.
3. Eine Vorschau von 4 s in halber Auflösung: `previews/NN.mp4`, aus derselben Funktion gezeichnet, nicht aus anderem Code.
4. Die Quelle in `CREDITS.md`, mit einem Link, den du selbst geöffnet hast.

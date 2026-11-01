# Stilbank – die visuelle Sprache des ganzen Videos

Die Bewegungen (`references/moves.md`) beantworten **„Wie bewegt es sich“**. Der Stil beantwortet **„Wie sieht es aus“**: Fläche, Textur, Schrift, Kartenform, Sticker und der Charakter der Bewegung.
Dieselbe Bewegung „gestaffelter Aufstieg“ wirkt im Papierstil wie Papier und im Keynote-Stil sauber und weich.

| Die Datei | Was darin steht |
|---|---|
| `motion/styles.js` | 17 Stile (Tokens) + Flächen, Karten, Sticker und Signaturen · `STYLES.make(spec)` |
| `motion/styles/catalog.json` | daraus erzeugt (`node motion/styles.js --catalog`) – wird von `35_moves.py` gelesen |

## 1) Der Stil kommt mit der Palette des Videos

`python3 scripts/35_moves.py plan …` gibt jetzt einen **`style`** mit Familie und Bewegungen aus (eine Wahl, die zu Familie und Momenten passt, sich nicht hintereinander wiederholt, und ein Drittel der Videos bekommt eine **Mischung** `a+b`).
- `--style auto` (Standard) · `--style paperCut` · `--style explainer+keynote` · `--style none` (nur das Theme des Nutzers).
- `moments` = ein Momentstil (VHS, Brutal) für Hook oder Aufruf **nur 1–3 s**, nicht für das ganze Video.
- Sag dem Nutzer in einer Zeile: „Die Palette dieses Videos: Papier-Cutout – gestaffelter Aufstieg + Zug + Benachrichtigungen.“

## 2) ⚠️ Eine Sprache, keine Vorlage – das ist die wichtigste Zeile

Der Stil ist **Vokabular**, mit dem du dich ausdrückst, keine Form zum Kopieren. Wirklich stark:
- **Mische:** `A+B` = Fläche, Textur, Karte und Person von A, Schrift, Bewegung und Sticker von B. (Nicht zwei Texturen und nicht zwei Display-Schriften.)
- **Nimm einen Teil:** nur die Fläche des Dokustils mit den Karten von Keynote, oder den Stempel des Dokustils in einem einzigen Moment in einem Papier-Video.
- **Erfinde aus dem Sinn des Satzes – das lässt den Zuschauer „wow“ sagen:** Er sagte „kopieren“ → daraus entstanden 3 Kopien. Er sagte „davor gab es schon Ideen“ → hinter seinem Rücken breitete sich eine Wand voller Ideenkarten aus („Kreativität“). Die Bank (Bewegungen und Stile) **begrenzt dich nicht:** Verdient der Satz etwas, das es nicht gibt, bau es von Grund auf. Der Stil gibt dir die Textur, die Idee kommt aus dem Satz.
- Stopf nicht alle Signaturen eines Stils in ein Video – 2–3 Signaturmomente reichen, der Rest sind saubere Untertitel.

## 3) Die 17

| id | Name | Wann | Hinweis |
|---|---|---|---|
| `keynote` | Keynote | Enthüllung, Zahl, Launch, Ruhe | ein riesiges Wort hinter dem Kopf · nur eine Farbe |
| `glassUI` | Glas-Oberfläche | App, Chat, Listen | Benachrichtigungen und Glaskarten über dem Video |
| `explainer` | Zeitungs-Erklärer | Nachricht, Vergleich, Quelle | gelber Textmarker, Schnipsel mit Reißzwecke, roter Faden |
| `paperCut` | Papier-Cutout | Schlag, Liste, Spaß | die Person als Sticker mit weißem Rand · 12 Frames pro Sekunde (Stop-Motion) |
| `archive` | Doku | Geschichte, Historie, Geheimnis | Sepia + Körnung nur auf dem Hintergrund · Schreibmaschine · Stempel |
| `editorial` | Magazin | Zitat, Profil | riesiger Titel hinter dem Kopf + feine Linien |
| `swiss` | Schweizer Stil | Zahlen, Schritte, Daten | Raster, Rot/Schwarz/Weiß, keine Drehung |
| `doodle` | Handzeichnung | Betonung, Tipp, Erklärung | ein Kreis um das Wort, ein Handpfeil, der kocht |
| `terminal` | Terminal | Code, KI-Tools | dunkles Fenster, Befehle, Cursor · jede Codezeile für sich LTR |
| `riso` | Riso | Hook, Titel | zwei versetzte Farben · die Person als Halbton (Momente, nicht das ganze Video) |
| `newsprint` | Zeitung | Nachrichten, Eilmeldung | die Zeitungsrolle · kein echtes Zeitungslogo |
| `blueprint` | Bauplan | „Wie funktioniert es“, Teile | Messraster, Callouts, Maßpfeile |
| `vhs` | VHS | Rückblende, „früher“ | **nur ein Moment** – nicht auf den Untertiteln |
| `brutal` | Brutal | Hook, Aufruf | **nur ein Moment** – schwarze Rahmen, harter Schatten und Wackeln |
| `studio3D` | Produktstudio | Toolname, „kostenlos“ | gedimmter, hervorgehobener Name + schwarzes Tag ✓ |
| `stickerToon` | Cartoon-Sticker | Spaß, Tool-Erklärung | schwarzer Rand fester Stärke · Blase · Maskottchen **aus unserer Zeichnung** |
| `devCard` | Tool-Karte | Skill, Tool, Tatsache | weiße Karte auf Raster und Strahlen · ein Akzentwort im Flicken · Chips |

**`needsCut`** (Keynote, Zeitungs-Erklärer, Papier, Magazin, Schweizer Stil, Riso, Zeitung, Bauplan, Studio, Sticker, Tool-Karte): Die Fläche tauscht den Videohintergrund – braucht die Personen-Freistellung (Mac). Außerhalb des Mac oder ohne Freistellung: Der Stil legt seine Farben, Schriften und Karten über das normale Video, ohne zu brechen.
**Die Identitätsfarbe:** Der Stil nimmt `acc` aus dem Theme des Nutzers, außer jenen, deren Farbe Teil ihrer Identität ist (`lockAcc`: Zeitungs-Erklärer, Doku, Riso, Schweizer Stil, Terminal, VHS, Bauplan, Brutal, Zeitung).

## 4) Im Code

**Der Motion-Film** (`motion/` · `render.js`): `project.json` → `"style": "paperCut"` → die Farben und Schriften des Projekts kommen vom Stil, und `ctx.S` ist bereit:
```js
draw(t, lt, ctx) {
  const { X, S } = ctx;
  S.background(X, t, { video: Y => drawVideo(Y), person: Y => drawPerson(Y), behind: Y => S.label(Y, 'komplett', 540, 720, { k: S.ease((t - 0.4) / 0.5) }) });
  S.label(X, 'gebaut auf Arbeit', 540, 1500, { k: S.ease((t - 2) / 0.4), tape: true });   // ein Sticker mit der Signatur des Stils
  S.sig.tape(X, t, { x: 300, y: 1440 });   // die Signaturen: tape pin string typewriter redact arrow code tag breadcrumb mascot bubble dimension shake spin
  S.post(X, t);              // die letzte Textur (Körnung/Vignette)
}
```
**Das Sprech-Reel** (`compose.html`): einmal über deinen Szenen:
```js
const S = MV.useStyle('explainer+keynote');            // MV.P und die Schriften display/body/num kommen vom Stil
MV.scene('s', (Y, t) => {
  S.background(Y, t, { video: y => MV.video(y), person: MV.person.ok() ? y => MV.person(y) : null });
  S.label(Y, 'Die Zahl', 540, 420, { k: S.ease((t - 3.1) / 0.5) });
  S.post(Y, t);
});
```
- `S.label(X, Text, x, y, {k, size, color, bg, rot, seed, …})` – `k` = Fortschritt des Eintritts 0..1 (gib ihn mit `S.ease` mit). Jeder Stil hat seinen Sticker (slap/stamp/highlight/chip/notif/…), und `{kind:'stamp'}` borgt den Sticker eines anderen Stils.
- `S.card(X, x, y, w, h, {kind})` · `S.text(X, Text, x, y, {role:'display'|'body'|'num'|'accent'|'hand'})` gibt die Breite zurück.
- `S.tq(t)` = die Zeit „auf Zweien“ für Stile mit `fps` (Papier, Sticker) – nutz sie für die Bewegung, damit es nach Stop-Motion wirkt.
- Normale Ziffern, die Zufallswerte sind fest (`S.rng(seed)`).

## 5) Lizenzen

Alles ist per Code gezeichnet (keine externen Assets). Die Schriften stammen aus `motion/fonts` (OFL). **Apple-Schriften (SF) sind verboten** – ihre Lizenz gilt nur für Oberflächen auf Apple-Geräten, nicht für Reels. „Keynote“ ist ein Stilname, keine Nachahmung von Apple: weder ihr Logo noch ihre Icons.

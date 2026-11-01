<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

### 7.9) 🖼️ Generierte Szenen (v3.2) – Format und Regeln

**Die Idee (Nutzer, 18. September 2026):** Ein Satz, den der Code nicht gut zeichnet, bekommt ein generiertes Bild oder einen Clip als Hintergrund der Szene, und die Engine zeichnet per Code darüber. Eine neue Quelle für Szenen in der Hauptengine selbst, keine eigene Engine, und sie folgt denselben Regeln für Untertitel und sichere Zone.

Sagt er einen Satz, den der Code nicht gut zeichnet („Stell dir vor, du sitzt im Büro, das iPad aufgeklappt und der Kaffee daneben“ · „Was ist besser: Papier oder das Handy?“): Aus dem Satz selbst entsteht ein Bild oder kurzer Clip, kommt als Szene herein, und die Engine zeichnet darüber (Zahl, Vergleich, ein Kreis um den Gewinner, ein Häkchen).

```bash
# 1) Schreib <work>/gen.json: die Assets (Beschreibung jedes Bildes/Clips) + die Szenen (wann sie hereinkommen und was darüber gezeichnet wird – nach Wort, nicht nach Sekunde)
python3 scripts/17_gen_scenes.py <work> cost     # was es kostet, bevor du generierst (Bild ≈ 0,04 $ · Clip 5 s ≈ 0,25 $)
python3 scripts/17_gen_scenes.py <work> fetch    # generiert nur das Fehlende → gen/ und aktualisiert studio.json · danach normal 04_render_frames
```

**Die Datei `<work>/gen.json`:**
```json
{
 "assets": [
  {"k":"desk",        "kind":"video", "dur":10, "ar":"9:16", "prompt":"cinematic slow dolly across a tidy wooden desk, a tablet on a stand, a coffee cup with steam, warm window light"},
  {"k":"paper_phone", "kind":"image", "ar":"3:4",  "prompt":"top-down flat lay: on the LEFT an open paper notebook with a pen (empty ruled lines only), on the RIGHT a smartphone with a blank glowing screen, cream desk"}
 ],
 "scenes": [
  {"s":"w:diesen", "e":"w:Clips+", "k":"desk", "mode":"bg", "kb":false},
  {"s":"w:dass", "e":"w:Antwort+", "k":"paper_phone", "mode":"card", "draw":[
     {"op":"vs",     "at":"w:oder",    "l":"Papier", "r":"Handy"},
     {"op":"circle", "at":"w:gezeichnet", "x":0.74, "y":0.52, "r":0.2},
     {"op":"check",  "at":"w:Antwort", "x":0.74, "y":0.30}
  ]},
  {"s":"w:Clip", "e":"w:Bild+", "k":"desk", "mode":"card", "kb":false, "draw":[{"op":"num","at":"w:25","txt":"25 Cent"}]}
 ]
}
```

| Schlüssel | Bedeutung |
|---|---|
| `s` / `e` | Sekunden, oder `"w:Wort"` = der Moment, in dem das Wort gesprochen wird (sucht ab Beginn der Szene), und `"w:Wort+"` = das Ende seiner Aussprache. **Die Szene hängt am Wort** – 6.1: Sie bleibt bis `e` und geht danach ruhig über 0,4 s |
| `k` | der Name des Assets aus `assets` |
| `mode` | `bg` Vollbild-Hintergrund dahinter (nutz es mit `R_LOWER`, dann wird er zu einer kleinen Karte darüber) · `card` eine Karte oben 130..950×230..1230 mit `R_LOWER` · `full` deckt alles ab mit `R_OFF` |
| `kb` | Ken-Burns-Bewegung (langsamer Zoom 1→1,08) – automatisch an für Bilder und aus für Clips |
| `draw` | Operationen über dem Bild, jede kommt mit einer Feder bei `at` herein und bleibt bis zum Ende der Szene. Die Koordinaten sind Anteile 0..1 der Karte (x von links, y von oben) |

**Zeichenoperationen:** `text` (Kapsel in der Akzentfarbe: `txt,x,y,size`) · `num` (riesige Zahl oben auf der Karte: `txt`) · `circle` (ein Ring, der sich um einen Punkt zeichnet: `x,y,r`) · `vs` (eine Vergleichslinie in der Mitte + zwei Beschriftungen: `l` links, `r` rechts) · `check` (Häkchen-Kreis: `x,y`) · `underline` (Handlinie: `x,y,w`).

**Aufteilung der Szenen im Video (`studio.json` → `scenes`):** Die generierte Szene `bg`/`card` braucht `R_LOWER` im selben Bereich, damit der Sprecher als kleine Karte nach unten rückt; danach direkt wieder Vollbild (gleiche Regel wie die 8 Sekunden).

**⛔ Die Regeln (vom Nutzer abgenommen):**
1. **2 bis 4 Szenen** im Video, und der Satz, der eine Szene bekommt, enthält einen Ort, einen Vergleich oder etwas Greifbares. Hook und Schlussaufruf nicht.
2. **Gib die Bildbeschreibungen im Chat aus, bevor du generierst** – der Nutzer stimmt zuerst der Idee zu (gleiche Regel wie Skript vor Design), und nenn die geschätzten Kosten (`cost`).
3. **Das Bild drückt die Idee aus, nicht das Produkt:** Das echte Produkt (Gerät, App) kommt von seiner offiziellen Website, damit wir keine falschen Tasten zeigen. Generierte Bilder sind für Stimmung und Metapher.
4. **Keine Frauen · keine gezeichneten Logos · kein lesbarer Text im Bild** (das Skript fügt das der Beschreibung automatisch hinzu, und du schreibst „empty ruled lines only“, wenn Papier vorkommt). Erscheinen Buchstaben im Bild, lösche es und generiere neu (4 Cent).
5. **Die Richtung beim Vergleich ist von links nach rechts:** Die erste Seite steht links (`l`), die zweite rechts (`r`) – und schreib in die Beschreibung LEFT/RIGHT in gleicher Reihenfolge, damit das Bild zu den Beschriftungen passt.
6. **Es zahlt nicht doppelt:** `fetch` generiert nur das Fehlende; schlägt eine Anfrage fehl, hält es an und nennt den Grund – wiederhole sie nicht ohne Diagnose.
7. Die aktuellen Modelle: Bild nano banana (fal-ai/nano-banana ≈ 0,04 $) · Clip Wan 2.5 (fal-ai/wan-25-preview 720p ≈ 0,05 $/s, 5 oder 10 Sekunden). Der Clip wird in Frames mit 30/s im Ordner `gen/` verwandelt.

**Der Schlüssel:** `FAL_KEY` in der Umgebung oder in einer `.env`-Datei (Arbeitsordner, Projekt oder Home). Kein Schlüssel? Sag ihm: „Ich brauche einen Schlüssel von fal.ai – du registrierst dich, lädst 5 Dollar auf und gibst mir den Schlüssel.“

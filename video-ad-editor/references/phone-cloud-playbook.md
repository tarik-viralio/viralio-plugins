# 📱 Das Handy-und-Cloud-Buch – erprobte Rezepte, um den Skill in jeder Umgebung zu betreiben

> Ein Betriebshandbuch (keine Änderungsaufgabe). Alles hier wurde **tatsächlich erprobt** in einer echten Sitzung auf dem Handy in der Claude-Cloud
> (Linux, zwei Prozessoren, 7 GB Speicher) und ergab ein vom Eigentümer des Skills abgenommenes Video (6. Oktober 2026). Lies es, wenn du in einer
> anderen Umgebung als einem lokalen Mac arbeitest oder wenn die Freistellung der Person vom Hintergrund nicht sauber war.
> Die Abschnitte: 1 Umgebungsprüfung · 2 Fähigkeitentabelle · 3 Transkription/Pausen/HDR · **4 Freistellung der Person (das Wichtigste)** · **5 Motion-Engine** · 6 Zusammenbau · 7 Qualitätstore · 8 Drehtipps · 9 Fehler, die passiert sind.

---

## 0) Das erste Prinzip: Das Ergebnis ist festgelegt, das Werkzeug wird gewählt

Der Eigentümer des Skills will **dasselbe Ergebnis** auf jedem Gerät. Binde den Skill nicht an ein Werkzeug.

- ⛔ Schreib im Skill oder in den Skripten keine Sätze wie „läuft nur auf dem Mac“, „läuft nicht in der Cloud“ oder „verboten, weil …“.
- ✅ Schreib **das Verlangte** (Person vom Hintergrund freistellen, Sprache hinter dem Kopf, Untertitel nach Wortzeit, Motion …) und dann eine **Liste erprobter Werkzeuge**, und du wählst das passendste für deine Umgebung.
- Die hier genannten Werkzeuge sind **erprobte Beispiele, keine Beschränkungen**. Findest du in deiner Umgebung ein besseres, nutze es und trag es in dieselbe Datei ein.
- Nimm nichts an, **prüfe**. Alles, was du für gesperrt oder fehlend hältst, probierst du mit einem kurzen Befehl, bevor du urteilst.
- Scheitert ein Werkzeug, halte nicht an: probier die Alternative. Das erprobte Prinzip: „Das erste Werkzeug lief nicht → lade ein zweites.“

### Regel für Nachrichten an den Nutzer
- Ein Satz, der sagt, wo die Arbeit steht, ohne schwere Fachbegriffe.
- Sag dem Nutzer nicht „ich kann nicht“, bevor du mindestens zwei Alternativen versucht hast.
- Gib ihm keine Liste mit Befehlen zum Ausführen. Du bereitest vor.

---

## 1) Erster Schritt: Umgebungsprüfung (`probe`)

Füge ein Skript `scripts/30_probe.sh` hinzu, das eine Fähigkeitentabelle ausgibt und nie scheitert:

```bash
echo "os: $(uname -s) cores: $(nproc 2>/dev/null || sysctl -n hw.ncpu) mem: $(free -m 2>/dev/null | awk '/Mem/{print $2"MB"}')"
for c in ffmpeg python3 node chromium google-chrome swiftc; do command -v $c >/dev/null && echo "have: $c" || echo "missing: $c"; done
python3 - <<'E'
import importlib
for m in ["faster_whisper","onnxruntime","cv2","numpy","mediapipe","whisper"]:
    try: importlib.import_module(m); print("py:",m,"ok")
    except Exception as e: print("py:",m,"missing")
E
# Das Netzwerk: probiere die wichtigen Hosts, statt anzunehmen
for u in https://pypi.org https://huggingface.co https://registry.npmjs.org https://github.com; do
  printf "%s -> " $u; curl -s -o /dev/null -m 8 -w "%{http_code}\n" $u
done
```

Das Ergebnis der Prüfung legt den Pfad unten fest (Fähigkeitentabelle). (`00_setup.sh` stoppt in der Cloud jetzt nicht mehr – es warnt und macht weiter.)

### Notizen zum Cloud-Netzwerk (erprobt)
| Der Host | Das Ergebnis in der Cloud |
|---|---|
| PyPI, npm, GitHub, HuggingFace | offen |
| Ubuntu-apt-Mirror | offen |
| `openaipublic.azureedge.net` (das offizielle Whisper-Modell) | gesperrt oder liefert einen Fehler |
| Chromium-Download vom CDN von Playwright | gesperrt |
| Google Cloud Storage (`storage.googleapis.com`) | 403 |

Die Lösung in der Cloud: Modelle von HuggingFace und ein Browser aus einem npm-Paket (Abschnitt 3.3).

---

## 2) Fähigkeitentabelle: Das Verlangte ← die erprobten Werkzeuge

| Das Verlangte | Mac | Cloud / Linux / Windows |
|---|---|---|
| HDR zu SDR | Apple-Konverter (im Skill enthalten) | `ffmpeg` + `zscale` + `tonemap=hable` (Abschnitt 3.1) |
| Transkription mit Wortzeit | das originale `whisper` | `faster-whisper` von HuggingFace (Abschnitt 3.2) |
| Folien und Untertitel zeichnen | Chrome | `@sparticuz/chromium` + `puppeteer-core` (Abschnitt 3.3) |
| Person vom Hintergrund freistellen | Apple Vision | MODNet ONNX + Differenz zu einem Referenzhintergrund (Abschnitt 4) |
| Schnittgrenzen glätten | derselbe Abschnitt 4 gilt für alle | |
| Ebenen zusammenbauen | `ffmpeg` | `ffmpeg` (Abschnitt 6) |
| Lautheit messen | `ffmpeg loudnorm` | dasselbe |

**Das Beste im Ergebnis ist nicht das stärkste Werkzeug:** Die Kombination aus der Personenmaske eines Modells und der Differenz zu einem Referenzhintergrund (bei fester Kamera) ergab das sauberste Ergebnis, ohne irgendein schweres Modell.

---

## 3) Erprobte Rezepte

### 3.1 HDR (iPhone) mit `ffmpeg` zu SDR umwandeln

Ist das Video `color_transfer=arib-std-b67` oder `smpte2084`, nimm:

```bash
VF="fps=30,zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
ffmpeg -ss START -i src.mp4 -frames:v N -vf "$VF" -an -c:v libx264 -crf 12 -preset fast seg.mp4
```

Eine naive Umwandlung macht das Bild flau. Dieser Filter ergab Farben, die dem Original entsprechen.

### ⛔ Die Speicherfalle: Mach kein `trim` für neun Zweige in einem Filter
Ein `filter_complex`-Graph mit 9 `trim` auf einem 4K/1080-Video tötete den Prozess (OOM, SIGKILL). Richtig: **Schneide jeden Abschnitt mit einem eigenen `ffmpeg`-Befehl** (`-ss` vor `-i` und `-frames:v`) und dann den `concat`-Demuxer:

```bash
printf "file 'segs/s%d.mp4'\n" 0 1 2 3 > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy cut.mp4
ffmpeg -i cut.mp4 -q:v 2 vfr/%05d.jpg      # die Frames, auf denen die übrigen Ebenen aufbauen
```

### Pausen schneiden (eine erprobte Regel)
```bash
ffmpeg -i a.wav -af silencedetect=noise=-32dB:d=0.30 -f null - 2>&1 | grep silence_
```
- **Entferne eine Pause nur, wenn sie ≥ 1,2 Sekunden ist.** Kürzere Pausen (0,5 bis 1 Sekunde) lass stehen: Sie geben einen natürlichen Atem.
- Beginn des Abschnitts = Ende der Pause − 0,10. Ende des Abschnitts = Beginn der Pause + Sicherheitsabstand.
- ⛔ **Schneide das Satzende nicht genau am Beginn der Pause.** `silencedetect` meldet die Pause 0,1 bis 0,2 Sekunden, bevor der Atem des Worts endet, und genau das „nahm etwas von seiner Stimme“. Die Regel:
  - **Beim Ton:** Füge nach dem Ende jedes Abschnitts einen Schwanz von 0,13 Sekunden hinzu (er geht über den Übergang und kollidiert nicht mit dem Beginn des nächsten Abschnitts).
  - **Letzter Abschnitt im Video:** Zieh ihn bis zum Ende der Originaldatei ganz aus (es gibt keinen Übergang, der es verdeckt) mit einer Tonausblendung von 150 Millisekunden.
- **Miss nach dem Schnitt erneut:** Analysiere die Tonenergie nach dem Ende jedes Abschnitts (alles über –58 Dezibel bedeutet, dass noch Ton da ist).

### Ton, der dem Schnitt vorausgeht (J-Cut) – verlangt vom Nutzer
Der Ton muss beginnen, bevor der Übergang endet. Baue eine eigene Tonspur (verlass dich nicht auf den Ton des geschnittenen Abschnitts):

- Der Ton jedes Abschnitts beginnt **0,16 Sekunden vor** seinem Schnitt (überlappt mit dem Ende des vorigen).
- Einblendung 35 Millisekunden, Ausblendung 70 Millisekunden (letzter Abschnitt 150).
- Der erprobte Code (numpy, `a48.wav` mit 48 kHz stereo):

```python
LEAD=0.16
for i,c in enumerate(cuts):
    lead = LEAD if i>0 else 0
    tail = 0.13 if i<len(cuts)-1 else 0.0
    s=int((c['src_start']-lead)*sr); e=int((c['src_end']+tail)*sr)
    seg=x[s:e].copy(); fi=int(.035*sr); fo=int((.15 if i==len(cuts)-1 else .07)*sr)
    seg[:fi]*=np.linspace(0,1,fi)[:,None]; seg[-fo:]*=np.linspace(1,0,fo)[:,None]
    o=int((c['out_start']-lead)*sr); out[o:o+len(seg)]+=seg
```

### 3.2 Die Transkription: `faster-whisper`

```bash
pip install --break-system-packages faster-whisper
```
```python
from faster_whisper import WhisperModel
import wave, numpy as np
w=wave.open("a.wav","rb"); audio=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
m=WhisperModel("medium",device="cpu",compute_type="int8",cpu_threads=2)   # wird automatisch von HuggingFace geladen
segs,_=m.transcribe(audio,language="de",word_timestamps=True,vad_filter=True,beam_size=5)
```
- ⛔ **Gib `audio` als `numpy`-Array, nicht als Dateipfad.** Der Dateipfad geht durch PyAV und lieferte in dieser Umgebung den Fehler `av.open(... metadata_errors)`.
- Schreib das Ergebnis im selben Format wie das `whisper`-JSON (`segments[].words[]` mit `word,start,end`), damit die übrigen Skripte laufen.
- ⛔ **Whisper macht Fehler** bei Eigennamen, Fachwörtern, Anglizismen und Dialekt oder Umgangssprache. Korrigiere den Text von Hand aus dem Kontext, aber:
  - **Die Wortzahl in jedem Satz bleibt gleich** (oder streich ein Wort mit einer ausdrücklichen Anweisung, ergänze keins), damit die Zeiten nicht aus dem Takt kommen.
  - ⛔ Erfinde nichts, was der Sprecher nicht gesagt hat. Ein Wort, das du nicht kennst, bleibt wörtlich stehen, und sag dem Nutzer am Ende der Antwort die Liste der unsicheren Wörter.
- **Erkenne Wiederholungen (Retakes):** Der Sprecher wiederholt manchmal einen Satz, weil er sich im ersten verhaspelt hat. Findest du denselben Satz zweimal (z. B. der erste bricht ab), **lösche den ersten unvollständigen**. Wir haben es mit einer zweiten Transkription des Videotons **nach** dem Schnitt mit dem Modell `small` erkannt (eine Minute), und das ist eine Pflichtprüfung:
  - Transkribiere den geschnittenen Ton ein zweites Mal.
  - Vergleiche die Satzanfänge mit der Untertitelzeit (Unterschied unter 0,15 Sekunden).

### 3.3 Der Browser zum Zeichnen in der Cloud

Der Download des Playwright-Browsers ist gesperrt, also nimm das Paket `@sparticuz/chromium` (es trägt die ausführbare Datei in sich):

```bash
npm i puppeteer-core @sparticuz/chromium
node -e "const c=require('@sparticuz/chromium');c.executablePath().then(p=>console.log(p))"   # entpackt und gibt den Pfad aus
```
Dann:
```js
puppeteer.launch({executablePath:CHROME_PATH, headless:'new',
  args:['--no-sandbox','--allow-file-access-from-files','--font-render-hinting=none','--force-color-profile=srgb']})
```
- Die Schriften als lokale `woff2`-Dateien (`@fontsource/inter`) und per `@font-face` + `document.fonts.load` vor dem ersten Zeichnen geladen.
- `page.screenshot`: Die Option `quality` gilt **nur für JPEG** (bei PNG gibt sie einen Fehler).
- Verlass dich nicht auf `pkill -f` in einem Befehl, der denselben Text enthält (er tötet deinen eigenen Befehl).

---

## 4) Die Person vom Hintergrund freistellen (der wichtigste Teil)

Das Ziel: eine feste und ruhige Maske (Alpha) für jeden Frame. Die erfolgreiche Methode sind **drei Ebenen, die sich vereinen**:

### 4.1 Die Modellmaske: MODNet (ONNX, jedes Gerät)
```bash
python3 - <<'E'
# lade modnet.onnx von HuggingFace (irgendein Mirror von MODNet photographic portrait matting)
E
```
```python
sess=ort.InferenceSession('modnet.onnx',so,providers=['CPUExecutionProvider'])
# Referenzgröße 640 in der Breite (ein Vielfaches von 32), Normalisierung (x-0.5)/0.5, RGB
m=cv2.resize(sess.run(None,{name:x})[0][0,0],(w,h),interpolation=cv2.INTER_CUBIC)
```
Geschwindigkeit ≈ 0,8 Sekunden pro Frame auf zwei Prozessoren (1300 Frames ≈ 18 Minuten). Starte es im Hintergrund und arbeite weiter.

**Ausprobiert und verworfen:** `BiRefNet_lite` (224 MB) starb an Speichermangel bei 1024×1024 auf 7 GB, und `RMBG-1.4` ergab keinen Unterschied zu MODNet. Verschwende auf einem kleinen Gerät keine Zeit damit.

### 4.2 ⭐ Differenz zu einem Referenzhintergrund (wenn die Kamera fest und der Hintergrund weich ist)
Das löste das Problem mit dem schwarzen Oberteil, dem Bereich zwischen den Händen und dem unteren Bildrand (das Modell allein verwirrt sich dort):

```python
# 1) sammle die „Vereinigung“ von allem, was das Modell im ganzen Video als Körper sah, und erweitere sie um 61 Pixel
# 2) lege eine glatte Fläche (ein Polynom vom Grad 4 in den Koordinaten x,y) nur auf die gesicherten Hintergrundpixel,
#    für jeden Farbkanal, aus dem Median mehrerer Frames. Das ergibt ein „leeres Hintergrundbild“ auch unter dem Körper
P = polynomial_background(frames, union_mask)         # speichert plate.npy
# 3) für jeden Frame:
d   = sqrt(((frame - P)**2).sum(axis=2))
fgp = clip((d-46)/24, 0, 1); fgp[:int(h*.25)] = 0      # der obere Teil wird vom Modell abgedeckt
fgp = morphologyEx(fgp, MORPH_OPEN, ones((5,5)))       # entfernt Staub
fgp = GaussianBlur(fgp, (0,0), 1.2)
mask = maximum(mask_from_model, fgp)                    # die Vereinigung
```
- Die Haut liegt nahe an der Hintergrundfarbe, also fängt die Differenz sie nicht – deshalb **deckt das Modell Gesicht und Hände ab, und die Differenz den dunklen Stoff und die Arme**.
- Reste von Flaum in den unteren Ecken vom Rand des Polynoms: Die Schwelle 46 schaltet sie aus.
- ⛔ Schreib keine Regel „zieh den Körper senkrecht bis zum unteren Bildrand“ und keine „füll die Löcher“: Die erste erzeugte weiße Säulen in den Ecken, die zweite füllt die echte Lücke zwischen Arm und Körper. Die Differenz zum Hintergrund liefert die Wahrheit ohne beide.
- Bewegt sich die Kamera oder ist der Hintergrund nicht weich: nimm nur das Modell + die Glättung (4.3) und sag dem Nutzer offen, dass die Qualität geringer ist. (Die erste Einstellung im Auto war schwierig wegen eines weißen Hemds und eines hellen Autohintergrunds.)

### 4.3 Die Maske zeitlich glätten (verhindert das Zittern)
Der Nutzer verlangte: **„Das Wichtigste: Dass die Auswahl nicht zittert und ruhig ist.“** Das Maß: die mittlere Änderung der Kante zwischen zwei Frames (nach der Glättung ≈ 0,002, davor 0,006).

```python
# ein zentrales Fenster ±2 Frames mit Gewichten [1,2,3,2,1]/9 auf der Rohmaske
A = sum(raw(i+k)*w for k,w in {-2:1,-1:2,0:3,1:2,2:1}.items())/9
M = raw(i)
f = clip((abs(M-A)-.18)/.30, 0, 1)      # schnelle Bewegung (Hände) = weniger Glättung, damit sie nicht nachhängt
m = A + (M-A)*f
# ein geführter Filter (guided filter) mit dem Graubild des Frames, halbe Auflösung, r=6, eps=2e-3
# dann die Kanten härten: m = clip((m-.30)/.45, 0, 1)
```
- ⛔ `cv2.ximgproc.guidedFilter` fehlt in den normalen `opencv-python`-Paketen oder kollidiert mit anderen Versionen. Schreib den Filter selbst mit `cv2.boxFilter` (liegt fertig im Repository unter `refine.py`).
- **Der weiße Rand (der Sticker) und der Schatten werden aus der geglätteten Maske abgeleitet:** ein elliptischer Dilatationsfilter 23×23, Weichzeichner 2,2, **dann ein zeitliches Mittel ±2** und eine weiche Schwelle `clip((D-.40)/.20,0,1)`. Der Schatten: Weichzeichner 14 mit Versatz (12,18).

### 4.4 Frame-Nummerierung nach dem Löschen eines Abschnitts
Löschst du einen Abschnitt (eine Wiederholung), nachdem der Schnitt begonnen hat, **berechne die Masken nicht neu**: Lege ein Verzeichnis `vfrN/` und `raw2/` mit symbolischen Links in der neuen Nummerierung an (`new j -> old j+74` nach dem Löschpunkt) und ergänze eine Funktion `OLD(i)`.

---

## 5) Die Motion-Engine: erprobte Entscheidungen

### 5.1 Papier-Cutout in Ebenen (der Stil, der abgenommen wurde)
- Ein Hintergrund in einer anderen Farbe für jeden Abschnitt (9 Farbpaletten, die sich wiederholen `PAL[k % PAL.length]`), gewellte Papierbündel, überlappende Scheiben, Papierkörnung (`NOISE` transparent).
- Alles mit weichem Schatten (`shadowBlur`), damit das Papier sichtbar wird.
- Die Person mit cremefarbenem Rand (#FFF6E3) und Schatten.

### 5.2 ⭐ Sprache hinter dem Kopf + Dehnstrich (ohne Gerätekenntnis)
> ⚠️ **Nur für arabische Schrift.** Das Rezept dehnt ein Wort mit einem Kashida-Strich. Für deutschen Text gibt es das nicht (siehe Hinweis in `references/cut-styles.md`); ein deutsches Wort fällt als Brustkarte nach vorn (5.3).

Die Regel des Skills: Die Buchstaben stehen immer **außerhalb des Kopfes**, und der Dehnstrich **allein** verläuft hinter dem Kopf. Umsetzung mit dem `canvas` ohne Vision:

1. Wähle einen **Verbindungspunkt** im Wort: ein Buchstabe, der sich mit dem folgenden verbindet (nicht aus `ا أ إ آ د ذ ر ز و ؤ ة ء ى`, und nicht `ل` vor `ا`). Wähle den Punkt, der den rechten und linken Teil in der Breite nahe beieinander hält.
2. Zeichne das Wort **einmal** mit einem Dehnstrich (`ـ`) auf ein eigenes `canvas` (Rand + Füllung) und miss die Stelle des Dehnstrichs mit `measureText`:
   ```js
   const Pw = m.measureText(prefix + 'ـ').width;      // die Breite vor der Verbindung einschließlich des Dehnstrichs
   const tw = m.measureText('ـ').width, Wt = m.measureText(withK).width;
   const xs = cw/2 + Wt/2 - Pw + tw/2;                 // die Mitte des Dehnstrichs (RTL: der Beginn ist rechts)
   ```
3. **Ziehe einen Streifen aus der Mitte des Dehnstrichs in Pixeln** (nicht durch Wiederholen von Buchstaben, denn das ergibt „Lücken“):
   ```js
   // Der Streifen: seine Breite 0,36*tw aus der Mitte des Dehnstrichs. Der rechte und linke Teil werden unverändert gezeichnet
   X.drawImage(sp,xs-sw,0,2*sw,ch, -midW/2,-ch/2, midW,ch);            // der gedehnte Streifen
   X.drawImage(sp,xs+sw,0,rightW,ch, -midW/2+midW-.5,-ch/2, rightW,ch);  // rechts
   X.drawImage(sp,0,0,leftW,ch,       -midW/2-leftW+.5,-ch/2, leftW,ch);  // links
   // midW = S - (tw - 2*sw)  wobei S = 372 (etwas breiter als der Kopf)
   ```
4. **Der gedehnte Bereich hat seine Mitte in der Bildmitte (x=540) und eine Breite von 372 Pixeln**, deckt also den Kopf vollständig ab (der Kopf ≈ 300 Pixel breit), und alle Buchstaben liegen außerhalb. Sind die übrigen Buchstaben breiter als der verfügbare Platz (`336 - pad`), verkleinere die Schrift automatisch.
5. Ein Wort ohne gültigen Verbindungspunkt: Dehne es nicht, mach daraus ein Brustwort (5.3).
6. Höchstens drei Wörter hinter dem Kopf in einer Szene (Regel des Skills).

### 5.3 Das letzte Wort fällt auf die Brust (Wunsch des Nutzers)
Ist der Satz lang: ein Wort hinter dem Kopf (gedehnt), **und das letzte Wort auf der Brust vor ihm** (eine vordere Ebene über der Person):
- ein dicker cremefarbener Rand (`lineWidth = size*.12`) und Schatten, Größe ≈ 210, senkrechte Position ≈ 1160 (zwischen Kinn und Untertitel).
- Es kommt 0,16 Sekunden nach dem hinteren Wort mit einer federnden Vergrößerung (`eob`).

### 5.4 Der Eintritt des Hintergrunds mit Bewegung (Wunsch des Nutzers)
**Der Hintergrund erscheint nicht vom ersten Frame an.** Das Video beginnt mit dem Originalhintergrund des Nutzers, dann öffnet sich ein **Papierkreis**:
- 0,18 Sekunden Beginn, 0,8 Sekunden Dauer, der Radius wächst bis 1800 mit Verlangsamung `easeInOut`.
- Drei Ringe: dunkel (`INK`), die Akzentfarbe (`acc`) bei 0,93 des Radius, dann die Wand und die Scheiben bei 0,84.
- Eine **Enthüllungsmaske (`rev`)**, die die Engine als dritte Ebene zeichnet (ein weißer Kreis auf Schwarz). Schatten und weißer Rand werden damit multipliziert, damit sie nicht vor dem Kreis erscheinen. Nach anderthalb Sekunden wird sie ganz weiß.

### 5.5 Ein schneller Übergang (Wunsch des Nutzers)
- Vier Papierstreifen mit 0,03 Sekunden Verzögerung, jeder Streifen dauert 0,28 Sekunden, beginnt 0,13 Sekunden vor dem Abschnitt und endet 0,24 danach (gesamt ≈ 0,4 Sekunden, vorher 0,88).
- Der Ton beginnt vor ihrem Ende (Abschnitt 3).

### 5.6 Formate und sichere Zonen
- 1080×1920, 30 Bilder/Sekunde. Sichere Zone von Instagram: oben 0–150, unten 1620–1920, rechts x950–1080 bei y1100–1750.
- Die Untertitel der Rede: eine cremefarbene Karte mit einem in der Akzentfarbe hervorgehobenen Wort im Moment seiner Aussprache, unter der Brust (y≈1385), und der Fortschrittsbalken bei y=1494.
- Bestimme die Kopfposition aus dem Video selbst (x 390 bis 690, Kopfspitze ≈ 515, Kinn ≈ 1000 im Video des Eigentümers) und passe die Zahlen in der Engine an den Rahmen jedes Videos an.

---

## 6) Der Zusammenbau der Ebenen mit `ffmpeg` (ein Befehl, erprobt)

Die Ebenen (alle mit der Nummerierung `%05d`): `vfrN` (der Originalframe JPEG), `back` (JPEG aus dem Browser), `revF` (Enthüllungsmaske PNG), `shadR`, `outlR`, `maskR` (graues PNG), `front` (transparentes PNG).

```bash
ffmpeg -y -framerate 30 -i vfrN/%05d.jpg -framerate 30 -i back/%05d.jpg -framerate 30 -i revF/%05d.png \
 -framerate 30 -i shadR/%05d.png -framerate 30 -i outlR/%05d.png -framerate 30 -i maskR/%05d.png \
 -framerate 30 -i front/%05d.png -i cut_audio.wav -filter_complex "
[0:v]scale=in_range=pc:in_color_matrix=bt709,format=rgba,split=2[b1][b2];
[1:v]scale=in_range=pc:in_color_matrix=bt601,format=gbrp,format=rgba[bk];
[2:v]format=gray,split=3[r1][r2][r3];
[bk][r1]alphamerge[bka];[b1][bka]overlay=format=auto[l0];
[3:v]format=gray[sh0];[sh0][r2]blend=all_mode=multiply[sh1];[sh1]lutyuv=y=val*0.38[sh];
color=c=black:s=1080x1920:r=30,format=rgba[blk];[blk][sh]alphamerge[shd];[l0][shd]overlay=format=auto[l1];
[4:v]format=gray[ol0];[ol0][r3]blend=all_mode=multiply[ol];
color=c=0xFFF6E3:s=1080x1920:r=30,format=rgba[cr];[cr][ol]alphamerge[out];[l1][out]overlay=format=auto[l2];
[5:v]format=gray[mk];[b2][mk]alphamerge[per];[l2][per]overlay=format=auto[l3];
[6:v]format=rgba[fr];[l3][fr]overlay=format=auto,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]" \
 -map "[v]" -map 7:a -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:v libx264 -preset medium -crf 23 -maxrate 6M -bufsize 12M \
 -r 30 -c:a aac -b:a 160k -shortest -movflags +faststart out.mp4
```

Wichtige Zahlen:
- ⛔ **Farbmatrizen:** Das JPEG aus dem Browser = `bt601 pc`, und die extrahierten Videoframes (aus ffmpeg) = `bt709 pc`. Verwechselst du sie, wird die Haut gelblich oder grün.
- Maske, Rand und Schatten werden mit `blend multiply` mit der Enthüllungsmaske vereint.
- Die Zusammenbaudauer für 1300 Frames ≈ 3 Minuten auf zwei Prozessoren. Die Endgröße ≈ 24 MB (unter der Grenze von 30 MB).
- `loudnorm` ergibt ≈ –15 LUFS (akzeptabel; das Ziel ist –14).

---

## 7) Qualitätstore vor der Lieferung (Pflicht, der Reihe nach)

1. **Ein Kontaktblatt:** 8 bis 12 Frames, über das Video verteilt, auf einem Blatt, und lies es selbst. Such nach:
   - Löchern oder weißen Säulen am unteren Bildrand und zwischen den Händen.
   - Buchstaben, die hinter dem Kopf versteckt sind (die Dehnung wurde also nicht richtig verteilt).
   - Wörtern, die an den Rändern abgeschnitten sind, oder Text in der sicheren Zone der Buttons.
2. **Das Zittermaß:** die mittlere Differenz der Randmaske zwischen zwei aufeinanderfolgenden Frames in einer ruhigen Einstellung (< 0,003).
3. **Synchronität:** Transkribiere den fertigen Ton und vergleiche die Satzanfänge (Abschnitt 3.2).
4. **Ton:** Spitze unter –1,5 dBTP und Lautheit ≈ –14/–15 LUFS. Und prüf, dass das letzte Wort im Video vollständig ist (der Schwanz).
5. **Größe:** unter 30 MB.
6. **Nicht veröffentlichen.** Geliefert wird nur eine Datei.
7. **Sag dem Nutzer offen** am Ende der Antwort: welche Wörter du aus der Transkription korrigiert hast und bei welchen du unsicher bist, welchen Abschnitt du gelöscht hast (eine Wiederholung) und welches Ersatzwerkzeug du benutzt hast (z. B. Chrome + ffmpeg statt des Schnitttools).

---

## 8) Drehtipps für den Nutzer (aus dem tatsächlichen Test)

- Der Unterschied zwischen dem Dreh im Auto (weißes Hemd, heller Hintergrund, wechselndes Licht) und dem Studio (schwarzes Oberteil, ein weicher pfirsichfarbener Hintergrund, festes Licht) war **sehr groß**. Die erste Einstellung brauchte Mühe, die zweite kam fast ohne Eingriff sauber heraus.
- Die Regel: **dunkle Kleidung vor weichem hellem Hintergrund (oder umgekehrt) + feste Kamera (Stativ) + festes Licht**.
- Muss im Auto gedreht werden: Die Kamera aufs Stativ, und vermeide Kleidung in der Farbe des Hintergrunds.
- Sagt der Nutzer einen Satz und verhaspelt sich, soll er ihn direkt nach dem Fehler wiederholen (der Skill entfernt den ersten).

---

## 9) Fehler, die wirklich passiert sind (nicht wiederholen)

| Der Fehler | Die Lösung |
|---|---|
| `ffmpeg` OOM mit `trim` ×9 | schneide jeden Abschnitt mit einem eigenen Befehl + `concat` (Abschnitt 3.1) |
| `PTS-STARTPS` (ein Buchstabe fehlt) | `PTS-STARTPTS` |
| `faster-whisper` + Dateipfad | gib `numpy` mit |
| `screenshot` PNG mit `quality` | `quality` nur für JPEG |
| `cv2.ximgproc.guidedFilter` fehlt | schreib `guidedFilter` mit `boxFilter` |
| `pkill -f matte` tötete den Befehl selbst | nimm `pgrep` mit einem Muster, das nicht auf die Befehlszeile passt, oder stoppe mit einem eigenen Befehl |
| BiRefNet 1024 OOM | MODNet 640 + Differenz zum Hintergrund |
| weiße Säulen am unteren Bildrand | lösche die Regel „nach unten ziehen“ |
| Der Dehnstrich aus wiederholten `ـ`-Zeichen ergibt Lücken | ein Streifen aus der Mitte des Dehnstrichs in Pixeln |
| der Ton am Satzende bricht ab | ein Schwanz von 0,13 Sekunden und den letzten Abschnitt bis zum Ende der Datei ziehen |
| gelbliche Farben | Farbmatrizen (Abschnitt 6) |
| ein gelöschter Abschnitt nach dem Schnitt zerstört die Nummerierung | `OLD(i)` (Abschnitt 4.4) |
| 9 Farbpaletten und 10 Abschnitte | `PAL[k % PAL.length]` |

---

*Die Quelle dieser Datei: eine tatsächliche Testsitzung vom 2026-10-06, ein Video von 70 Sekunden → 43,4 Sekunden, Ausgabe 1080×1920 mit einer Größe von ≈ 23 MB.*

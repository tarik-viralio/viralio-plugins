<!-- Gemeinsame Referenz für alle Modi des Skills – wird zu Beginn jedes Auftrags gelesen -->

# Start – Tools, Geschmack und Identität vorbereiten

Gleicher Start für alle Modi: Sprechvideo-Reel, Podcast, Montage und Motion.
Alle Pfade beziehen sich auf den Hauptordner des Skills (`video-ad-editor`).

---

## Vor allem anderen – Modell- und Aufwandstipp (einmal pro Sitzung)
Sag dem Nutzer in der ersten Nachricht der Sitzung in zwei Zeilen (und wiederhole es nicht):
> „Für das stärkste Ergebnis: **Opus 5.5** mit Aufwand **max**. Das verbraucht mehr von deinem Kontingent, aber der Schnitt wird deutlich besser.“
- **Im Chat (claude.ai / App):** Modellmenü neben dem Senden-Button → Opus 5.5 → Effort → Max.
- **Claude Code (Terminal, Desktop, Code-Tab am Handy):** `/model opus`, dann `/effort max`.
- Ist er schon auf Opus 5.5 (du kennst dein Modell), nenn nur den Aufwand. Empfiehl für den Schnitt kein „ultracode“: Es teilt die Arbeit auf Agenten auf, jeder gestaltet nach eigenem Geschmack, und der Verbrauch vervielfacht sich – ein Agent mit Aufwand max ist für ein Video besser.
- Nenne keine Verbrauchs- oder Minutenzahlen – sie wurden nicht gemessen.

## Schritt 0 – Still vorbereiten

```bash
bash scripts/00_setup.sh
```

- Meldet „alles bereit“ → das Thema nicht erwähnen.
- Meldet „🆕 neuere Version verfügbar“ → frag: „Es gibt ein Update für den Skill – soll ich es jetzt einspielen?“
  - Zustimmung → führe die Zeile aus, die das Skript selbst ausgibt (sie unterscheidet sich zwischen Skill und Plugin).
- Fehlt etwas → sag in einem Satz, was du herunterlädst, hol die Zustimmung ein, dann:

```bash
bash scripts/00_setup.sh --install
```

- Etwas fehlgeschlagen → nenn die Lösung in einem menschlichen Satz, ohne den Fehler einzufügen.
- In der Zeile „Zusätze“ steht „—“? Die sind optional (smarte Tonreinigung, Suche nach Bedeutung).
  - Biete sie **einmal** an, wenn du sie brauchst: „Soll ich dir das smarte Tonreinigungs-Tool installieren? Zwei Minuten.“
  - Zustimmung → `bash scripts/00_setup.sh --extras`
  - Jeder Zusatz fällt auf den alten Weg zurück, wenn er fehlt.

Lege einen Arbeitsordner an und kopiere `scripts/compose.REFERENCE.html` als `compose.html` hinein.

### 💡 Tipps aus einem Reel mit vielen iPhone-Clips (6.0)
- **Viele iPhone-Clips (HLG/HDR) zu einem Video zusammenfügen? Erst jeden Clip nach SDR wandeln, dann zusammenfügen.**
  `03_cut_zoom.py` erkennt HDR nur bei einer einzelnen Datei – fügst du vorher mit ffmpeg zusammen, geht das HLG-Tag verloren, und die Farben wirken flau oder orange, ohne dass es auffällt.
  ```bash
  swiftc -O -o scripts/hdr2sdr scripts/hdr2sdr.swift          # einmalig (Mac + Xcode-Tools)
  mkdir -p sdr; for f in IMG_*.MOV; do scripts/hdr2sdr "$f" "sdr/${f%.*}.mov"; done   # jeden Clip einzeln
  ```
  So erkennst du HDR: `ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 IMG_1.MOV` → `arib-std-b67` (HLG) oder `smpte2084`.
- **Tonreinigung in Claude Code = DeepFilterNet auf dem Gerät** (`bash scripts/00_setup.sh --extras`, dann `02b_enhance_audio.sh <work> --local`).
  Das Adobe-Tool `media_enhance_speech` startet die Arbeit, aber in Claude Code gibt es kein Folge-Tool, das die saubere Datei holt – verlass dich hier nicht darauf.

---

## Schritt 0.5 – Kennenlern-Seite (nur beim ersten Mal)

```bash
python3 scripts/00_onboard.py show
```

Ergebnis `{}` = keine gespeicherten Auswahlen.

**1. Gibt Auswahlen aus** → nichts öffnen:

```bash
python3 scripts/00_onboard.py theme <work>
```

Und sag in einer Zeile: „Ich arbeite mit deinen Einstellungen: Farben so und so, Untertitel so.“
(Code 4 = es gibt schon eine `theme.json` – lass sie.)

**2. Gibt `{}` aus, aber er hat eine Identitätsdatei** (`.auto-memory/creator-profile.md`) → nicht öffnen, weiter mit Schritt 1.

**3. Gibt `{}` aus und keine Datei vorhanden** → starte die Seite im Hintergrund:

```bash
python3 scripts/00_onboard.py --work <work>
```

- Sag ihm: „Ich habe dir eine kleine Seite geöffnet, auf der du deinen Geschmack wählst – oder schreib, was du willst, und überspring sie. Ich warte.“
- Beendet mit Code 0 → `python3 scripts/00_onboard.py theme <work>`
- Enthält `skip:true` → arbeite nach `note`.

**Weitere Fälle:**
- Sagt „ändere meine Einstellungen“ → öffne die Seite (sie öffnet sich ausgefüllt), danach `theme <work> --force` mit seiner Zustimmung.
- Sitzung ohne Browser → nicht öffnen, weiter mit Schritt 1.
- Wohin jedes Feld geht, Identität aus einem Link, generierte Stimme → `references/onboarding.md`.
- ⛔ Generierte Stimme ohne Standard: Er wählt (Sprache und Stimme, männlich oder weiblich).

---

## Schritt 1 – Seine visuelle Identität (es gibt keine Standardfarbe)

⛔ **Nimm nicht Creme und Lehm an** – das ist das Claude-Theme, nicht seins.
⛔ **Ändere kein früheres Theme.** Hat er von einem früheren Video eine `theme.json`? Nutze sie unverändert.
Eine Grundfarbe ändern nur auf seinen ausdrücklichen Wunsch.

**0.** Wurde `theme.json` in Schritt 0.5 geschrieben? Dann überspring diesen Schritt.

**1.** Suche `.auto-memory/creator-profile.md`.
Gefunden? Nimm Farben, Schrift und Account und sag: „Ich arbeite mit deinen Farben: so und so – passt das?“

**2.** Nicht vorhanden? **Eine Frage:**
„Welche Farben hat dein Account? Gib mir Hintergrundfarbe, Akzentfarbe und dein Logo.
Oder den Link zu deinem Account oder ein paar Bilder, deren Stil dir gefällt – daraus erstelle ich das Theme.“

**Hat er Referenzbilder geschickt?** (auch wenn er „Referenz“ nicht sagt – Stilbilder + „so will ich es“):

```bash
python3 scripts/00_theme_refs.py <work> bild1 bild2 …
```

- Liefert Farben mit lesbarem Kontrast und schreibt `theme.json` und `refs_palette.jpg`.
- **Sieh dir das Blatt selbst an.** Danach ist der Geschmack deine Entscheidung nach der Anmutung der Bilder:
  - Schrift: `font`
  - Untertitel: weich → `shadow` oder `underline` · kräftig → `card` oder `big`
  - Rhythmus: ruhige Bilder → `"pace":"calm"`
- Sag ihm in einer Zeile: „Aus deinen Bildern habe ich genommen: Hintergrund so, Akzent so, Untertitel so – passt das?“
- Haben die Bilder Schatten oder Gelbstich? `--light` oder `--dark` legt die Richtung fest.

**3.** Schreibe `<work>/theme.json` und kopiere sein Logo `logo.png` hinein:

```json
{ "bg":"#101828", "ink":"#F5F7FA", "acc":"#F2B33D", "clay":"#C98B18", "mut":"#98A2B3",
  "font":"Inter", "handle":"@sein_handle", "logo":"logo.png", "grade": false,
  "faceAnchor": 0.30, "badgeUntil": 0, "capStyle": "card" }
```

- Alle Grafik leitet ihre Farben aus diesen Werten ab. Dunkel oder hell – beides funktioniert.
- Farben von Hand geschrieben? Führ das hier aus, damit keine weiße Schrift auf hellem Akzent entsteht:

```bash
python3 scripts/00_onboard.py onacc <work>
```

### Weitere Schlüssel im Theme

| Schlüssel | Was er tut |
|---|---|
| `badgeUntil` | Account-Badge. Aus (0) – der Name steht auf der Plattform und auf der Schlusskarte. `3` = die ersten 3 Sekunden, wenn gewünscht |
| `grade` | immer aus – siehe Regel „keine Farbbearbeitung“ |
| `capStyle` | Untertitelstil → `references/word-fx.md` |
| `capStill` | `true` = Untertitel ohne Bewegung: Die Karte blendet nur über Transparenz ein und aus, das Wort springt und pulsiert nicht. Einfärben des gesprochenen Worts und die Kapsel bleiben. Standard ist mit Bewegung → `references/word-fx.md` |
| `bar` | `false` = ohne Fortschrittsbalken. Standard sichtbar. (Nicht `capStyle: "bar"` – das ist ein Untertitelstil) |
| `pace` | `"calm"` ruhiger Rhythmus → `references/explainer-and-pace.md` |
| `hookZoom` | sanfter Zoom auf sein Gesicht zu Beginn des Hooks (Sekunden = Ende des Hooks). Standardmäßig aus |
| `outro` | Schlusskarte `{l1,l2,chips,cta,word,sub}` |
| `hook` | geschriebener Hook für Podcast-Reels – wird von `22_hook.py apply` geschrieben, nicht von Hand |

**Ruhige Premium-Anzeige:** `"capStill": true` + `"bar": false`, und jedes `FX.doorway`, das sich auf sein Gesicht öffnet, bekommt `zoomB: false` (kein Zoom aufs Gesicht).

**`hookZoom` im Detail:**
- Starte nach Schritt 6 `python3 scripts/22b_hook_center.py <work>` – es schreibt `hookCenter` auf sein Gesicht.
- Ohne das nimmt es das Gesicht aus `behind.json`.
- Dazu ein sehr leichtes Whoosh in `sfx.json`:

```json
"soft": [[0, 0.035], [Ende_des_Hooks - 0.22, 0.06]]
```

**⚠️ `outro`:** Der Standard ist die Anzeige des Skills selbst („Kommentiere mit dem Wort Video“).
Jedes Video, das keine Werbung für den Skill ist (z. B. ein Podcast-Reel), muss ihn ändern.

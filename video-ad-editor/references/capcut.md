# 🎞️ Schnitt in CapCut – ein Projekt, das er selbst bearbeitet, statt MP4

**Wann:** Er sagt „mach es in CapCut“, „ich will selbst in CapCut nachbearbeiten“, „gib mir ein CapCut-Projekt“, und er hat CapCut Desktop (Mac oder Windows).

**Was herauskommt:** ein CapCut-Projekt, in dem jedes Element unabhängig ist und er es bewegen oder löschen kann:

| Die Spur | Der Inhalt |
|---|---|
| Einstellungen | seine Clips und B-Roll, jede mit Keyframe-Zoom (hinein/heraus) |
| Motion | die Motion-Karten in seinen Farben – ProRes 4444 transparent über den Einstellungen |
| Titel + Untertitel | echte CapCut-Texte (er ändert Wort, Farbe und Schrift in CapCut) |
| Die Stimme | seine gereinigte Stimme, ein Clip pro Satz |
| Effekte 1..n | jeder Effekt ein eigener Clip – er senkt oder entfernt ihn |
| Hintergrund-Audio | die Hintergrund-Audiodatei mit Ein- und Ausblendung, wiederholt sich, wenn sie kürzer ist |

Alles mit einem Skript: `scripts/40_capcut.py` (Vorlage, Motion und Renderer sind darin eingebaut).

---

## ⛔ Bevor du beginnst

1. **Ein leeres Projekt mit Namen.** Sag ihm: „Öffne CapCut, lege ein neues leeres Projekt mit dem Namen `<Name>` an und beende CapCut komplett (Cmd+Q).“
   Prüf, dass es existiert: `python3 scripts/40_capcut.py projects`
2. **CapCut muss beim Schreiben geschlossen sein.** Das Skript verweigert, wenn es läuft – umgehe das nicht, CapCut überschreibt die Datei, und die Arbeit geht verloren.
3. **Die Tools:** dieselben wie beim Skill (ffmpeg, Chrome, puppeteer-core) + ein ffmpeg mit `prores_ks` (das aus brew hat es).
4. **Mac:** CapCut ist in einer Sandbox – es liest nur `~/Movies`. Das Skript legt alles in `~/Movies/capcut-<name>/` und kopiert jede Datei von außerhalb automatisch dorthin. Ändere diesen Pfad nicht.

## Die Schritte

**1. Derselbe Start wie beim Skill:** das Theme (`references/start.md`), der Schnittplan `01_cut_plan.py`, die Transkription (`a.json`), die Korrektur und 5.5 (zeig den Text und entferne, was er nicht will). Tonverbesserung `02b` ist optional.

**2. Ein erster Plan aus dem Sprechvideo:**

```bash
python3 scripts/40_capcut.py skeleton <work> <work>/capcut.plan.json
```

Ein Sprechabschnitt pro Stück aus `cut.json` mit seinen Wörtern von Whisper und eine synchrone Videoeinstellung für jeden Abschnitt.

**3. Arbeite am Plan** (das Format steht unten): Korrigiere die Wörter (`text`), die betonten Wörter (`emph`), den Hook-Titel, die B-Roll zwischen seinen Einstellungen, das Motion aus dem Sinn des Satzes, die Effekte und das Hintergrund-Audio.

**4. Prüfen und zeigen:**

```bash
python3 scripts/40_capcut.py check  <plan>      # Tabelle der Einstellungen und Zeiten
python3 scripts/40_capcut.py stills <plan>      # zwei PNG-Frames pro Motion in ~/Movies/capcut-<name>/stills
```

⛔ **Zeig ihm die Frames und warte auf seine Zustimmung vor dem Gesamtrender.**

**5. Bauen und schreiben** (CapCut geschlossen):

```bash
python3 scripts/40_capcut.py all <plan>         # Effekte + Motion rendern + das Projekt schreiben
```

Sag ihm: „Öffne CapCut → das Projekt `<Name>` – alles darin kannst du ändern.“
Etwa eine Minute pro 50 Sekunden (das Rendern ist das Schwerste). Ein einzelnes Motion geändert? `render <plan> <Name>`, dann `write <plan>`.

**Zurück:** Vor jedem Schreiben wird das Original in `~/Movies/capcut-<name>/backup/<Zeit>/` gesichert – kopiere es über den Projektordner, während CapCut geschlossen ist.

---

## Das Planformat

```json
{
 "name": "weihnachts-ad",          "capcut": "weihnachts-ad",
 "theme": "<work>/theme.json",     "gap": 0.22,
 "emph": ["Weihnachten", "25%"],
 "speech": [
  {"key": "S1", "file": "<work>/voice48k.wav", "a": 2.35, "b": 8.05, "words": [["drei", 2.30, 2.84], ["Ideen", 2.84, 3.14]],
   "text": "drei Ideen", "gap": 0},
  {"key": "REVEAL", "pause": 1.35},
  {"key": "S2", "file": "...", "a": 15.8, "b": 23.1, "words": [...], "groups": [2, 3, 2]}
 ],
 "visuals": [
  {"file": "<work>/src.mov", "sync": true, "to": "S1>", "zoom": "in"},
  {"file": "broll.mp4", "src": 4.0, "speed": 1.5, "to": "S2:und-0.05", "zoom": "out", "fit": "fill"},
  {"file": "rec.mov", "src": 63, "span": 16, "to": "REVEAL"},
  {"file": "photo.heic", "dur": 0.45},
  {"file": "<work>/src.mov", "sync": true}
 ],
 "titles":   [{"text": "3 Ideen\nfür Weihnachtsfotos", "emph": ["3 Ideen"], "to": "S2", "y": 0.6, "size": 17}],
 "overlays": [
  {"type": "badge",   "at": "S2", "dur": 2.2, "n": "1", "label": "Die Idee", "title": "Natürliches Licht"},
  {"type": "roll",    "at": "S3:und-0.1", "to": "S4-0.05", "label": "Dasselbe Foto … jedes Jahr", "items": ["2025","2026","2027"],
   "marks": {"items": ["S3:dasselbe", "S3:jedes"]}},
  {"type": "card",    "at": "S5", "to": "S6", "big": "25%", "line": "Rabatt auf den Druck", "chips": ["Album","Einzelfotos"], "foot": "example.com",
   "marks": {"in": "S5:Album-0.25", "big": "S5:Rabatt", "big_end": "S5:25%+0.35", "line": "S5:Druck", "chips": ["S5:Album","S5:Einzelfotos"], "foot": "S5:einfach"}},
  {"type": "endcard", "at": "S6", "to": "end", "text": "Folge mir @handle"},
  {"name": "mine", "html": "<work>/my_scene.html", "at": "S4", "dur": 3}
 ],
 "sfx": [{"s": "shutter", "at": "REVEAL+0.45", "vol": 0.9}, {"s": "sub", "at": "S5:25%", "vol": 0.7}],
 "auto_sfx": true,
 "bg": {"file": "bg.wav", "vol": 0.13}
}
```

**Zeiten über Verweise, nicht über Zahlen** – wird ein Satz gelöscht, zieht alles mit:

| Der Verweis | Bedeutung |
|---|---|
| `"S2"` / `"S2>"` | Beginn / Ende des Sprechabschnitts S2 (oder der Pause) |
| `"S2:Wort"` · `"S2:Wort>"` · `"S2:Wort#2"` | Beginn des Worts · sein Ende · beim zweiten Mal, wenn es gesagt wird |
| `"+0.2"` / `"-0.05"` am Ende | Versatz in Sekunden |
| `"end"` · eine Zahl | Ende des Videos · eine absolute Sekunde |

**Die Rede:** `a`/`b` sind die Satzgrenzen in der Datei (in Whisper-Zeit), `off`, wenn die Datei später beginnt als Whisper.
- Das Skript passt die Wortzeiten an den ersten und letzten tatsächlichen Ton an (Whisper verschiebt nach vorn und hinten). Du hast die Grenzen? `on`/`end`. Du willst es nicht? `"tighten": false`.
- `text` = Korrektur der Wörter mit derselben Anzahl.
- `groups` = wie viele Wörter pro Untertitel (die Summe = Zahl der Wörter). Ohne: 3 Wörter oder 18 Zeichen, und es teilt sich an jedem Atemzug.
- `{"pause": s}` = ein Moment ohne Rede (Bildenthüllung, Ergebnis).

**Die Einstellungen** nacheinander: jede bis `to` oder `dur`, die letzte bis zum Ende.
- `sync: true` = das Sprechvideo selbst, die Quelle läuft mit dem Ton.
- `span` = wie viele Sekunden der Quelle auf die Dauer zusammengedrückt werden (berechnet die Geschwindigkeit).
- `fit`: `fill` füllt 9:16 (Standard) · `contain` · oder eine Zahl.
- `zoom`: `in` / `out` / `null`.
- Bilder (heic/jpg/png) werden als Standbild gesetzt.

**Das Motion:** vier fertige Karten in den Farben, der Schrift und dem Logo seines Themes (`badge` · `roll` · `card` · `endcard`). Die große Karte zählt die Zahl bis zu ihrem Wert (`25%` zählt ab 0).
- ⛔ **Das sind Grundlagen, keine Vorlage** – die Szenen entstehen aus dem Sinn des Satzes.
- Eine neue Szene: eine HTML-Seite mit transparentem Hintergrund 1080×1920 mit `window.setup(o)` und `window.render(t)` (t in Sekunden ab Szenenbeginn, `o.marks` relative Zeiten) → `"html": "<Pfad>"`.

**Die Effekte:** `auto_sfx` setzt Whoosh + Pop zum Titel und zu jeder Karte. Den Rest setzt du im Moment selbst (nicht streuen):
`whoosh_up whoosh_down pop thud tap click shimmer sub riser glitch shutter counter`

---

## Bekannte Grenzen

- Die Vorlage stammt aus einem CapCut-Projekt der Version `183.0.0` (CapCut 9.x). Eine andere Version? Das Skript warnt und schreibt trotzdem. Öffnet es sich nicht, spiel die Sicherung zurück und sag es ihm.
- Die Untertitel sind CapCut-Text mit dunklem Rand und Akzentfarbe aus seinem Theme – ohne die Wortbewegungen des Skills (hinter dem Rücken). Will er sie? Das ist der MP4-Modus.
- CapCut speichert das Projekt neu, sobald es es öffnet, und rastet die Zeiten auf den Frame ein – das ist normal.
- Windows: Der Projektordner ist `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft` (keine Sandbox). Nicht vorhanden? `write <plan> --draft-dir <Projektordner>`.

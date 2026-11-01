<!-- Referenz für den Skill Thumbnail und Cover – vor jedem Reel-Cover oder YouTube-Thumbnail lesen -->

# Regeln für Cover und Thumbnail – lesbar auf dem Handybildschirm

Recherche vom 3. Oktober 2026 + Messung an einem iPhone-Screenshot (Reels-Tab). Jede Zahl ist gekennzeichnet: **bestätigt** (mit Quelle) · **berechnet** (Rechnung gezeigt) · **Meinung**.

## Warum ist das Cover „aus der Ferne nicht lesbar“?
- Das Profilraster verkleinert das Cover auf **12 %** seiner Größe: Ein Cover mit 1080 Breite wird auf einem 393er-Handy zu einem Quadrat von 130 Punkten (**bestätigt durch Messung**). Auf dem Handy des Nutzers 146 Punkte (13,5 %).
- Die kleinste lesbare Schrift auf dem iPhone ist **11 Punkte**, die normale **17** (**bestätigt** – Apple HIG).
- ⇒ Ein Text mit 11 Punkten braucht im Cover **91 Pixel**, einer mit 17 Punkten **141 Pixel** (**berechnet**: Punkte ÷ 0,1204).
- Lateinische Schrift wirkt bei gleicher Größe eher größer als andere Schriftsysteme; die Mindestwerte unten gelten deshalb auch für Deutsch, nur der Titel darf etwas kleiner sein als beim arabischen Original (≥ 150 statt 170 px).
- Beim ersten Cover eines Kunden: Der Titel kam auf ≈ 13 Punkte, die kleine Zeile auf ≈ 6, der Logo-Text auf ≈ 5 und der Account auf ≈ 4 – alle unter der Grenze.

---

## 🎬 Reel-Cover (1080×1920) – wird als erster Frame des Videos eingesetzt

| Regel | Wert | Grad |
|---|---|---|
| Sichere Zone | alles Wichtige in einem 1:1-Quadrat in der Mitte (y von 420 bis 1500) – unsichtbar, ohne Rahmen | Entscheidung des Nutzers (enger als 4:5 und 3:4, deckt also beide ab) |
| Das Raster | Das Profil schneidet 3:4 aus der Mitte (y 240–1680), der Feed 4:5 (y 285–1635), der Reels-Tab zeigt das ganze 9:16 | bestätigt (3:4) · wahrscheinlich (4:5) |
| Titel | **mindestens 150 Pixel** (besser 170–210) | berechnet |
| Jeder andere Text | **mindestens 110 Pixel** – und nichts unter 91 | berechnet |
| Wörter | **höchstens 5**, zwei Zeilen, **ungefähr 9 Zeichen pro Zeile** bei 170 | Meinung + berechnet (Inter 900 ≈ 0,6 der Größe pro Zeichen) |
| Logo / Icon | **mindestens 200 Pixel** | berechnet (24 Punkte) |
| Linien und Rahmen | **mindestens 10 Pixel** (dünnere verschwinden) | berechnet |
| Gewicht | Bold oder Black – kein Light, kein Thin, und keine Sperrung von Buchstaben | bestätigt (HIG) · Meinung |
| Kontrast | 4,5:1 (oder 3:1 bei sehr großem Text) | wahrscheinlich (WCAG) |
| Der Account `@handle` | **nein** – nicht lesbar und steht ohnehin im Profil | berechnet |

**Reihenfolge im Quadrat:** (Nachrichtenelemente oben, falls vorhanden) → das Gesicht → der Titel unten auf der Brust. Kein Wort auf dem Gesicht.
**Logos:** je nach Titel – keine Regel. ✕ auf dem, was er verlassen hat, und ✓ auf der Alternative **nur**, wenn die Geschichte „von so zu so“ ist.
**Prüfung:** `python3 scripts/34_phone_preview.py <work>/cover.jpg` – zeigt das Cover in echter Größe (Reels-Tab · Profil · aus der Ferne). Kannst du es in der Vorschau nicht lesen, ist es auf dem Handy nicht lesbar.

---

## ▶️ YouTube-Thumbnail (16:9)

| Regel | Wert | Grad |
|---|---|---|
| Format | **3840×2160** empfohlen (mindestens 640 Breite), dazu liefern wir 1280×720. Dateigröße unter 2 MB für den Upload vom Handy | bestätigt (YouTube Help 72431) |
| Hochkant-Video | YouTube erzeugt dafür auf der Startseite ein 4:5-Thumbnail – lass das Wichtige in der Mitte | bestätigt |
| Kleinste Breite | die Seitenleiste (Empfehlung) 218×123 am Computer → Maßstab 0,17 | bestätigt durch Messung |
| Text (auf 1280) | **mindestens 100 Pixel** | berechnet |
| Logo / Icon (auf 1280) | **mindestens 140 Pixel** | berechnet |
| Unten rechts | **310×145 frei** – der Platz der Videodauer | berechnet aus der Messung |
| Wörter | 3–5 | Meinung |
| Gesicht | klare Emotion (Staunen, großes Lächeln), und das Gesicht ist groß | bestätigt (YouTube-Tipps: „shocked face“) |
| Einfachheit | eine Idee, „das Design nicht verkomplizieren“, klare Schrift | bestätigt |

**3 Fassungen:** Jedes Thumbnail entsteht in drei verschiedenen Ideen (Gesicht + Wort · Gesicht + etwas aus der Geschichte · Vorher/Nachher), und er wählt.
**Prüfung:** `python3 scripts/34_phone_preview.py thumb.jpg --youtube` – die Startseite auf dem Handy + die kleine Seitenleiste + der Platz der Dauer.

---

## Bild und Hintergrund (Entscheidung des Nutzers vom 3. Oktober)
- **Frag zuerst:** „Soll ich dein Foto aus dem Video nehmen, oder hast du Fotos für mich?“ – Aus dem Video: `_cutout.py` wählt den Frame (größtes Gesicht × klarstes Bild) und stellt die Person mit Vision frei (Mac). Das Gesicht aus dem Video hat meist keine Emotion, das Bild ist also für das Thumbnail schwächer – sag es ihm.
- **Der Hintergrund ist cremefarben wie bei Claude** `#F0EEE6`, die Ränder 8–10 % dunkler (nicht schwarz) · Text dunkel `#1F1F1D` beim Thumbnail · beim Cover steht der Text weiß auf der Brust (dunkles Oberteil) – und kein dunkler Schatten auf dem Creme.
- **Das Bild aus dem Video beim Cover:** Der Körper ist auf Brusthöhe abgeschnitten – das Kinn liegt über dem Titel (≈ 1000), und die Ränder lösen sich im Hintergrund auf.

## Schriften (einheitlich)
- **Inter** für alles (900 für den Titel, 800 für die kleine Zeile) · **IBM Plex Mono** nur für kleine englische Zeilen.
- Das Theme (`theme.json ← font`) hat Vorrang, wenn der Nutzer auf der Kennenlern-Seite eine Schrift gewählt hat.

## Quellen
- Apple HIG Typography — developer.apple.com/design/human-interface-guidelines/typography
- Instagram-Raster 3:4 (Januar 2025) — petapixel.com/2025/01/23/instagram-swaps-square-profile-grids-for-rectangles
- YouTube thumbnails — support.google.com/youtube/answer/72431 · support.google.com/youtube/answer/12340300

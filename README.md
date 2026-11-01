# Viralio Video – Videoschnitt auf Deutsch für Claude

**Du sprichst in die Kamera – Claude liefert ein fertiges Reel.**
Pausen raus, deutsche Untertitel wortgenau, Motion Graphics in deinen Farben. Ohne Schnittprogramm: Der Schnitt ist Code (ffmpeg + Whisper + eine Render-Engine), und Claude steuert ihn.

> **Stand: Vorabversion `1.0.0-alpha.1`.** Reel mit Untertiteln, Hook-Karte, Untertitelstile und der Motion-Modus sind mit deutschem Text getestet. Der Effekt „Sprache hinter dem Kopf“, der Podcast-Modus mit zwei Kameras, die 3D-Geräte und das Studio sind es noch nicht – siehe [Bekannte Grenzen](#bekannte-grenzen).

## Was drin ist – 5 Skills

| Skill | Wofür | So sagst du es |
|---|---|---|
| **video-ad-editor** | Sprechvideo → 9:16-Reel oder Anzeige | „Schneid dieses Video“ · „Mach ein Reel daraus“ · „Entferne die Pausen“ |
| **motion-video** | 3D-Motion-Erklärvideo aus Text, Website- und App-Erklärungen | „Mach ein Motion-Video aus diesem Text“ · „Erklär diese Website als Video“ |
| **podcast-video** | Podcast und Interview: mehrere Kameras → Reels, ganze Folge 16:9, einstündige Folge → mehrere Reels | „Reels aus der Folge“ · „Ganze Folge im Querformat“ |
| **montage-video** | Clips ohne Sprache auf den Beat schneiden | „Montage aus diesen Clips“ · „Auf den Beat schneiden“ |
| **thumbnail-video** | Reel-Cover und YouTube-Thumbnail, lesbar auf dem Handy | „Mach ein Cover“ · „YouTube-Thumbnail“ |

Dazu: ein geschriebener **Hook** am Reel-Anfang (mit Regelprüfung), **17 Stile**, **100 Bewegungen**, ein Review-Seite für ganze Folgen und ein Studio zum Nachbearbeiten.

## Voraussetzungen

- **Claude Code** (Desktop oder Terminal) oder Claude auf claude.ai mit Plugin-Unterstützung.
- Auf dem Rechner (das Plugin richtet das beim ersten Start selbst ein und fragt vorher): `ffmpeg`, `python3`, `node`, Google Chrome, `openai-whisper`.
- **Mac** für Personen-Freistellung und Gesichtserkennung (Vision). Windows/Linux/Cloud laufen über Ersatzwerkzeuge (`references/any-environment.md`).
- Empfohlen: Modell **Opus 5.5** mit Aufwand **max**.

## Installation

Die Adresse des Marketplaces: `tarik-viralio/viralio-plugins`

**In claude.ai oder der Desktop-App**
1. Einstellungen → **Plugins** → **Marketplace hinzufügen**.
2. Die Adresse einfügen und **Viralio Video** hinzufügen.
3. Bei **Marketplaces verwalten** die automatische Synchronisierung einschalten, dann kommen Updates von selbst.

**Im Terminal**
```bash
claude plugin marketplace add tarik-viralio/viralio-plugins
claude plugin install viralio-video@viralio-plugins
```
Danach eine neue Unterhaltung öffnen.

## Erste Schritte

1. Neue Unterhaltung, Modell Opus 5.5, Aufwand max.
2. Das Video anhängen und schreiben: **„Mach ein Reel daraus“**.
3. Beim ersten Mal öffnet sich eine kleine Seite für deinen Geschmack (Farben, Schrift, Untertitelform). Du kannst sie überspringen und stattdessen im Chat sagen, was du willst.
4. Claude zeigt dir den Text zum Streichen, ein Blatt mit Vorschau-Frames und liefert dann `MP4`, `.srt` und den Text für die Caption. **Veröffentlicht wird nie etwas.**

Auf dem Handy: Video an den Chat hängen, das Handy darf gesperrt werden, das Ergebnis wartet im selben Chat (Cloud-Umgebung, etwas langsamer).

## Sprache

Standard ist **Deutsch**. Für eine andere Sprache die Umgebungsvariable `VIDEO_LANG` setzen (z. B. `VIDEO_LANG=en`); die Stimme und die Hook-Prüfung sind aber auf Deutsch ausgelegt.

## Bekannte Grenzen

- **„Sprache hinter dem Kopf“ und „Ebenen“** wurden für arabische Schrift gebaut (Dehnung per Kashida). Bei deutschem Text fällt das Wort als Karte vor den Körper; die Wirkung ist ungetestet. Betroffen: einige Bewegungen der Bank (62, 63, 66, 67, `pageTurnRTL`, `ayahCalm`).
- **Nicht getestet mit deutschem Material:** Podcast-Modus mit mehreren Kameras, 3D-iPhone/-MacBook, Studio, Review-Seite, CapCut-Export.
- Die **Kennenlern-Seite** und das Studio zeigen noch teilweise die Oberfläche des Originals. Ohne Browser fragt Claude einfach im Chat.
- Die Namen im Bewegungskatalog sind noch in der Sprache des Originals.
- Whisper `small` verhört gelegentlich Wörter; für den Schnitt `medium` oder `turbo` nutzen. Claude korrigiert den Text ohnehin, bevor die Untertitel entstehen.

## Support

https://viralio.de

## Herkunft und Lizenz

Viralio Video ist eine deutsche Bearbeitung von **video-ad-editor / majed-video** von **Majed Alzaabi** (MIT-Lizenz).
Copyright (c) 2026 Majed Alzaabi · Copyright (c) 2026 Viralio (deutsche Bearbeitung).
Der vollständige Lizenztext steht in [`LICENSE`](LICENSE). Die Schriften unter `video-ad-editor/motion/fonts` stehen unter der SIL Open Font License, Drittbibliotheken (three.js u. a.) unter ihren eigenen Lizenzen – siehe `video-ad-editor/motion/fonts/LICENSES.txt` und `video-ad-editor/motion/moves/CREDITS.md`.

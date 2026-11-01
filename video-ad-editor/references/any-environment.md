# 🌍 Läuft überall – Handy · Cloud · Windows · Linux · Codex

**Die Regel:** Sag dem Nutzer nie „das geht nicht auf dem Handy / in der Cloud / auf deinem Gerät“. Jeder Schritt
hat eine Leiter von Alternativen – probier die oberste, und wenn sie nicht läuft, geh zur nächsten und nenn ihm in einer Zeile, was du genutzt hast. Der lokale Rechner
(Mac + Claude Code) bleibt der stärkste und schnellste, ist aber nicht Pflicht.

**📖 Details und erprobte Codes:** `references/phone-cloud-playbook.md` – Personen-Freistellung mit Modell + Referenzhintergrund + zeitlicher Glättung (Abschnitt 4, löst dunkles Oberteil, Bereich zwischen den Händen und unteren Bildrand), die Papier-Motion-Engine (Abschnitt 5: Dehnung in Pixeln, Brustwort, Eintrittskreis, Übergang 0,4 s), der Zusammenbau mit einem ffmpeg-Befehl und die Qualitätstore.

**Der Beweis, dass es geht:** Eine Sitzung auf dem Handy (Claude-App, Cloud-Umgebung) nahm ein Rohvideo und lieferte ein komplettes Reel von 43 s mit Pausenschnitt,
Personen-Freistellung vom Hintergrund, Motion in Ebenen, Untertiteln und Ton mit –14,7 LUFS – bei gesperrtem Handy. Sie nutzte die Alternativen unten.

## Wie das Video ankommt
| Wo | Wie |
|---|---|
| Claude-App am Handy oder Web | Video an den Chat anhängen → es kommt in der Arbeitsumgebung an. Die mp4 kommt im Chat zurück (Uploadgrenze je nach App). |
| Claude Code oder Codex auf einem Gerät | Der lokale Pfad läuft normal. |
| Codex / jeder Agent, der Befehle ausführt | Lies `SKILL.md` und `references/` als Textanweisungen und führ dieselben Skripte aus. Nichts ist Claude-spezifisch außer dem Ort der Dateien. |

## Die Leiter der Alternativen (von oben nach unten)
| Schritt | Am besten (lokaler Mac) | Umgebung ohne Mac / Cloud |
|---|---|---|
| Sprache transkribieren | `mlx-whisper` (am schnellsten) → `whisper` | `faster-whisper` (`pip install faster-whisper`, Modell von huggingface `Systran/faster-whisper-*`). ✅ lief in der Handy-Sitzung. |
| Person vom Hintergrund freistellen | Vision (`personmask.swift`) | **MODNet** ✅ lief in der Handy-Sitzung · dann `rembg` (`pip install rembg`, Modell `u2net_human_seg`) · dann BiRefNet. ⚠️ Haare und Hände sind schwieriger – schneide nicht den Teil frei, der ohnehin verdeckt ist. |
| Gesichtserkennung (Hochkant-Beschnitt, Kartenbeschnitt) | Vision (`facetrack.swift`) | MediaPipe oder OpenCV Haar · ohne beides: Beschnitt aus der Mitte mit Hinweis. (nicht getestet) |
| Handerkennung | Vision (`handpose.swift`) | MediaPipe Hands. (nicht getestet) |
| iPhone-HDR-Video | `hdr2sdr.swift` | `ffmpeg` mit Filter `zscale` + `tonemap=hable` (braucht einen ffmpeg-Build mit zscale). (nicht getestet) |
| Motion als Frames rendern | puppeteer + Chrome | Chrome/Chromium ohne Oberfläche (headless) + ffmpeg ✅ lief in der Handy-Sitzung · oder playwright (`npx playwright install chromium`). |
| Modelle herunterladen | normal | Ist eine Domain gesperrt, probier eine Alternative (huggingface oder GitHub-Releases). Sind beide gesperrt: Nenn dem Nutzer die Domain beim Namen und stoppe die Arbeit nicht – mach mit den Schritten weiter, die sie nicht brauchen. |
| Kennenlern-Seite (Farben/Schrift) | öffnet im Browser | Ohne Browser: eine Frage im Chat zu den Farben |

⛔ Erfinde kein Tool. Jede Alternative oben ist entweder ✅ wirklich erprobt oder mit „nicht getestet“ gekennzeichnet – teste Nicht-Getestetes in einem Satz, bevor du darauf aufbaust.

## Qualitätsregeln, die sich mit der Umgebung nicht ändern
- Nach jedem Freistellen: Vergleiche die Kante (Haare, Hände, unter dem Bild) an 3 schwierigen Frames, bevor du alle Frames renderst.
- „Sprache hinter der Person“: Das Wort wird gedehnt, damit es nicht hinter dem Kopf abgeschnitten wird (`references/cut-styles.md`).
- Der Übergang zwischen Clips ist schnell (≈ eine Drittelsekunde), nicht langsam.
- Der verdeckte Teil des Körpers braucht keine Freistellung.
- Ton –14 LUFS (`06b_master.sh`).
- Liefere nie ohne Prüf-Frames, und sag offen, was du gesehen hast und was nicht.

## Das Handy: wie die Arbeit läuft
1. Der Nutzer hängt das Video an und schreibt seinen Wunsch in einem Satz.
2. Du arbeitest im Hintergrund, und das Handy darf gesperrt werden – du sagst ihm, dass das Ergebnis im selben Chat auf ihn wartet.
3. Du schickst die mp4 + eine Zusammenfassung: was sich geändert hat, was du ersetzt hast, was du nicht geprüft hast.
4. Seine Anmerkungen (z. B. „der Schnitt zerstört die Haare“) setzt du um, ohne neu zu drehen.

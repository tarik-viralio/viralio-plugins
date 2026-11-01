<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Bearbeitungsbildschirm (Remotion) – die zweite Engine

**Starte immer mit der leichten, und ohne ein Wort darüber.** Erwähne weder „Remotion“ noch „Canvas“ noch „Engine“, und biete nicht zwei Optionen an.
Du öffnest sie nur, wenn **er** nach der Ansicht der Anzeige sagt: „Ich will selbst nachbearbeiten“ · „Das gefällt mir an dieser Stelle nicht, ich will es verschieben“ · „Gibt es einen Bildschirm, auf dem ich die Bearbeitung sehe?“
Dann ein Satz: „Ich öffne dir einen Live-Bearbeitungsbildschirm, auf dem du das Video siehst, alles verschieben kannst und sofort das Ergebnis siehst – der Download dauert einmalig 5 Minuten, soll ich anfangen?“
**Wiederhole keinen früheren Schritt** – Schnitt, Transkription, Untertitel und Effekte werden geteilt.

| | **Die leichte** (Standard) | **Bearbeitungsbildschirm** |
|---|---|---|
| Download | null zusätzlich | ~500 MB einmalig |
| Was er sieht | Frames, die du ihm zeigst | ein Live-Video, in dem er zieht und sofort sieht |
| Lizenz | frei | Ein Unternehmen mit vier oder mehr Mitarbeitern zahlt (sag es ihm, wenn es ein Unternehmen ist) |
| Befehl | `04_render_frames.js` | `04b_remotion.sh` |

```bash
bash scripts/04b_remotion.sh <work> setup                     # einmalig – nach seiner Erlaubnis (~500 MB)
bash scripts/04b_remotion.sh <work> studio                    # Live-Timeline im Browser
bash scripts/04b_remotion.sh <work> render <work>/ad-final.mp4   # MP4 direkt ohne Einzelframes
```
- Die Szenen werden in `<work>/remotion/src/Scenes.tsx` geschrieben (gleiche Logik: Jede Szene bekommt `t`).
- Die Rechtecke der Videoanzeige in `<work>/stage.json`, die Schlusstexte in `<work>/outro.json`.
- Sichere Zone: `"guides": true` in `safe.json`, dann `studio` – du siehst die roten Bereiche live.
- Es kennt `R_OFF` noch nicht.

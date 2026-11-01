<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

### 7.75) Verblasster Hintergrund – „wie ein Kinomodus“ (v2.6)

Wenn der Drehhintergrund schlecht ist (Hotel, volles Büro) und der Nutzer ihn mit der Kamera nicht freistellen kann: Der Sprecher bleibt klar, und der Hintergrund wird mit einer cremefarbenen Farbe aus dem Theme überdeckt – in allen Modi, damit die Übergänge flüssig bleiben.

```bash
python3 scripts/14_backdrop.py <work> 0.62      # baut cover/ für jeden Frame (die Maske kommt von Vision auf dem Mac)
node scripts/04_render_frames.js <work> all --force
```
Stärke 0,62 = Hintergrund sichtbar, aber blass. Zum Aufheben: `cover/` löschen und neu rendern. Für den Bau der Maske braucht es einen Mac; liegt ein fertiges `cmask/` vor, wird es genutzt.

**Zwei Tipps, vom Nutzer abgenommen (4. September):** `faceAnchor: 0.42` in `theme.json` rückt seinen Kopf in den verkleinerten Modi näher an den oberen Rand der Karte (weniger Platz über dem Kopf, und die Hand ist zu sehen). Und der letzte Schnitt: Wiederholt der Sprecher das letzte Wort nach dem letzten Satz, lösche den letzten Abschnitt aus `cut.json` – der Schnittplan zählt ihn als Sprache.

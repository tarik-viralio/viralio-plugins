<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# 📱 Das Studio (v3.1) – Handy oder Browser

**Wann öffnest du es?** Wenn er sagt „Ich will selbst nachbearbeiten“ · „Gib mir die Timeline“ · „Ich will den Untertitelstil ändern“ – oder nach der ersten Lieferung, wenn er viele kleine Änderungen hat (billiger, als alles im Chat zu wiederholen).
⚠️ Der Server öffnet sich im lokalen Netzwerk (gleiches WLAN) ohne Passwort – starte ihn nicht in einem öffentlichen Netz.

```bash
python3 studio/studio.py <work> [port]      # gibt einen Link aus, den du auf dem Handy im selben WLAN öffnest (Standardport 8792)
```

Eine Touch-Timeline über derselben Engine und demselben Renderer (null Token pro Änderung). Sie enthält:
- Schnittsteuerung (Pausen zurückholen oder schneiden, einen Abschnitt oder Satz löschen – baut neu und rechnet alle Zeiten um)
- 6 Untertitelstile (`references/word-fx.md`) · Effekt auf jedem Wort (Fall · Wackeln · Tippen · Puls)
- „Hinter dem Kopf“ mit einem Tipp · Soundeffekt am Satz
- B-Roll vom Handy hochladen (Vollbild oder Karte oben) · die vier Szenen + Collage
- Identität · sichere Zonen von Instagram · Vorher/Nachher · ein Link für den Kunden, der jede Sekunde kommentieren kann (`/share`) · Export vom Handy

Änderungen werden in `studio.json` gespeichert (+caps/theme/sfx) und wirken in jedem späteren Render – `04_render_frames.js` und `08_safe_check.js` lesen sie.
Leertaste = abspielen/stoppen · Pfeile = ein Frame · Shift+Pfeil = eine Sekunde.

## Schlüssel in `studio.json`, die die Engine liest
`scenes` (`[{s,e,m:"R_FULL"|"R_DOWN"|"R_LOWER"|"R_OFF"|"R_COLLAGE",nocap?,gb?,tr?}]` – `tr` ist die Übergangsdauer der Szene, 6.1) · `stickers` (6.1: Der Sticker bleibt bis `e` und geht danach ruhig über 0,4 s) · `brollClips` + `brNeed` · `behindOff` · `outro` (`l1,l2,chips,cta,word`) · `gen` + `genFrames` (`references/gen-scenes.md`) ·
`sceneFx`: Namen von Szenenfunktionen, die in compose.html geschrieben und mit `SCENE_LIST` registriert sind (Beispiel `["myPanel"]`) – **standardmäßig gibt es keine eigene Szene**; `false` leert die Liste.

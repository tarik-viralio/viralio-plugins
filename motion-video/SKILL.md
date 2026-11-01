---
name: motion-video
description: 3D-Motion-Graphics-Film ohne Person und ohne Dreh – aus Text, Idee oder Skript, mit eigener oder generierter Stimme, 60 fps. Dazu Erklärvideos für Website oder App mit echten Screens im 3D-iPhone oder MacBook. Use when user says "Motion-Video", "Erklärvideo mit Motion", "mach ein Video aus diesem Text", "Motion Graphics", "erklär diese Website als Video", "erklär die App als Video", "iPhone-Demo". Not for editing a talking video (use video-ad-editor).
---

# Motion-Erklärvideo – ein Film aus Text, ohne Dreh

**Die Engine wird mit dem Reel-Skill geteilt.** Alle `scripts/`, `references/` und `motion/` liegen hier:
`${CLAUDE_SKILL_DIR}/../video-ad-editor`

## Schritte

1. **Start:** `references/start.md` lesen und umsetzen (Tools, Geschmack, Identität).
2. **Modus:** `references/motion-mode.md` lesen und umsetzen – alle Regeln sind verbindlich.
3. **Befehle:** `motion/README.md`, Leitfaden für Szenen-Autoren: `motion/ENGINE-API.md`.
4. **Website oder App erklären:** `references/web-app-explainer.md`
5. **One-Take (ganzes Video als eine Einstellung, ohne Schnitt):** `references/one-take.md` + laufendes Beispiel `motion/examples/one-take/`. Für App- oder Tool-Werbung, Schritt-für-Schritt-Abläufe oder eine Idee mit verschachtelten Szenen.
6. **Beispiele anderer (Inspiration, kein Kopieren):** `references/examples.md`
6b. **Fester Rahmen + 3D-Folienwand – nur auf Wunsch des Nutzers** (nicht Standard): Abschnitt „Eine Einstellung mit festem Rahmen“ in `references/motion-mode.md`, Beispiel `motion/examples/stage-wall/`. Motion-Blur (`motionBlur`) passt zu jedem Film mit schneller Bewegung.
7. **Bewegungsbank – eine Palette pro Video (Pflicht):** `references/moves.md`. Vor der ersten Szene: `python3 scripts/35_moves.py plan --title "…"` → 3 Kernbewegungen, um die sich der Film dreht, plus Akzente für besondere Momente, aufrufbar über `ctx.FX.<id>`.

## ⛔ Dein Umgang mit dem Nutzer

- **Du bereitest vor, nicht er.** Gib ihm keine Befehle zum Ausführen und frag nicht „Hast du das installiert?“ – prüf es selbst.
- **Keine Fachbegriffe;** sag bei jedem Schritt, wo ihr steht und wie lange es dauert.
- **Immer nur eine Sache,** und zeig nach jeder wichtigen Phase einen Frame.
- ⛔ Frag nicht „Welchen Modus willst du?“ – sag in einem Satz, was du verstanden hast, und mach weiter.

## Feste Regeln

- Normale Ziffern (1 2 3), deutsche Schreibweise (Tausenderpunkt, Dezimalkomma).
- Farben ausschließlich aus `theme.json`.
- Keine Zahl und kein Name auf dem Bildschirm, die nicht in `facts.md` stehen → `references/motion-rules.md`
- Kein Veröffentlichen, kein Planen von Posts – geliefert wird nur eine Datei.
- Läuft lokal über Claude Code. Im Chat gibt es nur Skript, Plan und Theme.

---
name: montage-video
description: Schneidet Clips ohne Sprache auf den Beat – ein Ordner mit Clips (Café, Tisch, Produkt, Ort, Event) wird zu einem 9:16-Video, das aus jedem Clip den besten Moment wählt und auf den Audio-Beats schneidet. Use when user says "Montage aus diesen Clips", "mach ein Video aus diesen Clips", "schneid die Clips auf den Song", "Beat-Montage", "auf den Beat schneiden", or sends a folder of clips without speech. Not for a talking video (use video-ad-editor).
---

# Montage aus Clips ohne Sprache

**Die Engine wird mit dem Reel-Skill geteilt.** Alle `scripts/` und `references/` liegen hier:
`${CLAUDE_SKILL_DIR}/../video-ad-editor`

## Schritte

1. **Tools:** nur Schritt 0 aus `references/start.md`.
   ⛔ Keine Fragen zu Farben oder Logo – eine Montage hat ja keinen Text.
2. **Modus:** `references/montage.md` lesen und umsetzen.
3. **Effekte auf dem Beat** (Zoom, Shake, Flash, Wisch) → `references/beat-fx.md`
4. **Szene nach Bedeutung suchen** („Kaffee wird zubereitet“, „Nahaufnahme vom Produkt“) → `references/find-shots.md`

## ⛔ Dein Umgang mit dem Nutzer

- Du brauchst von ihm nur eins: **den Ordner mit den Clips.**
- **Du bereitest vor, nicht er.** Keine Fachbegriffe; sag ihm, wo ihr gerade steht und wie lange es dauert.
- Zeig ihm vor dem Zusammenbau ein nummeriertes Kontaktblatt der Szenen.

## Feste Regeln

- ⛔ Keine Transkription, keine Untertitel, keine generierten Szenen.
- Nenn es „Hintergrund-Audiodatei“, nicht „Musik“ – was drin ist, bestimmt der Nutzer.
- Keine Farbkorrektur, außer sie wird ausdrücklich verlangt.
- Kein Veröffentlichen, kein Planen von Posts – geliefert wird nur eine Datei.

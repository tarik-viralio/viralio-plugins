---
name: podcast-video
description: Schneidet Podcasts und Interviews – zwei oder mehr Kameras derselben Session zu 9:16-Reels mit deutschen Untertiteln und geschriebenem Hook, oder die ganze Folge in 16:9 für YouTube, oder eine einstündige Folge zu mehreren Reels. Use when user says "Podcast", "zwei Kameras", "ganze Folge im Querformat", "YouTube-Folge", "Reels aus der Folge", "mach Reels aus dem Interview", or sends multi-camera files or a long episode. Not for a single talking video (use video-ad-editor).
---

# Podcasts und Interviews

**Die Engine wird mit dem Reel-Skill geteilt.** Alle `scripts/` und `references/` liegen hier:
`${CLAUDE_SKILL_DIR}/../video-ad-editor`

## Schritte

1. **Start:** `references/start.md` lesen und umsetzen (Tools, Geschmack, Identität).
2. **Pfad aus dem Material wählen** – ohne den Nutzer zu fragen:

| Material | Pfad | Lesen |
|---|---|---|
| Zwei oder mehr Kameras derselben Session | Vertikale Reels (Standard) | `references/podcast.md` |
| Sagt „ganze Folge“, „YouTube“ oder „im Querformat“ | Ganze Folge 16:9 | `references/podcast.md` (Abschnitt „Ganze Folge im Querformat“) |
| Lange Folge (eine Stunde) → mehrere Reels | Schnelle Transkription → Vorschläge → Schnitt | `references/landscape.md` (Abschnitt „Ganze Folge“) |

3. **🪝 Jedes Reel aus einer Folge oder einem Interview beginnt mit einem geschriebenen Hook – Pflicht** → `references/podcast-hook.md`
   - Kamera-Modus: **vor** `15_podcast.py plan` anwenden.
4. **Reel aus einem einzelnen Stück:** weiter mit Schritt 5–11 des Reel-Skills:
   `${CLAUDE_SKILL_DIR}/../video-ad-editor/SKILL.md`
5. **Jede Naht zwischen zwei Stücken wird geprüft** (`19_seam_check.py`) – Pflicht.
6. Podcast-Extras → `references/podcast-upgrades.md`
7. **Schlusswort + Folgen-Link per DM (Automation):** in `theme.json ← outro` eine Karte mit dem Folgen-Stichwort setzen → `references/keyword-automation.md`
8. **Arbeitsweise bei jeder neuen Folge:**
   - **Der Chat ist für Entscheidungen:** Folge transkribieren und ein **nummeriertes Vorschlagsblatt** zeigen (Hook + Anfang/Ende + warum es funktioniert); der Nutzer wählt per Nummer. Nicht schneiden, bevor er gewählt hat.
   - **Nach der Montage – Review-Seite (Pflicht ab 2 Elementen):** alle Reels und Karussells auf einer Seite mit Notiz, Freigabe und Download → `references/review-page.md`. Änderungen danach kommen aus seinen Notizen auf der Seite („schau dir die Notizen an“).
   - **Ein „Setup“ pro Folge:** Stichwort + Folgen-Link + Schlusskarte + eine Automation auf „jeden Post“ – identisch für alle Reels der Folge.
   - **Karussell aus der Folge:** nur das Foto des Gasts oder Sprechers auf dem Cover, die übrigen Folien aus freigestellten Bildern oder Elementen – vor dem Export eine Vorschau-Übersicht zeigen.

## ⛔ Dein Umgang mit dem Nutzer

- **Du bereitest vor, nicht er.** Gib ihm keine Befehle zum Ausführen.
- **Keine Fachbegriffe;** sag bei jedem Schritt, wo ihr steht und wie lange es dauert.
- **Immer nur eine Sache,** und zeig nach jeder wichtigen Phase ein Kontaktblatt.

## Feste Regeln

- Untertitel kommen nie auf das Gesicht des Sprechers.
- Normale Ziffern, Farben ausschließlich aus `theme.json`.
- Keine Farbkorrektur am Bild, außer sie wird ausdrücklich verlangt.
- Nichts erfinden, was nicht gesagt wurde; kein Veröffentlichen, kein Planen – geliefert wird nur eine Datei.
- Gesichtserkennung und Personen-Freistellung (Vision-Bibliothek) gibt es nur auf dem Mac.

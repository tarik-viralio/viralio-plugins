<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Szene „komplette Erklärung“ (`R_OFF`) und „ruhiger“ Rhythmus (v2.5)

## „Komplette Erklärung“ – `R_OFF`
Der Sprecher **verschwindet** (seine Karte gleitet unter den Bildschirm), der ganze Bildschirm ist eine Infografik, **seine Stimme läuft weiter, und die Untertitel bleiben unten** an ihrem gewohnten Platz (Unterkante bei 1460, der Balken bei 1492).
In den Szenen: `{s:12.4,e:18.9,m:R_OFF}` (oder `"m":"R_OFF"` in studio.json) – die Struktur kümmert sich um Gleiten, Untertitel und Balken.

**⛔ Regeln:**
1. **Ein- bis zweimal pro Video** – öfter, und der Zuschauer merkt, dass du verschwunden bist.
2. **4 bis 8 Sekunden** pro Szene, danach direkt wieder Vollbild (das Gesicht kehrt zurück).
3. **Bei Sätzen mit Zahlen, Liste oder Vergleich** – dem, was wirklich Platz braucht. **Nicht beim Hook und nicht beim Schlussaufruf.**
4. Die Szene muss eine **visuelle Metapher für seine Worte** sein (Zähler, Karten, Tabelle) – keine Zierde, die Leere füllt.
5. Derzeit nur die leichte Engine (Remotion kennt es noch nicht).

## Ruhiger Rhythmus – `theme.json` → `"pace":"calm"`
Wenn der Nutzer „in ruhigem Rhythmus“ sagt oder sich über zu viele Schnitte beschwert:
- Der Zoom ist leichter (1,00–1,06 statt 1,00–1,14) und weniger abwechslungsreich.
- **Der Zoom ändert sich nicht, bevor 4 Sekunden** derselben Einstellung vergangen sind (`03_cut_zoom.py` fasst kurze Clips auf einem Zoom zusammen).
- Und in den Szenen: **Wechsle das Rechteck nicht vor 4 Sekunden**, überschreite **nicht 6 Wechsel pro 30 Sekunden**, und die Erklärung bleibt stehen, bis der Gedanke fertig ist.
- Der Hook bleibt wie gehabt Vollbild.

Ohne seinen Wunsch bleibt der Rhythmus der normale.

# Studio – eine optionale Ebene über dem Skill

Ein eigenständiger Ordner: Er startet einen kleinen Server und liefert eine Bearbeitungsseite für Touch oder Maus über **denselben** Dateien des Skills (caps.json · theme.json · studio.json · sfx.json) und denselben Renderer. Löschst du diesen Ordner, ändert sich am Skill nichts.

```bash
python3 studio/studio.py <work>     # gibt den Link für Handy und Rechner aus
```

Die einzige Auswirkung auf den Haupt-Skill: `compose.REFERENCE.html` liest `studio.json`, wenn vorhanden (Szenen · Sticker · B-Roll · Wortbewegungen · „Hinter dem Kopf“ ausschalten). Ohne sie läuft alles wie bisher.

Rückgängig: Der Knopf ↶ (oder Cmd+Z) macht die letzte Änderung rückgängig (40 Schritte). „Letzten Schnitt oder letzte Löschung rückgängig“ im Tab Export stellt die Dateien vor dem letzten Neubau wieder her.

<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Suche nach Bedeutung in Clips – `26_find_shots.py`

Sucht eine Einstellung per Beschreibung in vielen Videos: „Nahaufnahme vom Produkt“, „eine Hand drückt einen Knopf“, „Sonnenuntergang am Meer“.
Das Modell **SigLIP2** von Google läuft auf seinem Gerät (ohne Guthaben und nach dem ersten Download von ~1,5 GB ohne Internet).
Braucht einmalig `00_setup.sh --extras` (torch ist mit Whisper ohnehin da).

### Wann?
- **Montage:** Er will eine bestimmte Einstellung aus einem Ordner mit Dutzenden Clips.
- **B-Roll:** Das Firmenvideo ist lang, und er will die Einstellung, die zu einem Satz aus seiner Rede passt (z. B. er sagt „der Akku“ → `a phone battery indicator`).
- **Suche per Bild:** Er hat ein Bild der gewünschten Form → `--like bild.jpg`.

### Befehle
```bash
python3 scripts/26_find_shots.py <work> index <Ordner_oder_Dateien…> [--every 1.0]   # eine Einstellung pro Sekunde
python3 scripts/26_find_shots.py <work> find "a close-up of a camera lens" --top 8 --sheet
python3 scripts/26_find_shots.py <work> find --like ref.jpg --sheet
python3 scripts/26_find_shots.py <work> where "…"     # mit den Clipnummern der Montage (montage.json)
```
- Der Index liegt in `<work>/shots/` und aktualisiert sich nur für neue Dateien.
- Ergebnisse: `Clip @ von→bis` (aufeinanderfolgende Einstellungen werden zusammengefasst) + `shots/hits.json`, und `--sheet` ein Blatt `shots/hits.jpg` in gleicher Reihenfolge – **lies es als Ganzes** und prüf mit eigenen Augen, bevor du das Ergebnis nutzt.

### ⛔ Regeln
1. **Die Beschreibung auf Englisch und wie eine Bildunterschrift** – „a person pouring coffee into a white cup“, nicht „Kaffee gießen“. Übersetze seine Worte selbst.
2. Die Bewertung ist relativ: Der höchste Treffer kann falsch sein, wenn die Einstellung gar nicht existiert – **das Blatt entscheidet**, nicht die Zahl.
3. B-Roll aus dem Ergebnis: Extrahiere ihren Bereich als Frames (`ffmpeg -ss <von> -to <bis> … broll/<name>_%04d.jpg`) und mach wie bei normaler B-Roll weiter.

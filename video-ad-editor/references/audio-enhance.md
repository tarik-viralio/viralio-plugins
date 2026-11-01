<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

### 3.5) „Ton verbessern“ – Aufnahme ohne Mikrofon (optional, vor der Transkription)
Sagt er „verbessere den Ton“, oder wurde mit dem Handymikrofon an einem Ort mit Hall oder Rauschen aufgenommen:
> ⚠️ **In Claude Code (6.0):** `media_enhance_speech` von Adobe startet die Arbeit, aber es gibt kein Folge-Tool, das die saubere Datei holt – geh direkt zu Option 2 (DeepFilterNet auf dem Gerät). Adobe taugt nur in einer Claude-Sitzung mit dem Folge-Tool.

1. **Adobe:** Ist der Adobe-Connector in der Claude-Sitzung vorhanden (Tools `media_enhance_speech` und `asset_initialize_file_upload`), rufst **du** ihn auf: Lade `<work>/src.mov` zu Adobe hoch (Upload initialisieren → Teile per curl hochladen → Upload abschließen), dann `media_enhance_speech(assetId)` – es gibt einen Pfad für saubere Sprache, einen für den Hintergrund und einen für den Hall zurück. Lade den Sprachpfad herunter und mische ihn ein:
   ```bash
   bash scripts/02b_enhance_audio.sh <work> <clean.wav>
   ```
   Beim Nutzer nötig: Der Adobe-Connector ist in Claude aktiviert, und ein Adobe-Konto ist angemeldet (Typ `auth`, prüfen mit `get_account_type`). Nichts wird auf dem Gerät installiert.
2. **Ohne Adobe – auf seinem Gerät:** `bash scripts/02b_enhance_audio.sh <work> --local [Stärke]`
   - Hat `00_setup.sh --extras` **DeepFilterNet3** installiert (ein kleines Programm ohne Python, das nichts auf einen Server hochlädt): intelligente Reinigung, die Klimaanlage, Lüfter, Straße und leichten Hall entfernt. In unserem Test: Abstand zwischen Sprache und Rauschen von 17 auf 55 Dezibel (der alte ffmpeg-Filter: 26).
   - Stärke 0..1 (Standard 0,85): die Grenze der Dämpfung im Modell – 1 ist komplett sauber, kann aber „dünn“ klingen, 0,5 ist weicher. **Mische es nicht mit dem Original** – die Mischung bringt das ganze Rauschen zurück.
   - `--ai` statt `--local` = zwingend die intelligente Variante (bricht ab, wenn nicht installiert).
   - Nicht installiert? Es fällt selbst auf den ffmpeg-Filter zurück (Rauschunterdrückung + Tiefenschnitt + Kompression + Lautheit) – schwächer, aber läuft überall.
Das Original wird als `src_rawaudio.mov` gesichert. Mach es **vor** der Transkription, damit Whisper sauberen Ton hört. Sag dem Nutzer in einem Satz, welchen Weg du gegangen bist.

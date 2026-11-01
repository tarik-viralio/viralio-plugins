<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Karte der Skripte und Dateien

| | Was es tut | Die Engine |
|---|---|---|
| `00_setup.sh` | prüft die Tools und lädt Fehlendes herunter · `--update` zum Aktualisieren | geteilt |
| `01_cut_plan.py` | misst die Pausen und erzeugt die Sprechabschnitte | geteilt |
| `02a_whisper_check.py` | 6.1: prüft die Whisper-Transkription (halluzinierte Wiederholung + verlorene Rede) vor der Korrektur · `--fix` transkribiert die Fenster in Stücken ohne Kontext neu | geteilt |
| `02_captions.py` | die Zeit jedes Worts auf der neuen Timeline | geteilt |
| `02b_enhance_audio.sh` | Tonverbesserung lokal (`references/audio-enhance.md`) | geteilt |
| `03_cut_zoom.py` | Schnitt + Zoom pro Abschnitt + bt709-Tag + HDR-Konverter | geteilt |
| `_landscape.py` | wird von 03 selbst für Querformat-Videos aufgerufen: Einstellungsgrenzen + Gesicht → 9:16-Beschnitt pro Einstellung · `shots.json` (`references/landscape.md`) | geteilt (Gesicht: Mac) |
| `04_render_frames.js` | rendert die Frames (Fortsetzen + Fenster + Vorschau) · gibt Szenenfehler als `[compose]` aus · Design-Fingerabdruck: Änderung oder `--force` = löscht zuerst das Alte | die leichte |
| `04b_remotion.sh` | richtet ein Remotion-Projekt ein/öffnet/rendert es (`references/remotion.md`) | Remotion |
| `05_sfx.py` | die Soundeffekte aus `sfx.json` | geteilt |
| `06_encode.sh` | fügt Frames + Ton zusammen · `FIT=1` zweistufig unter `MAXMB` MB (6.1 – Reel ohne Cover) | die leichte |
| `06b_master.sh` | –14 LUFS + Hintergrund-Audiodatei mit automatischem Absenken | geteilt |
| `06c_loudfix.sh` | wenn 06b unter dem Ziel stoppt (–15/–16 wegen hoher Spitzen): leichte Kompression + –14 zweistufig, das Bild bleibt | geteilt |
| `07_contact_sheet.sh` | ein Kontaktblatt: 3 Spalten × 2 Reihen (höchstens 6) | geteilt |
| `08_safe_check.js` | sichere Zone + Hook (dieselbe Last wie 04: theme + studio + behind) | die leichte |
| `09_srt.py` | Untertiteldatei + Untertiteltext | geteilt |
| `10_script_edit.py` | `show` (gibt Text und wiederholte Sätze aus) · `drop` · `keep` · `undo` | geteilt |
| `11_behind_text.js` + `personmask.swift` | die drei Schnittstile (`references/cut-styles.md`) | die leichte (Mac) |
| `12_montage.py` | **Montage-Modus** (`references/montage.md`) | eigenständig |
| `13_collage.js` · `13_collage_sfx.py` · `collage.TEMPLATE.html` | der Collage-Stil (`references/collage.md`) | eigenständig |
| `13_assets.py` | ein Bild von Wikimedia (freie Lizenz) mit optionaler Freistellung | geteilt |
| `14_backdrop.py` | verblasster Hintergrund (`references/backdrop.md`) | die leichte |
| `23_headcrop.py` (+`facetrack.swift`) | **Beschnitt der Karte über dem Kopf** – konstant über das ganze Video, schreibt `studio.json ← cardTop` (Schritt 6.1) | Mac |
| `15_podcast.py` · `16_render_pod.js` · `compose.PODCAST.html` · `facetrack.swift` | **Podcast-Modus** (`references/podcast.md`) | eigenständig (Mac) |
| `17_gen_scenes.py` | generierte Szenen (`references/gen-scenes.md`) | die leichte |
| `18_long_transcribe.py` | transkribiert eine ganze Folge in 20-s-Stücken an Pausen (mlx am Mac ~8× schneller) → `words.json` + `transcript.txt` | geteilt |
| `20_episode_cuts.py` | Folge → Reel: `spec.json` (Schnitte nach Wörtern) → `cut.json` mit Grenzen auf der Pause + `a.json` (Transkription pro Stück, `seg`) + Vorlage `fixes.json` + `src.mov` | geteilt |
| `19_seam_check.py` | transkribiert das fertige Reel um jede Naht und erkennt das wiederholte Wort oder Reste von Rede von außerhalb | geteilt |
| `00_theme_refs.py` | Theme aus Referenzbildern (Pinterest/Aufnahmen/Bilder) → `theme.json` + `refs_palette.jpg` mit lesbarem Kontrast | geteilt |
| `02c_denoise.py` | intelligente Tonreinigung DeepFilterNet3 auf dem Gerät (wird von `02b --local` aufgerufen) – fällt auf ffmpeg zurück, wenn es fehlt | geteilt |
| `24_podcast_wide.py` | ganzer Podcast im Querformat 16:9 aus den rohen Kameras: Synchronisation + Wechsel je nach Sprecher + weite Einstellung → `episode-wide.mp4` | geteilt |
| `27_web_capture.js` | nimmt eine Website auf: Handyscreens + weiches Scrollen + Computer + `site.json` (Texte und Farben) für ein Erklärvideo | geteilt |
| `28_cover.py` | das Reel-Cover = erster Frame des Videos: alles Wichtige im 1:1-Quadrat in der Mitte · freigestelltes Bild (`--photo`) oder der klarste Frame · Logos ✕/✓ · `--first` setzt es als ersten Frame → `cover.jpg` + `cover_grid.jpg` + `*-cover.mp4` | geteilt |
| `33_thumb.py` | YouTube-Thumbnail 16:9 mit drei Ideen (großes Gesicht + Hook ≥ 100 Pixel + unten rechts frei) → 3840×2160 und 1280×720 + `thumbs_sheet.jpg` | das Cover |
| `34_phone_preview.py` | Vorschau von Cover/Thumbnail in echter Handygröße (Reels-Tab · Profil · aus der Ferne · YouTube) | das Cover |
| `40_capcut.py` | Schnitt in CapCut: Plan aus der Transkription → transparentes ProRes-Motion + Effekte → schreibt ein bearbeitbares CapCut-Projekt (`projects` · `skeleton` · `check` · `stills` · `render` · `sfx` · `write` · `all`) | CapCut |
| `41_review.py` + `review.TEMPLATE.html` | Review-Seite der Folge: alle Reels und Karussells auf einer Seite (Notiz · freigeben · herunterladen), privat veröffentlicht auf claude.ai – `references/review-page.md` | Podcast |
| `29_handtrack.py` + `handpose.swift` | Handerkennung (Vision) → geglättetes `palm.js`: ein Element, das der Hand folgt | geteilt (Mac) |
| `36_facetrack.py` + `facetrack.swift` | Gesichtserkennung (Vision) → geglättetes `face.js`: `MV.faceAt(t)` für die Galerie-Bewegungen 85 und 86 (`references/moves.md` 3d) | geteilt (Mac) |
| `37_env.py` | Lautstärke seiner Stimme pro Frame → `env.js` (`window.ENV`): `MV.env(t)` für eine Welle/einen Puls, der sich mit seiner echten Rede bewegt (`references/moves.md` 3e) | geteilt |
| `22b_hook_center.py` | Zoommitte des Hooks = sein Gesicht → `theme.hookCenter` | die leichte (Mac) |
| `30_demo.js` | Kino-Demo: Bildschirmaufnahme/Website-Aufnahmen in einem Handy-/Browserrahmen + Zoom auf einen Punkt + 3D-Neigung + Tippmarkierung + Titel | geteilt |
| `31_device3d.js` + `motion/device3d.html` | echtes 3D-iPhone/MacBook (three.js, Metall, Glas und Schatten) mit derselben `demo.json` | geteilt |
| `32_midframes.py` | Prüfung vor dem Export: ein Frame aus der Mitte jeder Szene → Blätter `mid_N.jpg` | die leichte |
| `25_scopes.py` | Licht- und Farbprüfung → `scopes.json` + Belichtungskorrektur (`grade:"auto"` mit seiner Zustimmung) | geteilt |
| `26_find_shots.py` | Suche nach Bedeutung in Clips (SigLIP2) – `references/find-shots.md` | geteilt |
| `compose.REFERENCE.html` | die Engine: Video · Untertitel · hinter dem Kopf · B-Roll · generiert · Sticker · Schlusskarte | die leichte |
| `compose.EXAMPLES.js` | die Szenen des alten Beispiels zum Lesen – **wird standardmäßig nicht geladen** | — |
| `studio/studio.py` | das Studio – eine Touch-Timeline über denselben Dateien und demselben Renderer (`references/studio.md`) | die leichte |
| `21_avatar_scene.py` | die Avatar-Szene: ein Bild an einem anderen Ort + er spricht mit seiner Stimme (`references/talking-avatar.md`) | fal |
| `22_hook.py` + `hook-card.js` | 🪝 der geschriebene Hook am Anfang jedes Podcast-/Interview-Reels: `suggest` die stärksten Zeilen · `check` Regelprüfer (3–8 Wörter, Spannungsmittel, Zahl aus seinem Text) · `apply` schreibt `theme.json ← hook` und baut die Karte ein · `preview` ein Blatt mit 4 Frames · `overlay` eine transparente Ebene `hook.mov` (oder eingebrannt über eine mp4) für ein Reel, das nicht von unseren Engines kommt – die Interview-Linie in DaVinci (`references/podcast-hook.md`) | geteilt |
| `moves-compose.js` | 🎞️ lässt die Galerie-Bewegungen (`motion/moves.js` → `FX`) im Sprech-Reel laufen: `MV` = Text- und Zeitwerkzeuge (aus `caps.json`) und das Theme über dem Canvas von compose · `MV.video` · `MV.panel` · `MV.hideCaption` · `MV.scene` · `MV.ready` (`references/moves.md` §3) | die leichte |

## Dateien des Arbeitsordners
`src.mov` · `spec.json` (Folge → Reel) · `a.json` (Whisper) · `fixes.json` · `cut.json` · `caps.json` · `theme.json` · `studio.json` · `sfx.json` · `behind.json` · `safe.json` (optional) · `hook-card.js` + `hook_sheet.jpg` (der Hook) · `vfr/` (Quellframes) · `out/` (gerenderte Frames) · `prev/` (Vorschau) · `ad-final.mp4` · `ad-master.mp4/.srt/.txt`.
**Sichere `caps.json` und `cut.json`** – jede spätere Änderung braucht dann keine neue Transkription.

<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Upgrades der Podcast-Linie – Vergleich mit SupoClip (28. September 2026)

Die Quelle: zwei Fassungen von SupoClip („offene Alternative zu OpusClip“) – `github.com/cspenn/supoclip` (ein Python, Mac, lokale Transkription) und `github.com/3oconnects/supoclip` (Docker + React + FastAPI, Cloud-Transkription).
Den Code selbst gelesen (flache Kopien), nicht nur die README.

## Was an ihnen wirklich gut ist
| Die Idee | Wo | Warum sie uns interessiert |
|---|---|---|
| **Viralitätsbewertung 4×25** (Stärke des Hooks · Interaktion · Wert · Teilbarkeit) + **Hook-Typ** (Frage · kühne Aussage · Zahl · Geschichte · Widerspruch) | `3oc backend/src/ai.py` | eine einheitliche Sprache, um Vorschläge zu ordnen, statt „ich fand ihn stark“ |
| **Regeln zur Texttreue**: bestehende Abschnitte wählen, nicht umschreiben, ein zusammenhängender Abschnitt, „beginne so spät wie möglich, solange der Hook bleibt, und ende, sobald die Lösung fertig ist“, und widerspricht Viralität der Genauigkeit → Genauigkeit | dieselbe Datei (der Prompt) | derselbe Geist wie unsere Regel „nichts erfinden“, nur klarer geschrieben |
| **Den Beginn des Abschnitts an Szenenschnitte kleben** (ffmpeg `scene`) | `cspenn src/pipeline/quality.py` | geschnittene YouTube-Folgen mit Kameras – ein Beginn 3 Frames vor dem Schnitt wirkt falsch |
| **Filter für dunkle Abschnitte** (mittlere Helligkeit) | dieselbe Datei | billig, verhindert ein Reel aus einer schwarzen Einstellung |
| **Urteil eines Bildmodells**: wer spricht in einer Einstellung nebeneinander · Umordnen per Bild · den schönsten Frame fürs Cover wählen | `cspenn src/pipeline/vision.py` | die Idee von Cover und Sprecher ist gut; ihre Umsetzung ist eine Vermutung eines Bildmodells |
| **B-Roll-Gelegenheit mit einem Suchwort** aus dem Text + Abruf von Pexels | `3oc backend/src/broll.py` | eine kostenlose Option für Einstellungen statt bezahlter Generierung |
| **Untertitelvorlagen mit Namen** (hormozi · mrbeast · tiktok …) + Editor für Schneiden/Teilen/Zusammenführen + Exporteinstellungen je Plattform | `3oc caption_templates.py` · `clip_editor.py` | Nutzererlebnis: eine Form per Namen wählen |
| **Aufgabenprotokoll** (jede Folge mit Status und Reels) | beide | „Folge → Reels“ braucht eine Statusübersicht |

**Was sie nicht haben (am Code geprüft):** Keines von beiden schreibt einen Hook auf den Bildschirm. Bei cspenn erscheint `title` nur in der Oberfläche der Website, bei 3oc sind `hook_score`/`hook_type` nur Zahlen in der Datenbank. ⇒ Den geschriebenen Hook (Wunsch des Nutzers vom 28. September) haben wir von Grund auf gebaut.

## Was wir von ihnen übernommen haben (v3.8)
1. **Die Hook-Typen** wurden zu den „Spannungsmitteln“ in `22_hook.py` (Zahl · Widerspruch · Frage · Neugier · Befehl · Geschichte) – jeder Hook braucht eines, am stärksten zwei.
2. **Das Prinzip der Texttreue** wurde zu einer automatischen Prüfung: Jede Zahl im Hook muss in der Rede des Clips vorkommen (als Ziffer oder ausgeschrieben), und der Hook wird nicht zu seinem ersten Satz.
3. **Das Ordnen der Zeilen** (`22_hook.py suggest`): eine deterministische Fassung ohne Modell der Hook-Bewertung – sie gibt Claude die stärksten 8 Zeilen, aus denen es schreibt, statt den ganzen Clip zu lesen.
4. **Der geschriebene Hook selbst** (`hook-card.js`): die ersten 1,5–3 s, lesbar vom ersten Frame, Theme-Farben, innerhalb der sicheren Zone. Details: `references/podcast-hook.md`.
   - **Wo er läuft (v3.8.1, an Frames erprobt):** Folge → Reel (`compose.html` in allen Modi: Voll · `R_DOWN` · `R_OFF` · `sceneFx:false`) · Kameras (`compose.PODCAST.html`: FULL · SPLIT auf der Trennlinie · QUOTE schaltet die große Frage in seiner Zeit ab · HEAD oben auf dem Papier und schaltet die Collage ab) · **die Interview-Linie in DaVinci/Lottie** und jede fertige mp4: `22_hook.py overlay` erzeugt eine transparente Ebene `hook.mov` (oder brennt sie über das Reel).
   - **Bekannte Grenze:** Über einer fertigen mp4 lassen sich eingebrannte Untertitel nicht entfernen – der Hook wird `mid` zwischen Gesicht und Untertitel gesetzt, aber beide Texte erscheinen in den ersten 3 s zusammen. Die richtige Lösung in DaVinci: die Ebene auf der obersten Spur, und der erste Untertitel verzögert sich, bis der Hook weg ist.

## Was wir besser machen als sie
| Bei uns | Bei ihnen |
|---|---|
| Whisper large-v3-turbo auf der Mac-Grafik, in 20-s-Stücken an Pausen + ein Halluzinationswächter („Abonniert den Kanal“) | cspenn: parakeet-tdt-0.6b-v2 (**nur Englisch**) · 3oc: AssemblyAI in der Cloud (API-Schlüssel, und der Ton verlässt das Gerät) |
| Der Schnitt am **ruhigsten Punkt zwischen zwei Wörtern** + eine zweite Transkription für jedes Stück + `19_seam_check` für jede Naht | Die Grenzen schreibt das Modell selbst: 3oc im Format MM:SS (ganze Sekunde Genauigkeit – `ai.py:50`) · cspenn im Format MM:SS.mmm (`analyze.py:199`), aber ohne Anheften an die Wortzeiten („künftig“ – `analyze.py:582`) ← ein Beginn mitten im Wort kommt bei beiden vor |
| Der gesprochene Hook **aus der Mitte der Rede**, dann die Frage, dann die Antwort (nicht zusammenhängende Schnitte) | ein zusammenhängender Abschnitt ist Pflicht |
| Hochformat-Beschnitt um das Gesicht **für jede Einstellung** (Vision von Apple) + mehrere Kameras mit Tonsynchronisation und dem Sprecher aus der Mundbewegung | MediaPipe (oder OpenCV Haar) an einer Stichprobe von ~10 Frames pro Abschnitt / die Vermutung eines Bildmodells links-rechts |
| Eine Zeichen-Engine: Untertitel mit Wortzeit und Hervorhebung, Motion aus dem Sinn des Satzes, hinter der Person, Modi Karte/Voll/ohne Gesicht | ASS-Untertitel, per ffmpeg eingebrannt (und braucht einen ffmpeg-Build mit Sonderausstattung) |
| Automatische Prüfung der sicheren Zone · Lautheit –14 LUFS · Weiterrendern per Fingerabdruck · die Identität von der Person selbst | nichts davon |

## Die kommenden Ergänzungen – nach Priorität
(Die Schätzung = Arbeit von Claude in einer Sitzung, ungefähr)

| # | Die Ergänzung | Warum | Aufwand |
|---|---|---|---|
| 1 | **`23_rank_clips.py` – ein Vorfilter für Vorschläge vor dem Lesen**: Fenster von 20–60 s auf `words.json` mit Bewertung (Spannungsmittel + Zahlendichte + eigenständiger Beginn + ohne „wie gesagt“) → die stärksten 15 Fenster, und Claude liest nur diese und schreibt für jedes eine Bewertung 4×25 + Hook-Typ + 3 Hooks, die `check` bestehen | Eine einstündige Folge = 10.000 Wörter; sie ganz zu lesen ist der teuerste Schritt bei den Token | 3–4 Stunden |
| 2 | **Ein Befehl pro Reel** (`episode_reel.sh <work>`): 20 → 02 → Hook → 03 → 04 → 05 → 06 → 06b → 08 → 19, und schreibt eine Statuszeile in `episode/status.json` (Tabelle: Reel · Hook · Dauer · LUFS · Nähte) | ihr „Aufgabenprotokoll“; heute sind die Schritte manuell, und man vergisst einen (ist passiert) | ein halber Tag |
| 3 | **Reel-Cover aus dem Hook**: der schönste Frame des Clips (Augen offen + hohe Schärfe aus Vision/Laplace) + dasselbe `hook-card.js` → `cover.jpg` | dieselbe Idee des Covers wie bei ihnen, ohne Bildmodell | 3 Stunden |
| 4 | **Den Beginn an Szenenschnitte kleben** in `20_episode_cuts.py`: Liegt ein Kameraschnitt innerhalb von 0,3 s nach dem Beginn des Stücks, verschiebt sich der Beginn dorthin (sofern er nicht in ein Wort greift) | geschnittene YouTube-Folgen | 1–2 Stunden |
| 5 | **Der Sprecher in einer einzigen weiten Einstellung** (zwei Personen in einem Bild): Erkennung beider Gesichter + Mundbewegung jedes einzelnen (gibt es in 15 für getrennte Kameras) → der Beschnitt geht zum Sprecher, und im schnellen Dialog geteilt oben/unten | Die meisten YouTube-Podcasts sind weit gefilmt | 1–2 Tage |
| 6 | **Zwei Hooks zum Testen (A/B)**: dasselbe Reel mit zwei Hooks – sie unterscheiden sich nur in den ersten 3 s (`range` rendert 90 Frames) – und sie gehen in die Test-Reels | So erfahren wir in Zahlen, welche Hook-Formel bei seinem Publikum funktioniert | 2 Stunden |
| 7 | **Filter für dunkle/verwackelte Einstellungen** vor den Vorschlägen | billig | 1 Stunde |
| 8 | **Kostenlose B-Roll von Pexels** mit einem Wort aus dem Text (optional, ein kostenloser Schlüssel vom Nutzer) neben der bezahlten Generierung | eine kostenlose Alternative | ein halber Tag |
| 9 | **Ein „Einfrieren“-Modus für den Hook**: die ersten 0,6 s ein gedimmter Standframe mit riesigem Hook, bevor der Ton beginnt | wenn der Nutzer ihn stärker will – aber eine Stille am Reel-Anfang senkt die Bindung; teste ihn zuerst im A/B | ein halber Tag |

**Wir raten ab von:** Untertitelvorlagen mit Namen von Personen (bei uns kommt die Identität von der Person selbst) · fertigen Übergangsclips vor jedem Reel (der Hook verspätet sich) · den Hook mit einer generierten Stimme (edge-tts) über die Rede des Gasts zu lesen – eine zweite Stimme verwirrt, und unsere Regel ist, niemandem Worte in den Mund zu legen.

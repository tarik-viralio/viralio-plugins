<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# Querformat-Video → Hochformat-Reel (v3.5)

Interview, Podcast, TV-Folge, jedes Video, das breiter ist als 9:16. **Es gibt keinen Zusatzbefehl:** `03_cut_zoom.py` erkennt, dass das Video quer ist, und schneidet es selbst hochkant. Früher hat es gedehnt (die Gesichter wurden breit).

## Was es tut
1. **Findet die Einstellungsgrenzen** in jedem Abschnitt in `cut.json` (Kamerawechsel) auf den Frame genau.
2. **Findet das Gesicht der größten Person in jeder Einstellung** (Vision-Bibliothek auf dem Mac, derselbe Detektor wie im Podcast-Modus – wird einmal gebaut).
3. **Ein fester Beschnitt pro Einstellung**, der das Gesicht ins obere Drittel setzt wie ein Kameramann: Er folgt dem Gesicht nicht Frame für Frame (das würde zittern).
4. **Eine weite Einstellung** (kleines Gesicht) wird ×1,35 herangezoomt, und **das ganze Studio von weitem** ×1,6.
5. **Einstellung ohne klares Gesicht** → der Beschnitt geht an die Stelle des Sprechers in der Nachbareinstellung.
6. Schreibt `<work>/shots.json`: jede Einstellung mit Reel-Zeit, Art und Beschnitt-Rechteck. Prüf es, wenn eine Einstellung falsch ausfiel.

Das Hochformat-Video läuft genau auf dem alten Weg (getestet: derselbe Fingerabdruck für jeden Frame).

## Sag ihm in einem Satz
„Das Video ist quer – ich habe es für jede Einstellung hochkant um dein Gesicht geschnitten, X Einstellungen.“ Erkläre nicht mehr.

## Grenzen, die du kennst
- **Qualität:** Ein Hochformat-Beschnitt aus 1080p = 608×1080, auf ×1,8 vergrößert. Im Reel akzeptabel, 4K ist schöner.
- **Einstellung mit zwei Personen:** Es nimmt das größere Gesicht (das der Kamera nächste), nicht unbedingt den Sprecher. Ist es falsch, passe `crop` in `shots.json` für diese Einstellung an und wiederhole 03… oder mach die Einstellung zur Karte (`R_DOWN`).
- **Senderrahmen** (Bild im Bild, farbiger Hintergrund um den Sprecher): Der Beschnitt zeigt den Rahmen um ihn herum. Besser den Moment als Karte (`R_DOWN`) und mit einer Grafik darüber zeigen und nur aus dem Inneren des Quadrats schneiden.
- **Windows / ohne Xcode-Tools:** keine Gesichtserkennung → Beschnitt aus der Mitte mit Hinweis.

## Reels aus einem langen Interview – zwei Lehren
- **Der Hook aus der Mitte der Rede:** Stellst du einen Satz aus der Mitte voran, muss der Abschnitt danach **nach** seinem Ende beginnen – sonst wiederholt sich ein halbes Wort an der Naht („Meine… meine“). Prüf jede Naht: Ende eines Abschnitts ≠ im Inneren eines anderen.
- **Schneide nicht in die Rede des Moderators:** Der Anfang des Abschnitts darf das letzte Wort des vorigen nicht fassen. Die Wortgrenzen kommen von Whisper, und gedehnt wird nur bis zur Pause, ohne in das nächste Wort zu geraten.

## Ganze Folge → mehrere Reels (einstündiger Podcast – erprobt am 27. September an einer Folge von 53 Min., 5 Reels)
1. **Lade** die Folge **herunter** (ein aktuelles `yt-dlp` – das alte auf Python 3.9 funktioniert mit YouTube nicht; am Mac `brew install yt-dlp`, und wenn ein neues Python sich über `python3` legt, löse es mit `brew unlink python@3.x`).
2. **Transkribiere sie ganz** mit `18_long_transcribe.py` (10 Minuten für eine Stunde am Mac). ⛔ Transkribiere die lange Datei nicht auf einmal – Whisper verschluckt Minuten und erfindet „Abonniert den Kanal“. ⛔ Das Modell small ist für Dialekte ungenau.
3. **Lies den ganzen Text und zeig eine Liste**: für jedes Reel (Anfang, Thema, 3 Hooks aus seinen eigenen Worten, warum es sich lohnt) – er wählt, baue nicht mehr als 6, bevor er gewählt hat. Das erste Reel lässt du freigeben, bevor die anderen kommen.
4. **Die Schnitte nach Wörtern** → `<work>/spec.json`: `{"segments":[[Beginn_erstes_Wort, Beginn_letztes_Wort], …]}` in Sekunden der Folge (aus `transcript.txt`). Der Hook ist ein erstes Stück aus der Mitte der Rede (3–12 s), der Rest in seiner Reihenfolge. **Die Stücke überlappen sich nicht** außer dem Hook (sein Satz wiederholt sich ganz normal in der Antwort).
5. **`20_episode_cuts.py <work> <Folge> <words.json>`** – setzt jede Grenze an den ruhigsten Punkt zwischen einem Wort und seinem Nachbarn (greift nicht in ein Nachbarwort), transkribiert jedes Stück einzeln (genauer) und schreibt `cut.json` + `a.json` (jeder Satz trägt die Nummer seines Stücks `seg`) + eine Vorlage `fixes.json` + `src.mov` (Link zur Folge).
   Korrigiere `fixes.json` (gleiche Wortzahl · `""` entfernt ein Wort aus den Untertiteln, der Ton bleibt · **ein Text** statt der Liste, wenn Whisper halluziniert hat – er wird nach der Länge verteilt) → `02_captions.py`.
6. `03_cut_zoom.py` schneidet sie hochkant → **🪝 geschriebener Hook (Pflicht für jedes Folgen-Reel):** `22_hook.py suggest` → schreib 3 Hooks → `check` → `apply` → `preview` (`references/podcast-hook.md`) → die Szenen → `theme.json`: `hookZoom` (= Länge des ersten Stücks) + **`outro` für die Folge** (der Standard ist die Anzeige des Skills!) · `sfx.json`: `soft` für das Whoosh → Rendern → 06b (und liegt es unter –14,5: `06c_loudfix.sh`).
7. **`19_seam_check.py` ist Pflicht** – es ist beim ersten Versuch zweimal von fünf durchgefallen und wäre sonst in die Veröffentlichung gegangen.

**Erprobte Fallen:**
- Die Wortzeiten einer Folgen-Transkription driften bis zu einer halben Sekunde ← Reste von Rede vor dem ersten Wort („also du äh“). Die Lösung: Setze den Beginn von Hand auf die Pause, nachdem du den Pegel darum gesehen hast.
- Ein wiederholtes Wort an der Naht kann von ihm selbst in der Folge stammen („und ich gewinne nicht… und ich gewinne nicht“) – prüf an der Quelle; wird das Ende des Hooks dadurch schwach, kürze es.
- **Eingebrannter Text im Originalvideo** (Dank an einen Sponsor, der Name des Gasts) in bestimmten Einstellungen: Der Hochformat-Beschnitt schneidet seinen Rand ab. Verschiebe den Beschnitt für diese Einstellung weg (`crop` in `shots.json`).
- 04 bricht manchmal mit einem Netzwerkfehler mitten im Rendern ab. Seit v3.5 löscht es die alten Frames, sobald sich das Design ändert oder mit `--force` (Fingerabdruck in `out/.design.sha1`), also starte es nach dem Absturz noch einmal **ohne** `--force`, und es ergänzt nur das Fehlende.
- Zahlentafel (`from` ≠ `at`): Lass das Zählen beim Erscheinen der Tafel beginnen, sonst ist sie sekundenlang leer.
- Ein Rechner, der von einer anderen Sitzung beim Rendern belegt ist = alles ×2–3 langsamer – starte nicht Transkription und Rendern gleichzeitig.

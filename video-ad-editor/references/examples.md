<!-- Referenz für den Skill video-ad-editor / motion-video – Beispiele aus den Prompts anderer (Inspiration, kein Kopieren) -->

# Motion-Beispiele von anderen

Die ursprüngliche Quelle: [awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) – 513 Videos mit dem Prompt, den ihr Autor benutzt hat (Stand 2026-10-08). Die Sammlung steht unter MIT-Lizenz, aber **jeder Prompt gehört seinem Autor** – deshalb steht hier eine Zusammenfassung der Ideen und Techniken mit dem Link ihres Autors, **keine Kopie des Textes**.

## So nutzt du sie
- **Für Inspiration und zur Prüfung:** Bevor du einen Film baust, lies das Beispiel, das deiner Idee am nächsten ist, und sieh, welche Technik ihn „professionell“ macht.
- **Es gibt keine Vorlagen.** Nimm die Technik und baue deine Bewegung aus dem Sinn des Skripts.
- **Nicht jedes Beispiel passt zu jedem Film:** Der One-Take ist für Oberflächen und Ideen, nicht für lange Rede.
- **Was wir nicht haben:** KI-Generierung von Bildern/Videos (Higgsfield ist gestrichen) und Bewegungsunschärfe als Mittel von Subframes. Setz sie nicht voraus.

## Gemeinsame Muster der besten Prompts
1. **Eine Struktur aus Tags:** `<inputs>` (frag zuerst nach dem Material) → `<direction>` (der Stil + die Verbote) → `<structure>` (was bei jedem Schlag passiert) → `<build>`/`<export>` (visuelle Prüfung, dann Rendern).
2. **Ausdrückliche Verbote** sind stärker als positive Beschreibungen.
3. **Rhythmus nach Schlägen** (120 BPM): Es gibt keine tote Zeit.
4. **Ein Vorschauframe für jeden Schlag** vor dem Rendern.
5. **Jede Zahl echt,** und kein generierter Text in Bildern.

---

### 1 – Eine Form, die sich in jede Oberfläche verwandelt
**Art:** One-Take

**Die Idee:** Ein Knopf wird zu einem Lader, dann einem Häkchen, dann der Dynamic Island, dann einem Musikplayer, dann einem Schalter, dann einem Diagramm, dann ⌘K, dann einer Benachrichtigung, und kehrt zum Knopf zurück. 7 Takte bei 120 BPM.

**Was wir daraus lernen:**
- Bei jedem Schlag passiert etwas, es gibt keine tote Zeit.
- Der Inhalt wechselt mit einer kurzen Unschärfe, und der Cursor macht jede Änderung mit echten Klicks und Ziehen.
- Letzter Frame = erster Frame, also eine Schleife.
- Er verlangte vom Nutzer 8–12 Oberflächenzustände und einen Song von ~120 BPM, bevor er begann.

**Bei uns:** `motion/examples/one-take/` setzt dieselbe Idee um. Lies `references/one-take.md`.

Quelle: @twoclipping — https://x.com/twoclipping/status/2103273003555402193

### 2 – Ein Canvas und eine Zeichenfunktion
**Art:** One-Take

**Die Idee:** Eine HTML-Datei, ein Canvas, eine Funktion `draw(t)`. Eine Form, die nie verschwindet: Jeder Zustand ist dasselbe Element, dessen Größe, Rundung und Farbe sich ändern.

**Was wir daraus lernen:**
- Keine CSS-Transitions, keine Timer und kein Zustand, der zwischen Frames wandert – jeder Frame wird nur aus der Zeit berechnet.
- Eine geschlossene Feder für jeden Wert, und ändert ein Wert mehrfach sein Ziel, summierst du eine Feder pro Änderung.
- Der Inhalt kommt herein, nachdem der Container begonnen hat, sich zu verwandeln, und geht vor der nächsten Verwandlung – Text überlagert sich nicht.
- Verwandle Schwarz nicht direkt in die Identitätsfarbe: Bewege das Farbelement zwischen den Zuständen.
- Der Tab-Indikator dehnt sich, weil jede Kante auf einer anderen Feder liegt.
- Vor dem finalen Rendern: ein Frame pro Schlag auf einem Vorschaublatt, und behebe, was gedrängt ist.
- Export: 60 Frames, Mittel aus 6 Subframes für Bewegungsunschärfe, und in allen Formaten (1:1, 16:9, 9:16) parallel.

**Bei uns:** Unsere Engine arbeitet nach demselben Prinzip (`draw(t)` deterministisch). Das Mittel der Subframes haben wir nicht.

Quelle: @verbove — https://x.com/verbove/status/2103483957266268381

### 3 – Jede Szene wächst aus der vorigen (Keynote)
**Art:** One-Take

**Die Idee:** Ein Launchfilm im Stil einer Apple-Keynote, eine Einstellung. Jede Szene ist aus der vorigen gemacht: kein Blenden, keine Unschärfe, kein Schnitt.

**Was wir daraus lernen:**
- Dinge ändern ihre Form, statt zu verschwinden: Text kommt aus einer Maskenlinie, Icons explodieren auf einer Feder, Balken zeichnen sich, Seiten schieben sich hinein.
- Eine schwarze Form flutet den ganzen Rahmen und schrumpft zu einer neuen Szene.
- Die Kamera zoomt im Stil von Screen Studio, sodass jeder Moment das Quadrat füllt, und der Cursor wächst mit.
- Eine ausdrückliche Verbotsliste: Crossfade, Eintrittsunschärfe, 3D-Flip, Partikel, Glow, länger als eine Sekunde stehen, alles, was nach Vorlage aussieht.
- 54 Schläge bei 120 BPM, und bei jedem Schlag passiert etwas.
- Er fragt zuerst nach: dem Markennamen in einem Wort, 9–12 hochwertigen Bildern, einem Song von ~120 BPM mit Drops und Ruhe.

**Bei uns:** Wir können diese Form mit unserer Engine bauen. Hast du keine Bilder, frag den Nutzer nur nach dem, was du nicht beschaffen kannst.

Quelle: @twoclipping — https://x.com/twoclipping/status/2103835273813496100

### 4 – Die Kugel, die sich in jede Oberfläche verwandelt
**Art:** One-Take

**Die Idee:** Eine gestaltete Pokédex-Oberfläche: eine Kugel (der mittlere Knopf, die Linie, die Schale) verwandelt sich in die Elemente jedes Zustands. 28 Schläge ≈ 14 Sekunden, und am Ende kehrt es zur Kugel zurück.

**Was wir daraus lernen:**
- Die Elemente der ursprünglichen Form (Knopf, Linie, Rahmen) sind selbst die Bedienelemente – die Verwandlung hat also Logik.
- Inhaltswechsel mit kurzer Unschärfe, mit getrennter Eintritts- und Austrittszeit.
- Die Kamera rahmt weich neu ein, und die Oberfläche bleibt groß und lesbar.
- Verboten: übertriebenes Bounce, Partikel, Glow, Verläufe auf Oberflächenelementen, Icons mit unterschiedlicher Strichstärke, tote Zeit.

**Bei uns:** Das Prinzip passt auf jede Identität: Wähle eine Form aus deiner Geschichte (Logo, Buchstabe) und lass sie sich in die Bildschirmelemente verwandeln.

Quelle: @TheGrootDev — https://x.com/TheGrootDev/status/2103516567824966114

### 5 – Endloser Zoom zwischen den Welten
**Art:** One-Take (Schleife)

**Die Idee:** Die Kamera fliegt von einer Landschaft zur nächsten durch alte Dinge (Taschenuhr, Linse, Lupe, Spiegel) und kehrt zum Anfang zurück.

**Was wir daraus lernen:**
- Das Glas jedes Tors trägt die nächste Welt, und es schneidet weich, wenn es den Rahmen füllt.
- Konstante Geschwindigkeit: ein exponentieller Zoom, und die Dauer jedes Abschnitts verhält sich proportional zum Logarithmus des Zooms.
- Jede Landschaft hat 3 Tiefenebenen mit Parallaxe: Maßstab der Ebene = Kamera^Z.
- Die Schnipsel bewegen sich mit 15 Frames (on twos), damit sie handgemacht wirken.
- 20 Sekunden Schleife, und die Musik mit genau 96 BPM: 8 Takte ergeben 20 s.

**Bei uns:** Er nutzt KI-Bildgenerierung (Magnific). Wir können es mit einem Canvas und den echten Bildern des Nutzers bauen, müssen die Bilder aber vorher prüfen.

Quelle: @koldo2k — https://x.com/koldo2k/status/2103129343253778767

### 6 – Eleganz durch Einfachheit: eine Idee pro Einstellung
**Art:** Produktanzeige

**Die Idee:** 10 Takte bei 120 BPM, jeder Takt zwei Sekunden: Der Hook kommt Wort für Wort auf den Schlägen, ein Wort verwandelt sich in die Produktoberfläche, und der Cursor tippt und klickt.

**Was wir daraus lernen:**
- Eine Idee pro Einstellung, viel Leerraum, eine Farbe, eine Schrift mit engem Abstand.
- Textenthüllung mit Maske, Match-Cut, eine einzige Kamerasprache.
- Nur echte Aufnahmen, keine Platzhalterkarten.
- Kein Punkt am Ende von Text auf dem Bildschirm.
- Verboten: Schockwellenringe, Partikelexplosion, RGB-Trennung, Kamerawackeln, Neon-Glow, Rasterboden.

**Bei uns:** Das passt zu unserer Regel „keine Zahl und kein Name außerhalb von facts.md“. Echte Aufnahmen: aus der Bildschirmaufnahme des Nutzers.

Quelle: @twoclipping — https://x.com/twoclipping/status/2102554209166000267

### 7 – Von einem Punkt zu einem ganzen System
**Art:** Motion/Launch

**Die Idee:** Es beginnt mit einem einzigen Punkt auf einem schwarzen Bildschirm, Fenster erscheinen (Gebühren, Zentren, eine Kette von Optionen, eine Watchlist), zoomt hinein und hinaus in verschiedenen Maßstäben, dann zieht die Kamera zurück, bis der Computer ein Punkt im Raum ist, und zoomt wieder hinein und enthüllt einen Handybildschirm.

**Was wir daraus lernen:**
- Eine Geschichte im Maßstab: vom Kleinen zum Großen zum Kleinen. Die Kamera ist der Erzähler.
- Ein Ende mit einem einzigen Satz: „Trading mit einem Bildschirm.“

**Bei uns:** Eine Idee, die für die Anzeige einer App mit Desktop- und Handyversion taugt.

Quelle: @dale_vaz — https://x.com/dale_vaz/status/2103290592679879074

### 8 – Eine Erklärung von 60 Sekunden ohne Aufsicht
**Art:** Erklärung

**Die Idee:** Die Reise eines Photons aus dem Kern der Sonne. Erzählstil, das Photon hat eine Persönlichkeit, alles Code Frame für Frame.

**Was wir daraus lernen:**
- Eine echte Simulation: Der Random Walk ist ein tatsächlicher Random Walk, keine Zeichnung.
- Echte Zahlen (Temperatur, Entfernung, Zeit) mit Ehrlichkeit über die Unsicherheit.
- Humor und Callbacks für die Aufmerksamkeit, und zeitliche Parallelität zu Ereignissen auf der Erde.
- Eine starke visuelle Idee für jede Szene und ein schlüssiges Designsystem.
- Er sagt dem Agenten: Arbeite für dich und sag mir am Ende, was du entschieden hast.

**Bei uns:** Unsere Regel: Jede Zahl aus facts.md, und normale Ziffern.

Quelle: @AstroTheWizard — https://x.com/AstroTheWizard/status/2103629247751618782

### 9 – „Ein Blick in die App“
**Art:** App-Anzeige

**Die Idee:** Ein Hochformat-Video von 45–50 Sekunden: Jede Funktion wird aus einer echten Aufnahme im Simulator gezeigt, kommt aus dem Handy heraus und verändert die Welt um sich.

**Was wir daraus lernen:**
- Echt, nicht gefälscht: Jede Zahl und jeder Titel auf dem Bildschirm stammt aus den Aufnahmen.
- Jede Funktion mindestens 2,5 Sekunden, damit der Zuschauer mitkommt.
- Der Text bleibt weg von der Oberfläche von TikTok und Instagram.
- Keine fertigen Soundeffekte (der Nutzer fügt die Musik hinzu).

**Bei uns:** Dieselben Regeln: sichere Zone, und der Ton kommt vom Nutzer.

Quelle: @Bilimfili1 — https://x.com/Bilimfili1/status/2103743617848459762

### 10 – Eine Geschichte ohne Worte
**Art:** Erklärung/Erzählung

**Die Idee:** Origami und Doodle: die Entwicklung der Menschheit von der Geburt bis zur künstlichen Intelligenz. Poetisch und bewegend.

**Was wir daraus lernen:**
- Fast ohne gesprochene Sprache: einfacher Text, den jede Kultur versteht.
- Ein einheitlicher Zeichenstil (warmer Doodle) bricht den Look eines „KI-Videos“.

**Bei uns:** Für menschliche Geschichten. Halte die Wörter wenige und kurz.

Quelle: @songkeys — https://x.com/songkeys/status/2102743212922384673

### 11 – Das Gerüst einer 30-Sekunden-Erklärung
**Art:** einfache Erklärung

**Die Idee:** 5 Szenen: das Problem des Kunden, was ich tue, wie es in 3 Schritten funktioniert, ein Beweis, und mein Name am Ende.

**Was wir daraus lernen:**
- Das Gerüst ist nützlich als Ausgangspunkt für das Skript, nicht als Vorlage für die Bewegung. Die Bewegung wird aus dem Sinn jedes Satzes gebaut.

**Bei uns:** Wir nutzen es nicht als Bewegungsvorlage.

Quelle: @alex_prompter — https://x.com/alex_prompter/status/2103499977632997524

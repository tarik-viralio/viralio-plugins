# Motion-Paket `motion-kit.js` – Shorts-Niveau innerhalb deiner Identität (v3.6)

**Warum:** Nach einer Szene mit Zahlenbeleg in einem Reel (27. September 2026) sagte der Nutzer: „Jaaa, genau das wollte ich schon lange … ich will diese dynamische Bewegung, egal ob ich spreche und in der Bildmitte bin, oder als kleine Karte unten, oder wenn ich verschwinde … ich will grenzenlose Kreativität.“
Das Paket = fertige Bausteine in hoher Qualität, die auf **derselben Engine und denselben Modi** laufen (R_DOWN · R_LOWER · R_OFF) – keine parallele Engine.

## Laden
```bash
cp scripts/motion-kit.js <work>/
```
Und in `compose.html` unter dem Engine-Skript und vor dem Skript deiner Szenen: `<script src="motion-kit.js"></script>`
(6.1) Die Engine stellt `X`, die Theme-Farben und ihre Schrift selbst auf `window` bereit – vorher brach `MK.*` ab („reading 'save'“), bis du in deiner Szene eine `defineProperty`-Zeile ergänzt hast. Du brauchst sie jetzt nicht mehr.

## Die Boxen je Modus
| Modus | Die Box `box` | Hinweis |
|---|---|---|
| `R_DOWN` (du in der Mitte) | in `panelIn(t,s,e,()=>…)`: `{x:130,y:278,w:820,h:180}` | wird automatisch um 1,2 vergrößert – ein einziger einfacher Baustein (Kinetik, Stempel, Kommentarfeld, kleiner Zähler) |
| `R_LOWER` (kleine Karte unten) | `{x:60,y:170,w:960,h:1150}` | die große Fläche: Kartenraster, Timeline, Balkenvergleich |
| `R_OFF` (ohne dich) | `{x:60,y:170,w:960,h:1400}` | der ganze Bildschirm: `techFrame` + riesiger Zähler + Kurve + Karten |
| `R_FULL` (Vollbild) | direkt über dem Video | nur `stamp` oder ein kurzes `kinetic` – decke das Gesicht nicht ab |

## Die Bausteine
| Die Funktion | Was sie zeichnet | Wichtigste Optionen |
|---|---|---|
| `MK.odometer(t,o)` | eine Zahl mit Walzen, die läuft und einschlägt + Punkteexplosion | `s, dur, val, cx, cy, size, prefix, suffix, slam` |
| `MK.shake(t,s)` | Versatz der Erschütterung im Moment des Einschlags `[dx,dy]` | wickle deine Zeichnung in `X.translate(dx,dy)` |
| `MK.burst(t,o)` | Punkteexplosion von einem Punkt | `s, cx, cy, spread` |
| `MK.statCard(t,o)` | eine Karte, die mit Feder aufpoppt und ihre Zahl zählt + eine kleine Grafik | `label, val, format:'k'\|'comma', prefix, bg, ink, viz:'ring'\|'bars'\|'avatars'\|'bubbles'\|'spark'` |
| `MK.statGrid(t,o)` | eine große Karte + 4 kleine nacheinander | `hero:{…}, cards:[…]` |
| `MK.lineChart(t,o)` | eine Kurve, die sich zeichnet + Füllung + ein pulsierender Punkt | `points:[0..1]\|'hockey'\|'steady', max:'1M'` |
| `MK.compareBars(t,o)` | Vergleichsbalken (vorher/nachher) mit ihren Zahlen | `items:[{l,v,u,hot}]` |
| `MK.kinetic(t,o)` | Wörter, die aus einer Maske kommen (oder einschlagen) | `words, hot:[i], mode:'rise'\|'slam', times:[…], underline` |
| `MK.techFrame(t,o)` | technischer Rahmen: Ecken + Timecode + Lineal | `title, sub` |
| `MK.timeline(t,o)` | Schnitt-Timeline + Rauten + Abspielkopf + „Render“-Knopf | `steps:[…], clickAt` |
| `MK.commentBox(t,o)` | ein Kommentarfeld, das sich selbst schreibt + ein pulsierendes Senden | `text, cps` |
| `MK.stamp(t,o)` | ein Doppelstempel, der schief aufschlägt + Welle | `text, cx, cy, rot` |
| `MK.iconArray(t,o)` | ein Raster von Personen-Icons „X von je N“, das sich füllt, und die Markierten färben sich | `total, hot, cols, hotAt, pick` |

Jeder Baustein: `o.s` Beginn (binde ihn an das Wort: `wordsOf(i)[j].s`), und `o.e` optionales Ende: ein ruhiger Ausgang von 0,4 s, der dort endet (6.1) – **setz es auf letztes Wort + 0,45**, nicht auf das nackte letzte Wort (`motion-rules.md` §3).

## Beispiel – der Satz „Ein Reel brachte fast eine Million Aufrufe“ im Modus R_OFF
```html
<script src="motion-kit.js"></script>
<script>
SCENES=[{s:0,e:3.2,m:R_FULL},{s:3.2,e:8.6,m:R_OFF,nocap:true},{s:8.6,e:99,m:R_FULL}];
function viewsScene(t){ if(t<3.2||t>8.6) return; const w=wordsOf(1), hit=w[3].s;      // „Million“
  MK.techFrame(t,{s:3.2,e:8.6,title:'Reel-Statistik'});
  const [dx,dy]=MK.shake(t,hit+1.4); X.save(); X.translate(dx,dy);
  MK.odometer(t,{s:hit-0.5,dur:1.9,val:963007,cx:540,cy:640,size:170,e:8.6});
  MK.lineChart(t,{s:hit+1.2,dur:1.2,box:{x:110,y:780,w:860,h:420},max:'1M',e:8.6}); X.restore(); }
SCENE_LIST.push(['viewsScene',viewsScene]);
</script>
```
`8.6` ist hier = letztes Wort des Satzes + 0,45 – die Bausteine bleiben nach seiner Stimme und gehen ruhig, und die Szene kehrt danach ins Vollbild zurück.
Und in `sfx.json`: `"counter":[[Beginn, 1.9]]` (Ticks, die mit dem Zähler schneller und weiter auseinander werden) + `"thud":[Moment des Einschlags]` + `"tap":[Momente, in denen die Karten aufpoppen]`.

## ⛔ Das Paket ist eine Grundlage, keine Vorlage (Anweisung des Nutzers, 27. September)
„Ich will nicht auf die Bewegungen beschränkt sein, die du hinzugefügt hast, sodass sie sich wiederholen … du kennst dich mit Motion Graphics und Infografik aus und entscheidest, was die Szene braucht.“
Die Bausteine oben sind fertiges Vokabular. **Jeder Satz wird aus seinem Sinn gestaltet** – baue auf dem Baustein auf, brich ihn auf oder zeichne etwas ganz Neues mit dem Canvas. Dieselbe Szene in zwei Videos ist verboten.

### Entscheidungstabelle: Art der Information → Form
| Er sagt | Art der Information | Infografik-Form (Beispiele – keine Liste) |
|---|---|---|
| „4 von 100 erkranken“ | Teil vom Ganzen | ein Raster aus 100 Icons, 4 leuchten (`iconArray`) · 100 Punkte zerstreuen sich und 4 sammeln sich |
| „fast die Hälfte“ / 38 % | Anteil | ein Donut, der sich füllt · ein Becher, der sich bis zur Linie füllt · ein Balken, der aufbricht |
| „stieg / fiel“ | Richtung | eine Kurve, die sich zeichnet · ein Pfeil, der steigt und bricht · eine Treppe, die aufsteigt |
| „mehr als / weniger“ | Vergleich | zwei Balken · die Schalen einer Waage · zwei Kreise in zwei Größen |
| „der Erste, der Zweite …“ | Rangfolge | ein Balkenrennen · ein Siegerpodest · eine Liste, die kippt |
| „aufnehmen → hochladen → veröffentlichen“ | Prozess | eine Zeitleiste mit Schritten · Pfeile nacheinander · eine Timeline |
| „in 3 Sekunden / jeden Tag“ | Zeit | eine Uhr, die sich dreht · ein Countdown · ein Kalender, der umblättert |
| „in Deutschland / Europa“ | Ort | eine vereinfachte Karte mit fallender Nadel · Wellen von einem Punkt |
| „100 Euro / eine Million“ | Geld | Münzen, die sich stapeln · eine Rechnung, die sich druckt · eine Zahl, die einschlägt |
| „weil / also“ | Ursache und Wirkung | Domino, der fällt · ein Zahnrad, das ein Zahnrad dreht · eine Kette, die bricht |
| „Fehler / Störung“ | Problem | Glitch + Risse · ein ✕, das einschlägt · ein Bildschirm, der schwarz wird |
| Zitat / starker Satz | Botschaft | kinetische Typografie · ein Wort, das sich dehnt · Text hinter dem Kopf |

### Die Tonpalette (`sfx.json`) – ein Ton für jedes visuelle Ereignis
| Das Ereignis | Der Schlüssel | Das Format |
|---|---|---|
| ein Element kommt herein / wechselt | `whoosh_up` · `whoosh_down` · `soft` | `[Sekunde]` · `[[Sekunde, Stärke]]` |
| ein Zähler läuft | `counter` | `[[Beginn, Dauer]]` |
| Einschlag einer Zahl / großer Moment | `thud` + `sub` | `[Sekunde]` |
| vor einer wichtigen Enthüllung | `riser` | `[[Moment der Enthüllung, Dauer]]` (endet darauf) |
| eine Karte / Blase kommt hoch | `pop` | `[Sekunde]` |
| Knopf / Auswahl / ein Icon leuchtet | `click` · `tap` | `[Sekunde]` |
| Text wird getippt | `type` | `[[Beginn, Dauer]]` |
| Hervorhebung eines Worts / Glanz | `shimmer` | `[Sekunde]` |
| Fehler / Bruch | `glitch` | `[Sekunde]` |
**Stille ist ein Werkzeug:** Nimm eine halbe Sekunde vor dem wichtigsten Satz alle Töne weg. ≤ 15 Ereignisse pro Minute (die Ticks zählen als ein Moment).

## Regeln der Kreativität (nicht brechen)
1. **Die Zeichnung ist der Beleg für das Wort, keine Zierde** – er sagt eine Zahl → ein Zähler schlägt auf demselben Wort ein; er sagt „stieg“ → eine Kurve; er vergleicht → Balken; er zählt auf → Karten nacheinander; er bittet um einen Kommentar → ein Kommentarfeld. Sammle 3 Ideen pro Satz und wähle die stärkste.
2. **Ein Held pro Szene** – ein Hauptbaustein + höchstens ein Begleiter in `R_DOWN`; `R_LOWER`/`R_OFF` tragen ein Raster.
3. **Der Einschlag auf dem gesprochenen Wort** – die `dur` des Zählers endet auf `w.s` des Worts (die Zahl selbst), und Erschütterung, Explosion und Ton liegen im selben Frame.
4. **Nur echte Zahlen** – vom Nutzer oder aus einer Quelle; erfinde keine Zahl, nur um den Zähler zu nutzen.
5. **Die Identität ist fest** – Farben aus `theme.json` (ACC/INK/BG/CLAY), die Schrift der Engine, das Raster; das Paket liest sie automatisch.
6. **Sichere Zone und Untertitelregel wie gehabt** – `R_OFF` mit einer Tafel, die den Text enthält → `nocap:true`; kein Text unter y 1500 außer den Untertiteln.
7. **Rhythmus** – jeder Baustein bleibt ≥ 1,2 s stehen, nachdem er fertig ist; Effekte nur auf Momenten (≤ 15 pro Minute, die Ticks zählen als ein Moment).
8. **Sieh es dir vor dem Gesamtrender an** – ein Blatt mit 6 Frames (Schritt 7) und ein Frame bei jedem Einschlag.

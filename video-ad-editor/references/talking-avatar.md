<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

# 🎭 „Du bist woanders und sprichst mit deiner Stimme“ – die Avatar-Szene (erprobt und abgenommen am 28. September 2026)

**Wann:** Er sagt einen Satz mit einem Ort, an dem er nicht ist („Ich sitze gleich auf einer Bühne“ · „Stell dir mich im Büro vor“) und will sich dort **sprechend** sehen.
Die vom Nutzer abgenommene Form: Fingerschnipsen → der Hintergrund kippt zu einem weißen Raum, er sitzt auf einem Stuhl unten in der Mitte, und **die ganze Erklärung steht per Code über ihm**.
Tatsächliche Kosten: zwei Bilder 0,08 $ + Avatar ≈ 0,115 $/s (eine Szene von 6 Sekunden ≈ 0,85 $). **Unter einem Dollar pro Szene.**

## Das Rezept (3 Schritte, zwei Befehle)
```bash
# 1) Das Bild – aus einem Frame mit seinem Gesicht + (optional) einem Referenzbild für Komposition/Stuhl. Zwei Optionen, zeig sie und wähle
python3 scripts/21_avatar_scene.py <work> still 31.3 "He sits relaxed on a modern white armchair in a seamless pure white studio, black trousers and black sneakers." ref_chair.jpg
# 2) Die Sprache – seine echte Stimme für genau denselben Bereich → Avatar-Lipsync → Frames clips/seat_####.jpg
python3 scripts/21_avatar_scene.py <work> talk 29.20 34.87 <work>/ai/avatar_still0.jpg seat          # gibt nur die Kosten aus
python3 scripts/21_avatar_scene.py <work> talk 29.20 34.87 <work>/ai/avatar_still0.jpg seat --yes    # nach seiner Zustimmung
# 3) Zeichne es in einer Szene der Videoebene (Code unten) + nocap für denselben Bereich + die Erklärung per Code darüber
```
- **Der Bereich = vom Moment des Schnipsens/der Verwandlung bis zum Ende des letzten Satzes der Szene** (aus `caps.json`). Frame 1 = genau der Moment `von` → die Lippen folgen seiner Originalstimme (der Videoton bleibt der Ton der Aufnahme, nicht die Stimme des Modells).
- Das Bild ist **medium-wide** (sein Kopf bei ~38 % der Höhe): kleiner, und das Modell bewegt den Mund nicht gut, größer, und es zerstört das „Erklärung darüber“.

## ⛔ Ausprobiert und gescheitert – gib dafür kein Geld mehr aus
| Versuch | Warum gescheitert |
|---|---|
| Kling image-to-video (O3) ohne Ton | erfindet Mundbewegungen → **er lacht** („ehrlich lustig“) |
| Seedance 2.5 reference-to-video mit Ton | **lehnt jedes echte Gesicht ab** (`content_policy_violation · partner_validation_failed`) – nicht für das Gesicht des Nutzers versuchen |
| Referenzbild mit einer zweiten Person | Das Modell übernimmt die **Kleidung** der Referenzperson – gib die Referenz nur für die Komposition und schreib seine Kleidung ausdrücklich in die Beschreibung |
| Ihn sehr klein machen (0,6) | Das Lachen/der Ausdruck verschwindet, aber man verliert, dass er spricht – 0,72 mit dem Avatar ist besser |
| Generierte „Kamerawinkel“-Einstellungen (rechts/oben), beschleunigt | „Ich sah aus wie ein Clown“ – **endgültig gestrichen**; schlag sie nicht vor |

## Das Zeichnen in compose (Szene der Videoebene)
```js
const SNAP={x:390,y:1010,t:29.20}, END=34.87;               // Ort seiner Finger + Moment des Schnipsens
function seatScene(t){ if(t<SNAP.t||t>=END) return; const im=clipAt('seat',SNAP.t,t); if(!im) return;
  const rv=eio(pr(t,SNAP.t,SNAP.t+0.42));
  X.save(); X.beginPath(); X.arc(SNAP.x,SNAP.y,2300*rv,0,7); X.clip();           // ein Kreis, der sich von seinen Fingern öffnet
  const g=X.createLinearGradient(0,0,0,H); g.addColorStop(0,'rgb(236,242,242)'); g.addColorStop(1,'rgb(245,248,247)'); X.fillStyle=g; X.fillRect(0,0,W,H);
  const SC=0.72, dw=1080*SC, dh=1890*SC; X.drawImage(featherClip(im),(W-dw)/2,1600-1570*SC,dw,dh);   // seine Füße bei 1600
  seatText(t);                                                                       // die Erklärung darüber – Wörter mit der Zeit aus caps.json
  X.restore(); ring(SNAP.x,SNAP.y,2300,rv,ACC,18);                                   // goldener Ring + weißer Blitz 0,16 s + Schlag in sfx
}
seatScene.layer='video';
/* featherClip: Zeichne den Frame auf ein Hilfs-Canvas 1080×1890 und dann destination-out:
   - oben: lösche alles über y=420 und einen Verlauf 420→640 (die Oberkante der Avatar-Aufnahme hat graue Schattierung, die eine Linie zeigt)
   - rechts/links/unten: Verlauf von 160 px – die Aufnahme löst sich im Hintergrund auf, ohne Rahmen */
```
- **Blende Fortschrittsbalken und Untertitel** im Bereich aus (`nocap:true` in der Szene + `bar` überschreiben) – der Text darüber ist der Untertitel.
- **Die Erklärung darüber (y 150–860) in dunkler Tinte** (`#16161A`) und die Betonung in der Identitätsfarbe: Wörter erscheinen in dem Moment, in dem sie gesprochen werden, und verteilen sich nach ihrer gemessenen Breite (keine festen Positionen – sie kleben zusammen), „bewegt sich“ = Wörter, die mit Spur nach oben fliegen, „Motion Graphics“ = kreisende Ringe + eine Kurve mit Keyframes + ein Balken, der sich füllt.

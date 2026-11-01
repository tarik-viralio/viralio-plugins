<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen -->

# Bildschirmaufnahme im Handyrahmen – Regeln und fertiger Code (v2.9)

## Die Regeln (vom Nutzer am 13. September 2026 abgenommen)
1. **Das Seitenverhältnis ist heilig:** Die Aufnahme wird vollständig in ihrem Originalverhältnis gezeigt – `sc = Math.min(R.w/sw, R.h/shh)` und zentriert. Kein `Math.max` (das beschneidet) und kein Dehnen. Dein Test: Jeder Kreis in der Aufnahme (Profilbild) muss ein Kreis bleiben.
2. **Der Rahmen im Verhältnis der Aufnahme:** `PH_W = PH_H / (shh/sw)`. Ist die Aufnahme 1080×2346, ist das Verhältnis 2,172. Der Rahmen ist per Code gezeichnet (scharf in jeder Größe), und ein kleines PNG-Rahmenbild zu dehnen ist verboten.
3. **Innerhalb der sicheren Zone:** y von 150 bis 1480, und der Hintergrund mit Raster dahinter. Der Sprecher ist `R_OFF`, und die Untertitel sind währenddessen ausgeblendet.
4. **Harter Schnitt** zwischen den Einstellungen – kein Ein-/Ausblenden und kein Zoom. Der Rhythmus kommt aus der Rede: Jeder Schritt, den er ausspricht, ist eine Einstellung.
5. **Tippmarkierung** in **Quellpixel-Koordinaten** (aus einem vergrößerten Frame mit PIL lesen), umgerechnet mit demselben `sc/dx/dy`, mit dem die Aufnahme gezeichnet wurde. Linie unter einem Wort: `underline()`.
6. **Der Fortschrittsbalken** sinkt während der Aufnahme auf y=1846 (eine Zeile ohne Text) – erlaube es in `safe.json`: `unterer Bildrand max: 0.006`.

## Frames extrahieren
```bash
ffmpeg -v error -y -ss <von> -t <Dauer> -i screen.MP4 -vf "fps=30,scale=1080:-2" broll/<name>_%04d.jpg
```
Und definiere sie mit `BR_NEED={<name>:[1,<Anzahl>]}`.

## Der Code (aus compose.html eines Edits-Videos – unverändert kopieren)
```js
const PH_H=1320, PH_W=Math.round(PH_H/2.172);                      /* Verhältnis der Bildschirmaufnahme selbst 1080×2346 – ohne jede Stauchung, nur proportionale Verkleinerung */
const PH={x:Math.round(540-PH_W/2),y:150,w:PH_W,h:PH_H,r:Math.round(PH_W*0.16)};
function fullShot(k,dt,crop,tap){
  const im=brFrame(k,dt,1); if(!im) return;
  const [sx,sy,sw,shh]=crop; const bz=Math.round(PH.w*0.032); const R={x:PH.x+bz,y:PH.y+bz,w:PH.w-2*bz,h:PH.h-2*bz,r:PH.r-bz};
  X.save(); sh(70,28,0.30); X.fillStyle='#111'; rr(PH.x,PH.y,PH.w,PH.h,PH.r); X.fill(); nsh();
  X.strokeStyle='rgba(255,255,255,0.35)'; X.lineWidth=3; rr(PH.x+4,PH.y+4,PH.w-8,PH.h-8,PH.r-4); X.stroke();
  X.save(); rr(R.x,R.y,R.w,R.h,R.r); X.clip();
  /* Die Aufnahme vollständig im Verhältnis: ein einziger Maßstab für Breite und Höhe (contain), zentriert im Bildschirm */
  const sc=Math.min(R.w/sw,R.h/shh); const dw=sw*sc, dh=shh*sc; const dx=R.x+(R.w-dw)/2, dy=R.y+(R.h-dh)/2;
  X.fillStyle='#000'; X.fillRect(R.x,R.y,R.w,R.h); X.drawImage(im,sx,sy,sw,shh,dx,dy,dw,dh); X.restore();
  window._SHOTMAP={sc,dx,dy,sx,sy};
  X.fillStyle='#111'; rr(540-PH.w*0.17,PH.y+bz+10,PH.w*0.34,PH.w*0.055,PH.w*0.03); X.fill();   /* Dynamic Island */
  X.restore();
  if(tap){ const M=window._SHOTMAP; const px=M.dx+(tap[0]-M.sx)*M.sc, py=M.dy+(tap[1]-M.sy)*M.sc; const ph=(dt-(tap[2]||0.4)); if(ph<0||ph>1.2) return;
    if(px<R.x||px>R.x+R.w||py<R.y||py>R.y+R.h) return;
    X.save(); X.strokeStyle=ACC; X.lineWidth=8; X.globalAlpha=1-pr(ph,0.8,1.2); X.beginPath(); X.arc(px,py,44,0,7); X.stroke();
    X.globalAlpha=0.7*(1-pr(ph,0.2,0.9)); X.lineWidth=5; X.beginPath(); X.arc(px,py,44+ph*110,0,7); X.stroke();
    X.globalAlpha=0.45*(1-pr(ph,0,0.6)); X.fillStyle=ACC; X.beginPath(); X.arc(px,py,30,0,7); X.fill(); X.restore(); }
}
const SCR=[0,0,1080,2346];
/* Eine orangefarbene Linie wird unter ein Wort auf dem Bildschirm geschrieben: pos=[x,y,Breite] in Quellpixeln */
function underline(k,dt,at,pos,crop){ if(dt<at) return; const [sx,sy,sw,shh]=crop; const bz=Math.round(PH.w*0.032); const R={x:PH.x+bz,y:PH.y+bz,w:PH.w-2*bz,h:PH.h-2*bz};
  const M=window._SHOTMAP; if(!M) return; const x=M.dx+(pos[0]-M.sx)*M.sc, y=M.dy+(pos[1]-M.sy)*M.sc, w=pos[2]*M.sc*sm(pr(dt,at,at+0.35));
  X.save(); X.strokeStyle=ACC; X.lineWidth=7; X.lineCap='round'; X.beginPath(); X.moveTo(x,y); X.lineTo(x+w,y); X.stroke(); X.restore(); }

```
Und in `bar(t)` als erste Zeile: `if(t>=<Beginn>&&t<<Ende>){ X.save(); X.globalAlpha=a; X.fillStyle=ACC; X.fillRect(0,1846,W*(t/DUR),6); X.restore(); return; }`
Und in `caption(t)`: `if(t>=<Beginn>&&t<<Ende>) return;`

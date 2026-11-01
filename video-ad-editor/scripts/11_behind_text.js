/* ═══ الكلام يمرّ ورا الشخص (كشيدة عربية) ═══
   node 11_behind_text.js <work> plan            → يرشّح الجُمل المناسبة
   node 11_behind_text.js <work> build 1 9       → يجهّز قصّ الشخص لهالجُمل ويكتب behind.json
   node 11_behind_text.js <work> build 2:6-8     → كلمات بعينها داخل جملة
   node 11_behind_text.js <work> stack 1         → «طبقات»: كلمة فوق الراس بعرض الشاشة ← كلمة/ثنتين ورا الراس ← الباقي قدّام جسمه
   node 11_behind_text.js <work> stack 3:1-5     → «طبقات» لكلمات بعينها
   node 11_behind_text.js <work> cutout 23.8-26.6 → «واقف قدام اللوحة»: بلا كرت، أنت العنصر
   node 11_behind_text.js <work> headout 23.8-26.6 → «راسك برّا المستطيل»: الفيديو بكرت وراسك يطلع فوق حافته
   node 11_behind_text.js <work> person 23.8-26.6 → قصّ بس (بلا تأثير): MV.person لحركات البنك 51–61 (مدار، كسر الإطار، غلاف مجلة…)
   node 11_behind_text.js <work> drop 9          → يشيل جملة وحدة (أو أكثر: drop 1 9) ويخلّي الباقي
   node 11_behind_text.js <work> off             → يلغي التأثير كله (الجُمل + cutout + headout)

   كل أمر build/stack = **القائمة الكاملة لنوعه**: build 1 9 ثم build 1 → يبقى 1 بس (جُمل «طبقات» ما تنلمس، والعكس).
   cutout/headout يتجمّعون (نفس المدى مرتين = مرة وحدة). ranges تنحسب من جديد كل مرة (بلا تكرار).

   شلون يشتغل: ماك فيه فصل الأشخاص مدمج بالنظام (Vision). نقصّ جسم المتحدث بكل فريم،
   نرسم الكلمة ممدودة بالكشيدة تحته، ثم نرجّع جسمه فوقها — فالكشيدة وحدها تمرّ ورا الراس
   والحروف تبقى بارزة على الجانبين.  يحتاج: ماك + swiftc (مجاني مع أدوات Xcode) + ffmpeg. */
const path=require('path'), fs=require('fs'), cp=require('child_process');
const W=path.resolve(process.argv[2])+path.sep, MODE=process.argv[3]||'plan';
const SC=path.dirname(path.resolve(process.argv[1]))+path.sep;
const caps=JSON.parse(fs.readFileSync(W+'caps.json','utf8'));
const FPS=30, MAXW=4, MINDUR=0.85;

const words=c=>c.w.map(w=>w.t).join(' ');
if(MODE==='off'){ try{fs.unlinkSync(W+'behind.json');}catch(e){} console.log('Der Effekt wurde aufgehoben.'); process.exit(0); }
/* ranges (مدى الفريمات اللي يحمّل لها 04 صورة الشخص) تنحسب من الجُمل والمشاهد الموجودة — مو تتراكم مع كل تشغيل */
function rebuildRanges(o){
  let nv=1e9; try{ nv=fs.readdirSync(W+'vfr').filter(f=>f.endsWith('.jpg')).length||1e9; }catch(e){}
  const fr=(a,b)=>[Math.max(1,Math.floor(a*FPS)+1), Math.min(nv,Math.ceil(b*FPS)+1)], rs=[];
  (o.lines||[]).forEach(l=>rs.push(fr(l.s,l.e)));
  (o.cutouts||[]).concat(o.headouts||[],o.persons||[]).forEach(c=>rs.push(fr(c[0],c[1])));
  rs.sort((p,q)=>p[0]-q[0]); const out=[];
  for(const r of rs){ const z=out[out.length-1]; if(z&&r[0]<=z[1]+1) z[1]=Math.max(z[1],r[1]); else out.push(r.slice()); }
  o.ranges=out; return o; }
if(MODE==='drop'){
  if(!fs.existsSync(W+'behind.json')){ console.log('Keine behind.json – es gibt nichts zu entfernen'); process.exit(0); }
  const o=JSON.parse(fs.readFileSync(W+'behind.json','utf8'));
  const ids=new Set(process.argv.slice(4).map(x=>parseInt(x,10)-1).filter(x=>x>=0));
  if(!ids.size){ console.log('Gib mir die Satznummer: drop 9'); process.exit(2); }
  const before=(o.lines||[]).length; o.lines=(o.lines||[]).filter(l=>!ids.has(l.card));
  fs.writeFileSync(W+'behind.json',JSON.stringify(rebuildRanges(o),null,1));
  console.log('✅ Entfernt:',before-o.lines.length,'Sätze – übrig:',o.lines.map(l=>(l.card+1)+(l.style==='stack'?'(Ebenen)':'')).join(' ')||'nichts');
  process.exit(0);
}

/* ── ماك فقط (مضاف): القصّ يعتمد على Vision عبر swiftc ── */
if(['build','stack','cutout','headout','person'].indexOf(MODE)>=0){
  let hasSwift=false;
  if(process.platform==='darwin'){
    try{ hasSwift = cp.spawnSync('swiftc',['--version'],{stdio:'ignore'}).status===0; }catch(e){ hasSwift=false; }
  }
  if(!hasSwift){
    console.log('⛔ „Sprache hinter der Person“ braucht einen Mac + swiftc – dein System: '+process.platform);
    console.log('   Der Rest des Skills läuft normal: Untertitel, Motion Graphics, Effekte und Schluss.');
    process.exit(20);
  }
}

if(MODE==='plan'){
  console.log('Sätze, in denen die Rede hinter der Person laufen kann (kurz und klar):');
  let n=0;
  caps.cards.forEach((c,i)=>{
    const dur=c.w[c.w.length-1].e-c.w[0].s;
    if(c.w.length>MAXW||dur<MINDUR) return;
    n++;
    console.log(`  ${i+1}  [${c.s.toFixed(2)}]  ${words(c)}   (${c.w.length} Wörter · ${dur.toFixed(2)}s)${i===0?'  ← der Hook, der stärkste':''}`);
  });
  if(!n) console.log('  Kein kurzer Satz – wähle bestimmte Wörter: build 2:6-8 (die Wörter 6→8 aus Satz 2)');
  /* «طبقات»: جملة 2-8 كلمات (فوق الراس + ورا + قدّام) — الهوك أول مرشّح */
  const st=[]; caps.cards.forEach((c,i)=>{ const dur=c.w[c.w.length-1].e-c.w[0].s;
    if(c.w.length>=2&&c.w.length<=8&&dur>=1.2) st.push(`  ${i+1}  [${c.s.toFixed(2)}]  ${words(c)}   (${c.w.length} كلمات)${i===0?'  ← الهوك':''}`); });
  if(st.length){ console.log('\nGeeignet für „Ebenen“ (ein Wort über dem Kopf → hinter dem Kopf → der Rest davor):'); st.slice(0,8).forEach(x=>console.log(x));
    console.log('   node 11_behind_text.js <work> stack <Nummer>   – und bei einem langen Satz: stack 2:1-6'); }
  console.log('\n⚠️ Wähle höchstens ein oder zwei – kommt es in jedem Satz vor, verliert es die Wirkung.');
  console.log('Dann: node 11_behind_text.js <work> build <Satznummern>   oder   stack <Nummer>');
  process.exit(0);
}

if(MODE==='cutout'||MODE==='headout'||MODE==='person'){
  /* «واقف قدام اللوحة»: نقصّ المتحدث بمدى زمني كامل، ونرسمه فوق التصميم بلا كرت */
  const m=String(process.argv[4]||'').match(/^([\d.]+)-([\d.]+)$/);
  if(!m){ console.log('Gib mir einen Bereich in Sekunden: cutout 23.8-26.6'); process.exit(2); }
  const a=Math.max(0,parseFloat(m[1])), b=Math.min(caps.total,parseFloat(m[2]));
  if(!(b>a)){ console.log('Ungültiger Bereich'); process.exit(2); }
  if(!fs.existsSync(W+'vfr')){ console.log('❌ Kein Ordner vfr'); process.exit(3); }
  const NVF2=fs.readdirSync(W+'vfr').filter(f=>f.endsWith('.jpg')).length;
  const f0=Math.max(1,Math.floor(a*FPS)+1), f1=Math.min(NVF2,Math.ceil(b*FPS)+1);
  fs.mkdirSync(W+'bt/src',{recursive:true}); fs.mkdirSync(W+'bt/mask',{recursive:true}); fs.mkdirSync(W+'bt/person',{recursive:true});
  const BIN2=W+'bt/personmask';
  if(!fs.existsSync(BIN2)){
    try{ cp.execSync('swiftc -O -o '+JSON.stringify(BIN2)+' '+JSON.stringify(SC+'personmask.swift'),{stdio:'pipe'}); }
    catch(e){ console.log('❌ Du brauchst die Xcode-Tools: xcode-select --install'); process.exit(4); }
  }
  let n=0;
  for(let f=f0;f<=f1;f++){ const id=String(f).padStart(5,'0');
    if(fs.existsSync(W+'vfr/'+id+'.jpg')){ fs.copyFileSync(W+'vfr/'+id+'.jpg', W+'bt/src/'+id+'.jpg'); n++; } }
  console.log('Frames zum Freistellen:',n,'— Ich stelle dich vom Hintergrund frei…');
  cp.execSync(JSON.stringify(BIN2)+' '+JSON.stringify(W+'bt/src')+' '+JSON.stringify(W+'bt/mask')+' accurate 2.5',{stdio:'inherit'});
  cp.execSync('ffmpeg -v error -start_number '+f0+' -i '+JSON.stringify(W+'bt/src/%05d.jpg')+
    ' -start_number '+f0+' -i '+JSON.stringify(W+'bt/mask/%05d.png')+' -frames:v '+(f1-f0+1)+
    ' -filter_complex "[1:v]format=gray,scale=1080:1920[a];[0:v][a]alphamerge,format=rgba"'+
    ' -start_number '+f0+' -y '+JSON.stringify(W+'bt/person/%05d.png'),{stdio:'pipe'});
  const prev=fs.existsSync(W+'behind.json')?JSON.parse(fs.readFileSync(W+'behind.json','utf8')):{lines:[],ranges:[],faces:{}};
  const key=MODE==='headout'?'headouts':MODE==='person'?'persons':'cutouts';
  prev[key]=(prev[key]||[]).filter(c=>!(c[0]===a&&c[1]===b)).concat([[a,b]]);   /* نفس المدى مرتين = مرة وحدة */
  rebuildRanges(prev);
  const meta=JSON.parse(fs.readFileSync(W+'bt/mask/meta.json','utf8'));
  prev.faces=prev.faces||{};
  for(const mm of meta) if(mm.face) prev.faces[parseInt(mm.f,10)]=mm.face;
  /* 8 سبتمبر: حدود ثابتة للمشهد كله (وسيط حدود الجسم عبر فريماته) — بدونها الكرت الصغير كان يتبع الجسم بكل فريم
     فتهتز الخلفية (بلاغ المستخدم). المحرّك يقرأ headbox[بداية المدى] ويثبّت التأطير، والحركة الوحيدة حركة المتحدث نفسه.
     20 أكتوبر: كانت تنحسب بـ`python3 -c` عبر الشِل — JSON.stringify يحوّل أسطر الكود لـ«\n» حرفية والشِل ما يفكها
     ← SyntaxError، والرسالة تقول «يحتاج PIL» غلط، فما انكتب headbox أبداً. الحين بـffmpeg (اشتغل فوق) + نود: بلا بايثون ولا PIL */
  if(MODE==='headout'){
    try{
      const xs0=[],xs1=[],ys0=[],ys1=[];
      for(let f=f0;f<=f1;f+=3){ const p=W+'bt/mask/'+String(f).padStart(5,'0')+'.png'; if(!fs.existsSync(p)) continue;
        const g=cp.execFileSync('ffmpeg',['-v','error','-i',p,'-vf','scale=1080:1920,format=gray','-f','rawvideo','-'],{maxBuffer:1<<23});
        let x0=1e9,x1=-1,y0=-1,y1=-1;   /* نفس getbbox بعد عتبة 140: x1/y1 = آخر بكسل + 1 */
        for(let y=0;y<1920;y++){ const r=y*1080; for(let x=0;x<1080;x++) if(g[r+x]>140){ if(x<x0)x0=x; if(x>x1)x1=x; if(y0<0)y0=y; y1=y; } }
        if(x1<0) continue; xs0.push(x0); ys0.push(y0); xs1.push(x1+1); ys1.push(y1+1); }
      const med=v=>{ v=v.slice().sort((p,q)=>p-q); const m=v.length>>1; return v.length%2?v[m]:(v[m-1]+v[m])/2; };
      if(!xs0.length) throw new Error('Die Maske ist in allen Frames leer');
      prev.headbox=prev.headbox||{}; prev.headbox[String(a)]={x0:med(xs0),x1:med(xs1),y0:med(ys0),y1:med(ys1),n:xs0.length};
      console.log('📐 headbox:',JSON.stringify(prev.headbox[String(a)]));
    }catch(e){ console.log('⚠️ Konnte die festen Grenzen nicht berechnen ('+String(e.message||e).split('\n')[0]+') – die Karte folgt dem Körper in jedem Frame'); }
  }
  fs.writeFileSync(W+'behind.json',JSON.stringify(prev,null,1));
  console.log('✅ '+(MODE==='headout'?'„Dein Kopf außerhalb des Rechtecks“':MODE==='person'?'Freistellung des Sprechers (MV.person)':'„Er steht vor der Tafel“')+' bereit aus',a,'bis',b,'Sekunden.');
  console.log('   Rendere: node 04_render_frames.js '+W+' range '+a+' '+b);
  process.exit(0);
}
if(MODE!=='build'&&MODE!=='stack'){ console.log('Befehle: plan · build · stack · cutout · headout · person · drop · off'); process.exit(2); }
/* «2» = الجملة كاملة · «2:6-8» = الكلمات 6→8 داخل الجملة 2 */
const pick=process.argv.slice(4).map(a=>{
  const m=String(a).match(/^(\d+)(?::(\d+)-(\d+))?$/); if(!m) return null;
  const i=parseInt(m[1],10)-1; if(i<0||i>=caps.cards.length) return null;
  const n=caps.cards[i].w.length;
  return {i, from:m[2]?Math.max(0,parseInt(m[2],10)-1):0, to:m[3]?Math.min(n-1,parseInt(m[3],10)-1):n-1};
}).filter(Boolean);
if(!pick.length){ console.log('Gib mir die Satznummern: '+MODE+' 1 9   oder   '+MODE+' 2:6-8'); process.exit(2); }
if(!fs.existsSync(W+'vfr')){ console.log('❌ Kein Ordner vfr – extrahiere zuerst die Frames'); process.exit(3); }

/* 1) بناء أداة القصّ مرة وحدة */
const BIN=W+'bt/personmask';
fs.mkdirSync(W+'bt/src',{recursive:true}); fs.mkdirSync(W+'bt/mask',{recursive:true}); fs.mkdirSync(W+'bt/person',{recursive:true});
if(!fs.existsSync(BIN)){
  try{ cp.execSync('swiftc -O -o '+JSON.stringify(BIN)+' '+JSON.stringify(SC+'personmask.swift'),{stdio:'pipe'}); }
  catch(e){ console.log('❌ Konnte das Freistellungs-Tool nicht bauen – du brauchst die Xcode-Tools: xcode-select --install'); process.exit(4); }
}

/* 2) الفريمات المطلوبة فقط (مو الفيديو كله) */
const NVF=fs.readdirSync(W+'vfr').filter(f=>f.endsWith('.jpg')).length;
const lines=[], ranges=[];
for(const sel of pick){
  const c=caps.cards[sel.i];
  const ws=c.w.slice(sel.from, sel.to+1);
  const a=Math.max(0,ws[0].s-0.20), b=Math.min(caps.total,ws[ws.length-1].e+0.45);
  const f0=Math.max(1,Math.floor(a*FPS)+1), f1=Math.min(NVF,Math.ceil(b*FPS)+1);
  ranges.push([f0,f1]);
  const ln={card:sel.i, s:a, e:b, words:ws.map(w=>({t:w.t,s:w.s,e:w.e}))};
  if(MODE==='stack'){ ln.style='stack'; ln.umask='bt/umask_'+(sel.i+1)+'.png'; }
  lines.push(ln);
}
let copied=0;
for(const [f0,f1] of ranges) for(let f=f0;f<=f1;f++){
  const id=String(f).padStart(5,'0');
  if(fs.existsSync(W+'vfr/'+id+'.jpg')){ fs.copyFileSync(W+'vfr/'+id+'.jpg', W+'bt/src/'+id+'.jpg'); copied++; }
}
console.log('Frames des Effekts:',copied,'— Ich stelle die Person darin frei…');

/* 3) القصّ + بيانات الوجه */
cp.execSync(JSON.stringify(BIN)+' '+JSON.stringify(W+'bt/src')+' '+JSON.stringify(W+'bt/mask')+' accurate 2.5',{stdio:'inherit'});

/* 4) دمج القناع كشفافية → صورة الشخص وحده (كل مدى على حدة) */
for(const [f0,f1] of ranges){
  cp.execSync('ffmpeg -v error -start_number '+f0+' -i '+JSON.stringify(W+'bt/src/%05d.jpg')+
    ' -start_number '+f0+' -i '+JSON.stringify(W+'bt/mask/%05d.png')+
    ' -frames:v '+(f1-f0+1)+
    ' -filter_complex "[1:v]format=gray,scale=1080:1920[a];[0:v][a]alphamerge,format=rgba"'+
    ' -start_number '+f0+' -y '+JSON.stringify(W+'bt/person/%05d.png'),{stdio:'pipe'});
}

/* 5) «طبقات»: قناع الجمع لكل جملة = متوسط أقنعة فريماتها (ربع الدقة). المحرّك يقرأ منه حدود الجسم صف صف
   فيثبّت التخطيط طول الجملة، والحروف ما تدخل مكاناً وقف فيه الشخص ولو بفريم (عتبة 5٪) */
if(MODE==='stack'){
  lines.forEach((ln,k)=>{ const [f0,f1]=ranges[k], n=Math.min(1024,f1-f0+1);
    cp.execSync('ffmpeg -v error -start_number '+f0+' -i '+JSON.stringify(W+'bt/mask/%05d.png')+' -frames:v '+n+
      ' -vf "scale=270:480,format=gray,tmix=frames='+n+'" -update 1 -y '+JSON.stringify(W+ln.umask),{stdio:'pipe'});
    if(!fs.existsSync(W+ln.umask)){ console.log('❌ Die Summenmaske für den Satz wurde nicht gebaut',ln.card+1); process.exit(5); } });
}

const meta=JSON.parse(fs.readFileSync(W+'bt/mask/meta.json','utf8'));
/* 28 سبتمبر: الأمر = القائمة الكاملة لنوعه. build يستبدل كل جُمل «ورا الراس» العادية، وstack يستبدل كل جُمل «طبقات»،
   والنوع الثاني + cutouts/headouts يبقون. الجملة اللي انبنت بالنوع الثاني تنتقل للجديد (جملة وحدة = نوع واحد).
   تشيل جملة وحدة؟ drop <رقم>. off يمسح الكل. */
const prev=fs.existsSync(W+'behind.json')?JSON.parse(fs.readFileSync(W+'behind.json','utf8')):{};
const newCards=new Set(lines.map(l=>l.card)), isStack=l=>l.style==='stack';
const kept=(Array.isArray(prev.lines)?prev.lines:[]).filter(l=>!newCards.has(l.card)&&isStack(l)!==(MODE==='stack'));
const gone=(Array.isArray(prev.lines)?prev.lines:[]).filter(l=>!newCards.has(l.card)&&isStack(l)===(MODE==='stack'));
if(gone.length) console.log('ℹ️  Alte Sätze derselben Art entfernt:',gone.map(l=>l.card+1).join(' '),'— Willst du sie? Füge sie demselben Befehl hinzu');
prev.lines=kept.concat(lines).sort((p,q)=>p.s-q.s);
rebuildRanges(prev);
prev.faces=prev.faces||{};
for(const m of meta) if(m.face) prev.faces[parseInt(m.f,10)]=m.face;
fs.writeFileSync(W+'behind.json',JSON.stringify(prev,null,1));
console.log('✅ behind.json ist bereit –',lines.length,MODE==='stack'?'Satz/Sätze „Ebenen“ (über dem Kopf → dahinter → davor).':'Satz/Sätze, deren Rede hinter der Person läuft.');
console.log('   Vorschau: node 04_render_frames.js '+W+' preview '+lines.map(l=>(l.e-0.3).toFixed(2)).join(' '));
console.log('   Dann rendern: node 04_render_frames.js '+W+' all --force');

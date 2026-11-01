# -*- coding: utf-8 -*-
"""🪝 الهوك المكتوب لريلات البودكاست/المقابلة (v3.8.1) — كل ريل يبدأ بجملة هوك مكتوبة على الشاشة (1.5-3 ث) ثم يكمل المقطع.
القواعد وصيغ الكتابة: references/podcast-hook.md

  python3 22_hook.py suggest <work> [--words f.json]              ← يرتّب أقوى سطور المقطع (رقم/تناقض/سؤال/قصة) عشان تكتب منها الهوك
  python3 22_hook.py check   <work> "<الهوك>" [...] [--words f.json] ← فاحص القواعد: 3-8 كلمات · أداة شد · لهجة كويتية · الرقم من كلامه · مو أول جملة
  python3 22_hook.py apply   <work> "<الهوك>" [--dur 2.4] [--pos auto|top|mid|low] [--style bold|card] [--kicker "اسم برنامجك"]
                                                [--em "10 دقايق"] [--keep-caps] [--force]
        ← يكتب theme.json ← hook + ينسخ hook-card.js للمجلد ويركّبه بـcompose.html (04/16 يركّبونه وحدهم لو ناقص)
  python3 22_hook.py preview <work>                              ← 4 لقطات للهوك (بداية · 0.3 · آخره · بعده) بورقة وحدة hook_sheet.jpg
  python3 22_hook.py off     <work>                              ← يشيل الهوك
  python3 22_hook.py overlay <out> "<الهوك>" --theme theme.json --words reel.json [--video reel.mp4] [--pos mid] [...]
        ← لريل **مو** من محرّكاتنا (خط المقابلة بدافنشي/لوتي، أو mp4 جاهز): طبقة شفافة hook.mov (ProRes 4444 بألفا — حطها
          بأعلى تراك بدافنشي عند 0) ولو أعطيته --video يطلّع <اسم>_hook.mp4 محروق فوقه + hook_sheet.jpg

<work> لازم يكون فيه caps.json أو a.json (أو --words ملف وِسبر/caps) — بدونها الفاحص ما يقدر يتأكد إن الأرقام من كلامه فيوقف
(--no-words يتخطّى هالفحص عمداً).
بعد apply على ريل مرسوم من قبل: لا تعيد الرسم كامل — `node 04_render_frames.js <work> range 0 <dur+0.5>` ثم 06_encode/06b كالعادة
(وضع الكاميرات: `node 16_render_pod.js <work> range 0 <dur+0.5>` ثم أعد التجميع من `15_podcast.py make`)."""
import sys as _sys, builtins as _bi
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace"); _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
_real_open = _bi.open
def _utf8_open(f, mode="r", *a, **k):
    if "b" not in mode: k.setdefault("encoding", "utf-8")
    return _real_open(f, mode, *a, **k)
_bi.open = _utf8_open
import json, os, re, sys, shutil, subprocess, argparse

SC = os.path.dirname(os.path.abspath(__file__))
HIND = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
PUNCT = "…?!.,;:„“”«»‚‘’\"'*|()–—-"
def norm(w):
    return w.translate(HIND).strip(PUNCT).lower()
def toks(s): return [t for t in (norm(x) for x in re.split(r"[\s|…]+", s.translate(HIND))) if t]

# ── Zahlen als Wörter (damit „die Zahl kommt im Gesagten vor“ nicht scheitert, wenn Whisper sie ausschreibt) ──
NUMW = {"zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10, "elf": 11,
        "zwölf": 12, "dreizehn": 13, "vierzehn": 14, "fünfzehn": 15, "zwanzig": 20, "dreißig": 30, "vierzig": 40,
        "fünfzig": 50, "sechzig": 60, "siebzig": 70, "achtzig": 80, "neunzig": 90, "hundert": 100, "zweihundert": 200,
        "tausend": 1000, "zweitausend": 2000, "million": 1000000, "millionen": 1000000, "zweimal": 2, "dreimal": 3, "viermal": 4}
def nums_in(text):
    out = set(int(n) for n in re.findall(r"\d+", text.translate(HIND)))
    for t in toks(text):
        if t in NUMW: out.add(NUMW[t])
    return out

# Dialekt-Prüfung gibt es im Deutschen nicht (leer = keine Warnungen)
DIALECT = {}
DEV = {  # Spannungsmittel — jeder Hook braucht mindestens eins, am stärksten zwei (Zahl + Widerspruch)
    "Zahl":         lambda s, T: bool(re.search(r"\d", s.translate(HIND))) or any(t in NUMW for t in T),
    "Widerspruch":  lambda s, T: "…" in s or any(t in ("aber", "doch", "trotzdem", "statt", "anstatt", "obwohl", "außer", "nie", "nicht", "kein", "keine", "ohne", "sondern", "dennoch", "jedoch", "dabei") for t in T),
    "Frage":        lambda s, T: "?" in s or any(t in ("wie", "warum", "wieso", "weshalb", "was", "wer", "wo", "wann", "wieviel", "welche", "welcher", "welches") for t in T),
    # Neugier = Wort, das eine Lücke öffnet (Geheimnis/Grund/Fehler/niemand) — keine Alltagswörter wie „das/der/die“
    "Neugier":      lambda s, T: any(t in ("geheimnis", "grund", "fehler", "niemand", "keiner", "wahrheit", "einzige", "einzigen", "unterschied", "problem", "trick", "geheimnisse") for t in T),
    "Befehl":       lambda s, T: bool(T) and T[0] in ("hör", "hört", "stopp", "nimm", "probier", "öffne", "achtung", "lass", "kauf", "vergiss", "mach", "geh", "schau", "stell", "bevor"),
    "Geschichte":   lambda s, T: any(t in ("war", "hatte", "sagte", "damals", "einmal", "verlor", "gewann", "lernte", "bereute", "passierte", "wurde", "lehnte", "flog", "kündigte") for t in T),
}
HOT = ("erste", "ersten", "meisten", "größte", "größten", "schwerste", "beste", "besten", "nie", "immer", "alle", "niemand", "meiste", "falsch", "unmöglich", "geheimnis", "million", "kostenlos", "umsonst", "fast", "einzige")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F000-\U0001F2FF]")

NO_WORDS = False
WORDS = None   # --words <ملف> (caps.json أو مخرج وِسبر) — يغلب ملفات المجلد
def read_words(p):
    c = json.load(open(p))
    if "cards" in c: return [(x["s"], " ".join(w["t"] for w in x["w"])) for x in c["cards"]]
    if "segments" in c: return [((s.get("words") or [{}])[0].get("start", s.get("start", 0)), s["text"].strip()) for s in c["segments"] if s.get("text", "").strip()]
    return []
def load_sentences(W):
    if WORDS: return read_words(WORDS)
    for fn in ("caps.json", "a.json"):
        p = os.path.join(W, fn)
        if os.path.exists(p): return read_words(p)
    return []

def devices(s): T = toks(s); return [k for k, f in DEV.items() if f(s, T)]

def check(W, hook, quiet=False):
    """يرجّع (أخطاء، تنبيهات، أدوات)"""
    errs, warns = [], []
    words = [w for w in re.split(r"[\s|]+", hook.replace("…", " ").replace("*", "")) if w.strip(PUNCT)]
    n = len(words)
    if n < 3: errs.append(f"nur {n} Wörter — ein Hook hat 3–8 Wörter (unter 3 trägt keine Idee)")
    if n > 8: errs.append(f"{n} Wörter — höchstens 8 (der Zuschauer hat zwei Sekunden zum Lesen). Füllwörter streichen: also/halt/ja/ich")
    if re.search("[٠-٩۰-۹]", hook): errs.append("Östlich-arabische Ziffern — nur 1 2 3 verwenden. apply wandelt sie selbst um")
    if EMOJI.search(hook): errs.append("Emoji im Hook — entfernen (die Flamme ist komplett verboten)")
    for t in toks(hook):
        if t in DIALECT and DIALECT[t][0]:
            (errs if DIALECT[t][1] == 1 else warns).append(f"„{t}“ ist kein natürliches Deutsch – sag stattdessen „{DIALECT[t][0]}“")
    dv = devices(hook)
    if not dv: errs.append("Kein Spannungsmittel: nimm eine Zahl, einen Widerspruch („…“ / aber / nicht), eine Frage (wie/warum) oder Neugier (Grund/Fehler/niemand)")
    elif len(dv) == 1: warns.append(f"nur ein Mittel ({dv[0]}) — stärker sind zwei: Zahl + Widerspruch oder Frage + Zahl")
    if len(hook.replace("*", "")) > 46: warns.append(f"{len(hook)} Zeichen — lang, die Schrift wird kleiner. Unter 40 kürzen")
    sents = load_sentences(W) if (W and (WORDS or os.path.isdir(W))) else []
    if sents:
        body = " ".join(s for _, s in sents)
        miss = sorted(nums_in(hook) - nums_in(body))
        if miss: errs.append(f"Die Zahl {', '.join(map(str, miss))} kommt im Clip nicht vor — ⛔ keine Zahl erfinden, die nicht gesagt wurde")
        first = set(toks(" ".join(s for _, s in sents[:2]))); H = set(toks(hook))
        if H and len(H & first) / len(H) >= 0.75:
            errs.append("Das ist fast sein erster Satz im Clip — der geschriebene Hook muss etwas hinzufügen: nimm die stärkste Zeile (suggest), nicht die erste")
    elif NO_WORDS: warns.append("--no-words: nicht geprüft, ob die Zahlen aus seinem Text stammen — prüf selbst")
    else: errs.append(f"Sein Text (caps.json/a.json) fehlt in {W} — ich kann nicht prüfen, ob die Zahlen aus seinem Text stammen. Richtigen Ordner angeben oder --words <Datei> (oder bewusst --no-words)")
    if not quiet:
        print(f"🪝 «{hook}» — {n} Wörter · Mittel: {' + '.join(dv) if dv else 'keine'}")
        for e in errs: print("  ❌", e)
        for w in warns: print("  ⚠️", w)
        if not errs: print("  ✅ passt" + (" — besser noch die Hinweise beheben" if warns else ""))
    return errs, warns, dv

def suggest(W):
    S = load_sentences(W)
    if not S: sys.exit("Weder caps.json noch a.json im Ordner gefunden – führe zuerst 02_captions.py (oder 20_episode_cuts.py) aus")
    rows = []
    for i, (t, s) in enumerate(S):
        T = toks(s); dv = devices(s); sc = 0.0
        sc += 3 * ("Zahl" in dv) + 2 * ("Widerspruch" in dv) + 2 * ("Frage" in dv) + 1.5 * ("Geschichte" in dv) + 1 * ("Neugier" in dv) + 1 * ("Befehl" in dv)
        sc += 1.2 * sum(t2 in HOT for t2 in T)
        sc -= 0.6 * sum(t2 in ("also", "äh", "ähm", "okay", "ja", "naja", "halt", "eben", "quasi", "irgendwie") for t2 in T)
        if len(T) < 3: sc -= 1.5
        if i + 1 < len(S) and nums_in(S[i + 1][1]) and not nums_in(s): sc += 0.5      # سطر قبل رقم = إعداد
        rows.append((sc, i, t, s, dv))
    print(f"Sein erster Satz (nicht als Hook kopieren): „{S[0][1]}“\n\nDie stärksten Zeilen für den Hook (Bewertung · Zeit · Mittel):")
    seen = {}                                   # السطر المكرر (الهوك الصوتي يعيد جملة من الوسط) يطلع مرة وحدة بأوقاته كلها
    for sc, i, t, s, dv in sorted(rows, reverse=True):
        k = " ".join(toks(s))
        if k in seen: seen[k]["ts"].append(t); continue
        seen[k] = {"sc": sc, "i": i, "ts": [t], "s": s, "dv": dv}
    for r in sorted(seen.values(), key=lambda r: -r["sc"])[:8]:
        i = r["i"]; ctx = (S[i + 1][1] if i + 1 < len(S) else "")
        ts = " و".join(f"{x:.2f}" for x in sorted(r["ts"]))
        print(f"  {r['sc']:4.1f}  {ts}s  [{' + '.join(r['dv']) or '—'}]  „{r['s']}“" + (f"  ← danach „{ctx}“" if ctx else ""))
    nums = sorted(nums_in(" ".join(s for _, s in S)))
    print(f"\nDie Zahlen, die er gesagt hat (nur diese darfst du verwenden): {', '.join(map(str, nums)) or 'keine Zahl'}")
    print("\nSchreib 3 Hooks nach den Formeln (references/podcast-hook.md) – Zahl + Widerspruch · die peinliche Frage · Neugier · der gegenläufige Befehl · Geschichte im halben Satz – dann:\n"
          f"  python3 {os.path.basename(__file__)} check {W} \"هوك 1\" \"هوك 2\" \"هوك 3\"")

def inject(W):
    shutil.copy(os.path.join(SC, "hook-card.js"), os.path.join(W, "hook-card.js"))
    ch = os.path.join(W, "compose.html")
    if os.path.exists(ch):
        h = open(ch).read()
        if 'src="hook-card.js"' not in h:
            i = h.rfind("</body>")
            h = (h[:i] + '<script src="hook-card.js"></script>\n' + h[i:]) if i >= 0 else h + '\n<script src="hook-card.js"></script>\n'
            open(ch, "w").write(h)
        return "compose.html"
    if os.path.exists(os.path.join(W, "cams.json")): return "كاميرات (16_render_pod.js يركّبه وحده)"
    return None

def theme_rw(W, fn):
    p = os.path.join(W, "theme.json"); th = json.load(open(p)) if os.path.exists(p) else {}
    fn(th); json.dump(th, open(p, "w"), ensure_ascii=False, indent=1); return th

def hook_cfg(a, hook):
    n = len([w for w in re.split(r"[\s|]+", hook.replace("…", " ").replace("*", "")) if w.strip(PUNCT)])
    dur = a.dur or round(min(3.0, max(1.6, 0.9 + 0.28 * n)), 2)
    cfg = {"text": hook, "dur": dur, "pos": a.pos, "style": a.style}
    if a.kicker: cfg["kicker"] = a.kicker.translate(HIND)
    if a.em: cfg["em"] = [e.translate(HIND) for e in a.em]
    if getattr(a, "keep_caps", False): cfg["keepCaps"] = True
    return cfg

def apply(W, a):
    hook = a.hook.translate(HIND).strip()
    errs, warns, dv = check(W, hook)
    if errs and not a.force: sys.exit("⛔ Nicht angewendet – behebe die Fehler oben (oder --force, wenn du sicher bist)")
    cfg = hook_cfg(a, hook); dur = cfg["dur"]
    theme_rw(W, lambda th: th.__setitem__("hook", cfg))
    where = inject(W)
    print(f"✓ Der Hook ist eingebaut ({dur} s · {a.pos} · {a.style}) – " + (where or "Noch keine compose.html gefunden – normal: 04_render_frames.js baut ihn beim Rendern selbst ein"))
    pj = os.path.join(W, "plan.json")
    if os.path.exists(pj):
        q = [x for x in json.load(open(pj)).get("scenes", []) if x.get("m") == "QUOTE" and x["s"] < dur + 0.3]
        if q: print(f"  ⚠️ „Die große Frage“ beginnt bei {q[0]['s']:.1f}s – unter dem Hook (sie schaltet sich in dieser Zeit ab, ihre ersten Wörter gehen verloren). "
                    "أعد `15_podcast.py plan` — الحين يختار سؤالاً بعد الهوك")
    print(f"  Vorschau: python3 {os.path.basename(__file__)} preview {W}")
    rj = "16_render_pod.js" if os.path.exists(os.path.join(W, "cams.json")) else "04_render_frames.js"
    print(f"  Reel schon gerendert? Rendere nur das Hook-Fenster: node {rj} {W} range 0 {dur + 0.5:.1f}  dann wie gewohnt zusammenbauen")

def sheet(files, labels, out):
    """ورقة وحدة من اللقطات — بـPIL لو موجود (مع وسم الوقت)، وإلا ffmpeg (بلا وسم — الترتيب مطبوع بالطرفية)."""
    try:
        from PIL import Image, ImageDraw
        ims = []
        for f, lb in zip(files, labels):
            im = Image.open(f).convert("RGB").resize((360, 640)); d = ImageDraw.Draw(im)
            d.rectangle([0, 0, 92, 34], fill=(0, 0, 0)); d.text((8, 8), lb, fill=(255, 255, 255)); ims.append(im)
        sh = Image.new("RGB", (360 * len(ims) + 8 * (len(ims) - 1), 640), (17, 17, 17))
        for i, im in enumerate(ims): sh.paste(im, (i * 368, 0))
        sh.save(out, quality=88)
    except ImportError:
        cmd = ["ffmpeg", "-v", "error", "-y"]
        for f in files: cmd += ["-i", f]
        fl = ";".join(f"[{i}:v]scale=360:640,setsar=1" + (",pad=368:640:0:0:0x111111" if i < len(files) - 1 else "") + f"[v{i}]" for i in range(len(files)))
        fl += ";" + "".join(f"[v{i}]" for i in range(len(files))) + f"hstack={len(files)}"
        subprocess.run(cmd + ["-filter_complex", fl, "-q:v", "3", out], check=True)
        print("  (ohne Pillow gibt es keine Zeitmarke – die Reihenfolge von links: " + " · ".join(labels) + ")")
    print("✓", out)

def preview(W):
    th = json.load(open(os.path.join(W, "theme.json"))); h = th.get("hook")
    if not h: sys.exit("Kein Hook in theme.json – führe zuerst apply aus")
    d = float(h.get("dur", 2.4)); ts = [0.0, 0.3, round(d * 0.7, 2), round(d + 0.4, 2)]
    cams = os.path.exists(os.path.join(W, "cams.json"))
    js = os.path.join(SC, "16_render_pod.js" if cams else "04_render_frames.js")
    subprocess.run(["node", js, W, "preview"] + [f"{t:.2f}" if not cams else str(t) for t in ts], check=True, stdout=subprocess.DEVNULL)
    files = [os.path.join(W, "prev", (f"t{t:.2f}.jpg" if not cams else str(t).replace(".", "_") + ".jpg")) for t in ts]
    sheet(files, [f"{t:.2f}s" for t in ts], os.path.join(W, "hook_sheet.jpg"))

# ── overlay: ريل مو من محرّكاتنا (خط المقابلة بدافنشي/لوتي · mp4 جاهز) ──
OVERLAY_JS = r"""
const [,, SC, OUT, CFGF, FPS] = process.argv; const fs=require('fs'), path=require('path'), {pathToFileURL}=require('url');
const C=JSON.parse(fs.readFileSync(CFGF,'utf8'));
function pupp(){ for(const p of [process.env.PUPPETEER_PATH,'puppeteer-core','puppeteer',path.join(process.cwd(),'node_modules/puppeteer-core'),path.join(SC,'..','node_modules','puppeteer-core'),path.join(SC,'..','..','node_modules','puppeteer-core')]){ if(!p) continue; try{return require(p);}catch(e){} } throw new Error('puppeteer-core nicht gefunden – führe 00_setup.sh aus'); }
function chrome(){ if(process.env.CHROME_PATH) return process.env.CHROME_PATH; const LA=process.env.LOCALAPPDATA||'', PF=process.env.ProgramFiles||'C:/Program Files', P86=process.env['ProgramFiles(x86)']||'C:/Program Files (x86)';
  for(const c of ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',PF+'/Google/Chrome/Application/chrome.exe',P86+'/Google/Chrome/Application/chrome.exe',LA+'/Google/Chrome/Application/chrome.exe',PF+'/Microsoft/Edge/Application/msedge.exe','/usr/bin/google-chrome','/usr/bin/chromium']) if(fs.existsSync(c)) return c; throw new Error('Chrome nicht gefunden – setze CHROME_PATH'); }
(async()=>{ const b=await pupp().launch({executablePath:chrome(),headless:'new',args:['--no-sandbox','--allow-file-access-from-files','--font-render-hinting=none','--force-color-profile=srgb']});
  const p=await b.newPage(); p.on('pageerror',e=>console.log('PAGEERR',e.message)); p.on('console',m=>{ if(m.type()==='error') console.log(m.text()); });
  await p.setViewport({width:1080,height:1920,deviceScaleFactor:1});
  const th=C.theme, font=th.font||'Inter';
  let ff=''; if(th.fontFiles) ff='<style>'+th.fontFiles.map(f=>"@font-face{font-family:'"+font+"';src:url('"+pathToFileURL(f.src).href+"');font-weight:"+(f.weight||400)+"}").join('')+'</style>';
  else ff='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family='+encodeURIComponent(font)+':wght@400;700;800;900&display=swap">';
  const html='<!doctype html><html dir="ltr"><head><meta charset="utf-8">'+ff+'<style>html,body{margin:0;background:transparent}</style></head><body><canvas id="cv" width="1080" height="1920"></canvas></body></html>';
  fs.writeFileSync(path.join(OUT,'.hook_overlay.html'),html);
  await p.goto(pathToFileURL(path.join(OUT,'.hook_overlay.html')).href,{waitUntil:'networkidle0'});
  await p.addScriptTag({path:path.join(SC,'hook-card.js')});
  await p.evaluate(async (h,t)=>{ HookCard.setup(h,t); await HookCard.ready(); },C.hook,th);
  const fps=+FPS, n=Math.ceil(C.hook.dur*fps), dir=path.join(OUT,'hook_frames'); fs.mkdirSync(dir,{recursive:true});
  for(const f of fs.readdirSync(dir)) fs.unlinkSync(path.join(dir,f));
  for(let i=0;i<n;i++){ const d=await p.evaluate(t=>{ const c=document.getElementById('cv'), x=c.getContext('2d'); x.setTransform(1,0,0,1,0,0); x.clearRect(0,0,1080,1920); HookCard.draw(t); return c.toDataURL('image/png'); }, i/fps);
    fs.writeFileSync(path.join(dir,String(i).padStart(5,'0')+'.png'),Buffer.from(d.split(',')[1],'base64')); }
  console.log('frames',n); await Promise.race([b.close(),new Promise(r=>setTimeout(r,8000))]); process.exit(0); })();
"""

def probe(v):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate",
                        "-of", "json", v], capture_output=True, text=True, check=True)
    st = json.loads(r.stdout)["streams"][0]; a, b = st["r_frame_rate"].split("/")
    return st["width"], st["height"], float(a) / float(b)

def overlay(OUT, a):
    os.makedirs(OUT, exist_ok=True)
    tp = a.theme or os.path.join(OUT, "theme.json")
    if not os.path.exists(tp): sys.exit(f"Theme ({tp}) nicht gefunden – gib --theme <theme.json> an (die Farben und die Schrift seiner Identität)")
    th = json.load(open(tp)); th.pop("hook", None); tdir = os.path.dirname(os.path.abspath(tp))
    if th.get("fontFiles"): th["fontFiles"] = [dict(f, src=os.path.join(tdir, f["src"])) for f in th["fontFiles"]]
    hook = a.hook.translate(HIND).strip()
    errs, warns, dv = check(OUT, hook)
    if errs and not a.force: sys.exit("⛔ Nicht ausgeführt – behebe die Fehler oben (oder --force, wenn du sicher bist)")
    cfg = hook_cfg(a, hook); cfg["pad"] = a.pad; cfg["surface"] = "video"
    vw = vh = None; fps = a.fps
    if a.video:
        vw, vh, vf = probe(a.video); fps = fps or vf
        if abs(vw / vh - 1080 / 1920) > 0.01: sys.exit(f"Das Video {vw}×{vh} ist nicht 9:16 – der Hook ist für 1080×1920 gestaltet")
    fps = fps or 30
    json.dump({"theme": th, "hook": cfg}, open(os.path.join(OUT, ".hook_overlay.json"), "w"), ensure_ascii=False)
    jsf = os.path.join(OUT, ".hook_overlay.js"); open(jsf, "w").write(OVERLAY_JS)
    subprocess.run(["node", jsf, SC, OUT, os.path.join(OUT, ".hook_overlay.json"), str(fps)], check=True)
    fr = os.path.join(OUT, "hook_frames", "%05d.png"); mov = os.path.join(OUT, "hook.mov")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", f"{fps:g}", "-i", fr, "-c:v", "prores_ks", "-profile:v", "4444",
                    "-pix_fmt", "yuva444p10le", mov], check=True)
    print(f"✓ {mov} – eine transparente Ebene von {cfg['dur']} s mit {fps:g} Frames: Leg sie auf die oberste Spur in DaVinci bei 0, und verzögere den ersten Untertitel bis {cfg['dur'] - 0.2:.1f}s (zwei Texte zusammen sind nicht lesbar)")
    if a.video:
        base = os.path.splitext(os.path.basename(a.video))[0]; outv = os.path.join(OUT, base + "_hook.mp4")
        fl = f"[1:v]scale={vw}:{vh},format=rgba[o];[0:v][o]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-framerate", f"{fps:g}", "-i", fr, "-filter_complex", fl,
                        "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "copy",
                        "-movflags", "+faststart", outv], check=True)
        print(f"✓ {outv} – ⚠️ Die in das Original-Reel eingebrannten Untertitel bleiben unter dem Hook (ich kann sie aus einer fertigen mp4 nicht entfernen) – deshalb ist der Standard mid zwischen Gesicht und Untertitel")
        d = cfg["dur"]; ts = [0.0, 0.3, round(d * 0.7, 2), round(d + 0.4, 2)]; files = []
        for t in ts:
            f = os.path.join(OUT, f".sh_{t:.2f}.jpg"); files.append(f)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", outv, "-frames:v", "1", f], check=True)
        sheet(files, [f"{t:.2f}s" for t in ts], os.path.join(OUT, "hook_sheet.jpg"))
        for f in files: os.remove(f)

def args_for(kind, argv):
    ap = argparse.ArgumentParser(prog=f"22_hook.py {kind}"); ap.add_argument("hook"); ap.add_argument("--dur", type=float)
    ap.add_argument("--pos", default="mid" if kind == "overlay" else "auto", choices=["auto", "top", "mid", "low"])
    ap.add_argument("--style", default="bold", choices=["bold", "card"]); ap.add_argument("--kicker"); ap.add_argument("--em", action="append")
    ap.add_argument("--force", action="store_true")
    if kind == "apply": ap.add_argument("--keep-caps", action="store_true")
    else:
        ap.add_argument("--theme"); ap.add_argument("--video"); ap.add_argument("--fps", type=float)
        ap.add_argument("--pad", type=int, default=150, help="ارتفاع تلاشي الظل فوق وتحت النص (px)")
    return ap.parse_args(argv)

if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--no-words" in argv: argv.remove("--no-words"); NO_WORDS = True
    if "--words" in argv:
        k = argv.index("--words"); WORDS = os.path.abspath(argv[k + 1]); del argv[k:k + 2]
        if not os.path.exists(WORDS): sys.exit(f"⛔ Die Sprachdatei {WORDS} existiert nicht")
    if len(argv) < 2: sys.exit(__doc__)
    cmd, W = argv[0], os.path.abspath(argv[1])
    if cmd != "overlay" and not os.path.isdir(W): sys.exit(f"⛔ Ordner {W} existiert nicht – gib den Arbeitsordner des Reels an (mit caps.json)")
    if cmd == "suggest": suggest(W)
    elif cmd == "check":
        if len(argv) < 3: sys.exit("Gib mindestens einen Hook zwischen Anführungszeichen an")
        bad = 0
        for h in argv[2:]: bad += bool(check(W, h)[0]); print()
        sys.exit(1 if bad else 0)
    elif cmd == "apply": apply(W, args_for("apply", argv[2:]))
    elif cmd == "overlay": overlay(W, args_for("overlay", argv[2:]))
    elif cmd == "preview": preview(W)
    elif cmd == "off": theme_rw(W, lambda th: th.pop("hook", None)); print("✓ Der Hook wurde entfernt (hook-card.js bleibt, zeichnet aber nichts)")
    else: sys.exit(__doc__)

#!/bin/bash
# فحص وتجهيز الأدوات.  ./00_setup.sh          → يفحص ويقول وش ناقص
#                      ./00_setup.sh --install → ينزّل الناقص (بعد إذن المستخدم)
#                      ./00_setup.sh --extras  → الإضافات الاختيارية: تنظيف صوت ذكي · نبض · بحث بالمعنى
# ✏️ معدّل ليشتغل على ويندوز وماك ولينكس. الأصل الماكي محفوظ بـ00_setup.sh.mac-orig
. "$(dirname "$0")/_compat.sh"
INSTALL=0; [ "$1" = "--install" ] && INSTALL=1
MISS=(); OK=(); NOTE=()
have(){ command -v "$1" >/dev/null 2>&1; }
line(){ printf '%s\n' "$1"; }

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) OS=win ;;
  Darwin) OS=mac ;;
  *) OS=linux ;;
esac
SKILL="$(abspath "$(dirname "$0")/..")"
# ☁️ بيئة سحابية / جوال (6 أكتوبر 2026 — قرار ماجد: ما فيه «ما يصير»): بدل ما نوقف، ننبّه ونكمّل بالمسار البديل.
#    هنا تنزيل موديل وِسبر الأصلي قد يكون محجوب وما فيه واجهة، فنستخدم السلّم بـreferences/any-environment.md
#    (faster-whisper · MODNet · كروم بلا واجهة + ffmpeg). الجلسة الأولى على الجوال أثبتت إنه يشتغل.
if [ "$OS" = linux ] && { [ -n "$CLAUDE_SANDBOX" ] || [ ! -d /Applications ]; } && ! curl -sI -m 8 https://openaipublic.azureedge.net >/dev/null 2>&1; then
  echo "☁️ Cloud-Umgebung (Handy/Web): Das originale Whisper ist hier gesperrt – wir machen mit Alternativen weiter: faster-whisper zum Transkribieren, MODNet zur Freistellung, Chrome ohne Oberfläche zum Zeichnen."
  echo "   Lies references/any-environment.md. Nicht anhalten und dem Nutzer nicht sagen „das geht nicht“."
  CLOUD=1
fi

# 🔄 تحديث تلقائي (v2.9): نقارن VERSION المحلي بآخر إصدار على قت هب بصمت (5 ثوانٍ كحد أقصى).
#    لو فيه أحدث: نطبع سطراً واحداً — وكلود يسأل المستخدم ثم يشغّل: bash scripts/00_setup.sh --update
SKROOT="$(cd "$(dirname "$0")/.." && pwd)"; LOCALV="$(cat "$SKROOT/VERSION" 2>/dev/null || echo 0)"
# v4: لو السكل منصّب كـplugin (majed-video) التحديث يكون من مدير الإضافات — مو بالاستبدال اليدوي
case "$SKROOT" in */.claude/plugins/*) PLUGIN=1 ;; *) PLUGIN=0 ;; esac
# Updates kommen aus dem Viralio-Marketplace. Für Installationen ohne Plugin: VAE_UPDATE_REPO="<owner>/<repo>" (GitHub-Releases mit video-ad-editor.skill) setzen, sonst bleibt die automatische Prüfung aus.
UPDATE_REPO="${VAE_UPDATE_REPO:-}"
PLUG_UPD="claude plugin marketplace update viralio-plugins && claude plugin update viralio-video@viralio-plugins"
if [ "$1" = "--update" ] && [ "$PLUGIN" = 1 ]; then
  echo "ℹ️ Der Skill ist als Plugin installiert – führe aus: $PLUG_UPD  (dann eine neue Sitzung öffnen)"; exit 0
fi
if [ "$1" = "--update" ]; then
  TMP="$(mktemp -d)"; echo "⬇️ Lade die neueste Version herunter…"
  if [ -n "$UPDATE_REPO" ] && curl -sL -m 120 -o "$TMP/skill.zip" "https://github.com/$UPDATE_REPO/releases/latest/download/video-ad-editor.skill" \
     && unzip -q -o "$TMP/skill.zip" -d "$TMP/x" && [ -f "$TMP/x/video-ad-editor/SKILL.md" ]; then
    rsync -a --delete --exclude=bin --exclude=hdr2sdr --exclude=personmask --exclude=facetrack --exclude=node_modules "$TMP/x/video-ad-editor/" "$SKROOT/" \
      && echo "✅ Skill aktualisiert auf v$(cat "$SKROOT/VERSION" 2>/dev/null) – arbeite normal weiter" || echo "⚠️ Konnte die Dateien nicht ersetzen"
  else echo "⚠️ Kein Update-Ziel gesetzt oder Download fehlgeschlagen (VAE_UPDATE_REPO)."; fi
  rm -rf "$TMP"; exit 0
fi
LATEST=""; [ -n "$UPDATE_REPO" ] && LATEST="$(curl -sL -m 5 "https://api.github.com/repos/$UPDATE_REPO/releases/latest" 2>/dev/null | sed -n 's/.*"tag_name": *"v\([0-9.]*\)".*/\1/p' | head -1)"
if [ -n "$LATEST" ] && [ "$LATEST" != "$LOCALV" ] && [ "$(printf '%s\n%s' "$LOCALV" "$LATEST" | sort -V | tail -1)" = "$LATEST" ]; then
  if [ "$PLUGIN" = 1 ]; then
    echo "🆕 Es gibt eine neuere Version des Skills: v$LATEST (du hast v$LOCALV) – frag den Nutzer, und bei Zustimmung führe aus: $PLUG_UPD  (dann eine neue Sitzung)"
  else
    echo "🆕 Es gibt eine neuere Version des Skills: v$LATEST (du hast v$LOCALV) – frag den Nutzer, und bei Zustimmung führe aus: bash scripts/00_setup.sh --update"
  fi
fi

# ➕ الإضافات (v3.9، أفكار Palmier) — اختيارية، السكل يشتغل بدونها وكل وحدة ترجع للطريق القديم لو ناقصة:
#    ‹deep-filter› تنظيف صوت ذكي (02c) · ‹transformers› البحث بالمعنى (26)
# 🆕 6.0: pip القديم (قبل 23) ما يعرف --break-system-packages — كان يطلّع «no such option» ويفشل التنصيب.
#    نجرّب عادي ← لو pip يعرف الخيار نجرّبه ← وإلا --user (يشتغل بكل نسخ pip وبلا صلاحيات مدير).
pip_in(){ "$PY" -m pip install --quiet "$@" 2>/dev/null && return 0
  if "$PY" -m pip install --help 2>/dev/null | grep -q -- '--break-system-packages'; then
    "$PY" -m pip install --quiet --break-system-packages "$@" && return 0
  fi
  "$PY" -m pip install --quiet --user "$@"; }
extras_status(){
  local e=()
  { [ -x "$SKILL/bin/deep-filter" ] || [ -x "$SKILL/bin/deep-filter.exe" ] || have deep-filter; } && e+=("Tonreinigung✅") || e+=("Tonreinigung—")
  "$PY" -c "import transformers,PIL" 2>/dev/null && e+=("Bedeutungssuche✅") || e+=("Bedeutungssuche—")
  echo "${e[*]}"
}
if [ "$1" = "--extras" ]; then
  pipx2(){ pip_in "$@"; }
  mkdir -p "$SKILL/bin"
  DFV=0.5.6
  case "$OS-$(uname -m)" in
    mac-arm64)          T=aarch64-apple-darwin ;;
    mac-x86_64)         T=x86_64-apple-darwin ;;
    win-*)              T=x86_64-pc-windows-msvc.exe ;;
    linux-x86_64)       T=x86_64-unknown-linux-musl ;;
    *)                  T="" ;;
  esac
  DF="$SKILL/bin/deep-filter"; [ "$OS" = win ] && DF="$DF.exe"
  if [ -n "$T" ] && [ ! -x "$DF" ]; then
    line "⏬ Intelligente Tonreinigung (DeepFilterNet3, ~20 MB)…"
    if curl -sfL -m 180 -o "$DF" "https://github.com/Rikorose/DeepFilterNet/releases/download/v$DFV/deep-filter-$DFV-$T" \
       && [ "$(wc -c < "$DF")" -gt 1000000 ]; then
      chmod +x "$DF"; [ "$OS" = mac ] && xattr -d com.apple.quarantine "$DF" 2>/dev/null
      "$DF" --help >/dev/null 2>&1 && line "   ✅ Bereit" || { rm -f "$DF"; line "   ⚠️ Geladen, läuft aber nicht – es bleibt beim normalen ffmpeg-Filter"; }
    else rm -f "$DF"; line "   ⚠️ Konnte es nicht laden – es bleibt beim normalen ffmpeg-Filter"; fi
  fi
  "$PY" -c "import torch" 2>/dev/null || { line "⏬ torch (Grundlage der Modelle)…"; pipx2 torch; }
  "$PY" -c "import transformers,PIL" 2>/dev/null || { line "⏬ Bedeutungssuche (transformers – das Modell von ~1,5 GB wird bei der ersten Suche geladen)…"; pipx2 "transformers>=4.49" pillow sentencepiece protobuf || line "   ⚠️ Fehlgeschlagen"; }
  line "Zusätze: $(extras_status)"
  exit 0
fi

have ffmpeg  && OK+=("ffmpeg")  || MISS+=("ffmpeg")
have ffprobe && OK+=("ffprobe") || MISS+=("ffprobe")
"$PY" -c "import whisper" 2>/dev/null && OK+=("whisper") || MISS+=("whisper")
"$PY" -c "import numpy"   2>/dev/null && OK+=("numpy")   || MISS+=("numpy")

# كروم: نفس ترتيب البحث اللي بالسكربتات
find_chrome(){
  [ -n "$CHROME_PATH" ] && [ -f "$CHROME_PATH" ] && { echo "$CHROME_PATH"; return 0; }
  local c
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "${ProgramFiles:-C:/Program Files}/Google/Chrome/Application/chrome.exe" \
           "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
           "${LOCALAPPDATA:-}/Google/Chrome/Application/chrome.exe" \
           "${ProgramFiles:-C:/Program Files}/Microsoft/Edge/Application/msedge.exe" \
           /usr/bin/google-chrome /usr/bin/chromium /usr/bin/chromium-browser; do
    [ -f "$c" ] && { echo "$c"; return 0; }
  done; return 1
}
CHROME="$(find_chrome)" && OK+=("chrome") || MISS+=("chrome")

# puppeteer-core: يُبحث عنه من مجلد السكل نفسه (هناك ينزّل)
( cd "$SKILL" && node -e "require.resolve('puppeteer-core')" ) 2>/dev/null \
  && OK+=("puppeteer-core") || MISS+=("puppeteer-core")

line "System: $OS · Python: $PY"
[ -n "$CHROME" ] && line "Chrome: $CHROME"
line "Bereit: ${OK[*]:-nichts}"
line "Zusätze (optional – 00_setup.sh --extras): $(extras_status)"
if have npm; then line "Die zweite Engine (Remotion): auf Wunsch verfügbar – 04b_remotion.sh setup lädt sie (~500 MB)"
else line "Die zweite Engine (Remotion): braucht npm – nicht verfügbar, die leichte genügt"; fi
[ "$OS" = mac ] || NOTE+=("Der Effekt „Sprache hinter der Person“ (11_behind_text.js) läuft nur auf dem Mac – der Rest des Skills läuft normal")

if [ ${#MISS[@]} -eq 0 ]; then
  line "✅ Alles bereit – wir können anfangen."
  [ ${#NOTE[@]} -gt 0 ] && printf 'ℹ️  %s\n' "${NOTE[@]}"
  exit 0
fi
line "Es fehlt: ${MISS[*]}"
if [ $INSTALL -eq 0 ]; then line "Führe aus: $0 --install"; exit 10; fi

pipi(){ pip_in "$@"; }
for m in "${MISS[@]}"; do
  case "$m" in
    ffmpeg|ffprobe)
      [ "$m" = ffprobe ] && continue
      line "⏬ ffmpeg…"
      if   [ "$OS" = win ] && have winget; then winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements || NOTE+=("ffmpeg fehlgeschlagen – lade es von ffmpeg.org und füge es zum PATH hinzu")
      elif have brew;  then brew install ffmpeg || NOTE+=("ffmpeg fehlgeschlagen")
      elif have apt;   then sudo apt install -y ffmpeg || NOTE+=("ffmpeg fehlgeschlagen")
      else NOTE+=("Lade ffmpeg von Hand von ffmpeg.org und füge es zum PATH hinzu"); fi ;;
    whisper) line "⏬ openai-whisper… (das Modell wird beim ersten Start geladen, 1,4 GB)"
      pipi openai-whisper || NOTE+=("whisper fehlgeschlagen") ;;
    numpy)   pipi numpy || NOTE+=("numpy fehlgeschlagen") ;;
    puppeteer-core) line "⏬ puppeteer-core…"
      ( cd "$SKILL" && npm i --silent puppeteer-core ) || NOTE+=("puppeteer-core fehlgeschlagen") ;;
    chrome) NOTE+=("Chrome ist nicht installiert – lade es von google.com/chrome oder setze CHROME_PATH") ;;
  esac
done

FAIL=0
have ffmpeg || FAIL=1
"$PY" -c "import whisper,numpy" 2>/dev/null || FAIL=1
find_chrome >/dev/null || FAIL=1
( cd "$SKILL" && node -e "require.resolve('puppeteer-core')" ) 2>/dev/null || FAIL=1
[ ${#NOTE[@]} -gt 0 ] && printf '⚠️  %s\n' "${NOTE[@]}"
[ $FAIL -eq 0 ] && line "✅ Jetzt ist alles bereit." || { line "❌ Es fehlt noch etwas – sieh dir die Hinweise oben an."; exit 11; }

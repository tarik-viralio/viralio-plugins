<!-- Referenz für den Skill video-ad-editor – nur bei Bedarf lesen (Token sparen) -->

## 🪟 Den Skill auf Windows betreiben

Der Skill läuft seit v2.8 auf Windows (Git-Bash), mit Beitrag von thefhiter. `00_setup.sh` gibt in der ersten Zeile den richtigen Interpreter aus. Vier Unterschiede musst du kennen:

- **`python`, nicht `python3`** – Auf Windows ist `python3` eine Verknüpfung zum Microsoft Store und schlägt fehl.
  Die Shell-Skripte erkennen den Interpreter selbst (`scripts/_compat.sh`); die oben geschriebenen Python-Befehle ersetzt du durch `python`.
- **UTF-8** – Die Standardcodierung von Windows `cp1252` zerstört jede Ausgabe und Datei mit Umlauten oder Sonderzeichen.
  Alle Python-Skripte setzen UTF-8 gleich am Anfang, und die Shell-Skripte exportieren `PYTHONUTF8=1`.
- **Pfade** – `pwd` in Git-Bash liefert `/c/…`, und Python sieht das überhaupt nicht.
  Die Funktion `abspath` in `_compat.sh` liefert das native `C:/…` – **übergib den Arbeitsordner immer in dieser Form.**
- **Chrome** – wird automatisch erkannt (Chrome, dann Edge). Manuell festlegen: `export CHROME_PATH="…/chrome.exe"`.

**⛔ „Sprache hinter der Person“ (`11_behind_text.js`) läuft nicht auf Windows** – es braucht die Personen-Freistellung
des Mac-Systems (Vision + swiftc). Das Skript bricht mit einer klaren Meldung ab. **Alles andere läuft normal.**

Läuft Whisper nur auf dem Prozessor (torch ohne CUDA), nimm `--model small` statt `medium`.

**Nur Mac:** die drei Schnittstile (`references/cut-styles.md`) · der Podcast-Modus · der HDR-Konverter für iPhone-Videos.

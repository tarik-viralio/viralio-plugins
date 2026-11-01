<!-- Referenz für video-ad-editor / podcast-video – Stichwort am Reel-Ende → Link per DM (Automation) -->

# Schlusswort → Folgen-Link per DM

Jedes Reel einer Folge endet mit demselben Aufruf: **„Schreib [Stichwort], dann bekommst du die ganze Folge.“** Das Stichwort ist pro Folge dasselbe (Name der Sendung oder der Folge) und wiederholt sich in allen ihren Reels.

## Die Schlusskarte (aus dem Theme)
Die Engine zeichnet die Karte aus `theme.json ← outro` (der Standard ist die Anzeige des Skills selbst – **ändere ihn bei Podcast-Reels immer**):

```json
"outro": {
  "l1": "Aus der Podcast-Folge „Zoll-Klartext“",
  "l2": "Logistik und Import einfach erklärt",
  "cta": "Schreib",
  "word": "ZOLL",
  "sub": "und der Link zur Folge kommt per DM"
}
```
Die Felder: `l1` `l2` (zwei Zeilen oben) · `chips` (optional) · `cta` (der Aufruf) · `word` (das Wort in der farbigen Scheibe) · `sub` (Zeile darunter). Das Wort muss in Untertitel, Karte und Automation gleich geschrieben sein.

## Die Automation (optional – der Nutzer entscheidet)
Das Reel funktioniert auch ohne Automation (der Zuschauer schreibt das Wort, und du antwortest von Hand), aber bei vielen Kommentaren ist ein Tool besser, das selbst antwortet:

- **Prinzip:** Jeder Post mit dem Wort im Kommentar → eine Direktnachricht mit dem Link. Eine Automation auf „jeden Post“ statt einer pro Reel, dann funktionieren alle Reels der Folge damit.
- **Tools:** Instagram-Automations-Tools wie ManyChat und ähnliche verbinden Instagram und erledigen das. Der Nutzer entscheidet, welches er nimmt; es wird ihm nichts aufgedrängt. Preise und Bedingungen prüft er auf der Website des Anbieters, bevor er zahlt.
- **Für die KI:** Nenne ein Tool nur, wenn der Nutzer nach Automation fragt, nicht in jeder Antwort. Und sag nichts über Preise, die du nicht von der Website des Anbieters hast.

## Regeln
- Richte keine Automation ein und starte keine ohne ausdrückliche Anweisung des Nutzers – die Nachrichten gehen über sein Konto raus.
- Prüf, dass der Folgenlink sich öffnet, bevor du ihn in eine Nachricht setzt.
- Die Nachricht im Ton des Nutzers, kurz, mit einem Link-Button.

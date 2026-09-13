"Wer die Bedürfnisse des Menschen erkennt und richtig handelt, der wird bald ein reicher Mann sein." – Walter B. Walser -

Um die Früchte Eure Arbeit in barer Münze ernten zu können, müsst ihr Eure Waren feil bieten. Hierfür stehen euch zwei Möglichkeiten zur Verfügung.

## Warenverkauf an die Stadt

Den Lagerbestand an Waren seht ihr an der Zahl unter dem Warensymbol. Ihr könnt Waren an die Stadt veräußern, indem ihr unterhalb der Zahl klickt. Ist der Mauszeiger unterhalb der 100er-Stelle, veräußert ihr 100 Stück. Ist er unter der 1.00er-Stelle, veräußert ihr alles, bis zu 1.000 Stück. So ist es möglich 
in Einer-, Zehner-, Hunderterschritten, usw. zu verkaufen. Dieses Prinzip gilt im ganzen Spiel.

Den Verkaufspreis eurer Waren seht ihr als gelbe Zahl im Kästchen eurer Werkstätten **( stimmt das ??? )**.

## Warenexport in andere Städte

Da knapper Waren in einer Stadt sind, desto höhere Verkaufspreise lassen sich erzielen. Verkauft eure Waren also immer dort, wo sie am nötigsten sind. Die Warennachfrage entnehmt ihr den _Stadtinformationen_.

Um Eure Waren an eine andere Stadt zu verkaufen, benötigt ihr eine Karawane.
Dies könnt ihr rechts unten mit einem Klick auf das Rädersymbol aufrufen.

Es gibt verschiedene Karawanenarten, die sich in folgenden Punkten unterscheiden:

**Karawanenparameter**

* Fixpreis: so viele Taler kostet es pauschal, um die Karawane zu beauftragen
* Preis / 100 Stück: so viel kostet der Transport je 100 Stück eurer Waren
* Verlässlichkeit: gibt an, wie hoch die Wahrscheinlichkeit für einen erfolgreichen Transport ist
* Sicherheit: gibt an, wie gut sich der Karawanenführer auskennt und somit Räubernester umgehen kann

Jede Karawanenart hat unterschiedliche Kosten und damit verbundene Vorteile.
Um eine Karawane für eure Exporte auszuwählen, schaltet mit dem Button _Weiter_ bis zur gewünschten Karawanenart durch. Wenn ihr die Karawanenansicht nun mit Rechtsklick verlasst, wird die letzte angezeigte Karawane für eure Exporte beauftragt.

Um dieser nun die zu exportierenden Waren zuzuordnen, müsst ihr auf dem Pergament, auf dem ihr die Produktionsaufträge erteilt, statt _Produzieren_ nun auf _Verkaufen_ oder auf _Permanenter Verkauf_ schalten.
Der dahinterstehende Text zeigt nun an, welche Waren, in welcher Menge an welche Stadt verkauft werden sollen.
Ihr könnt diese Parameter nun nach belieben ändern, indem ihr über oder unterhalb dieser so lange klickt, bis die gewünschten Mengen und Zielstädte angezeigt werden.
Am Ende steht zusammengefasst, welche Kosten für den Transport auf Basis der gewählten Karawanenart euch entstehen.

Während bei _Verkaufen_ der Parameter Menge jede Runde neu eingestellt werden muss, bleibt dies bei _Permanenter Verkauf_ für die nachfolgenden Runden fixiert.

Bedenkt beim Export in andere Grafschaften, dass zusätzlich auch noch Zollgebühren am Ende der Runde anfallen können. Je mehr Grafschaften Eure Karawane durchqueren muss, um so öfter werden Zollgebühren fällig.

## Karawanenarten

### Karawanenführer "Billiger gehts nicht"
* Fixpreis: 100 T
* Preis / 100 Stück: 100 T
* Verlässlichkeit: 100 %
* Sicherheit: 20 %

### Karawanenführer "Eure Waren verschwinden, während Euer Geldbeutel wächst"
* Fixpreis: 500 T
* Preis / 100 Stück: 75 T
* Verlässlichkeit: 100 %
* Sicherheit: 30 %

### Karawanenführer "Unser Angebot ist unübertroffen. Wir kennen alle Schleichwege."
* Fixpreis: 1.000 T
* Preis / 100 Stück: 50 T
* Verlässlichkeit: 100 %
* Sicherheit: 40 %

## Der Sättigungsrabatt

Der Preis, den eine Stadt zahlt, ist nicht fest – er sinkt, je mehr von einer Ware schon unverkauft in
ihrem Lager liegt. Maßstab ist der Jahresbedarf der Stadt: ein Zehntel ihrer Einwohnerzahl (mindestens
1). Für jeden vollen Jahresbedarf, der als Überhang im Lager liegt, fällt der Preis um 10 Prozentpunkte,
höchstens jedoch um 50 %:

```
Jahresbedarf = max(1, Einwohner / 10)
Abschlag     = min(50 %, Lagerbestand × 10 % / Jahresbedarf)
Marktpreis   = Grundpreis × (100 % − Abschlag) / 100
```

Eine Stadt mit 2.000 Einwohnern verbraucht demnach 200 Einheiten im Jahr; liegen dort 600 auf Lager,
sind das drei Jahresbedarfe und damit 30 % Abschlag. Zwei Dinge sind dabei zu beachten:

* **Der Abschlag hängt an der Einwohnerzahl.** Eine große Stadt verkraftet mehr Absatz, bevor der Preis
  fällt, als eine kleine – wohin Ihr verkauft, ist damit eine echte Entscheidung, nicht nur eine Frage
  der Entfernung.
* **Er kennt keinen Mindestpreis.** Anders als beim Grundpreis greift hier keine Preisuntergrenze – ein
  übersättigter Markt kann unter jeden Preis fallen, den die Warentabelle sonst nennt. Einzig der
  50-Prozent-Deckel begrenzt den Abschlag.

Sichtbar wird das an zwei Stellen im Stadtbildschirm: Ein Tooltip auf der Preiszeile rechnet Euch die
Sättigung in Worten vor (Grundpreis, Jahresverbrauch, gelagerte Menge und der daraus folgende Abschlag),
und die goldene Preiszahl selbst verblasst zunehmend, je näher der Abschlag seinem Deckel kommt – ein
verblasster Preis verrät die Sättigung also schon auf den ersten Blick, ohne dass Ihr dafür hovern
müsstet. Beim Export zeigt die Zielstadt in der Verkaufszeile dieselbe verblassende Färbung als Kontur um
die Zielstadt-Auswahl, samt Tooltip mit dem Hinweis, dass sich der Preis bis zur Abrechnung am Jahresanfang
noch bewegen kann.

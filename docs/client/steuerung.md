"Ordnung ist das halbe Leben." - Sprichwort -

## Die eine Geste, die (fast) alles schließt

Fast der gesamte Client kennt nur eine einzige Eingabeaktion, um einen Dialog zu schließen oder einen
Vorgang abzubrechen: einen Rechtsklick oder die Esc-Taste. Beide sind ein und dieselbe
Eingabeaktion (`ui_next_or_close`), auf die praktisch jeder Dialog im Spiel reagiert.

## Ausnahme: im Kontor

Im Kontor - dem Bildschirm Eurer Heimatstadt, von dem aus Ihr Euren Zug bestreitet - sind Rechtsklick
und Esc bewusst getrennt:

* Ein Rechtsklick auf einen freien Bereich beendet sofort Euren Zug.
* Die Esc-Taste öffnet stattdessen das Ingame-Menü.

Das Ingame-Menü bietet: Weiterspielen, Speichern, Laden, Optionen, den aktiven Spieler aus dem Spiel
werfen, Feedback bzw. einen Fehler melden sowie die Rückkehr ins Hauptmenü.

## Das Cheatfenster

Wurde beim Anlegen eines neuen Spiels der Cheatmodus aktiviert, öffnet die Taste **U** im Kontor ein
Cheatfenster. Darin lassen sich für den aktiven Spieler Taler und Ansehen setzen, Handelsrechte für
alle Rohstoffe freischalten sowie einzelne Aktionen auslösen (ein Kind bekommen, sofort altern, ein Amt
niederlegen oder übernehmen, ein Haus bauen, sich verklagen lassen). Ein mit aktivem Cheatmodus
gespieltes Spiel fließt weder in die Bestenliste noch in die spielübergreifende Profil-Statistik ein.

## Auflösung und Skalierung

Der Godot-Client zeichnet unabhängig von der tatsächlichen Fenstergröße immer auf eine feste
Entwurfsfläche von 1600 × 900 Bildpunkten; das Bild wird anschließend unter Beibehaltung des
Seitenverhältnisses auf das Fenster skaliert. Das Fenster startet im Vollbildmodus, lässt sich aber
unter [Optionen](optionen-und-ton.md) auf Fenstermodus umschalten.

Der alte WinForms-Client verlangte noch eine Mindestauflösung von 1024 × 768 - diese Angabe betrifft
den Godot-Client nicht mehr, da er unabhängig vom Fenster stets auf derselben 1600×900-Fläche
zeichnet.

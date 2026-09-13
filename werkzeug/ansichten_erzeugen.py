#!/usr/bin/env python3
"""Erzeugt werkzeug/ansichten.txt aus den oeffentlichen Dialogfeldern von Main.cs.

Main.cs liegt im Conspiratio.Godot-Repo, das hier nicht ausgecheckt ist (siehe
CLAUDE.md dort). Dieses Skript wird deshalb von Hand aufgerufen, wenn sich die
Dialogliste in Main.cs aendert; das Ergebnis wird eingecheckt, damit die
Vollstaendigkeits-Zusage in pruefe_ausgabe.py ohne den Godot-Checkout auskommt
und eine Aenderung an der Liste im Diff sichtbar wird.

Main.cs verdrahtet jeden Dialog als oeffentliches Feld nach der Konvention
"Feldname == Typname" (siehe Main.VerdrahteKnoten):

    public LocalGameDialog LocalGameDialog;

Genau solche Zeilen werden erfasst. Die beiden generischen Dialoge YesNoDialog
und TextDialog sind in Main.cs bewusst *keine* Felder mehr (nur lokale
Variablen in _Ready, siehe der Kommentar dort) und tauchen deshalb hier gar
nicht erst auf - sie brauchen keine Ausnahme in ansichten.txt.

Bestehende "# Name - ..."-Ausnahmezeilen in ansichten.txt bleiben beim erneuten
Lauf erhalten, solange das zugehoerige Feld noch in Main.cs existiert - die
Begruendungen sind von Hand gepflegt und nicht aus dem Code ableitbar. Ein Feld,
das aus Main.cs verschwunden ist, wird mit einem Hinweis auf der Konsole
gemeldet und aus der Datei entfernt.

Aufruf: python werkzeug/ansichten_erzeugen.py <Pfad-zu-Main.cs>
"""
from __future__ import annotations

import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "werkzeug" / "ansichten.txt"

# "public LocalGameDialog LocalGameDialog;" - Typ- und Feldname muessen gleich
# sein (die Verdrahtungskonvention), sonst ist es kein auto-verdrahteter Dialog.
FELD_MUSTER = re.compile(r"^\s*public\s+(\w+)\s+(\w+)\s*;\s*$")

# Eine von Hand gepflegte Ausnahmezeile: "# Name - Begruendung".
AUSNAHME_MUSTER = re.compile(r"^#\s*(\w+)\s*-\s*(.+)$")


def lies_felder(pfad: pathlib.Path) -> list[str]:
    """Liest die oeffentlichen Dialogfelder aus Main.cs, in Deklarationsreihenfolge."""
    namen = []
    for zeile in pfad.read_text(encoding="utf-8").splitlines():
        treffer = FELD_MUSTER.match(zeile)
        if treffer and treffer.group(1) == treffer.group(2):
            namen.append(treffer.group(1))
    return namen


def lies_bestehende_ausnahmen(pfad: pathlib.Path) -> dict[str, str]:
    """Liest die bisherigen Ausnahme-Begruendungen aus ansichten.txt, falls vorhanden."""
    begruendungen: dict[str, str] = {}
    if not pfad.is_file():
        return begruendungen
    for zeile in pfad.read_text(encoding="utf-8").splitlines():
        treffer = AUSNAHME_MUSTER.match(zeile)
        if treffer:
            begruendungen[treffer.group(1)] = treffer.group(2)
    return begruendungen


def main() -> int:
    if len(sys.argv) != 2:
        print("Aufruf: python werkzeug/ansichten_erzeugen.py <Pfad-zu-Main.cs>")
        return 1

    haupt_datei = pathlib.Path(sys.argv[1])
    if not haupt_datei.is_file():
        print(f"FEHLER: {haupt_datei} nicht gefunden.")
        return 1

    felder = lies_felder(haupt_datei)
    if not felder:
        print(f"FEHLER: keine oeffentlichen Dialogfelder in {haupt_datei} gefunden.")
        return 1

    bestehend = lies_bestehende_ausnahmen(ZIEL)

    zeilen = [
        "# Diese Datei wird erzeugt aus den oeffentlichen Dialogfeldern von Main.cs",
        "# (Conspiratio.Godot-Repo, dort assets/scripts/Main.cs).",
        "# Neu erzeugen: python werkzeug/ansichten_erzeugen.py <Pfad-zu-Main.cs>",
        "#",
        "# Ausnahmen von Hand eintragen als \"# Name - Begruendung\" (komplette",
        "# Kommentarzeile) - sie werden beim erneuten Lauf am Namen wiedererkannt",
        "# und uebernommen, solange das Feld noch existiert.",
        "",
    ]
    for name in felder:
        if name in bestehend:
            zeilen.append(f"# {name} - {bestehend[name]}")
        else:
            zeilen.append(name)

    verworfen = sorted(set(bestehend) - set(felder))
    if verworfen:
        print("Hinweis: folgende Ausnahmen betreffen kein Feld mehr in Main.cs und wurden verworfen:")
        for name in verworfen:
            print(f"  - {name}")

    ZIEL.write_text("\n".join(zeilen) + "\n", encoding="utf-8", newline="")
    print(f"{len(felder)} Dialogfelder aus {haupt_datei.name} nach {ZIEL.relative_to(WURZEL)} geschrieben"
          f" ({len(bestehend)} bestehende Ausnahmen uebernommen).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

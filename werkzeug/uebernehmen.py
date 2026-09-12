#!/usr/bin/env python3
"""Uebernimmt die 24 Seiten des alten GitHub-Wikis ins neue MkDocs-Handbuch.

Kopiert die Wiki-Markdown-Dateien unter neuem, ASCII-slug-basiertem Namen nach
docs/, die neun Bilder aus images/ unveraendert nach docs/bilder/schreibstube/,
und schreibt dabei die Wiki-Verweise ([[...]], volle GitHub-Wiki-URLs) auf die
neuen relativen Pfade um. Der Wortlaut der Seiten selbst bleibt unangetastet -
das ist reine Uebernahme, keine inhaltliche Ueberarbeitung.

Aufruf: python werkzeug/uebernehmen.py
"""
from __future__ import annotations

import pathlib
import shutil

WURZEL = pathlib.Path(__file__).resolve().parent.parent
QUELLE = pathlib.Path(r"D:\Projekte\C# Projekte\Conspiratio.Wiki.wiki")
DOCS = WURZEL / "docs"

# Vollstaendige Zuordnung alter Wiki-Dateiname -> neuer Pfad unter docs/.
# ReadMe.md geht bewusst NICHT ueber - das uebernimmt Task 8 (Kapitel "Der Client").
ZUORDNUNG = {
    "1.-Hauptmenü.md": "hauptmenue/index.md",
    "2.-Schreibstube.md": "schreibstube/index.md",
    "2.1-Auf-ein-Amt-bewerben.md": "schreibstube/auf-ein-amt-bewerben.md",
    "2.1.1-Ämter.md": "schreibstube/aemter.md",
    "2.1.2-Privilegien.md": "schreibstube/privilegien.md",
    "2.2-Geldleiher-und-Kreditbuch.md": "schreibstube/geldleiher-und-kreditbuch.md",
    "2.3-Gesetze.md": "schreibstube/gesetze.md",
    "2.4-Kontrahenten.md": "schreibstube/kontrahenten.md",
    "2.5-Titel.md": "schreibstube/titel.md",
    "3.-Handel.md": "handel/index.md",
    "3.1-Grafschaften-und-Städte.md": "handel/grafschaften-und-staedte.md",
    "3.2-Stadtinformationen.md": "handel/stadtinformationen.md",
    "3.3-Städte,-Produktion-und-Wohnsitze.md": "handel/staedte-produktion-und-wohnsitze.md",
    "3.3.1-Wohnsitze.md": "handel/wohnsitze.md",
    "3.3.2-Produktion-von-Waren.md": "handel/produktion-von-waren.md",
    "3.3.3-Produktionsverhältnisse.md": "handel/produktionsverhaeltnisse.md",
    "3.3.4-Verkauf-und-Export-von-Waren.md": "handel/verkauf-und-export-von-waren.md",
    "4.-Hinterzimmer.md": "hinterzimmer/index.md",
    "5.-Kirche.md": "kirche/index.md",
    "6.-Söldner-&-Räuber.md": "soeldner-raeuber/index.md",
    "6.1-Räuberlager.md": "soeldner-raeuber/raeuberlager.md",
    "6.2-Zollburgen.md": "soeldner-raeuber/zollburgen.md",
    "999---Privilegien.md": "schreibstube/privilegienliste.md",
}

# Die neun Bilder aus images/ (Aemtertafeln) - unveraendert nach docs/bilder/schreibstube/.
BILDER = [
    "LandaemterKirch.png",
    "LandaemterMil.png",
    "LandaemterPolit.png",
    "ReichaemterKirch.png",
    "ReichaemterMil.png",
    "ReichaemterPolit.png",
    "StadtaemterKirch.png",
    "StadtaemterMil.png",
    "StadtaemterPolit.png",
]
BILDER_ZIEL = DOCS / "bilder" / "schreibstube"


def lies(pfad: pathlib.Path) -> str:
    with open(pfad, "r", encoding="utf-8", newline="") as f:
        return f.read()


def schreibe(pfad: pathlib.Path, inhalt: str) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    with open(pfad, "w", encoding="utf-8", newline="") as f:
        f.write(inhalt)


def ersetze(s: str, alt: str, neu: str) -> str:
    assert alt in s, f"Anker nicht gefunden: {alt!r}"
    return s.replace(alt, neu)


def kopiere_bilder() -> None:
    BILDER_ZIEL.mkdir(parents=True, exist_ok=True)
    for name in BILDER:
        shutil.copyfile(QUELLE / "images" / name, BILDER_ZIEL / name)


def schreibe_verweise_um(alter_name: str, s: str) -> str:
    """Schreibt Wiki-Verweise der jeweiligen Seite auf die neuen relativen Pfade um."""

    if alter_name == "2.1.1-Ämter.md":
        # Bild-Wiki-Verweise [[/images/NAME.png|ALT]] -> Markdown-Bild auf
        # docs/bilder/schreibstube/NAME.png (aemter.md liegt selbst in docs/schreibstube/).
        for bildname in BILDER:
            alt_muster = f"[[/images/{bildname}"
            treffer_start = s.find(alt_muster)
            assert treffer_start != -1, f"Bildverweis nicht gefunden: {alt_muster!r}"
            treffer_ende = s.find("]]", treffer_start)
            assert treffer_ende != -1, f"Bildverweis nicht geschlossen: {alt_muster!r}"
            ganzer_verweis = s[treffer_start : treffer_ende + 2]
            _, _, rest = ganzer_verweis[2:-2].partition("|")
            alt_text = rest
            neuer_verweis = f"![{alt_text}](../bilder/schreibstube/{bildname})"
            s = ersetze(s, ganzer_verweis, neuer_verweis)

    if alter_name == "2.1-Auf-ein-Amt-bewerben.md":
        # Volle GitHub-Wiki-URLs -> relative Pfade im neuen Handbuch.
        s = ersetze(
            s,
            "[Ämter](https://github.com/Conspiratio/Conspiratio.Wiki/wiki/2.1.1-%C3%84mter)",
            "[Ämter](aemter.md)",
        )
        s = ersetze(
            s,
            "[Privilegien](https://github.com/Conspiratio/Conspiratio.Wiki/wiki/2.1.2-Privilegien)",
            "[Privilegien](privilegien.md)",
        )
        s = ersetze(
            s,
            "[Hinterzimmer](https://github.com/Conspiratio/Conspiratio.Wiki/wiki/4.-Hinterzimmer)",
            "[Hinterzimmer](../hinterzimmer/index.md)",
        )

    return s


def main() -> None:
    for alter_name, neuer_pfad in ZUORDNUNG.items():
        s = lies(QUELLE / alter_name)
        s = schreibe_verweise_um(alter_name, s)
        schreibe(DOCS / neuer_pfad, s)
        print(f"{alter_name} -> docs/{neuer_pfad}")

    kopiere_bilder()
    print(f"{len(BILDER)} Bilder -> docs/bilder/schreibstube/")


if __name__ == "__main__":
    main()

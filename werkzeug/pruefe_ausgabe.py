#!/usr/bin/env python3
"""Prueft die gebaute Ausgabe unter site/ - nicht die Quellen.

Tritt an die Stelle der Tests, die es fuer eine statische Seite sonst nicht
gaebe, und laeuft auch in CI: Ein Fehler verhindert die Veroeffentlichung.

Eine neue Zusage ist eine Funktion mit @pruefung-Dekorator; sie ruft
pruefe(bedingung, meldung). Meldungen bleiben ASCII.

Aufruf: python werkzeug/pruefe_ausgabe.py
"""
from __future__ import annotations

import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).resolve().parent.parent
AUSGABE = WURZEL / "site"

_pruefungen = []
_meldungen: list[str] = []


def pruefung(funktion):
    """Meldet eine Funktion als Zusage an."""
    _pruefungen.append(funktion)
    return funktion


def pruefe(bedingung: bool, meldung: str) -> None:
    """Haelt einen Verstoss fest, ohne den Lauf abzubrechen."""
    if not bedingung:
        _meldungen.append(meldung)


def lies(pfad: pathlib.Path) -> str:
    return pfad.read_text(encoding="utf-8")


def seiten() -> list[pathlib.Path]:
    return sorted(AUSGABE.rglob("*.html"))


@pruefung
def pruefe_eigenes_stylesheet_eingebunden() -> None:
    """Ohne das eigene Stylesheet saehe das Handbuch aus wie Material von der Stange."""
    for seite in seiten():
        inhalt = lies(seite)
        pruefe(
            "stylesheets/conspiratio.css" in inhalt,
            f"{seite.relative_to(AUSGABE)}: bindet conspiratio.css nicht ein",
        )


@pruefung
def pruefe_keine_externen_schrift_oder_stilverweise() -> None:
    """Schriften liefern wir selbst aus - keine Google Fonts, keine fremden Stylesheets."""
    verboten = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net", "unpkg.com")
    for seite in seiten():
        inhalt = lies(seite)
        for muster in verboten:
            pruefe(
                muster not in inhalt,
                f"{seite.relative_to(AUSGABE)}: verweist auf {muster}",
            )


@pruefung
def pruefe_kein_bild_ohne_alternativtext() -> None:
    for seite in seiten():
        for treffer in re.finditer(r"<img\b[^>]*>", lies(seite)):
            marke = treffer.group(0)
            if 'role="presentation"' in marke:
                continue
            hat_alt = re.search(r'\balt="[^"]+"', marke) is not None
            pruefe(hat_alt, f"{seite.relative_to(AUSGABE)}: Bild ohne Alternativtext: {marke[:80]}")


@pruefung
def pruefe_keine_platzhalter() -> None:
    verboten = ("TODO", "TBD", "Lorem ipsum", "XXX", "FIXME")
    for seite in seiten():
        inhalt = lies(seite)
        for wort in verboten:
            pruefe(wort not in inhalt, f"{seite.relative_to(AUSGABE)}: enthaelt Platzhalter {wort}")


@pruefung
def pruefe_sprache_ist_deutsch() -> None:
    for seite in seiten():
        pruefe(
            'lang="de"' in lies(seite),
            f"{seite.relative_to(AUSGABE)}: ist nicht als deutsch ausgezeichnet",
        )


def main() -> int:
    if not AUSGABE.is_dir():
        print("FEHLER: site/ fehlt - erst 'mkdocs build' laufen lassen.")
        return 1

    for funktion in _pruefungen:
        funktion()

    for meldung in _meldungen:
        print("VERSTOSS: " + meldung)

    anzahl = len(_pruefungen)
    if _meldungen:
        print(f"{len(_meldungen)} Verstoesse bei {anzahl} Zusagen.")
        return 1

    print(f"{anzahl} Zusagen erfuellt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

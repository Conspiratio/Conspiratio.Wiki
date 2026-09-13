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
import urllib.parse

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
    """Schriften liefern wir selbst aus - keine Google Fonts, keine fremden Stylesheets.

    Geprueft wird nur, wo ein externer Verweis tatsaechlich wirksam wird: in
    <link>- und <script>-Marken sowie in @import-Regeln. Eine blosse Erwaehnung
    der Domaene im Fliesstext (etwa in einer Erklaerung, was wir NICHT nutzen)
    ist kein Verstoss.
    """
    verboten = ("fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net", "unpkg.com")
    wirkstellen = re.compile(
        r"<link\b[^>]*>|<script\b[^>]*>|@import\s+[^;]+;",
        re.IGNORECASE,
    )
    for seite in seiten():
        inhalt = lies(seite)
        for treffer in wirkstellen.finditer(inhalt):
            marke = treffer.group(0)
            for muster in verboten:
                pruefe(
                    muster not in marke,
                    f"{seite.relative_to(AUSGABE)}: verweist auf {muster}",
                )


@pruefung
def pruefe_kein_bild_ohne_alternativtext() -> None:
    """Jedes Bild braucht einen beschreibenden Alternativtext. Rein dekorative
    Bilder werden mit role="presentation" oder aria-hidden="true" ausgenommen;
    ein leeres alt allein genuegt hier absichtlich nicht.
    """
    for seite in seiten():
        for treffer in re.finditer(r"<img\b[^>]*>", lies(seite)):
            marke = treffer.group(0)
            if 'role="presentation"' in marke or 'aria-hidden="true"' in marke:
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


def _leuchtdichte(farbe: str) -> float:
    """Relative Leuchtdichte nach WCAG 2.1 fuer #rrggbb."""
    werte = []
    for teil in (farbe[1:3], farbe[3:5], farbe[5:7]):
        anteil = int(teil, 16) / 255
        werte.append(anteil / 12.92 if anteil <= 0.03928 else ((anteil + 0.055) / 1.055) ** 2.4)
    return 0.2126 * werte[0] + 0.7152 * werte[1] + 0.0722 * werte[2]


def _kontrast(vorne: str, hinten: str) -> float:
    a, b = _leuchtdichte(vorne), _leuchtdichte(hinten)
    hell, dunkel = max(a, b), min(a, b)
    return (hell + 0.05) / (dunkel + 0.05)


@pruefung
def pruefe_kontrast_beider_themen() -> None:
    """Die Farben werden aus dem CSS gelesen, nicht hier dupliziert."""
    css = lies(WURZEL / "docs" / "stylesheets" / "conspiratio.css")
    for thema, grund_name, schrift_name, leise_name in (
        ("hell", "--grund", "--schrift", "--schrift-leise"),
        ("dunkel", "--grund-dunkel", "--schrift-dunkel", "--schrift-leise-dunkel"),
    ):
        farben = {}
        for name in (grund_name, schrift_name, leise_name):
            treffer = re.search(rf"{name}:\s*(#[0-9a-fA-F]{{6}})", css)
            pruefe(treffer is not None, f"Thema {thema}: Farbe {name} steht nicht im CSS")
            if treffer:
                farben[name] = treffer.group(1)
        if len(farben) == 3:
            pruefe(
                _kontrast(farben[schrift_name], farben[grund_name]) >= 4.5,
                f"Thema {thema}: Fliesstext erreicht 4.5:1 nicht",
            )
            pruefe(
                _kontrast(farben[leise_name], farben[grund_name]) >= 4.5,
                f"Thema {thema}: leise Schrift erreicht 4.5:1 nicht",
            )


def _basis_pfad() -> str:
    """Der URL-Pfad-Anteil von site_url in mkdocs.yml, z.B. "/Conspiratio.Wiki".

    Wird aus mkdocs.yml gelesen statt fest eingetragen, damit die Zusage nicht
    bricht, sobald sich die Adresse aendert (etwa bei einer eigenen Domain).
    Kein YAML-Parser noetig - site_url steht als einzelne, einfache Zeile da.
    """
    text = (WURZEL / "mkdocs.yml").read_text(encoding="utf-8")
    treffer = re.search(r"^site_url:\s*(\S+)\s*$", text, re.MULTILINE)
    if not treffer:
        return ""
    return urllib.parse.urlparse(treffer.group(1)).path.rstrip("/")


@pruefung
def pruefe_keine_toten_internen_verweise() -> None:
    """Wurzelabsolute Hrefs (z.B. in der von MkDocs erzeugten 404.html, die aus
    jeder Tiefe ausgeliefert wird) tragen den Basispfad aus site_url voran und
    werden dagegen aufgeloest, nicht gegen den Dateisystemstamm. Ein
    wurzelabsoluter Href ohne diesen Basispfad ist weiterhin ein Verstoss.
    """
    basis = _basis_pfad()
    for seite in seiten():
        for ziel in re.findall(r'href="([^"#?]+)', lies(seite)):
            if ziel.startswith(("http://", "https://", "mailto:", "data:", "//")):
                continue
            if ziel.startswith("/"):
                if basis == "":
                    # Seite liegt im Wurzelverzeichnis einer eigenen Domain (site_url ohne
                    # Pfadanteil) - ein wurzelabsoluter Href meint dann direkt AUSGABE.
                    ohne_basis = ziel
                elif ziel == basis:
                    ohne_basis = "/"
                elif ziel.startswith(basis + "/"):
                    ohne_basis = ziel[len(basis):]
                else:
                    pruefe(
                        False,
                        f"{seite.relative_to(AUSGABE)}: wurzelabsoluter Verweis {ziel} "
                        f"beginnt nicht mit dem Basispfad {basis!r} aus site_url",
                    )
                    continue
                pfad = (AUSGABE / ohne_basis.lstrip("/")).resolve()
            else:
                pfad = (seite.parent / ziel).resolve()
            if pfad.is_dir():
                pfad = pfad / "index.html"
            pruefe(
                pfad.exists(),
                f"{seite.relative_to(AUSGABE)}: toter Verweis auf {ziel}",
            )


@pruefung
def pruefe_keine_wiki_syntax_uebriggeblieben() -> None:
    """Doppelte eckige Klammern sind Wiki-Verweise, die MkDocs nicht aufloest."""
    for seite in seiten():
        inhalt = lies(seite)
        pruefe("[[" not in inhalt, f"{seite.relative_to(AUSGABE)}: enthaelt unaufgeloeste Wiki-Verweise")


def _seite_zu_html(seite: str) -> pathlib.Path:
    """Bildet den docs/-Pfad einer Manifestzeile auf die von MkDocs gebaute Seite ab.

    MkDocs nutzt Verzeichnis-URLs: aus docs/a/b.md wird site/a/b/index.html, aus
    docs/a/index.md aber site/a/index.html (keine doppelte Verschachtelung).
    """
    pfad = pathlib.PurePosixPath(seite)
    if pfad.stem == "index":
        return AUSGABE / pfad.parent / "index.html"
    return AUSGABE / pfad.parent / pfad.stem / "index.html"


@pruefung
def pruefe_manifest_und_bilder_passen_zusammen() -> None:
    """Kein Manifesteintrag ohne Bild, kein Bild ohne Manifesteintrag, kein Bild,
    das seine Manifest-Seite zwar existiert, aber tatsaechlich nicht zeigt.

    Der dritte Teil prueft gegen die gebaute Seite unter site/, nicht gegen die
    Markdown-Quelle - genau wie jede andere Zusage hier. Ein Bild, dessen
    Manifestzeile auf eine Seite verweist, die es nie per ![]() einbindet, waere
    sonst ein "Waisenbild": aufbereitet und im Manifest gefuehrt, aber fuer den
    Leser nicht sichtbar.
    """
    import csv

    manifest = WURZEL / "werkzeug" / "manifest.tsv"
    with manifest.open(encoding="utf-8", newline="") as datei:
        zeilen = list(csv.DictReader(datei, delimiter="\t"))

    for zeile in zeilen:
        bild = WURZEL / "docs" / "bilder" / (zeile["Zielname"] + ".webp")
        pruefe(bild.is_file(), f"Manifest nennt {zeile['Zielname']}, das Bild fehlt")
        quelle = WURZEL / "docs" / zeile["Seite"]
        pruefe(quelle.is_file(), f"Manifest nennt Seite {zeile['Seite']}, die es nicht gibt")

        seite_html = _seite_zu_html(zeile["Seite"])
        if not seite_html.is_file():
            pruefe(
                False,
                f"Seite {zeile['Seite']} wurde nicht gebaut - erwartet unter "
                f"{seite_html.relative_to(AUSGABE)}",
            )
            continue
        pruefe(
            f"bilder/{zeile['Zielname']}.webp" in lies(seite_html),
            f"Bild {zeile['Zielname']} ist auf der Seite {zeile['Seite']} nicht eingebunden",
        )

    genannt = {z["Zielname"] for z in zeilen}
    for bild in (WURZEL / "docs" / "bilder").rglob("*.webp"):
        name = bild.relative_to(WURZEL / "docs" / "bilder").with_suffix("").as_posix()
        pruefe(name in genannt, f"Bild {name} steht in keinem Manifesteintrag")


@pruefung
def pruefe_keine_undokumentierte_ansicht() -> None:
    """Ein Dialog, den es im Client gibt und im Handbuch nicht, ist fehlende Doku.

    ansichten.txt wird aus den oeffentlichen Dialogfeldern von Main.cs erzeugt
    (werkzeug/ansichten_erzeugen.py) und im Handbuch-Repo mitgefuehrt, weil das
    Godot-Repo in CI nicht ausgecheckt ist. Eine Zeile ohne "#" muss im Manifest
    stehen; eine auskommentierte Zeile ("# Name - Begruendung") gilt als
    begruendet ausgenommen und wird uebersprungen.
    """
    import csv

    liste = WURZEL / "werkzeug" / "ansichten.txt"
    alle = {z.strip() for z in lies(liste).splitlines() if z.strip() and not z.startswith("#")}

    with (WURZEL / "werkzeug" / "manifest.tsv").open(encoding="utf-8", newline="") as datei:
        dokumentiert = {z["Ansicht"] for z in csv.DictReader(datei, delimiter="\t")}

    for ansicht in sorted(alle - dokumentiert):
        pruefe(False, f"Ansicht {ansicht} kommt im Handbuch nicht vor")


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

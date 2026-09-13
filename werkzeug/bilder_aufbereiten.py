#!/usr/bin/env python3
"""Bereitet die Bilder fuer das Handbuch auf.

Quellen:
  ernte - Conspiratio.Godot/docs/ansichten/*.png (Aufnahmen des E2E-Treibers)
  wiki  - Conspiratio.Wiki.wiki/images/*.png (Aemtertafeln des alten Wikis)
Ziel:   docs/bilder/<kapitel>/<name>.webp, 1000 px breit

Gesteuert von werkzeug/manifest.tsv. Dialoge werden auf das Pergament
zugeschnitten, Bildschirme und uebernommene Tafeln bleiben vollflaechig.

Ein Motiv ohne Alternativtext wird absichtlich NICHT aufbereitet.

Aufruf: python werkzeug/bilder_aufbereiten.py
"""
from __future__ import annotations

import csv
import pathlib
import sys

from PIL import Image

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ANSICHTEN = pathlib.Path(r"C:\Projekte\Godot\Conspiratio.Godot\docs\ansichten")
WIKI_BILDER = pathlib.Path(r"D:\Projekte\C# Projekte\Conspiratio.Wiki.wiki\images")
ZIEL = WURZEL / "docs" / "bilder"
MANIFEST = WURZEL / "werkzeug" / "manifest.tsv"
BREITE = 1000
SCHWELLE = 150      # ab dieser Helligkeit gilt ein Bildpunkt als Pergament

ALTERNATIVTEXTE = {
    "hauptmenue/hauptmenue": (
        "Das Hauptmenue mit dem Titel Conspiratio auf einem Schwert und den "
        "Knoepfen Lokales Spiel, Profile, Tutorial / Hilfe, Optionen, Credits, "
        "Bestenliste, Feedback & Fehler melden und Beenden"
    ),
    "hauptmenue/spiel-starten": (
        "Das Pergament mit den drei Optionen Spiel starten, Spiel laden und "
        "Spiel fortsetzen"
    ),
    "hauptmenue/neues-spiel": (
        "Das aufgeschlagene Buch Neues Spiel erstellen mit Spielname, Anzahl "
        "Spieler, Cheatmodus, Testmodus und Todesfaelle anzeigen links sowie "
        "Spielziel, Schwierigkeit und Aufgabe rechts"
    ),
    "hauptmenue/spieler-erstellen": (
        "Das aufgeschlagene Buch zur Spielererstellung mit Spielername, "
        "Geschlecht, Religion und der Bannerauswahl links sowie Heimatstadt, "
        "Rohstoff und Profil rechts"
    ),
    "handel/weltkarte": (
        "Die Landkarte des Koenigreiches mit den vier Grafschaften Meadowvalley, "
        "Wattern, Granitland und Redcoast und ihren Staedten"
    ),
    "handel/stadt": (
        "Der Stadtbildschirm von Crowbrigde mit den sechs leeren Kaestchen fuer "
        "die Werkstaetten in der Bildschirmmitte"
    ),
    "handel/lagerraum-kaufen": (
        "Das Pergament Lagerraum kaufen mit dem aktuellen Lagerraum und drei "
        "kaeuflichen Erweiterungen samt Quadratmeterzahl und Preis"
    ),
    "handel/stadtinformationen": (
        "Die Stadtinformationen von Crowbrigde mit Reichtum, Umsatzsteuer, "
        "Einwohnerzahl, Kriminalitaet, Haupt- und Nebenproduktion, Nachfrage, "
        "moeglichen Werkstaetten und Lagerbestand"
    ),
    "handel/wohnsitz-waehlen": (
        "Das Pergament Wohnsitz umbauen mit der Liste der Wohnsitze von der "
        "Kate bis zum Schloss samt ihrer Preise"
    ),
    "handel/wohnsitz-erweiterung": (
        "Das Pergament mit den Erweiterungen fuer die Kate: kleiner "
        "Gemuesegarten, Sitzbank und Blumenbeet samt Preis"
    ),
    "handel/wohnsitz-verwaltung": (
        "Das Pergament Wohnsitz mit dem Bild des Hauses und den Optionen "
        "Umbauen, Renovieren, Erweitern und Verkaufen sowie dem Zustand in Prozent"
    ),
    "schreibstube/schreibstube": (
        "Der Schreibtisch der Schreibstube mit dem Kreditbuch links, einer "
        "Geldtruhe in der Mitte, einem aufgeschlagenen leeren Buch und dem "
        "Gesetzbuch sowie einem Buch mit Kreuz rechts"
    ),
    "schreibstube/geldleiher": (
        "Das Pergament Der Geldleiher mit dem angebotenen Darlehen, dem "
        "Zinssatz, der Ruecklaufzeit und den Knoepfen Annehmen und Ablehnen"
    ),
    "schreibstube/kreditbuch": (
        "Das Pergament Kreditbuch mit dem Hinweis, dass derzeit keine Kredite "
        "offen sind"
    ),
    "schreibstube/gesetze": (
        "Das Pergament mit den geltenden Finanzgesetzen: Kredite und "
        "Gluecksspiel erlaubt, Bestechungen verboten, maximale Anwesen und "
        "maximale Taler"
    ),
    "schreibstube/amt-bewerben": (
        "Das Pergament Auf welches Amt wollt Ihr Euch bewerben mit dem Amt "
        "Priester in Crowbrigde und den Knoepfen Info und Bewerben"
    ),
    "schreibstube/amt-info": (
        "Das Pergament Informationen zur Wahl mit dem waehlenden Amtsinhaber "
        "und der Liste der Mitbewerber"
    ),
    "schreibstube/kontrahenten": (
        "Das Pergament Kontrahenten mit der alphabetischen Liste aller "
        "Mitspieler und Nichtspielercharaktere samt Amt und Blaetterleiste"
    ),
    "schreibstube/kontrahent-details": (
        "Das Pergament mit den Details zu einem Kontrahenten: Titel, Amt, "
        "Alter und dem Hinweis, dass ohne laufende Spionage Vermoegen, "
        "Gesundheit und Beweislast unbekannt sind"
    ),
    "schreibstube/privilegien": (
        "Das Pergament Eure Privilegien mit der Liste der verfuegbaren "
        "Privilegien wie Ahnentafel einsehen, Maetresse nehmen und Medikus "
        "konsultieren"
    ),
    "schreibstube/titelverleihung": (
        "Die Urkunde, mit der die Regentin dem Spieler den Titel Buerger verleiht"
    ),
    "schreibstube/StadtaemterPolit": "Tafel der politischen Ämter einer Stadt mit ihren Wählern und Privilegien",
    "schreibstube/LandaemterPolit": "Tafel der politischen Ämter einer Grafschaft mit ihren Wählern und Privilegien",
    "schreibstube/ReichaemterPolit": "Tafel der politischen Ämter des Königreiches mit ihren Wählern und Privilegien",
    "schreibstube/StadtaemterKirch": "Tafel der kirchlichen Ämter einer Stadt mit ihren Wählern und Privilegien",
    "schreibstube/LandaemterKirch": "Tafel der kirchlichen Ämter einer Grafschaft mit ihren Wählern und Privilegien",
    "schreibstube/ReichaemterKirch": "Tafel der kirchlichen Ämter des Königreiches mit ihren Wählern und Privilegien",
    "schreibstube/StadtaemterMil": "Tafel der militärischen Ämter einer Stadt mit ihren Wählern und Privilegien",
    "schreibstube/LandaemterMil": "Tafel der militärischen Ämter einer Grafschaft mit ihren Wählern und Privilegien",
    "schreibstube/ReichaemterMil": "Tafel der militärischen Ämter des Königreiches mit ihren Wählern und Privilegien",
    "kirche/kirche": "Die Fassade der Kirche mit Glockenturm, Rundfenster und dem steinernen Portal",
    "kirche/brautwerbung": (
        "Das Pergament Brautwerbung mit der Auswahl des Geschenks fuer die "
        "Umworbene: geflochtener Korb, Gemaelde oder goldbestickte Pantoffeln"
    ),
    "kirche/konfession-waehlen": (
        "Das Pergament mit der Frage, welchen Glauben ein konfessionsloser "
        "Spieler annehmen will: evangelisch, katholisch oder keinen"
    ),
    "hinterzimmer/hinterzimmer": (
        "Der Tisch im Hinterzimmer mit Fernrohr, Bombe, Kerze, Giftflasche und "
        "Kelch, Wuerfeln und einem versiegelten Brief"
    ),
    "soeldner-raeuber/karte": (
        "Die Landkarte des Koenigreiches mit den Symbolen der Raeuberlager und "
        "Zollburgen in den Grafschaften"
    ),
    "soeldner-raeuber/kaufangebot": (
        "Das Pergament mit den Informationen zum Raeuberlager Bandit Moor: "
        "Besitzer, Wert, Zustand, Tarnung und dem Feld fuer das Kaufangebot"
    ),
    "client/optionen": (
        "Das Pergament Einstellungen mit den Schaltern Musik ausschalten, Tipps "
        "anzeigen, Statistik anzeigen, Todesfaelle anzeigen, Stuetzpunkt- und "
        "Militaerereignisse der KI anzeigen, Duelle selbst austragen und "
        "Vollbildmodus, drei Lautstaerkereglern und dem Regler fuer die "
        "Aggressivitaet der KI-Spieler"
    ),
    "client/speichern": (
        "Das Pergament Unter welchem Namen speichern mit der Liste vorhandener "
        "Spielstaende und dem Eingabefeld fuer den Namen"
    ),
    "client/laden": (
        "Das Pergament Welcher Spielstand soll geladen werden mit der "
        "Spielstandliste und den Knoepfen Laden und Loeschen"
    ),
    "client/fehler-melden": (
        "Das Pergament Feedback und Fehler melden mit dem Beschreibungsfeld, "
        "dem Schalter Aktuellen Spielstand anhaengen und den Knoepfen Bericht "
        "erstellen und E-Mail vorbereiten, Log-Ordner oeffnen sowie Spielstand- "
        "und Profil-Ordner oeffnen"
    ),
    "hauptmenue/credits": (
        "Der Abspann mit den Mitwirkenden zu Programm, Grafiken, Wiki, Musik, "
        "Sounds und Vektor-Icons vor einem leuchtenden Pentagramm"
    ),
    "hauptmenue/profile": (
        "Das Pergament Profile verwalten mit der Liste der angelegten Profile, "
        "dem Eingabefeld fuer den Profilnamen und den Knoepfen Neu anlegen, "
        "Umbenennen, Loeschen, Aktiv setzen und Statistik anzeigen"
    ),
    "hauptmenue/bestenliste": (
        "Das Pergament Bestenliste mit dem Auswahlfeld fuer den Auftrag und der "
        "nach Spieljahren sortierten Liste der Bestzeiten"
    ),
    "hauptmenue/statistik": (
        "Das Pergament Statistik mit den Kennzahlen eines Spielers in zwei "
        "Spalten von Spionagen bis Taler"
    ),
}


def finde_pergament(bild: Image.Image) -> tuple[int, int, int, int]:
    """Kasten um die helle Flaeche. Ist nichts hell, gilt das ganze Bild."""
    grau = bild.convert("L")
    maske = grau.point(lambda wert: 255 if wert >= SCHWELLE else 0)
    kasten = maske.getbbox()
    if kasten is None:
        return (0, 0, bild.width, bild.height)
    return kasten


def bereite_auf(quelle: pathlib.Path, zielname: str, modus: str) -> tuple[int, int]:
    """Schneidet zu (nur bei modus 'dialog'), skaliert, schreibt WebP."""
    with Image.open(quelle) as bild:
        bild = bild.convert("RGB")
        if modus == "dialog":
            bild = bild.crop(finde_pergament(bild))
        hoehe = round(bild.height * BREITE / bild.width)
        bild = bild.resize((BREITE, hoehe), Image.LANCZOS)
        ziel = ZIEL / f"{zielname}.webp"
        ziel.parent.mkdir(parents=True, exist_ok=True)
        bild.save(ziel, "WEBP", quality=82, method=6)
    return BREITE, hoehe


def _finde_quelle(zeile: dict[str, str]) -> pathlib.Path | None:
    """Liefert die Quelldatei fuer eine Manifestzeile, oder None."""
    ansicht = zeile["Ansicht"]
    if zeile["Quelle"] == "wiki":
        pfad = WIKI_BILDER / f"{ansicht}.png"
        return pfad if pfad.is_file() else None
    treffer = sorted(ANSICHTEN.glob(f"*_{ansicht}_*.png"))
    return treffer[0] if treffer else None


def main() -> int:
    with MANIFEST.open(encoding="utf-8", newline="") as datei:
        zeilen = list(csv.DictReader(datei, delimiter="\t"))

    fehler: list[str] = []
    for zeile in zeilen:
        zielname = zeile["Zielname"]
        if zielname not in ALTERNATIVTEXTE:
            fehler.append(f"{zielname}: kein Alternativtext im Skript - nicht aufbereitet")
            continue

        quelldatei = _finde_quelle(zeile)
        if quelldatei is None:
            fehler.append(f"{zielname}: keine Aufnahme zur Ansicht {zeile['Ansicht']}")
            continue

        breite, hoehe = bereite_auf(quelldatei, zielname, zeile["Modus"])
        print(f"{zielname}: {breite}x{hoehe} aus {quelldatei.name}")

    for meldung in fehler:
        print("FEHLER: " + meldung)

    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())

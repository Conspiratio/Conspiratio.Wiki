"""Unittests fuer den Pergament-Zuschnitt."""
from PIL import Image

from bilder_aufbereiten import finde_pergament


def test_findet_die_helle_flaeche_auf_dunklem_grund():
    bild = Image.new("RGB", (1600, 900), (10, 10, 12))
    bild.paste(Image.new("RGB", (800, 500), (240, 235, 220)), (400, 200))

    links, oben, rechts, unten = finde_pergament(bild)

    assert (links, oben, rechts, unten) == (400, 200, 1200, 700)


def test_gibt_das_ganze_bild_zurueck_wenn_nichts_hell_ist():
    bild = Image.new("RGB", (1600, 900), (10, 10, 12))

    assert finde_pergament(bild) == (0, 0, 1600, 900)


def test_ignoriert_ein_isoliertes_helles_eckpixel():
    """Reale Godot-Screenshots tragen vereinzelt ein helles Randpixel (z. B.
    Helligkeit 130) ausserhalb des Pergaments. Bei SCHWELLE=150 darf das den
    engen Kasten nicht aufreissen; bei SCHWELLE=110 - dem alten, zu
    niedrigen Wert - tut es das sehr wohl. Dieser Test faellt daher genau
    dann durch, wenn SCHWELLE unter etwa 137 sinkt.
    """
    bild = Image.new("RGB", (1600, 900), (10, 10, 12))
    bild.paste(Image.new("RGB", (800, 500), (240, 235, 220)), (400, 200))
    bild.putpixel((0, 0), (130, 130, 130))

    assert finde_pergament(bild) == (400, 200, 1200, 700)

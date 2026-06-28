"""Unit tests for astrology_common (pure logic — independent of kerykeion)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import astrology_common as ac


class TestSignNames(unittest.TestCase):
    def test_abbrev_to_full(self):
        self.assertEqual(ac.full_sign("Gem"), "Gemini")
        self.assertEqual(ac.full_sign("Cap"), "Capricorn")
        self.assertEqual(ac.full_sign("Sco"), "Scorpio")

    def test_unknown_returns_input(self):
        self.assertEqual(ac.full_sign("Xyz"), "Xyz")


class TestTallyBalance(unittest.TestCase):
    def setUp(self):
        self.points = [
            {"element": "Fire", "quality": "Cardinal"},
            {"element": "Fire", "quality": "Fixed"},
            {"element": "Air", "quality": "Mutable"},
            {"element": "Water", "quality": "Cardinal"},
        ]

    def test_element_counts(self):
        bal = ac.tally_balance(self.points)
        self.assertEqual(bal["elements"], {"fire": 2, "earth": 0, "air": 1, "water": 1})

    def test_modality_counts(self):
        bal = ac.tally_balance(self.points)
        self.assertEqual(bal["modalities"], {"cardinal": 2, "fixed": 1, "mutable": 1})

    def test_dominant(self):
        bal = ac.tally_balance(self.points)
        self.assertEqual(ac.dominant(bal["elements"]), "fire")


class TestReference(unittest.TestCase):
    def test_twelve_signs(self):
        ref = ac.load_reference()
        self.assertEqual(len(ref["signs"]), 12)
        for s in ("Aries", "Gemini", "Pisces"):
            self.assertIn(s, ref["signs"])
            self.assertTrue(ref["signs"][s].get("keywords"))

    def test_planet_meanings(self):
        ref = ac.load_reference()
        for p in ("Sun", "Moon", "Venus", "Ascendant"):
            self.assertIn(p, ref["planets"])

    def test_aspect_meanings(self):
        ref = ac.load_reference()
        for a in ("conjunction", "trine", "square", "opposition", "sextile"):
            self.assertIn(a, ref["aspects"])


if __name__ == "__main__":
    unittest.main()

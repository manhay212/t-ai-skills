"""Unit tests for tarot_common (pure logic)."""
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tarot_common as tc


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = tc.load_deck()

    def test_has_78_cards(self):
        self.assertEqual(len(self.deck), 78)

    def test_22_major_56_minor(self):
        major = [c for c in self.deck if c["arcana"] == "major"]
        minor = [c for c in self.deck if c["arcana"] == "minor"]
        self.assertEqual(len(major), 22)
        self.assertEqual(len(minor), 56)

    def test_four_suits_of_14(self):
        for suit in ("wands", "cups", "swords", "pentacles"):
            cards = [c for c in self.deck if c.get("suit") == suit]
            self.assertEqual(len(cards), 14, f"{suit} should have 14 cards")

    def test_card_fields(self):
        for c in self.deck:
            self.assertTrue(c.get("name"))
            self.assertTrue(c.get("upright"))
            self.assertTrue(c.get("reversed"))
            self.assertTrue(c.get("keywords"))

    def test_unique_names(self):
        names = [c["name"] for c in self.deck]
        self.assertEqual(len(names), len(set(names)))


class TestSpreads(unittest.TestCase):
    def test_known_spreads_exist(self):
        for s in ("single", "three_card", "relationship", "celtic_cross"):
            self.assertIn(s, tc.SPREADS)

    def test_spread_sizes(self):
        self.assertEqual(len(tc.SPREADS["single"]), 1)
        self.assertEqual(len(tc.SPREADS["three_card"]), 3)
        self.assertEqual(len(tc.SPREADS["celtic_cross"]), 10)


class TestDraw(unittest.TestCase):
    def setUp(self):
        self.deck = tc.load_deck()

    def test_draw_count_matches_spread(self):
        rng = random.Random(1)
        drawn = tc.draw_spread("three_card", self.deck, rng)
        self.assertEqual(len(drawn), 3)

    def test_positions_match_spread(self):
        rng = random.Random(2)
        drawn = tc.draw_spread("three_card", self.deck, rng)
        self.assertEqual([d["position"] for d in drawn], tc.SPREADS["three_card"])

    def test_no_duplicate_cards(self):
        rng = random.Random(3)
        drawn = tc.draw_spread("celtic_cross", self.deck, rng)
        names = [d["card"]["name"] for d in drawn]
        self.assertEqual(len(names), len(set(names)))

    def test_orientation_values(self):
        rng = random.Random(4)
        drawn = tc.draw_spread("celtic_cross", self.deck, rng)
        for d in drawn:
            self.assertIn(d["orientation"], ("upright", "reversed"))

    def test_meaning_matches_orientation(self):
        rng = random.Random(5)
        drawn = tc.draw_spread("celtic_cross", self.deck, rng)
        for d in drawn:
            expected = d["card"]["upright"] if d["orientation"] == "upright" else d["card"]["reversed"]
            self.assertEqual(d["meaning"], expected)

    def test_reproducible_with_seed(self):
        a = tc.draw_spread("three_card", self.deck, random.Random(42))
        b = tc.draw_spread("three_card", self.deck, random.Random(42))
        self.assertEqual([(d["card"]["name"], d["orientation"]) for d in a],
                         [(d["card"]["name"], d["orientation"]) for d in b])

    def test_no_reversals_when_disabled(self):
        rng = random.Random(6)
        drawn = tc.draw_spread("celtic_cross", self.deck, rng, allow_reversals=False)
        self.assertTrue(all(d["orientation"] == "upright" for d in drawn))

    def test_unknown_spread_raises(self):
        with self.assertRaises(ValueError):
            tc.draw_spread("nope", self.deck, random.Random(0))


if __name__ == "__main__":
    unittest.main()

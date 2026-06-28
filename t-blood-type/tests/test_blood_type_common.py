"""Unit tests for blood_type_common (pure logic)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import blood_type_common as bt


class TestNormalize(unittest.TestCase):
    def test_plain(self):
        self.assertEqual(bt.normalize_type("A"), "A")

    def test_lowercase(self):
        self.assertEqual(bt.normalize_type("o"), "O")

    def test_ab(self):
        self.assertEqual(bt.normalize_type("ab"), "AB")

    def test_strips_rh(self):
        self.assertEqual(bt.normalize_type("A+"), "A")
        self.assertEqual(bt.normalize_type("O-"), "O")

    def test_strips_decorations(self):
        self.assertEqual(bt.normalize_type(" Type B "), "B")
        self.assertEqual(bt.normalize_type("O型"), "O")

    def test_invalid_raises(self):
        with self.assertRaises(ValueError):
            bt.normalize_type("C")
        with self.assertRaises(ValueError):
            bt.normalize_type("")


class TestData(unittest.TestCase):
    def test_all_types_have_profiles(self):
        data = bt.load_data()
        for t in ("A", "B", "O", "AB"):
            self.assertIn(t, data["types"])
            prof = data["types"][t]
            self.assertTrue(prof.get("keywords"))
            self.assertTrue(prof.get("strengths"))
            self.assertTrue(prof.get("in_love"))

    def test_profile_lookup(self):
        prof = bt.profile("A")
        self.assertEqual(prof, bt.load_data()["types"]["A"])


class TestCompatibility(unittest.TestCase):
    def test_all_pairs_resolve(self):
        for a in ("A", "B", "O", "AB"):
            for b in ("A", "B", "O", "AB"):
                c = bt.compatibility(a, b)
                self.assertIn("score", c)
                self.assertTrue(c.get("summary"))

    def test_symmetric(self):
        self.assertEqual(bt.compatibility("A", "B"), bt.compatibility("B", "A"))

    def test_score_in_range(self):
        c = bt.compatibility("O", "AB")
        self.assertIn(c["score"], (1, 2, 3, 4, 5))


if __name__ == "__main__":
    unittest.main()

"""Unit tests for chakras_common (pure logic)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chakras_common as cc


class TestData(unittest.TestCase):
    def test_seven_chakras(self):
        self.assertEqual(len(cc.load_chakras()), 7)

    def test_seven_keys_in_order(self):
        self.assertEqual(cc.CHAKRA_KEYS,
                         ["root", "sacral", "solar_plexus", "heart", "throat",
                          "third_eye", "crown"])

    def test_each_chakra_fields(self):
        for key, ch in cc.load_chakras().items() if isinstance(cc.load_chakras(), dict) else [(c["key"], c) for c in cc.load_chakras()]:
            for field in ("name", "sanskrit", "color", "location", "element",
                          "focus", "balanced", "underactive", "overactive", "practices"):
                self.assertIn(field, ch, f"{key} missing {field}")
            self.assertTrue(ch["balanced"])
            self.assertTrue(ch["practices"])

    def test_get_chakra(self):
        heart = cc.get_chakra("heart")
        self.assertEqual(heart["sanskrit"].lower().startswith("anahata"), True)


class TestClassify(unittest.TestCase):
    def test_underactive(self):
        self.assertEqual(cc.classify(2), "underactive")

    def test_balanced(self):
        self.assertEqual(cc.classify(5), "balanced")

    def test_overactive(self):
        self.assertEqual(cc.classify(9), "overactive")

    def test_boundaries(self):
        self.assertEqual(cc.classify(4), "balanced")
        self.assertEqual(cc.classify(7), "balanced")
        self.assertEqual(cc.classify(3), "underactive")
        self.assertEqual(cc.classify(8), "overactive")

    def test_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            cc.classify(11)
        with self.assertRaises(ValueError):
            cc.classify(-1)


class TestAssess(unittest.TestCase):
    def test_assess_returns_entry_per_score(self):
        result = cc.assess({"root": 2, "heart": 5, "throat": 9})
        self.assertEqual(set(result.keys()), {"root", "heart", "throat"})

    def test_assess_entry_shape(self):
        result = cc.assess({"root": 2})
        entry = result["root"]
        self.assertEqual(entry["status"], "underactive")
        self.assertEqual(entry["score"], 2)
        self.assertTrue(entry["signs"])          # underactive signs
        self.assertTrue(entry["practices"])      # balancing practices
        self.assertEqual(entry["name"], cc.get_chakra("root")["name"])

    def test_assess_balanced_uses_balanced_signs(self):
        result = cc.assess({"heart": 5})
        self.assertEqual(result["heart"]["signs"], cc.get_chakra("heart")["balanced"])

    def test_assess_unknown_chakra_raises(self):
        with self.assertRaises(KeyError):
            cc.assess({"nose": 5})


if __name__ == "__main__":
    unittest.main()

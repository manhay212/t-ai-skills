"""Unit tests for bazi_common (pure logic — independent of lunar-python)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bazi_common as bc


class TestElementMaps(unittest.TestCase):
    def test_gan_elements(self):
        self.assertEqual(bc.element_of_gan("甲"), "wood")
        self.assertEqual(bc.element_of_gan("庚"), "metal")
        self.assertEqual(bc.element_of_gan("癸"), "water")

    def test_zhi_elements(self):
        self.assertEqual(bc.element_of_zhi("午"), "fire")
        self.assertEqual(bc.element_of_zhi("亥"), "water")
        self.assertEqual(bc.element_of_zhi("未"), "earth")
        self.assertEqual(bc.element_of_zhi("申"), "metal")


class TestElementBalance(unittest.TestCase):
    def test_known_chart(self):
        # 庚午 壬午 辛亥 乙未 -> metal2 fire2 water2 wood1 earth1
        bal = bc.element_balance(["庚午", "壬午", "辛亥", "乙未"])
        self.assertEqual(bal, {"wood": 1, "fire": 2, "earth": 1, "metal": 2, "water": 2})

    def test_totals_eight(self):
        bal = bc.element_balance(["庚午", "壬午", "辛亥", "乙未"])
        self.assertEqual(sum(bal.values()), 8)

    def test_missing_elements_listed(self):
        bal = bc.element_balance(["甲子", "甲子", "甲子", "甲子"])  # only wood + water
        self.assertEqual(bc.missing_elements(bal), ["fire", "earth", "metal"])


class TestFiveElementRelations(unittest.TestCase):
    def test_generates(self):
        self.assertTrue(bc.generates("wood", "fire"))
        self.assertTrue(bc.generates("water", "wood"))
        self.assertFalse(bc.generates("fire", "wood"))

    def test_controls(self):
        self.assertTrue(bc.controls("wood", "earth"))
        self.assertTrue(bc.controls("metal", "wood"))
        self.assertFalse(bc.controls("earth", "wood"))

    def test_relationship_same(self):
        self.assertEqual(bc.element_relationship("fire", "fire"), "same")

    def test_relationship_generating(self):
        self.assertEqual(bc.element_relationship("wood", "fire"), "a_generates_b")
        self.assertEqual(bc.element_relationship("fire", "wood"), "b_generates_a")

    def test_relationship_controlling(self):
        self.assertEqual(bc.element_relationship("wood", "earth"), "a_controls_b")
        self.assertEqual(bc.element_relationship("earth", "wood"), "b_controls_a")


class TestZodiacRelationship(unittest.TestCase):
    def test_liu_he(self):
        self.assertEqual(bc.zodiac_relationship("子", "丑"), "六合")

    def test_san_he(self):
        self.assertEqual(bc.zodiac_relationship("申", "子"), "三合")

    def test_clash(self):
        self.assertEqual(bc.zodiac_relationship("子", "午"), "六沖")

    def test_neutral(self):
        self.assertEqual(bc.zodiac_relationship("子", "寅"), "平")

    def test_symmetric(self):
        self.assertEqual(bc.zodiac_relationship("丑", "子"), bc.zodiac_relationship("子", "丑"))


class TestCompatibility(unittest.TestCase):
    def test_score_and_fields(self):
        a = {"pillars": ["庚午", "壬午", "辛亥", "乙未"], "day_gan": "辛", "year_zhi": "午"}
        b = {"pillars": ["丙寅", "辛卯", "戊子", "甲寅"], "day_gan": "戊", "year_zhi": "寅"}
        c = bc.compatibility(a, b)
        self.assertIn(c["score"], (1, 2, 3, 4, 5))
        self.assertIn("zodiac", c)
        self.assertIn("day_master", c)
        self.assertTrue(c["notes"])

    def test_clash_lowers_score_vs_harmony(self):
        base = {"pillars": ["庚午", "壬午", "辛亥", "乙未"], "day_gan": "辛"}
        harmony = bc.compatibility({**base, "year_zhi": "子"}, {**base, "year_zhi": "丑"})  # 六合
        clash = bc.compatibility({**base, "year_zhi": "子"}, {**base, "year_zhi": "午"})    # 六沖
        self.assertGreater(harmony["score"], clash["score"])


if __name__ == "__main__":
    unittest.main()

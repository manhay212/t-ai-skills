"""Unit tests for ziwei_common (pure logic — independent of py-iztro)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ziwei_common as zc


class TestTimeIndex(unittest.TestCase):
    def test_early_zi(self):
        self.assertEqual(zc.hour_to_time_index(0), 0)   # 早子 00:00-00:59

    def test_late_zi(self):
        self.assertEqual(zc.hour_to_time_index(23), 12)  # 晚子 23:00-23:59

    def test_chou(self):
        self.assertEqual(zc.hour_to_time_index(1), 1)
        self.assertEqual(zc.hour_to_time_index(2), 1)

    def test_wu(self):
        self.assertEqual(zc.hour_to_time_index(11), 6)
        self.assertEqual(zc.hour_to_time_index(12), 6)

    def test_wei(self):
        self.assertEqual(zc.hour_to_time_index(14), 7)

    def test_invalid_hour(self):
        with self.assertRaises(ValueError):
            zc.hour_to_time_index(24)


class TestGender(unittest.TestCase):
    def test_male(self):
        self.assertEqual(zc.normalize_gender("male"), "男")
        self.assertEqual(zc.normalize_gender("M"), "男")
        self.assertEqual(zc.normalize_gender("男"), "男")

    def test_female(self):
        self.assertEqual(zc.normalize_gender("female"), "女")
        self.assertEqual(zc.normalize_gender("女"), "女")

    def test_invalid(self):
        with self.assertRaises(ValueError):
            zc.normalize_gender("other")


class TestZodiacRelationship(unittest.TestCase):
    def test_clash(self):
        self.assertEqual(zc.zodiac_relationship("午", "子"), "六沖")

    def test_liu_he(self):
        self.assertEqual(zc.zodiac_relationship("子", "丑"), "六合")

    def test_san_he(self):
        self.assertEqual(zc.zodiac_relationship("申", "子"), "三合")

    def test_neutral(self):
        self.assertEqual(zc.zodiac_relationship("子", "寅"), "平")


class TestReference(unittest.TestCase):
    def test_fourteen_major_stars(self):
        ref = zc.load_reference()
        self.assertEqual(len(ref["major_stars"]), 14)
        for s in ("紫微", "天府", "七殺", "破軍"):
            self.assertIn(s, ref["major_stars"])

    def test_twelve_palaces(self):
        ref = zc.load_reference()
        for p in ("命宮", "夫妻", "財帛", "官祿"):
            self.assertIn(p, ref["palaces"])

    def test_four_mutagens(self):
        ref = zc.load_reference()
        for m in ("祿", "權", "科", "忌"):
            self.assertIn(m, ref["mutagens"])


if __name__ == "__main__":
    unittest.main()

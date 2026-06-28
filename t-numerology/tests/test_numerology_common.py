"""Unit tests for numerology_common (pure logic). Run: python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numerology_common as nc


class TestReduceNumber(unittest.TestCase):
    def test_single_digit_unchanged(self):
        self.assertEqual(nc.reduce_number(7), 7)

    def test_reduces_multi_digit(self):
        self.assertEqual(nc.reduce_number(39), 3)  # 3+9=12 -> 1+2=3

    def test_preserves_master_11(self):
        self.assertEqual(nc.reduce_number(29), 11)  # 2+9=11, master kept

    def test_preserves_master_22(self):
        self.assertEqual(nc.reduce_number(22), 22)

    def test_preserves_master_33(self):
        self.assertEqual(nc.reduce_number(33), 33)

    def test_master_collapsed_when_disabled(self):
        self.assertEqual(nc.reduce_number(11, keep_master=False), 2)

    def test_ten_reduces_to_one(self):
        self.assertEqual(nc.reduce_number(10), 1)


class TestLifePath(unittest.TestCase):
    def test_known_date(self):
        # 1987-12-25: month 12->3, day 25->7, year 1987->7 ; 3+7+7=17->8
        self.assertEqual(nc.life_path(1987, 12, 25), 8)

    def test_master_components_preserved(self):
        # 1990-11-22: m=11, d=22, y=1990->1 ; 11+22+1=34 -> 7
        self.assertEqual(nc.life_path(1990, 11, 22), 7)


class TestLetterValue(unittest.TestCase):
    def test_a_is_one(self):
        self.assertEqual(nc.letter_value("a"), 1)

    def test_i_is_nine(self):
        self.assertEqual(nc.letter_value("I"), 9)

    def test_z_is_eight(self):
        self.assertEqual(nc.letter_value("z"), 8)


class TestNameNumbers(unittest.TestCase):
    def test_expression_all_letters(self):
        # JOHN: 1+6+8+5 = 20 -> 2
        self.assertEqual(nc.name_number("John", kind="expression"), 2)

    def test_soul_urge_vowels_only(self):
        # JOHN vowels: O=6 -> 6
        self.assertEqual(nc.name_number("John", kind="soul_urge"), 6)

    def test_personality_consonants_only(self):
        # JOHN consonants: J+H+N = 1+8+5 = 14 -> 5
        self.assertEqual(nc.name_number("John", kind="personality"), 5)

    def test_ignores_non_letters_and_spaces(self):
        self.assertEqual(nc.name_number("John  Smith!", kind="expression"),
                         nc.name_number("JohnSmith", kind="expression"))

    def test_empty_name_returns_none(self):
        self.assertIsNone(nc.name_number("", kind="expression"))


class TestPersonalYear(unittest.TestCase):
    def test_known(self):
        # born 12-25, current year 2026: 3 + 7 + (2026->10->1) ... 12->3, 25->7, 2026->2+0+2+6=10->1 ; 3+7+1=11
        self.assertEqual(nc.personal_year(12, 25, 2026), 11)


class TestRelationshipNumber(unittest.TestCase):
    def test_sum_and_reduce(self):
        # 8 and 7 -> 15 -> 6
        self.assertEqual(nc.relationship_number(8, 7), 6)

    def test_master_kept(self):
        # 9 and 2 -> 11 master kept
        self.assertEqual(nc.relationship_number(9, 2), 11)


class TestMeanings(unittest.TestCase):
    def test_every_core_number_has_meaning(self):
        meanings = nc.load_meanings()
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33]:
            self.assertIn(str(n), meanings, f"missing meaning for {n}")
            self.assertTrue(meanings[str(n)].get("keywords"))


if __name__ == "__main__":
    unittest.main()

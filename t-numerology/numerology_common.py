"""Pure numerology logic (Pythagorean system). No I/O except load_meanings().

Conventions:
- Master numbers 11, 22, 33 are preserved (not reduced) by default.
- Life Path uses the component method: reduce month, day, year separately, then
  sum and reduce (this preserves master numbers correctly).
- Vowels are A E I O U; Y is treated as a consonant.
"""
import json
import os

MASTER_NUMBERS = (11, 22, 33)
VOWELS = set("AEIOU")

# Pythagorean letter -> value
_LETTER_MAP = {}
for _i, _ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    _LETTER_MAP[_ch] = (_i % 9) + 1


def reduce_number(n, keep_master=True):
    """Reduce an integer to a single digit, preserving master numbers by default."""
    n = abs(int(n))
    while n > 9:
        if keep_master and n in MASTER_NUMBERS:
            return n
        n = sum(int(d) for d in str(n))
    return n


def life_path(year, month, day):
    """Life Path number from a birth date (component method)."""
    m = reduce_number(month)
    d = reduce_number(day)
    y = reduce_number(year)
    return reduce_number(m + d + y)


def letter_value(ch):
    """Pythagorean value (1-9) of a single A-Z letter, or 0 for non-letters."""
    return _LETTER_MAP.get(ch.upper(), 0)


def _filter_letters(name, kind):
    letters = [c.upper() for c in name if c.isalpha()]
    if kind == "expression":
        return letters
    if kind == "soul_urge":
        return [c for c in letters if c in VOWELS]
    if kind == "personality":
        return [c for c in letters if c not in VOWELS]
    raise ValueError(f"unknown name-number kind: {kind}")


def name_number(name, kind="expression"):
    """Name-derived number. kind: expression (all), soul_urge (vowels), personality (consonants).
    Returns None if the filtered set is empty (e.g. empty name, or no vowels)."""
    letters = _filter_letters(name, kind)
    if not letters:
        return None
    return reduce_number(sum(letter_value(c) for c in letters))


def personal_year(birth_month, birth_day, current_year):
    """Personal Year number for the given calendar year."""
    return reduce_number(reduce_number(birth_month) + reduce_number(birth_day)
                         + reduce_number(current_year))


def relationship_number(life_path_a, life_path_b):
    """A combined 'relationship' number from two Life Paths."""
    return reduce_number(life_path_a + life_path_b)


def load_meanings():
    """Load the bundled number-meaning canon from data/meanings.json."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "meanings.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

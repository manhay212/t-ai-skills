# t-numerology

Pythagorean numerology skill for **T**. Computes a person's core numbers (and pair compatibility)
from birth date + optional name, and returns them with canonical meanings. Pure offline
arithmetic — **no dependencies, no network, no API key**.

## What it computes

| Number | From | Notes |
|---|---|---|
| Life Path | birth date | component method; master numbers preserved |
| Personal Year | birth month/day + year | defaults to current year |
| Expression / Destiny | full name (all letters) | needs name |
| Soul Urge | name vowels | needs name |
| Personality | name consonants | needs name |
| Relationship number | two Life Paths | compatibility mode only |

## Install

Nothing to install (Python 3 standard library only).

## Usage

```bash
python3 numerology.py --date 1990-06-15 --name "Jane Doe"
python3 numerology.py --date 1990-06-15 --date2 1988-02-03            # compatibility
python3 numerology.py --date 1990-06-15 --current-year 2027 --output reading.json
```

Output is a JSON envelope on stdout (see `SKILL.md` for the schema). Exit `1` on a bad date.

## Testing walkthrough

```bash
# 1. Unit tests for the pure logic
python3 -m unittest discover -s tests
# -> Ran 21 tests ... OK

# 2. Single-person smoke test (John Smith, 1987-12-25)
python3 numerology.py --date 1987-12-25 --name "John Smith"
#    expect life_path 8, soul_urge 6, personality 11

# 3. Compatibility smoke test
python3 numerology.py --date 1987-12-25 --date2 1990-11-22
#    expect relationship_number 6 (life paths 8 and 7)

# 4. Bad-input path
python3 numerology.py --date not-a-date ; echo $?
#    expect an error message and exit code 1
```

## Files

- `numerology.py` — CLI entry; builds the JSON envelope.
- `numerology_common.py` — pure logic (reduce, life path, name numbers, etc.).
- `data/meanings.json` — canonical meanings for numbers 1-9, 11, 22, 33.
- `tests/` — offline unit tests.

## Method notes

Master numbers 11/22/33 are preserved. Life Path uses the component method. Vowels = A E I O U
(Y is a consonant). These are documented choices; numerology has variant conventions.

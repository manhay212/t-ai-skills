# t-chakras

Chakra reference + balance-assessment skill for **T**. Holds the seven-chakra canon and classifies
T-supplied 0-10 energy scores into underactive / balanced / overactive. Pure offline — **no
dependencies, no network**.

## Usage

```bash
# Reference
python3 chakras.py                 # all seven
python3 chakras.py --chakra heart  # one

# Assessment (4-7 balanced, 0-3 underactive, 8-10 overactive)
python3 chakras.py --root 2 --heart 5 --throat 9
```

Assessment flags: `--root --sacral --solar-plexus --heart --throat --third-eye --crown`. Only pass
the chakras you have signal on; the rest are reported under `unavailable`. Output is a JSON envelope
on stdout (see `SKILL.md`). Exit `1` on an out-of-range score.

## Testing walkthrough

```bash
# 1. Unit tests
python3 -m unittest discover -s tests
# -> Ran 13 tests ... OK

# 2. Reference for all seven
python3 chakras.py | python3 -m json.tool | head

# 3. Assessment
python3 chakras.py --root 2 --heart 5 --throat 9
#    root underactive, heart balanced, throat overactive; out_of_balance = [root, throat]

# 4. Bad score
python3 chakras.py --root 99 ; echo $?
#    error + exit 1
```

## Files

- `chakras.py` — CLI entry; reference + assessment modes.
- `chakras_common.py` — pure logic (load, classify, assess).
- `data/chakras.json` — the seven chakras (color, location, element, focus, signs, practices).
- `tests/` — offline unit tests.

This is an energy/wellness reflection framework, not medical advice.

# t-tarot

Tarot reading skill for **T**. Draws a real random spread from the full 78-card Rider-Waite-Smith
deck (upright/reversed) and returns the cards with canonical meanings. Pure offline — **no
dependencies, no network**. The draw uses `random.SystemRandom` (os.urandom entropy), so it can't be
biased.

## Spreads

`single` (1) · `three_card` (3, default) · `relationship` (4, two-person) · `celtic_cross` (10).

## Usage

```bash
python3 tarot.py                                   # 3-card draw
python3 tarot.py --spread single --question "..."
python3 tarot.py --spread relationship
python3 tarot.py --spread celtic_cross --no-reversals
```

Output is a JSON envelope on stdout (see `SKILL.md`). `--seed N` makes a draw reproducible (tests
only — don't use it for real readings).

## Testing walkthrough

```bash
# 1. Unit tests (deck integrity + draw logic)
python3 -m unittest discover -s tests
# -> Ran 15 tests ... OK

# 2. Reproducible seeded draw
python3 tarot.py --spread three_card --seed 42
#    Past = Knight of Cups (upright), Present = Queen of Cups (reversed), Future = Three of Swords

# 3. Two real draws should (almost always) differ
python3 tarot.py --spread single ; python3 tarot.py --spread single

# 4. No reversals
python3 tarot.py --spread celtic_cross --no-reversals
#    every card upright
```

## Files

- `tarot.py` — CLI entry; builds the JSON envelope, owns the RNG.
- `tarot_common.py` — pure logic (deck load, spreads, `draw_spread`).
- `data/deck.json` — 78 cards (22 major + 56 minor), upright/reversed/keywords.
- `tests/` — offline unit tests.

The deck was generated once from a builder embedding Rider-Waite-Smith meanings; only the resulting
`data/deck.json` is shipped.

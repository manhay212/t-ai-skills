"""Pure tarot logic: deck loading + spread drawing. No I/O except load_deck().

Randomness: the caller passes an `rng` (a random.Random instance). The CLI uses
random.SystemRandom() (os.urandom entropy) so real draws can't be biased or
predicted; tests pass a seeded random.Random for determinism.
"""
import json
import os

# Spread name -> ordered list of position labels.
SPREADS = {
    "single": ["The card"],
    "three_card": ["Past", "Present", "Future"],
    "relationship": ["You", "Them", "The connection", "The advice"],
    "celtic_cross": [
        "The present", "The challenge", "The foundation (past)", "The recent past",
        "The crown (potential)", "The near future", "Your attitude",
        "External influences", "Hopes and fears", "The outcome",
    ],
}


def load_deck():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "deck.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def draw_spread(spread_name, deck, rng, allow_reversals=True):
    """Draw a spread. Returns a list of dicts:
    {position, card, orientation ('upright'|'reversed'), meaning, keywords}.
    Cards are drawn without replacement. Raises ValueError on an unknown spread."""
    if spread_name not in SPREADS:
        raise ValueError(f"unknown spread: {spread_name!r} (choices: {', '.join(SPREADS)})")
    positions = SPREADS[spread_name]
    pool = list(deck)
    rng.shuffle(pool)
    chosen = pool[:len(positions)]
    out = []
    for position, card in zip(positions, chosen):
        reversed_ = bool(allow_reversals and rng.random() < 0.5)
        orientation = "reversed" if reversed_ else "upright"
        out.append({
            "position": position,
            "card": card,
            "orientation": orientation,
            "meaning": card["reversed"] if reversed_ else card["upright"],
            "keywords": card["keywords"],
        })
    return out

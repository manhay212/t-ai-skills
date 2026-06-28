#!/usr/bin/env python3
"""t-tarot — draw a tarot spread with real randomness.

  python3 tarot.py                                  # 3-card past/present/future
  python3 tarot.py --spread single --question "..."
  python3 tarot.py --spread relationship            # 2-person reading
  python3 tarot.py --spread celtic_cross
  python3 tarot.py --spread three_card --seed 42    # reproducible (testing)

By default the draw uses os.urandom entropy (random.SystemRandom) so it cannot be
biased or predicted. Prints a JSON envelope to stdout. The skill draws the cards;
T reads them in its own voice.
"""
import argparse
import datetime as _dt
import json
import random
import sys

import tarot_common as tc


def build_envelope(spread, question, allow_reversals, seed):
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    deck = tc.load_deck()
    cards = tc.draw_spread(spread, deck, rng, allow_reversals=allow_reversals)
    mode = "compatibility" if spread == "relationship" else "single"
    return {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "skill": "t-tarot",
        "mode": mode,
        "inputs": {"spread": spread, "question": question,
                   "reversals": allow_reversals, "seed": seed},
        "result": {
            "spread": spread,
            "positions": tc.SPREADS[spread],
            "question": question,
            "cards": cards,
        },
        "reference": {"deck": "Rider-Waite-Smith", "card_count": len(deck)},
        "unavailable": [],
        "notes": "Real-entropy draw (random.SystemRandom) unless --seed given. Each position's "
                 "'meaning' already reflects the drawn orientation (upright/reversed).",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Draw a tarot spread.")
    p.add_argument("--spread", default="three_card", choices=sorted(tc.SPREADS),
                   help="which spread to draw (default: three_card)")
    p.add_argument("--question", help="the querent's question/topic (echoed back for context)")
    p.add_argument("--no-reversals", action="store_true", help="draw all cards upright")
    p.add_argument("--seed", type=int, help="seed the RNG for a reproducible draw (testing only)")
    p.add_argument("--output", help="also write the JSON envelope to this path")
    args = p.parse_args(argv)

    envelope = build_envelope(args.spread, args.question, not args.no_reversals, args.seed)
    text = json.dumps(envelope, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

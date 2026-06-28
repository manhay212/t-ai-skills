#!/usr/bin/env python3
"""t-blood-type — blood-type personality (血型) reading for one person or a pair.

Single:        python3 blood_type.py --type A
Compatibility: python3 blood_type.py --type A --type2 O

Prints a JSON envelope to stdout (use --output to also write a file).
Pop-culture lore — entertainment, not science. T should frame it lightly.
"""
import argparse
import datetime as _dt
import json
import sys

import blood_type_common as bt


def build_envelope(args):
    a = bt.normalize_type(args.type)
    profile_a = bt.profile(a)

    if args.type2:
        mode = "compatibility"
        b = bt.normalize_type(args.type2)
        result = {
            "person_a": {"blood_type": a, **profile_a},
            "person_b": {"blood_type": b, **bt.profile(b)},
            "compatibility": bt.compatibility(a, b),
        }
        reference = {a: profile_a, b: bt.profile(b)}
        inputs = {"type": a, "type2": b}
    else:
        mode = "single"
        result = {"person": {"blood_type": a, **profile_a}}
        reference = {a: profile_a}
        inputs = {"type": a}

    return {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "skill": "t-blood-type",
        "mode": mode,
        "inputs": inputs,
        "result": result,
        "reference": reference,
        "unavailable": [],
        "notes": "East-Asian blood-type personality lore (血液型性格). Entertainment, not science.",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Blood-type personality reading for one person or a pair.")
    p.add_argument("--type", required=True, help="blood type: A, B, O, or AB (Rh ignored)")
    p.add_argument("--type2", help="second person's blood type (enables compatibility)")
    p.add_argument("--output", help="also write the JSON envelope to this path")
    args = p.parse_args(argv)

    try:
        envelope = build_envelope(args)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    text = json.dumps(envelope, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

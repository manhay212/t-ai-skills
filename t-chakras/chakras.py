#!/usr/bin/env python3
"""t-chakras — chakra reference + a simple text-based balance assessment.

Reference (default = all 7, or one):
  python3 chakras.py
  python3 chakras.py --chakra heart

Assessment (T scores each relevant chakra 0-10 from what the user shared;
4-7 = balanced, 0-3 = underactive, 8-10 = overactive):
  python3 chakras.py --root 2 --heart 5 --throat 9

Prints a JSON envelope to stdout. The skill supplies the canon + classification;
T does the gentle, holistic interpretation.
"""
import argparse
import datetime as _dt
import json
import sys

import chakras_common as cc

# CLI flag <-> chakra key (dashes for the two-word keys)
_FLAGS = {
    "root": "root", "sacral": "sacral", "solar_plexus": "solar_plexus",
    "heart": "heart", "throat": "throat", "third_eye": "third_eye", "crown": "crown",
}


def _envelope(mode_result, inputs, reference, notes, unavailable=None):
    return {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "skill": "t-chakras",
        "mode": "single",
        "inputs": inputs,
        "result": mode_result,
        "reference": reference,
        "unavailable": unavailable or [],
        "notes": notes,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Chakra reference + balance assessment.")
    p.add_argument("--chakra", choices=cc.CHAKRA_KEYS, help="reference for a single chakra")
    for flag in _FLAGS:
        p.add_argument(f"--{flag.replace('_', '-')}", type=int, metavar="0-10",
                       help=f"{flag} energy score (enables assessment)")
    p.add_argument("--output", help="also write the JSON envelope to this path")
    args = p.parse_args(argv)

    scores = {key: getattr(args, key) for key in _FLAGS if getattr(args, key) is not None}

    if scores:
        try:
            assessment = cc.assess(scores)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        chakras = cc.load_chakras()
        reference = {k: chakras[k] for k in assessment}
        out_of_balance = [k for k, v in assessment.items() if v["status"] != "balanced"]
        result = {
            "assessment": assessment,
            "out_of_balance": out_of_balance,
            "scored": list(assessment.keys()),
        }
        unavailable = []
        missing = [k for k in cc.CHAKRA_KEYS if k not in scores]
        if missing:
            unavailable.append(f"not scored (no info): {', '.join(missing)}")
        envelope = _envelope(result, {"scores": scores}, reference,
                             "Assessment from T-provided 0-10 scores. 4-7 balanced, 0-3 "
                             "underactive, 8-10 overactive. A gentle reflection, not a diagnosis.",
                             unavailable)
    else:
        chakras = cc.load_chakras()
        if args.chakra:
            selected = {args.chakra: chakras[args.chakra]}
        else:
            selected = chakras
        result = {"chakras": selected}
        envelope = _envelope(result, {"chakra": args.chakra}, {},
                             "Reference canon for the seven-chakra system.")

    text = json.dumps(envelope, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

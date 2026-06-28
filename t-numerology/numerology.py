#!/usr/bin/env python3
"""t-numerology — compute Pythagorean numerology for one person or a pair.

Single:        python3 numerology.py --date 1990-06-15 --name "John Smith"
Compatibility: python3 numerology.py --date 1990-06-15 --name "John" \
                                     --date2 1992-03-08 --name2 "Mary"

Prints a JSON envelope to stdout (use --output to also write a file).
The skill computes the numbers; T interprets them warmly in conversation.
"""
import argparse
import datetime as _dt
import json
import sys

import numerology_common as nc


def _parse_date(s):
    return _dt.date.fromisoformat(s)


def _person_reading(date, name, current_year, meanings, used):
    """Build a single person's numbers + record which numbers were used."""
    lp = nc.life_path(date.year, date.month, date.day)
    py = nc.personal_year(date.month, date.day, current_year)
    reading = {
        "birth_date": date.isoformat(),
        "name": name or None,
        "life_path": lp,
        "personal_year": {"year": current_year, "number": py},
        "expression": None,
        "soul_urge": None,
        "personality": None,
    }
    unavailable = []
    used.update([lp, py])
    if name:
        expr = nc.name_number(name, "expression")
        soul = nc.name_number(name, "soul_urge")
        pers = nc.name_number(name, "personality")
        reading["expression"] = expr
        reading["soul_urge"] = soul
        reading["personality"] = pers
        used.update(n for n in (expr, soul, pers) if n is not None)
    else:
        unavailable.append("expression/soul_urge/personality: name not provided")
    return reading, unavailable


def build_envelope(args):
    meanings = nc.load_meanings()
    current_year = args.current_year or _dt.date.today().year
    used = set()
    unavailable = []

    date_a = _parse_date(args.date)
    person_a, ua = _person_reading(date_a, args.name, current_year, meanings, used)
    unavailable += [f"person_a: {u}" for u in ua]

    if args.date2:
        mode = "compatibility"
        date_b = _parse_date(args.date2)
        person_b, ub = _person_reading(date_b, args.name2, current_year, meanings, used)
        unavailable += [f"person_b: {u}" for u in ub]
        rel = nc.relationship_number(person_a["life_path"], person_b["life_path"])
        used.add(rel)
        result = {
            "person_a": person_a,
            "person_b": person_b,
            "relationship_number": rel,
        }
        inputs = {"date": args.date, "name": args.name, "date2": args.date2,
                  "name2": args.name2, "current_year": current_year}
    else:
        mode = "single"
        result = {"person": person_a}
        inputs = {"date": args.date, "name": args.name, "current_year": current_year}

    reference = {str(n): meanings[str(n)] for n in sorted(used) if str(n) in meanings}

    return {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "skill": "t-numerology",
        "mode": mode,
        "inputs": inputs,
        "result": result,
        "reference": reference,
        "unavailable": unavailable,
        "notes": "Pythagorean system; master numbers 11/22/33 preserved. Life Path uses the "
                 "component method. Vowels=AEIOU (Y treated as consonant).",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Pythagorean numerology for one person or a pair.")
    p.add_argument("--date", required=True, help="birth date YYYY-MM-DD")
    p.add_argument("--name", help="full name (for expression/soul-urge/personality)")
    p.add_argument("--date2", help="second person's birth date YYYY-MM-DD (enables compatibility)")
    p.add_argument("--name2", help="second person's full name")
    p.add_argument("--current-year", type=int, help="year for Personal Year (default: this year)")
    p.add_argument("--output", help="also write the JSON envelope to this path")
    args = p.parse_args(argv)

    try:
        envelope = build_envelope(args)
    except ValueError as e:
        print(f"error: {e} (dates must be YYYY-MM-DD)", file=sys.stderr)
        return 1

    text = json.dumps(envelope, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

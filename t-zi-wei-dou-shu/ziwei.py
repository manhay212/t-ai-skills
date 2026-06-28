#!/usr/bin/env python3
"""t-zi-wei-dou-shu — 紫微斗數 astrolabe (12 palaces, 14 major stars, 四化) + comparison.

Single:
  python3 ziwei.py --date 1990-06-15 --time 14:30 --gender female
  python3 ziwei.py --date 1990-04-23 --time 09:00 --gender male --lunar

Compatibility (two people):
  python3 ziwei.py --date 1990-06-15 --time 14:30 --gender female \
                   --date2 1992-03-08 --time2 20:00 --gender2 male

Birth time is REQUIRED — the 命宮 placement depends on the 時辰, so a chart without
it would be fabricated. Output is a JSON envelope on stdout (traditional Chinese).
The skill computes the astrolabe (via py-iztro); T interprets it warmly.
"""
import argparse
import datetime as _dt
import json
import sys

import ziwei_common as zc


def _astrolabe(date_s, time_index, gender, lunar, lang):
    from py_iztro import Astro
    astro = Astro()
    y, m, d = date_s.year, date_s.month, date_s.day
    date_str = f"{y}-{m}-{d}"
    if lunar:
        return astro.by_lunar(date_str, time_index, gender, True, lang)
    return astro.by_solar(date_str, time_index, gender, True, lang)


def _palace(p, soul_branch, body_branch):
    return {
        "name": p.name,
        "branch": p.earthly_branch,
        "stem": p.heavenly_stem,
        "is_life_palace": p.earthly_branch == soul_branch,
        "is_body_palace": p.earthly_branch == body_branch,
        "major_stars": [{"name": s.name, "brightness": s.brightness or None,
                         "mutagen": s.mutagen or None} for s in p.major_stars],
        "minor_stars": [s.name for s in p.minor_stars],
        "decade": list(p.decadal.range) if p.decadal else None,
    }


def build_chart(date_s, time_s, gender_raw, lunar, lang):
    d = _dt.date.fromisoformat(date_s)
    t = _dt.time.fromisoformat(time_s)
    gender = zc.normalize_gender(gender_raw)
    time_index = zc.hour_to_time_index(t.hour)
    res = _astrolabe(d, time_index, gender, lunar, lang)

    soul_branch = res.earthly_branch_of_soul_palace
    body_branch = res.earthly_branch_of_body_palace
    palaces = [_palace(p, soul_branch, body_branch) for p in res.palaces]
    life = next((p for p in palaces if p["is_life_palace"]), None)
    year_branch = res.chinese_date.split()[0][1] if res.chinese_date else None

    return {
        "gender": gender,
        "solar_date": res.solar_date,
        "lunar_date": res.lunar_date,
        "chinese_date": res.chinese_date,
        "year_branch": year_branch,
        "zodiac": res.zodiac,
        "western_sign": res.sign,
        "five_elements_class": res.five_elements_class,
        "soul": res.soul,
        "body": res.body,
        "life_palace": life,
        "palaces": palaces,
    }


def _compare(chart_a, chart_b):
    rel = None
    if chart_a.get("year_branch") and chart_b.get("year_branch"):
        rel = zc.zodiac_relationship(chart_a["year_branch"], chart_b["year_branch"])
    return {
        "zodiac_relationship": rel,
        "a_life_palace_stars": [s["name"] for s in (chart_a["life_palace"] or {}).get("major_stars", [])],
        "b_life_palace_stars": [s["name"] for s in (chart_b["life_palace"] or {}).get("major_stars", [])],
        "a_spouse_palace": next((p for p in chart_a["palaces"] if p["name"] == "夫妻"), None),
        "b_spouse_palace": next((p for p in chart_b["palaces"] if p["name"] == "夫妻"), None),
        "note": "Simplified comparison: zodiac (year-branch) relationship plus each person's 命宮 "
                "and 夫妻 stars. Full 紫微合盤 (palace overlay) is beyond this skill's scope.",
    }


def build_envelope(args):
    reference = zc.load_reference()
    chart_a = build_chart(args.date, args.time, args.gender, args.lunar, args.lang)

    if args.date2:
        mode = "compatibility"
        chart_b = build_chart(args.date2, args.time2, args.gender2, args.lunar, args.lang)
        result = {"person_a": chart_a, "person_b": chart_b, "comparison": _compare(chart_a, chart_b)}
        inputs = {"date": args.date, "time": args.time, "gender": args.gender,
                  "date2": args.date2, "time2": args.time2, "gender2": args.gender2,
                  "lunar": args.lunar, "lang": args.lang}
    else:
        mode = "single"
        result = {"person": chart_a}
        inputs = {"date": args.date, "time": args.time, "gender": args.gender,
                  "lunar": args.lunar, "lang": args.lang}

    return {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "skill": "t-zi-wei-dou-shu",
        "mode": mode,
        "inputs": inputs,
        "result": result,
        "reference": reference,
        "unavailable": [],
        "notes": "Astrolabe computed by py-iztro (traditional Chinese). Read the 命宮 (life palace) "
                 "stars first, then 四化 (mutagens) and the palace relevant to the question.",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="紫微斗數 astrolabe and comparison.")
    p.add_argument("--date", required=True, help="birth date YYYY-MM-DD")
    p.add_argument("--time", required=True, help="birth time HH:MM (REQUIRED — sets the 時辰)")
    p.add_argument("--gender", required=True, help="male/female/男/女 (required)")
    p.add_argument("--lunar", action="store_true", help="treat the date(s) as lunar (default solar)")
    p.add_argument("--lang", default="zh-TW",
                   choices=["zh-TW", "zh-CN", "en-US", "ja-JP", "ko-KR", "vi-VN"],
                   help="output language (default zh-TW / traditional)")
    p.add_argument("--date2", help="second person's birth date (enables compatibility)")
    p.add_argument("--time2", help="second person's birth time HH:MM")
    p.add_argument("--gender2", help="second person's gender")
    p.add_argument("--output", help="also write the JSON envelope to this path")
    args = p.parse_args(argv)

    if args.date2 and not (args.time2 and args.gender2):
        print("error: compatibility needs --time2 and --gender2 for the second person",
              file=sys.stderr)
        return 1

    try:
        envelope = build_envelope(args)
    except ImportError:
        print("error: py-iztro is required. Run: pip install -r requirements.txt", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"error: {e} (date YYYY-MM-DD, time HH:MM, gender male/female)", file=sys.stderr)
        return 1

    text = json.dumps(envelope, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""t-bazi — BaZi / Four Pillars (八字 / 四柱) chart + simplified compatibility (合婚).

Single:
  python3 bazi.py --date 1990-06-15 --time 14:30 --gender male
  python3 bazi.py --date 1990-06-15                      # no time -> hour pillar unavailable
  python3 bazi.py --date 1990-04-23 --time 09:00 --lunar # treat date as lunar

Compatibility:
  python3 bazi.py --date 1990-06-15 --time 14:30 --gender male \
                  --date2 1992-03-08 --time2 20:00 --gender2 female

Prints a JSON envelope to stdout. Uses lunar-python for the calendar/ganzhi math;
the five-element and zodiac analysis is t-bazi's own (see bazi_common.py).
"""
import argparse
import datetime as _dt
import json
import os
import sys

import bazi_common as bc

_GENDER = {"male": 1, "female": 0, "m": 1, "f": 0}


def _load_reference():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "reference.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _eight_char(year, month, day, hour, minute, lunar):
    from lunar_python import Lunar, Solar
    if lunar:
        ln = Lunar.fromYmdHms(year, month, day, hour, minute, 0)
    else:
        ln = Solar.fromYmdHms(year, month, day, hour, minute, 0).getLunar()
    return ln, ln.getEightChar()


def build_chart(date_s, time_s, gender, lunar):
    """Return (chart_dict, unavailable_list)."""
    d = _dt.date.fromisoformat(date_s)
    unavailable = []
    has_time = time_s is not None
    if has_time:
        t = _dt.time.fromisoformat(time_s)
        hour, minute = t.hour, t.minute
    else:
        hour, minute = 12, 0  # placeholder noon; hour pillar is dropped below
        unavailable.append("hour pillar (時柱) and time-based ten-god: birth time not provided")

    ln, ec = _eight_char(d.year, d.month, d.day, hour, minute, lunar)

    pillars = {
        "year": ec.getYear(), "month": ec.getMonth(), "day": ec.getDay(),
    }
    ten_gods = {
        "year": ec.getYearShiShenGan(), "month": ec.getMonthShiShenGan(),
        "day": ec.getDayShiShenGan(),
    }
    nayin = {
        "year": ec.getYearNaYin(), "month": ec.getMonthNaYin(), "day": ec.getDayNaYin(),
    }
    pillar_list = [pillars["year"], pillars["month"], pillars["day"]]
    if has_time:
        pillars["time"] = ec.getTime()
        ten_gods["time"] = ec.getTimeShiShenGan()
        nayin["time"] = ec.getTimeNaYin()
        pillar_list.append(pillars["time"])

    day_gan = ec.getDayGan()
    chart = {
        "pillars": pillars,
        "pillar_list": pillar_list,
        "day_master": {"stem": day_gan, "element": bc.element_of_gan(day_gan)},
        "ten_gods": ten_gods,
        "nayin": nayin,
        "zodiac": ln.getYearShengXiao(),
        "year_zhi": ec.getYearZhi(),
        "element_balance": bc.element_balance(pillar_list),
        "missing_elements": bc.missing_elements(bc.element_balance(pillar_list)),
        "lunar_date": f"{ln.getYearInChinese()}年{ln.getMonthInChinese()}月{ln.getDayInChinese()}",
    }

    # Luck pillars (大運) need gender.
    if gender in _GENDER:
        yun = ec.getYun(_GENDER[gender])
        da = []
        for x in yun.getDaYun():
            gz = x.getGanZhi()
            if gz:
                da.append({"ganzhi": gz, "start_age": x.getStartAge(),
                           "start_year": x.getStartYear()})
        chart["luck_pillars"] = {
            "forward": yun.isForward(),
            "start_age_years": yun.getStartYear(),
            "start_age_months": yun.getStartMonth(),
            "decades": da[:8],
        }
    else:
        unavailable.append("luck pillars (大運): gender not provided")

    return chart, unavailable


def build_envelope(args):
    reference = _load_reference()
    chart_a, ua = build_chart(args.date, args.time, args.gender, args.lunar)
    unavailable = [f"person_a: {u}" for u in ua]

    if args.date2:
        mode = "compatibility"
        chart_b, ub = build_chart(args.date2, args.time2, args.gender2, args.lunar)
        unavailable += [f"person_b: {u}" for u in ub]
        compat = bc.compatibility(
            {"pillars": chart_a["pillar_list"], "day_gan": chart_a["day_master"]["stem"],
             "year_zhi": chart_a["year_zhi"]},
            {"pillars": chart_b["pillar_list"], "day_gan": chart_b["day_master"]["stem"],
             "year_zhi": chart_b["year_zhi"]},
        )
        result = {"person_a": chart_a, "person_b": chart_b, "compatibility": compat}
        inputs = {"date": args.date, "time": args.time, "gender": args.gender,
                  "date2": args.date2, "time2": args.time2, "gender2": args.gender2,
                  "lunar": args.lunar}
    else:
        mode = "single"
        result = {"person": chart_a}
        inputs = {"date": args.date, "time": args.time, "gender": args.gender,
                  "lunar": args.lunar}

    return {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "skill": "t-bazi",
        "mode": mode,
        "inputs": inputs,
        "result": result,
        "reference": reference,
        "unavailable": unavailable,
        "notes": "Pillars/ganzhi from lunar-python; five-element balance, zodiac and compatibility "
                 "analysis are t-bazi's own. Read the day master (日主) element first.",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="BaZi / Four Pillars chart and compatibility.")
    p.add_argument("--date", required=True, help="birth date YYYY-MM-DD")
    p.add_argument("--time", help="birth time HH:MM (24h); omit if unknown")
    p.add_argument("--gender", help="male/female (needed for luck pillars 大運)")
    p.add_argument("--lunar", action="store_true", help="treat the date(s) as lunar (default solar)")
    p.add_argument("--date2", help="second person's birth date (enables compatibility)")
    p.add_argument("--time2", help="second person's birth time HH:MM")
    p.add_argument("--gender2", help="second person's gender male/female")
    p.add_argument("--output", help="also write the JSON envelope to this path")
    args = p.parse_args(argv)

    try:
        envelope = build_envelope(args)
    except ImportError:
        print("error: lunar-python is required. Run: pip install -r requirements.txt",
              file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"error: {e} (date must be YYYY-MM-DD, time HH:MM)", file=sys.stderr)
        return 1

    text = json.dumps(envelope, ensure_ascii=False, indent=2)
    print(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

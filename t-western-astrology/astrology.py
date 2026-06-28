#!/usr/bin/env python3
"""t-western-astrology — natal chart + synastry via kerykeion.

Single:
  python3 astrology.py --date 1990-06-15 --time 14:30 --city "Hong Kong"
  python3 astrology.py --date 1990-06-15 --time 14:30 --lat 22.30 --lng 114.17 --tz Asia/Hong_Kong
  python3 astrology.py --date 1990-06-15 --city "Hong Kong"   # no time -> no houses/rising

Synastry (two people):
  python3 astrology.py --date 1990-06-15 --time 14:30 --city "Hong Kong" \
                       --date2 1992-03-08 --time2 20:00 --city2 "Shanghai"

Prints a JSON envelope to stdout. City names resolve offline (no network/key).
The skill computes the chart; T reads it warmly.
"""
import argparse
import datetime as _dt
import json
import sys

import astrology_common as ac
import astrology_geo as geo

PLANETS = ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn",
           "uranus", "neptune", "pluto"]
ANGLE_HOUSES = {"ascendant": "first_house", "descendant": "seventh_house",
                "midheaven": "tenth_house", "imum_coeli": "fourth_house"}
HOUSES = ["first_house", "second_house", "third_house", "fourth_house", "fifth_house",
          "sixth_house", "seventh_house", "eighth_house", "ninth_house", "tenth_house",
          "eleventh_house", "twelfth_house"]


def _point(p):
    return {
        "sign": ac.full_sign(p.sign),
        "sign_abbr": p.sign,
        "degree": round(p.position, 2),
        "element": p.element,
        "quality": p.quality,
        "house": (p.house or "").replace("_", " ") if p.house else None,
        "retrograde": bool(p.retrograde),
    }


def _make_subject(date_s, time_s, loc):
    from kerykeion import AstrologicalSubject
    d = _dt.date.fromisoformat(date_s)
    has_time = time_s is not None
    if has_time:
        t = _dt.time.fromisoformat(time_s)
        hour, minute = t.hour, t.minute
    else:
        hour, minute = 12, 0
    subj = AstrologicalSubject(
        "subject", d.year, d.month, d.day, hour, minute,
        lng=loc["lng"], lat=loc["lat"], tz_str=loc["tz"], city=loc.get("city", ""),
        online=False,
    )
    return subj, has_time


def _resolve_location(city, country, lat, lng, tz):
    if lat is not None and lng is not None and tz:
        return {"lat": lat, "lng": lng, "tz": tz, "city": city or "", "country": country}, None
    if city:
        loc = geo.resolve_city(city, country)
        if loc:
            return loc, None
        return None, f"could not resolve city {city!r} offline — provide --lat/--lng/--tz"
    return None, "no location: provide --city or --lat/--lng/--tz"


def build_chart(date_s, time_s, loc):
    subj, has_time = _make_subject(date_s, time_s, loc)
    planets = {name.capitalize(): _point(getattr(subj, name)) for name in PLANETS}
    balance = ac.tally_balance(list(planets.values()))
    unavailable = []

    chart = {
        "location": {"city": loc.get("city"), "country": loc.get("country"),
                     "lat": loc["lat"], "lng": loc["lng"], "tz": loc["tz"]},
        "planets": planets,
        "element_balance": balance["elements"],
        "modality_balance": balance["modalities"],
        "dominant_element": ac.dominant(balance["elements"]),
        "dominant_modality": ac.dominant(balance["modalities"]),
    }

    if has_time:
        angles = {}
        for label, house_attr in ANGLE_HOUSES.items():
            cusp = getattr(subj, house_attr)
            angles[label] = {"sign": ac.full_sign(cusp.sign), "degree": round(cusp.position, 2)}
        chart["angles"] = angles
        chart["rising_sign"] = angles["ascendant"]["sign"]
        chart["houses"] = {
            h.replace("_house", ""): ac.full_sign(getattr(subj, h).sign) for h in HOUSES
        }
    else:
        unavailable.append("rising sign, angles (ASC/DESC/MC/IC) and house placements: "
                           "birth time not provided")
        chart["notes"] = "Computed at 12:00 noon (no birth time); the Moon sign may be off if "
        chart["notes"] += "born near a sign cusp."

    return subj, chart, unavailable


def _simplify_aspects(aspect_list):
    out = []
    for a in aspect_list:
        out.append({
            "p1": a.p1_name, "p2": a.p2_name, "aspect": a.aspect,
            "degrees": a.aspect_degrees, "orbit": round(a.orbit, 2),
        })
    return out


def build_envelope(args):
    reference = ac.load_reference()
    loc_a, err = _resolve_location(args.city, args.country, args.lat, args.lng, args.tz)
    if err:
        raise ValueError(err)
    subj_a, chart_a, ua = build_chart(args.date, args.time, loc_a)
    unavailable = [f"person_a: {u}" for u in ua]

    from kerykeion import NatalAspects
    chart_a["aspects"] = _simplify_aspects(NatalAspects(subj_a).relevant_aspects)

    if args.date2:
        mode = "compatibility"
        loc_b, err2 = _resolve_location(args.city2, args.country2, args.lat2, args.lng2, args.tz2)
        if err2:
            raise ValueError(f"person_b: {err2}")
        subj_b, chart_b, ub = build_chart(args.date2, args.time2, loc_b)
        unavailable += [f"person_b: {u}" for u in ub]
        chart_b["aspects"] = _simplify_aspects(NatalAspects(subj_b).relevant_aspects)
        from kerykeion import SynastryAspects
        synastry = _simplify_aspects(SynastryAspects(subj_a, subj_b).relevant_aspects)
        result = {"person_a": chart_a, "person_b": chart_b,
                  "synastry_aspects": synastry}
        inputs = {"date": args.date, "time": args.time, "city": args.city,
                  "date2": args.date2, "time2": args.time2, "city2": args.city2}
    else:
        mode = "single"
        result = {"person": chart_a}
        inputs = {"date": args.date, "time": args.time, "city": args.city}

    return {
        "timestamp": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "skill": "t-western-astrology",
        "mode": mode,
        "inputs": inputs,
        "result": result,
        "reference": reference,
        "unavailable": unavailable,
        "notes": "Chart computed by kerykeion (Placidus houses). Element/modality balance tallied "
                 "across the ten planets. Synastry lists cross-aspects between the two charts.",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Western natal chart + synastry.")
    p.add_argument("--date", required=True, help="birth date YYYY-MM-DD")
    p.add_argument("--time", help="birth time HH:MM (needed for rising sign + houses)")
    p.add_argument("--city", help="birth city (resolved offline to lat/lng/tz)")
    p.add_argument("--country", help="ISO-2 country code to disambiguate the city")
    p.add_argument("--lat", type=float, help="birth latitude (alternative to --city)")
    p.add_argument("--lng", type=float, help="birth longitude")
    p.add_argument("--tz", help="IANA timezone, e.g. Asia/Hong_Kong")
    # second person
    p.add_argument("--date2", help="second person's birth date (enables synastry)")
    p.add_argument("--time2", help="second person's birth time HH:MM")
    p.add_argument("--city2", help="second person's birth city")
    p.add_argument("--country2", help="second person's country code")
    p.add_argument("--lat2", type=float)
    p.add_argument("--lng2", type=float)
    p.add_argument("--tz2")
    p.add_argument("--output", help="also write the JSON envelope to this path")
    args = p.parse_args(argv)

    try:
        envelope = build_envelope(args)
    except ImportError:
        print("error: kerykeion is required. Run: pip install -r requirements.txt", file=sys.stderr)
        return 2
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

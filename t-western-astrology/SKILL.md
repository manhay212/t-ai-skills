---
name: t-western-astrology
description: Compute a Western natal (birth) chart from a birth date, time, and place, or a synastry (relationship) comparison between two people. Returns the Sun, Moon, rising/Ascendant, Descendant, Midheaven and all ten planets by sign, house, and degree, plus element balance (fire/earth/air/water), modality balance (cardinal/fixed/mutable), and the chart's aspects. Synastry returns cross-aspects between two charts. Birth city is resolved offline to coordinates and timezone. Use when the user asks about their star sign, sun/moon/rising, natal chart, horoscope by birth details, or astrological compatibility. Requires kerykeion. No network, no API key.
version: 1.0.0
category: t
---

# t-western-astrology

Computes a real **natal chart** (and **synastry** for two people) with `kerykeion` and hands back
the structured chart + canonical reference. You (T) read it warmly. The skill exists so the chart is
**astronomically correct** — never guess someone's Moon or rising sign, compute it.

## When to use

- The user asks about their **sun/moon/rising**, star sign, natal chart, or "what my birth chart
  says".
- The user wants **astrological compatibility** (synastry) with a partner/friend/crush.

## Inputs to gather

- **Birth date** (required) — `YYYY-MM-DD`.
- **Birth time** `HH:MM` — needed for the **rising sign, angles, and houses**. Without it those are
  reported in `unavailable` and the Moon may be slightly off near a cusp (never faked).
- **Birth place** — pass `--city "Hong Kong"` (resolved offline to lat/lng/timezone). Use
  `--country HK` to disambiguate common city names, or pass `--lat/--lng/--tz` directly.

## How to run

```bash
python3 astrology.py --date 1990-06-15 --time 14:30 --city "Hong Kong"
python3 astrology.py --date 1990-06-15 --time 14:30 --lat 22.30 --lng 114.17 --tz Asia/Hong_Kong
python3 astrology.py --date 1990-06-15 --city "Hong Kong"        # no time -> no rising/houses
# Synastry:
python3 astrology.py --date 1990-06-15 --time 14:30 --city "Hong Kong" \
                     --date2 1992-03-08 --time2 20:00 --city2 "Shanghai"
```

Prints a JSON envelope to stdout. Exit `1` on a bad date or unresolvable location, `2` if
`kerykeion` isn't installed (`pip install -r requirements.txt`).

## Output (JSON envelope)

Single → `result.person` with: `planets` (each: sign, degree, element, quality, house, retrograde),
`angles` (Ascendant/Descendant/Midheaven/IC), `rising_sign`, `houses`, `element_balance`,
`modality_balance`, `dominant_element`, `dominant_modality`, `aspects`, and `location`.

Synastry → `result.person_a`, `result.person_b`, and `result.synastry_aspects` (cross-aspects
between the two charts). `reference` holds sign, planet, and aspect meanings.

## How to interpret (your job, T)

1. The big three are **Sun (core self)**, **Moon (inner emotional world)**, **Rising (how they
   meet the world)** — lead with those unless asked for more.
2. Use `dominant_element`/`dominant_modality` for the overall temperament; a missing element is as
   telling as a dominant one. Ground meanings in `reference`.
3. For synastry, highlight the tightest aspects (small `orbit`) between personal planets
   (Sun/Moon/Venus/Mars) — those carry the relationship's flavor. Trines/sextiles flow; squares/
   oppositions are the growth edges, not dealbreakers.
4. Reflection, not fate. Speak naturally; don't dump the JSON.

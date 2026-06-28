---
name: t-bazi
description: Compute a BaZi / Four Pillars chart (八字 / 四柱) from a birth date, time, and gender, or check compatibility (合婚) between two people. Returns the four pillars (year/month/day/hour in 干支), the day master (日主) and its element, ten gods (十神), nayin, Chinese zodiac (生肖), five-element balance with missing elements, and luck pillars (大運). Compatibility gives a score with zodiac and day-master analysis. Use when the user asks about their BaZi, Four Pillars, Chinese astrology by birth date, day master, element balance, or 合婚 compatibility. Requires lunar-python. No network, no API key.
version: 1.0.0
category: t
---

# t-bazi

Computes a **BaZi (八字 / Four Pillars)** chart and hands back the structured pillars + element
analysis. The calendar/ganzhi math is done by `lunar-python`; the five-element balance, zodiac
relationships, and compatibility are this skill's own logic. You (T) interpret it warmly.

## When to use

- The user asks about their **BaZi / Four Pillars / 八字 / 四柱**, day master (日主), element
  balance, or Chinese astrology from their birth date.
- The user wants a **合婚 / BaZi compatibility** read with someone.

## Inputs to gather

- **Birth date** (required) — `YYYY-MM-DD`.
- **Birth time** `HH:MM` — needed for the hour pillar (時柱). Without it, that pillar is reported in
  `unavailable` (never faked).
- **Gender** — `male`/`female`, needed for luck pillars (大運). Pass the user's stated value; this
  is the traditional input the method requires, not a judgment.
- **`--lunar`** if the date given is a lunar-calendar date (default is solar/Gregorian).

## How to run

```bash
python3 bazi.py --date 1990-06-15 --time 14:30 --gender male
python3 bazi.py --date 1990-06-15                       # degrade: no hour pillar, no luck pillars
python3 bazi.py --date 1990-04-23 --time 09:00 --lunar  # date is lunar
# Compatibility:
python3 bazi.py --date 1990-06-15 --time 14:30 --gender male \
                --date2 1992-03-08 --time2 20:00 --gender2 female
```

Prints a JSON envelope to stdout. Exit `1` on a bad date/time, `2` if `lunar-python` isn't
installed (`pip install -r requirements.txt`).

## Output (JSON envelope)

Single → `result.person` with: `pillars` (year/month/day[/time] 干支), `day_master`
(`stem` + `element`), `ten_gods`, `nayin`, `zodiac` (生肖), `element_balance`, `missing_elements`,
`luck_pillars` (大運 decades), and `lunar_date`. `reference` holds element and ten-god meanings.

Compatibility → `result.person_a`, `result.person_b`, and `result.compatibility`
(`score` 1-5, `zodiac` relationship, `day_master` relationship, `complementarity`, `notes`).

## How to interpret (your job, T)

1. **Read the day master (日主) element first** — it's the person's core self. Then look at the
   element balance: what's abundant supports them, what's missing or excessive shows tension.
2. Use `reference` for element traits and ten-god meanings so your reading is grounded.
3. For compatibility, the `score` is a starting point — explain it through the zodiac and day-master
   `notes`. A 六沖 clash isn't doom; frame it as friction-with-spark.
4. Hold it lightly and kindly — reflection, not fate. Don't read out the JSON; tell the story.

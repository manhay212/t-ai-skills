---
name: t-zi-wei-dou-shu
description: Compute a 紫微斗數 (Zi Wei Dou Shu / Purple Star Astrology) chart from a birth date, time, and gender — the full 12 palaces, 14 major stars with brightness and 四化 (transformations 祿權科忌), the 命宮 (life palace), 身宮 (body palace), 五行局, 命主/身主, and Chinese zodiac. Also compares two people. Use when the user asks about their 紫微斗數, 紫微, purple star astrology, life palace, 命盤, or Chinese astrology by birth chart. Birth time and gender are required. Output is in traditional Chinese by default. Requires py-iztro. No network, no API key.
version: 1.0.0
category: t
---

# t-zi-wei-dou-shu

Computes a full **紫微斗數** astrolabe via `py-iztro` (which mirrors the well-known `iztro` engine)
and hands back the structured chart. You (T) interpret it warmly. The skill exists so the placements
are **correct** — 紫微 star arrangement is intricate and must be computed, never guessed.

## When to use

- The user asks about their **紫微斗數 / 紫微 / 命盤 / purple star astrology / life palace (命宮)**.
- The user wants a 紫微 **comparison** with someone.

## Inputs to gather (all required)

- **Birth date** — `YYYY-MM-DD`.
- **Birth time** `HH:MM` — **required**. The 命宮 position depends on the 時辰, so a chart without
  the time would be fabricated — the skill refuses rather than fake it.
- **Gender** — `male`/`female` (男/女). Required (it sets the direction of the luck cycles).
- **`--lunar`** if the date is a lunar-calendar date (default solar).

## How to run

```bash
python3 ziwei.py --date 1990-06-15 --time 14:30 --gender female
python3 ziwei.py --date 1990-05-23 --time 09:00 --gender male --lunar
# Comparison:
python3 ziwei.py --date 1990-06-15 --time 14:30 --gender female \
                 --date2 1992-03-08 --time2 20:00 --gender2 male
```

Output is traditional Chinese (`--lang zh-CN` / `en-US` / etc. to change). Prints a JSON envelope to
stdout. Exit `1` on bad input, `2` if `py-iztro` isn't installed.

## Output (JSON envelope)

Single → `result.person` with: `soul` (命主), `body` (身主), `five_elements_class` (五行局),
`zodiac`, `western_sign`, `chinese_date`, `lunar_date`, `life_palace`, and `palaces` (all 12 — each
with name, branch, stem, `is_life_palace`/`is_body_palace`, `major_stars` (name + brightness +
mutagen), `minor_stars`, and `decade` range).

Comparison → `result.person_a`, `result.person_b`, and `result.comparison` (zodiac relationship +
each person's 命宮 and 夫妻 palace stars). `reference` holds the 14 major-star meanings, 12 palace
meanings, and the four 四化 mutagens.

## How to interpret (your job, T)

1. **Read the 命宮 (life palace) first** — its major star(s) describe the core self. Then look at
   the **四化 (mutagens)** — 祿 (flow), 權 (power), 科 (merit), 忌 (friction) — they show where energy
   concentrates. Then the palace relevant to the user's question (夫妻 for love, 官祿 for career…).
2. Use `reference` to ground every star/palace/mutagen meaning.
3. 紫微 is dense — don't dump everything; pick the few placements that answer what they asked.
4. Reflection, not fate. Speak naturally; never read out the JSON.

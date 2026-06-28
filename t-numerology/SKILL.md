---
name: t-numerology
description: Compute a person's numerology (Pythagorean system) from their birth date and optionally their name, or compare two people. Returns Life Path, Expression/Destiny, Soul Urge, Personality, and Personal Year numbers plus a relationship number for pairs, each with canonical meanings (light/shadow/in-love). Use when the user is curious about their numbers, life path, "what their birthday says about them", personal-year energy, or numerology compatibility with someone. Needs only a birth date (name unlocks more numbers). No network, no API key.
version: 1.0.0
category: t
---

# t-numerology

Computes **Pythagorean numerology** and hands back structured numbers + canonical meanings. You
(T) decide when to bring it up and how to interpret it warmly — the skill just gives you the
accurate numbers so you never have to compute or guess them.

## When to use

- The user asks about their **life path number**, "what my birthday means", their **personal year**
  energy, or their name's numbers.
- The user wants a **numerology compatibility** read with a partner/friend/crush.
- A casual moment where a quick numbers read would be fun and fitting.

Pure offline arithmetic — no dependencies, no network.

## Inputs to gather

- **Birth date** (required) — `YYYY-MM-DD`.
- **Full name** (optional) — unlocks Expression, Soul Urge, Personality numbers. Without it, those
  are reported as unavailable (never faked).
- For compatibility: a **second** person's birth date (and optionally name).
- Personal Year defaults to the current year; override with `--current-year`.

## How to run

```bash
# Single person
python3 numerology.py --date 1990-06-15 --name "Jane Doe"

# Personal year for a specific year
python3 numerology.py --date 1990-06-15 --current-year 2027

# Compatibility (presence of --date2 switches to compatibility mode)
python3 numerology.py --date 1990-06-15 --name "Jane" --date2 1988-02-03 --name2 "Alex"
```

Prints a JSON envelope to **stdout**. Add `--output path.json` to also write a file (avoid leaving
per-user files in shared space). Exit code `1` on a bad date.

## Output (JSON envelope)

```json
{
  "skill": "t-numerology",
  "mode": "single | compatibility",
  "inputs": { "...echoed..." },
  "result": {
    "person": {
      "life_path": 8, "personal_year": {"year": 2026, "number": 11},
      "expression": 8, "soul_urge": 6, "personality": 11
    }
  },
  "reference": { "8": {"name": "...", "keywords": [], "light": "", "shadow": "", "in_love": ""} },
  "unavailable": [],
  "notes": "..."
}
```

- Compatibility mode replaces `person` with `person_a`, `person_b`, and a `relationship_number`.
- `reference` only contains the numbers that actually came up.
- `unavailable` lists anything not computed (e.g. name not provided) — do not invent these.

## How to interpret (your job, T)

1. Read `result` for the numbers, `reference` for what each means (light / shadow / in_love).
2. Weave it into the conversation in your own warm voice — don't dump the JSON or read it like a
   manual. Lead with what's most relevant to what they asked.
3. Hold it lightly — numerology is for reflection and fun, not fate. If something lands as
   negative ("shadow"), frame it gently and as a tendency, not a verdict.
4. If `unavailable` says you're missing their name and the moment fits, you can offer: "if you tell
   me your full name I can read a couple more numbers."

## Method notes

- Master numbers **11, 22, 33** are preserved, not reduced.
- Life Path uses the **component method** (reduce month, day, year separately, then sum & reduce).
- Vowels are A E I O U; **Y is treated as a consonant**.

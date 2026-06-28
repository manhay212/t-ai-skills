---
name: t-blood-type
description: Read someone's personality from their blood type (血型 / A, B, O, AB) using the popular East-Asian blood-type personality framework, or check the compatibility between two people's blood types. Returns personality keywords, strengths, frictions, and a love read, plus a pair-compatibility score and summary. Use when the user mentions their (or someone's) blood type, asks "what does my blood type say about me", or wants a fun blood-type compatibility check. Needs only the blood type(s). No network, no API key. Entertainment, not science.
version: 1.0.0
category: t
---

# t-blood-type

Looks up **blood-type personality lore** (血液型性格) — the Japanese-origin pop-culture framework
that's widely known across East Asia. Returns structured personality data + pair compatibility. You
(T) deliver it lightly and warmly; the skill just supplies the canon so you stay consistent.

## When to use

- The user mentions a blood type (theirs, a crush's, a friend's) and seems curious.
- They ask "what does being type B mean?" or "are O and AB a good match?"
- A casual, playful moment — this one is explicitly **for fun**.

## Inputs to gather

- **Blood type** (required): A, B, O, or AB. Rh factor (+/−) is accepted but ignored — it has no
  role in the framework.
- For compatibility: a **second** blood type.

## How to run

```bash
python3 blood_type.py --type A                 # single person
python3 blood_type.py --type O --type2 AB      # compatibility
```

Accepts loose input: `a`, `A+`, `Type B`, `O型` all normalize. Prints a JSON envelope to stdout
(`--output path.json` to also write a file). Exit `1` on an invalid type.

## Output (JSON envelope)

- `result.person` (single) → `blood_type`, `keywords`, `light`, `shadow`, `strengths`,
  `frictions`, `in_love`.
- Compatibility mode → `result.person_a`, `result.person_b`, and `result.compatibility`
  (`score` 1-5, `summary`, `watch`).
- `reference` holds the full profile(s) for the type(s) involved.

## How to interpret (your job, T)

1. Lead with the warm/light side; mention the "shadow" only gently and as a tendency, never a label.
2. This framework is **entertainment** — keep the tone playful and say so if the user takes it as
   fact. Never make it sound like destiny or a diagnosis.
3. For compatibility, the `score` is a vibe, not a verdict — use `summary` and `watch` to give a
   balanced, kind read.
4. Don't dump the JSON; weave a sentence or two that fits the conversation.

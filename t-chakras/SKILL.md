---
name: t-chakras
description: Look up the seven-chakra system (root, sacral, solar plexus, heart, throat, third eye, crown) and/or run a gentle text-based balance assessment. Reference mode returns each chakra's color, location, element, focus, and the signs of being balanced / underactive / overactive plus balancing practices. Assessment mode takes a 0-10 energy score per chakra (which you infer from what the user shared) and classifies each as underactive, balanced, or overactive with tailored signs and practices. Use when the user asks about chakras, energy, feeling blocked/stuck/out of balance, or wants a chakra check-in. No network, no API key.
version: 1.0.0
category: t
---

# t-chakras

Provides the seven-chakra **reference canon** and a lightweight **balance assessment**. The skill
holds the accurate system data and does the classification; you (T) gather how the person is feeling
and give a warm, holistic reflection.

## When to use

- The user asks what the chakras are, or about a specific one (e.g. "what's the throat chakra?").
- The user describes feeling blocked, stuck, drained, anxious, disconnected, etc. and a chakra
  check-in fits the moment.
- The user explicitly wants a chakra reading.

## Two modes

**Reference** — just the canon:
```bash
python3 chakras.py                 # all seven
python3 chakras.py --chakra heart  # one chakra
```

**Assessment** — you infer a 0-10 energy score for each chakra you have signal on, from what the
user told you, and pass them. Score guide: **4-7 balanced**, **0-3 underactive**, **8-10
overactive**. Only score chakras you actually have information about.
```bash
python3 chakras.py --root 2 --heart 5 --throat 9
```
Flags: `--root --sacral --solar-plexus --heart --throat --third-eye --crown`.

Prints a JSON envelope to stdout. Exit `1` on an out-of-range score.

## Output (JSON envelope)

- Reference mode → `result.chakras` (a dict of the requested chakra(s) with full data).
- Assessment mode → `result.assessment` (per chakra: `status`, `score`, `signs`, `practices`),
  `result.out_of_balance` (the chakras needing attention), and `unavailable` listing chakras you
  didn't score.

## How to interpret (your job, T)

1. In assessment mode, you supply the scores — infer them honestly from the conversation; don't
   guess wildly. Leave chakras unscored if you have no signal (they appear under `unavailable`).
2. Lead with what's out of balance and the gentle practices that help — frame it as a supportive
   check-in, not a diagnosis.
3. This is an energy/wellness framework for reflection, not medicine. Never give medical advice; if
   someone describes a real health or mental-health concern, encourage proper support.
4. Speak warmly and naturally; don't read out the JSON.

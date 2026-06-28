---
name: t-tarot
description: Draw a tarot reading using a real random shuffle of the full 78-card Rider-Waite-Smith deck, with upright/reversed orientations and several spreads (single card, three-card past/present/future, a 4-card relationship spread for two people, and the 10-card Celtic Cross). Returns the drawn cards with their position, orientation, and canonical meaning. Use when the user asks for a tarot reading, "pull a card", guidance on a question, or a relationship tarot read. No network, no API key. The draw is genuinely random so it cannot be biased.
version: 1.0.0
category: t
---

# t-tarot

Draws a real, unbiased tarot spread and hands back the cards + their canonical meanings. You (T)
do the reading — connect the cards to the person's question in your own warm voice. The skill exists
so the **draw is genuinely random** (you can't and shouldn't make up which cards "came out").

## When to use

- The user asks for a tarot reading, wants you to "pull a card", or asks for guidance on a
  question or situation.
- A relationship question → use the `relationship` spread (works for the user + another person).

## Spreads

| `--spread` | Cards | Positions |
|---|---|---|
| `single` | 1 | The card |
| `three_card` (default) | 3 | Past · Present · Future |
| `relationship` | 4 | You · Them · The connection · The advice |
| `celtic_cross` | 10 | full Celtic Cross |

## How to run

```bash
python3 tarot.py                                     # 3-card draw
python3 tarot.py --spread single --question "Should I take the new job?"
python3 tarot.py --spread relationship --question "Me and Sam"
python3 tarot.py --spread celtic_cross
python3 tarot.py --spread three_card --no-reversals  # all upright
```

Prints a JSON envelope to stdout. The draw uses real entropy (`random.SystemRandom`) — **do not
pass `--seed`** in normal use (it's only for reproducible tests). Pass `--question` so the reading
has context.

## Output (JSON envelope)

`result.cards` is a list, one per position:

```json
{ "position": "Present", "card": { "name": "Queen of Cups", "arcana": "minor", "suit": "cups",
                                   "upright": "...", "reversed": "...", "keywords": [] },
  "orientation": "reversed", "meaning": "<the reversed text>", "keywords": [] }
```

`meaning` is already the correct text for the drawn orientation — use it directly.

## How to interpret (your job, T)

1. Read each card in its **position** and **orientation** — the position frames the meaning
   (e.g. the same card means different things in "Past" vs "The outcome").
2. Tell a coherent story across the cards, tied to the user's `question`. Don't just list meanings.
3. Reversed ≠ "bad" — it's a softer, blocked, or inward version of the card. Frame gently.
4. Tarot is for reflection, not fixed fate. Empower the person; never predict doom.
5. Don't reveal the raw JSON; speak the reading naturally.

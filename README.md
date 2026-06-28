# t-ai-skills

Custom skills for **T** ("Your Secret Third Wheel") — a Hermes agent that's a chill, friendly
companion who *happens* to know a handful of fortune-telling / divination crafts and pulls them out
when they're handy in conversation.

**Philosophy:** each skill is the *truth layer* — it computes the objective structure (the real
chart, the actual cards drawn, the 紫微 palaces, the correct life-path number) and returns
**structured facts + canonical reference meanings**. T is the *interpretation layer*: warmth,
context, and knowing when to bring it up. Skills never fake what they can't compute — missing inputs
are reported in an `unavailable[]` array, never invented. See [`DESIGN.md`](DESIGN.md) for the full
rationale and [`CLAUDE.md`](CLAUDE.md) for build conventions.

All skills print a consistent JSON envelope to **stdout** (birth data is PII and T is multi-user, so
nothing sensitive is left in a shared folder):

```json
{ "timestamp": "...", "skill": "...", "mode": "single | compatibility",
  "inputs": {}, "result": {}, "reference": {}, "unavailable": [], "notes": "" }
```

## Skills

| Skill | What it does | Engine | Single | Compatibility |
|---|---|---|:---:|:---:|
| [`t-numerology`](t-numerology/) | Pythagorean numbers (life path, expression, soul urge, personality, personal year) | built (arithmetic) | ✅ | ✅ |
| [`t-blood-type`](t-blood-type/) | Blood-type personality 血型 + pair compatibility | built (data) | ✅ | ✅ |
| [`t-tarot`](t-tarot/) | Real-RNG tarot draw with spreads & reversals | built (RNG + data) | ✅ | ✅ |
| [`t-chakras`](t-chakras/) | 7-chakra reference + text-based balance assessment | built (reference) | ✅ | — |
| [`t-bazi`](t-bazi/) | BaZi 八字 / Four Pillars + ten gods + zodiac | `lunar-python` | ✅ | ✅ |
| [`t-western-astrology`](t-western-astrology/) | Natal chart (sun/moon/rising + planets/houses + modality/element) + synastry | `kerykeion` | ✅ | ✅ |
| [`t-zi-wei-dou-shu`](t-zi-wei-dou-shu/) | 紫微斗數 — 12 palaces + 14 stars + 四化 | `py-iztro` | ✅ | ✅ |

## Install

Each skill is self-contained. Install its dependencies (if any) from its own `requirements.txt`:

```bash
cd t-western-astrology && pip install -r requirements.txt
```

`t-numerology`, `t-blood-type`, `t-tarot`, and `t-chakras` need only the Python 3.10+ standard
library. The library-backed skills need their listed packages (and Python 3.10+).

## Testing

Every skill ships offline unit tests for its pure logic:

```bash
cd <skill> && python3 -m unittest discover -s tests
```

## License

[AGPL-3.0](LICENSE) — because `t-western-astrology` depends on `kerykeion` (AGPL-3.0).

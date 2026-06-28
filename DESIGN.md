# t-ai-skills — Design

**Date:** 2026-06-28
**Author:** Claude (architect/builder), for Man Hay Hong
**Status:** Approved — building v1

Custom skills repo for **T** ("Your Secret Third Wheel"), a Hermes agent running on a standalone
laptop. T is a **chill, friendly companion** — someone to talk to — who *happens* to know a set of
fortune-telling / divination crafts and pulls them out when they come in handy in conversation.
These skills are **general-purpose** (not relationship-locked), usable for a single person or
between two+ people.

---

## 1. Core philosophy — why these are skills, not prompts

Each skill **computes the objective structure and hands T accurate, structured facts plus canonical
reference meanings.** T decides *when* to offer a reading and writes the actual interpretation in
its own warm voice. The split:

- **Skill = the truth layer.** The real natal chart, the actual cards drawn, the 紫微 palace
  placements, the correct life-path number. Deterministic, testable, never hallucinated.
- **T = the interpretation layer.** Warmth, context, knowing when to bring it up, weaving it into
  the conversation.

**Honesty rule (non-negotiable):** a skill NEVER fakes what it can't compute. Missing birth time →
return what's still valid (e.g. sun sign) and list what's unavailable (rising, houses) in an
`unavailable[]` array. Same principle as the Substack reader flagging paywalled teasers instead of
faking the body.

## 2. Repo layout — 7 flat skill folders

Mirrors the proven `dooleys-{skill}` pattern, `t-` prefixed so future *non-divination* T skills
can live in the same repo.

```
t-ai-skills/
  README.md            # skills table + setup + repo structure
  CLAUDE.md            # repo conventions (mirrors dooleys-ai-skills/CLAUDE.md)
  DESIGN.md            # this document
  LICENSE              # AGPL-3.0 (see §6)
  t-tarot/
  t-western-astrology/
  t-zi-wei-dou-shu/
  t-bazi/
  t-numerology/
  t-blood-type/
  t-chakras/
```

Each skill folder contains:

- `SKILL.md` — agent instructions. Frontmatter: `name`, `description` (precise — this is how T
  discovers the skill), `version`, `category: t`, optional `required_environment_variables` (none
  expected here). Plus when-to-use, step-by-step, inputs, output format.
- `README.md` — human setup + a testing walkthrough.
- Python entry script(s) at the skill root (e.g. `tarot.py`, `astrology.py`).
- `{skill}_common.py` — pure, side-effect-free logic (the unit-tested core).
- `data/` — bundled reference meanings (JSON/YAML), committed.
- `tests/` — offline unit tests for the pure logic.
- `requirements.txt`, `.gitignore`.

**No cross-skill imports.** Each folder runs standalone. (User requirement: skills are independent.)

## 3. Consistent JSON envelope

Every skill prints the same top-level shape so T sees one contract everywhere:

```json
{
  "timestamp": "2026-06-28T12:00:00+00:00",
  "skill": "t-western-astrology",
  "mode": "single | compatibility",
  "inputs": { "...echoed back for traceability..." },
  "result": { "...structured facts (the chart / cards / pillars / numbers)..." },
  "reference": { "...canonical meanings for exactly what came up..." },
  "unavailable": ["rising_sign: birth time not provided"],
  "notes": "free-text caveats"
}
```

- `result` is the computed truth. `reference` is the grounding so T interprets from canon, not
  memory. `unavailable` is the honesty array.

## 4. Output & privacy

Birth data is PII and T is **multi-user**. So skills **print the JSON envelope to stdout** by
default, with an optional `--output PATH`. This is a deliberate deviation from the dooleys
`output_{function}.json` convention — we do **not** want sensitive per-user birth data left sitting
in a shared skill folder. T captures stdout and routes it per user.

## 5. The seven skills

| Skill | Engine | Single-person output | Multi-person / compatibility | Inputs T must gather |
|---|---|---|---|---|
| **t-tarot** | build (real RNG draw) | spread (1/3-card, Celtic Cross) with reversals + per-position meanings | relationship spread (you / them / the connection) | optional question/topic, spread choice |
| **t-western-astrology** | `kerykeion` | sun/moon/**rising/descending** + all planets in signs+houses + aspects + **modality & element balance** | **synastry** (cross-aspects) + composite midpoints | birth date, **time**, place → (lat/lon/tz) |
| **t-zi-wei-dou-shu** 紫微斗數 | `py-iztro` (fallback: port on `lunar-python`) | 12 palaces + 14 major stars + 四化 + 五行局 | 合盤 — overlay two charts | birth date, **時辰**, gender, solar/lunar flag |
| **t-bazi** 八字 | `lunar-python` | four pillars (干支) + 十神 + element balance + 生肖 | 合婚 — element complement / clash | birth date, **time**, gender |
| **t-numerology** | build (arithmetic) | life-path, expression/destiny, personal-year + meanings | two life-paths + a relationship/compatibility number | birth date, name (optional) |
| **t-blood-type** 血型 | build (data lookup) | type → personality traits, strengths, frictions | A/B/O/AB pair compatibility | blood type(s) |
| **t-chakras** | build (reference + scaffold) | 7-chakra reference + a text-based balance assessment from self-described state | single only | self-described feelings/state |

### Per-skill engine notes

- **Western astrology** — `kerykeion` (AGPL-3.0) gives natal + synastry + composite. Rising sign
  and houses require exact birth time and location → coords + timezone.
- **紫微斗數** — `py-iztro` mirrors the JS `iztro` engine but pulls in `pythonmonkey` (an embedded
  JS interpreter). **Fork A decision: try `py-iztro` first; if it won't install cleanly, fall back
  to a pure-Python port** of the core placement (安星) built on `lunar-python`'s ganzhi/lunar data.
- **BaZi** — `lunar-python` (MIT) computes the four pillars, ten gods (十神), and zodiac from the
  lunar calendar.
- **Tarot / numerology / blood-type / chakras** — built from bundled data + a small deterministic
  engine. Tarot uses real RNG so T can't bias the draw; numerology is pure arithmetic.

### Offline city resolution

Astrology and the Chinese skills need coordinates + timezone. Bundle offline resolution
(`geonamescache` for city → lat/lon + country, `timezonefinder` for coords → IANA tz) so T can pass
a plain city name like `"Hong Kong"` — **no network call, no geonames API key**. If a city can't be
resolved, the skill asks (via `unavailable[]`/`notes`) for coords or a nearest major city.

### Graceful degradation (per skill)

- Astrology with no birth time → sun sign + sign-only planet positions where safe; rising, houses,
  moon-degree flagged unavailable.
- 紫微/BaZi with no 時辰/time → flag that hour pillar / time-sensitive palaces are unavailable.
- Numerology with no name → life-path + personal-year only; expression/destiny flagged unavailable.

## 6. Licensing

`kerykeion` is **AGPL-3.0** (viral). The whole repo is therefore licensed **AGPL-3.0** and stays
public, which satisfies the obligation. (Fork B decision: AGPL-3.0 for the repo.)

## 7. Inputs, gender, and time — what T collects

The computational skills need data T must gather conversationally and may store in the user's
profile:

- **Birth date** (all computational skills).
- **Birth time** (astrology rising/houses; 紫微 時辰; BaZi hour pillar). Degrade gracefully if absent.
- **Birth place** (astrology; resolved offline to lat/lon/tz).
- **Gender** (紫微 and BaZi need it for luck-cycle direction 大限/大運). Accept the traditional
  yin/yang-year convention the engines expect; pass through, don't editorialize.
- **Solar vs. lunar** date flag (Chinese skills; default solar, allow lunar).
- **Blood type** (blood-type skill only).

## 8. Build order

Per user: **build all seven in one run**, one by one, each independent. Sequence chosen so risk is
back-loaded and quick wins land first:

1. Repo scaffold: `README.md`, `CLAUDE.md`, `LICENSE`, `DESIGN.md`, `.gitignore`.
2. **t-numerology** (pure arithmetic — establishes the envelope + test pattern).
3. **t-blood-type** (data lookup).
4. **t-tarot** (RNG draw + data).
5. **t-chakras** (reference + assessment scaffold).
6. **t-bazi** (`lunar-python`, clean MIT lib).
7. **t-western-astrology** (`kerykeion`, AGPL).
8. **t-zi-wei-dou-shu** (`py-iztro`, riskiest dep; fall back to port if needed).
9. Final: repo `README.md` skills table, full test pass, push to a new GitHub repo `t-ai-skills`.

## 9. Testing standard (every skill)

- Unit tests for the pure logic in `{skill}_common.py` pass offline.
- The no-input / bad-input path exits cleanly with a helpful message (exit code documented).
- For library-backed skills, a live smoke test with a known birth example produces a sane chart.
- Generated artifacts cleaned up; no PII committed.

## 10. Out of scope (v1)

- Image inputs (face reading 面相, palm reading 手相) — text only for now.
- SVG/visual chart rendering (kerykeion can, but T delivers plain text on Telegram).
- Persistent per-user config inside skill folders (T owns user data in its profiles).

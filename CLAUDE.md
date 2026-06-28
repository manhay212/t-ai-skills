# CLAUDE.md — `t-ai-skills` (custom skills for the T agent)

This repo holds **self-contained, reusable skills** for **T** ("Your Secret Third Wheel"), a Hermes
agent running on a standalone laptop. T is a **chill, friendly companion** who *happens* to know a
set of fortune-telling / divination crafts and uses them when they come in handy in conversation.

**Claude builds and maintains skills directly in this repo** — clones, codes, **tests**, and pushes
(the skill-building exception). Read this before creating or editing any skill. The companion design
rationale lives in `DESIGN.md`.

---

## What a skill is

A folder `t-{skill-name}/` that is everything T needs to perform one divination craft:

- **`SKILL.md`** — AI-agent instructions. YAML frontmatter (`name`, `description`, `version`,
  `category: t`, optional `required_environment_variables`) + when-to-use + step-by-step + inputs +
  output format. The `description` is how T discovers the skill — make it precise.
- **`README.md`** — human setup + a testing walkthrough.
- **Working code** — Python, entry point(s) at the skill root (e.g. `tarot.py`, `astrology.py`).
  Factor pure logic into `{skill}_common.py`.
- **`data/`** — bundled reference meanings (committed): card meanings, sign/star/number canon, etc.
- **`requirements.txt`**, **`.gitignore`**.
- **`tests/`** — offline unit tests for the pure logic.

## Core philosophy (the whole point)

The skill is the **truth layer**: it computes the objective structure (the real chart, the actual
cards drawn, the 紫微 palaces, the correct life-path number) and returns **structured facts +
canonical reference meanings**. T is the **interpretation layer**: warmth, context, and knowing when
to bring it up. The skill never writes the "reading" prose.

**Honesty rule:** a skill NEVER fakes what it can't compute. Missing birth time → return what's
valid and list what's unavailable in `unavailable[]`. Never invent positions, cards, or numbers.

## Non-negotiable conventions

- **Naming:** folders `kebab-case` (`t-{skill-name}`); `SKILL.md` / `README.md` at skill root
  (what the agent loader expects).
- **Consistent JSON envelope** on every skill's stdout:
  `{timestamp, skill, mode, inputs, result, reference, unavailable, notes}`.
- **Print to stdout** by default (optional `--output PATH`). Birth data is PII and T is multi-user —
  do NOT leave per-user output files in the shared skill folder.
- **Self-contained, no cross-skill imports.** Each folder runs on its own.
- **No secrets, no PII committed.** Bundled `data/` is reference canon only.
- **Test before pushing:** unit tests for pure logic pass; the bad-input path exits cleanly; for
  library-backed skills, a live smoke test with a known example yields a sane result.

## Two flavors of skill

1. **Build-from-data** — fixed reference data + a small deterministic engine. Reference:
   `t-numerology` (arithmetic), `t-tarot` (real-RNG draw + card data), `t-blood-type`, `t-chakras`.
2. **Library-backed computation** — an established library does the astronomy/calendar math.
   `t-western-astrology` (`kerykeion`, AGPL-3.0), `t-bazi` (`lunar-python`, MIT),
   `t-zi-wei-dou-shu` (`py-iztro`; fall back to a pure-Python port on `lunar-python` if its
   `pythonmonkey` dependency won't install).

## Workflow for a new skill

1. **Read** this file + `DESIGN.md` + the closest reference skill.
2. **Build** with pure logic in `{skill}_common.py`; unit-test the pure parts (TDD).
3. **Test** (unit + bad-input path + live smoke for library skills); clean up artifacts.
4. **Document** `SKILL.md` (agent) and `README.md` (human + testing walkthrough).
5. **Update repo `README.md`** (skills table + structure).
6. **Commit & push.** GitHub authed via `gh`. Stage explicit paths (`git add t-{skill}/ README.md`),
   never `git add -A`. Do not modify other skills' folders without the user's say-so.

## Licensing

The repo is **AGPL-3.0** (because `kerykeion` is AGPL-3.0 and viral). Keep it public.

## Environment

- **Python** 3.10+ (`kerykeion`/`py-iztro` require it; host has 3.12).
- **GitHub:** authenticated via `gh` — clone/push without extra setup.
- Offline city resolution via `geonamescache` + `timezonefinder` (no geonames key, no network).

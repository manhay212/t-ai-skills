# t-bazi

BaZi / Four Pillars (八字 / 四柱) skill for **T**. Computes the four pillars, day master, ten gods,
nayin, Chinese zodiac, five-element balance, and luck pillars (大運) from a birth date/time/gender,
plus a simplified compatibility (合婚) for two people.

- **Calendar/ganzhi math:** [`lunar-python`](https://pypi.org/project/lunar-python/) (MIT).
- **Element balance, zodiac relationships, compatibility:** this skill's own pure logic
  (`bazi_common.py`), fully unit-tested offline without the library.

## Install

```bash
pip install -r requirements.txt   # lunar-python
```

## Usage

```bash
python3 bazi.py --date 1990-06-15 --time 14:30 --gender male
python3 bazi.py --date 1990-06-15                       # no time/gender -> graceful degradation
python3 bazi.py --date 1990-04-23 --time 09:00 --lunar  # lunar input date
python3 bazi.py --date 1990-06-15 --time 14:30 --gender male \
                --date2 1992-03-08 --time2 20:00 --gender2 female   # compatibility
```

Output is a JSON envelope on stdout (see `SKILL.md`). Exit `1` on bad date/time, `2` if the library
is missing.

## Testing walkthrough

```bash
# 1. Unit tests for the pure logic (no library needed)
python3 -m unittest discover -s tests
# -> Ran 17 tests ... OK

# 2. Single chart smoke test (needs lunar-python installed)
python3 bazi.py --date 1990-06-15 --time 14:30 --gender male
#    pillars 庚午 壬午 辛亥 乙未, day master 辛 (metal), zodiac 马

# 3. Graceful degradation (no time, no gender)
python3 bazi.py --date 1990-06-15
#    only year/month/day pillars; hour pillar + luck pillars listed under "unavailable"

# 4. Compatibility + bad input
python3 bazi.py --date 1990-06-15 --time 14:30 --gender male --date2 1992-03-08 --time2 20:00 --gender2 female
python3 bazi.py --date nope ; echo $?      # error + exit 1
```

## Files

- `bazi.py` — CLI entry; drives lunar-python, builds the JSON envelope.
- `bazi_common.py` — pure logic (element maps, balance, five-element & zodiac relationships, 合婚).
- `data/reference.json` — element traits + ten-god (十神) meanings.
- `tests/` — offline unit tests (pure logic only).

## Notes

The compatibility (合婚) here is a **simplified** model — year-branch zodiac relationship + day-master
element relationship + element complementarity. Traditional 合婚 is far deeper; this is for friendly
reflection, not matchmaking decisions.

# t-zi-wei-dou-shu

紫微斗數 (Zi Wei Dou Shu / Purple Star Astrology) skill for **T**. Computes the full 12-palace
astrolabe — 14 major stars with brightness and 四化 (祿權科忌), 命宮/身宮, 五行局, 命主/身主, zodiac —
from a birth date, time, and gender, plus a two-person comparison.

- **Astrolabe engine:** [`py-iztro`](https://pypi.org/project/py-iztro/) (a Python port of the
  `iztro` JS engine, via an embedded JS interpreter). Verified working on Python 3.12.
- **時辰 mapping, gender normalization, zodiac relationship, reference:** this skill's own pure logic
  (`ziwei_common.py`), unit-tested offline without the library.

## Install

```bash
pip install -r requirements.txt   # py-iztro (pulls in pythonmonkey)
```

## Usage

```bash
python3 ziwei.py --date 1990-06-15 --time 14:30 --gender female
python3 ziwei.py --date 1990-05-23 --time 09:00 --gender male --lunar
python3 ziwei.py --date 1990-06-15 --time 14:30 --gender female \
                 --date2 1992-03-08 --time2 20:00 --gender2 male   # comparison
```

Birth **time and gender are required** (the 命宮 depends on the 時辰). Output is traditional Chinese
by default (`--lang`). JSON envelope on stdout (see `SKILL.md`). Exit `1` on bad input, `2` if the
library is missing.

## Testing walkthrough

```bash
# 1. Unit tests for the pure logic (no library needed)
python3 -m unittest discover -s tests
# -> Ran 16 tests ... OK

# 2. Single chart (needs py-iztro). Verify the 命宮 tracks the birth time:
python3 ziwei.py --date 1990-06-15 --time 03:00 --gender female   # 命宮 辰, 七殺, 金四局
python3 ziwei.py --date 1990-06-15 --time 14:30 --gender female   # 命宮 亥, 巨門, 土五局
python3 ziwei.py --date 1990-06-15 --time 23:30 --gender female   # 命宮 午, 太陽(祿), 木三局

# 3. Comparison + error paths
python3 ziwei.py --date 1990-06-15 --time 14:30 --gender female --date2 1992-03-08 --time2 20:00 --gender2 male
python3 ziwei.py --date 1990-06-15 --gender female ; echo $?      # missing --time -> argparse error
```

## Files

- `ziwei.py` — CLI entry; drives py-iztro, builds the JSON envelope.
- `ziwei_common.py` — pure logic (時辰 index, gender, zodiac relationship, reference).
- `data/reference.json` — 14 major stars + 12 palaces + 4 mutagens meanings.
- `tests/` — offline unit tests (pure logic only).

## Notes

The life palace (命宮) is located via `earthly_branch_of_soul_palace` from the library (the
language-independent 命宮 marker), so it stays correct regardless of `--lang`. The compatibility mode
is a **simplified** comparison; full 紫微合盤 (palace overlay) is out of scope.

# t-western-astrology

Western natal-chart + synastry skill for **T**. Computes Sun/Moon/rising + all ten planets by sign,
house, and degree, element & modality balance, and aspects — and cross-aspects (synastry) between
two people.

- **Astronomy/chart:** [`kerykeion`](https://pypi.org/project/kerykeion/) (AGPL-3.0).
- **Offline city → lat/lng/timezone:** `geonamescache` + `timezonefinder` (bundled data, no network,
  no API key).
- **Sign mapping, element/modality tally:** this skill's own pure logic (`astrology_common.py`),
  unit-tested offline without kerykeion.

## Install

```bash
pip install -r requirements.txt   # kerykeion, geonamescache, timezonefinder
```

> **License note:** kerykeion is AGPL-3.0, so this repo is AGPL-3.0.

## Usage

```bash
python3 astrology.py --date 1990-06-15 --time 14:30 --city "Hong Kong"
python3 astrology.py --date 1990-06-15 --time 14:30 --lat 22.30 --lng 114.17 --tz Asia/Hong_Kong
python3 astrology.py --date 1990-06-15 --city "Hong Kong"        # no time -> no rising/houses
python3 astrology.py --date 1990-06-15 --time 14:30 --city "Hong Kong" \
                     --date2 1992-03-08 --time2 20:00 --city2 "Shanghai"   # synastry
```

Use `--country HK` to disambiguate a city name. Output is a JSON envelope on stdout (see `SKILL.md`).
Exit `1` on bad date / unresolvable city, `2` if kerykeion is missing.

## Testing walkthrough

```bash
# 1. Unit tests for the pure logic (no kerykeion needed)
python3 -m unittest discover -s tests
# -> Ran 8 tests ... OK

# 2. Single chart (needs deps installed)
python3 astrology.py --date 1990-06-15 --time 14:30 --city "Hong Kong"
#    Sun Gemini, Moon Pisces, Rising Libra; dominant element earth

# 3. Graceful degradation (no time)
python3 astrology.py --date 1990-06-15 --city "Hong Kong"
#    no rising/houses; listed under "unavailable"

# 4. Synastry + error paths
python3 astrology.py --date 1990-06-15 --time 14:30 --city "Hong Kong" --date2 1992-03-08 --time2 20:00 --city2 "Shanghai"
python3 astrology.py --date 1990-06-15 --time 14:30 --city "Zzxqville" ; echo $?   # error + exit 1
```

## Files

- `astrology.py` — CLI entry; drives kerykeion, builds the JSON envelope.
- `astrology_common.py` — pure logic (sign names, element/modality tally, reference).
- `astrology_geo.py` — offline city → lat/lng/tz resolution.
- `data/reference.json` — sign, planet, and aspect meanings.
- `tests/` — offline unit tests (pure logic only).

# t-blood-type

Blood-type personality (血型) skill for **T**. Looks up the East-Asian blood-type personality
framework for one person, or compatibility between two. Pure offline data lookup — **no
dependencies, no network**. This is pop-culture entertainment, not science.

## Usage

```bash
python3 blood_type.py --type A                 # single
python3 blood_type.py --type O --type2 AB      # compatibility
```

Input is forgiving: `a`, `A+`, `Type B`, `O型` all normalize to A/B/O/AB (Rh ignored). Output is a
JSON envelope on stdout (see `SKILL.md`). Exit `1` on an invalid type.

## Testing walkthrough

```bash
# 1. Unit tests
python3 -m unittest discover -s tests
# -> Ran 11 tests ... OK

# 2. Single
python3 blood_type.py --type a
#    expect blood_type A with keywords

# 3. Compatibility (O + AB is the lore "standout match")
python3 blood_type.py --type O --type2 ab
#    expect score 5

# 4. Bad input
python3 blood_type.py --type C ; echo $?
#    expect error + exit 1
```

## Files

- `blood_type.py` — CLI entry; builds the JSON envelope.
- `blood_type_common.py` — pure logic (normalize, profile, compatibility).
- `data/blood_types.json` — 4 type profiles + 10 unique pair compatibilities.
- `tests/` — offline unit tests.

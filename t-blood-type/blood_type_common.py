"""Pure logic for blood-type personality (血型) lookups. No I/O except load_data()."""
import json
import os

VALID = ("A", "B", "O", "AB")


def normalize_type(s):
    """Normalize a blood-type string to one of A/B/O/AB. Raises ValueError if invalid.
    Accepts 'a', 'A+', 'O-', 'Type B', 'O型', etc. (Rh factor is ignored — it has no
    bearing on the personality framework)."""
    if s is None:
        raise ValueError("no blood type given")
    cleaned = str(s).upper()
    for junk in ("TYPE", "型", "BLOOD", " "):
        cleaned = cleaned.replace(junk, "")
    cleaned = cleaned.strip().rstrip("+-").strip()
    if cleaned not in VALID:
        raise ValueError(f"invalid blood type: {s!r} (expected A, B, O, or AB)")
    return cleaned


def load_data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "blood_types.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def profile(t):
    """Personality profile for a normalized type."""
    return load_data()["types"][normalize_type(t)]


def compatibility(a, b):
    """Compatibility entry for a pair (symmetric)."""
    a, b = normalize_type(a), normalize_type(b)
    table = load_data()["compatibility"]
    key = f"{a}-{b}"
    if key in table:
        return table[key]
    return table[f"{b}-{a}"]

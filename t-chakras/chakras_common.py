"""Pure chakra logic: reference data + a simple balance assessment. No I/O except load."""
import json
import os

CHAKRA_KEYS = ["root", "sacral", "solar_plexus", "heart", "throat", "third_eye", "crown"]

# Score 0-10. Balanced band is 4-7 inclusive; below is underactive, above is overactive.
_UNDER_MAX = 3
_OVER_MIN = 8


def load_chakras():
    """Return an ordered dict {key: chakra} (insertion order = CHAKRA_KEYS)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "chakras.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {k: data[k] for k in CHAKRA_KEYS}


def get_chakra(key):
    if key not in CHAKRA_KEYS:
        raise KeyError(f"unknown chakra: {key!r}")
    return load_chakras()[key]


def classify(score):
    """Classify a 0-10 energy score into underactive / balanced / overactive."""
    if not (0 <= score <= 10):
        raise ValueError(f"score must be 0-10, got {score}")
    if score <= _UNDER_MAX:
        return "underactive"
    if score >= _OVER_MIN:
        return "overactive"
    return "balanced"


def _signs_for(chakra, status):
    return {"underactive": chakra["underactive"],
            "overactive": chakra["overactive"],
            "balanced": chakra["balanced"]}[status]


def assess(scores):
    """scores: {chakra_key: 0-10}. Returns {key: {name, score, status, signs, practices, ...}}.
    Raises KeyError for an unknown chakra, ValueError for an out-of-range score."""
    chakras = load_chakras()
    out = {}
    for key, score in scores.items():
        if key not in CHAKRA_KEYS:
            raise KeyError(f"unknown chakra: {key!r}")
        ch = chakras[key]
        status = classify(score)
        out[key] = {
            "name": ch["name"],
            "sanskrit": ch["sanskrit"],
            "color": ch["color"],
            "score": score,
            "status": status,
            "focus": ch["focus"],
            "signs": _signs_for(ch, status),
            "practices": ch["practices"] if status != "balanced" else [],
        }
    return out

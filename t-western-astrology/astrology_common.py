"""Pure astrology helpers — sign-name mapping, element/modality tally, reference.
Independent of kerykeion so it can be unit-tested offline."""
import json
import os

_SIGN_FULL = {
    "Ari": "Aries", "Tau": "Taurus", "Gem": "Gemini", "Can": "Cancer",
    "Leo": "Leo", "Vir": "Virgo", "Lib": "Libra", "Sco": "Scorpio",
    "Sag": "Sagittarius", "Cap": "Capricorn", "Aqu": "Aquarius", "Pis": "Pisces",
}
ELEMENTS = ["fire", "earth", "air", "water"]
MODALITIES = ["cardinal", "fixed", "mutable"]


def full_sign(abbr):
    """Map a kerykeion 3-letter sign ('Gem') to its full name ('Gemini')."""
    return _SIGN_FULL.get(abbr, abbr)


def tally_balance(points):
    """Count elements and modalities across a list of points (dicts with
    'element' and 'quality'). Returns {'elements': {...}, 'modalities': {...}}."""
    elements = {e: 0 for e in ELEMENTS}
    modalities = {m: 0 for m in MODALITIES}
    for p in points:
        el = (p.get("element") or "").lower()
        q = (p.get("quality") or "").lower()
        if el in elements:
            elements[el] += 1
        if q in modalities:
            modalities[q] += 1
    return {"elements": elements, "modalities": modalities}


def dominant(counts):
    """Key with the highest count (ties broken by canonical order)."""
    return max(counts, key=lambda k: counts[k])


def load_reference():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "reference.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

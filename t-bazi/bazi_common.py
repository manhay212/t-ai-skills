"""Pure BaZi (八字) analysis logic — element mapping, balance, five-element and
zodiac relationships, and a simplified compatibility (合婚) score.

Independent of lunar-python: it operates on the 干支 (ganzhi) strings that the
library produces, so it is fully unit-testable offline.
"""

# Heavenly stems (天干) -> five element (五行)
_GAN_WUXING = {
    "甲": "wood", "乙": "wood", "丙": "fire", "丁": "fire", "戊": "earth",
    "己": "earth", "庚": "metal", "辛": "metal", "壬": "water", "癸": "water",
}
# Earthly branches (地支) -> primary five element
_ZHI_WUXING = {
    "子": "water", "丑": "earth", "寅": "wood", "卯": "wood", "辰": "earth",
    "巳": "fire", "午": "fire", "未": "earth", "申": "metal", "酉": "metal",
    "戌": "earth", "亥": "water",
}
ELEMENTS = ["wood", "fire", "earth", "metal", "water"]
ELEMENT_ZH = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}

# Generating cycle 生: each element generates the next.
_GENERATES = {"wood": "fire", "fire": "earth", "earth": "metal", "metal": "water", "water": "wood"}
# Controlling cycle 克: each element controls another.
_CONTROLS = {"wood": "earth", "earth": "water", "water": "fire", "fire": "metal", "metal": "wood"}

# Earthly-branch zodiac relationships
_SAN_HE = [{"申", "子", "辰"}, {"寅", "午", "戌"}, {"巳", "酉", "丑"}, {"亥", "卯", "未"}]
_LIU_HE = [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}]
_LIU_CHONG = [{"子", "午"}, {"丑", "未"}, {"寅", "申"}, {"卯", "酉"}, {"辰", "戌"}, {"巳", "亥"}]


def element_of_gan(gan):
    return _GAN_WUXING[gan]


def element_of_zhi(zhi):
    return _ZHI_WUXING[zhi]


def element_balance(pillars):
    """Count five elements across the 8 chars of the four ganzhi pillars."""
    counts = {e: 0 for e in ELEMENTS}
    for gz in pillars:
        if len(gz) != 2:
            raise ValueError(f"pillar must be 2 chars (gan+zhi), got {gz!r}")
        counts[element_of_gan(gz[0])] += 1
        counts[element_of_zhi(gz[1])] += 1
    return counts


def missing_elements(balance):
    """Elements with zero count, in canonical order."""
    return [e for e in ELEMENTS if balance.get(e, 0) == 0]


def generates(a, b):
    return _GENERATES.get(a) == b


def controls(a, b):
    return _CONTROLS.get(a) == b


def element_relationship(a, b):
    if a == b:
        return "same"
    if generates(a, b):
        return "a_generates_b"
    if generates(b, a):
        return "b_generates_a"
    if controls(a, b):
        return "a_controls_b"
    if controls(b, a):
        return "b_controls_a"
    return "neutral"


def zodiac_relationship(zhi_a, zhi_b):
    """Relationship between two earthly branches: 六合 / 三合 / 六沖 / 平 (neutral)."""
    pair = {zhi_a, zhi_b}
    if len(pair) == 1:
        return "平"
    if pair in _LIU_HE:
        return "六合"
    for trine in _SAN_HE:
        if pair <= trine:
            return "三合"
    if pair in _LIU_CHONG:
        return "六沖"
    return "平"


def _clamp(n, lo=1, hi=5):
    return max(lo, min(hi, n))


def compatibility(chart_a, chart_b):
    """Simplified 合婚: combine year-branch zodiac relationship, day-master element
    relationship, and (if both charts give pillars) element complementarity.

    Each chart is a dict with: year_zhi (optional), day_gan (optional),
    pillars (optional list of 4 ganzhi). Returns a dict with score 1-5 + notes.
    """
    score = 3
    notes = []
    out = {}

    za, zb = chart_a.get("year_zhi"), chart_b.get("year_zhi")
    if za and zb:
        rel = zodiac_relationship(za, zb)
        out["zodiac"] = rel
        if rel in ("六合", "三合"):
            score += 1
            notes.append(f"Year-branch {rel} — a naturally harmonious zodiac pairing.")
        elif rel == "六沖":
            score -= 1
            notes.append("Year-branch 六沖 (clash) — more friction to navigate, but also spark.")
        else:
            notes.append("Year-branch neutral — neither strong harmony nor clash.")
    else:
        out["zodiac"] = None

    ga, gb = chart_a.get("day_gan"), chart_b.get("day_gan")
    if ga and gb:
        ea, eb = element_of_gan(ga), element_of_gan(gb)
        rel = element_relationship(ea, eb)
        out["day_master"] = {"a": ea, "b": eb, "relationship": rel}
        if rel in ("a_generates_b", "b_generates_a"):
            score += 1
            notes.append("Day masters in a generating (生) cycle — one naturally nourishes the other.")
        elif rel in ("a_controls_b", "b_controls_a"):
            score -= 1
            notes.append("Day masters in a controlling (克) cycle — a dynamic of challenge.")
        else:
            notes.append("Day masters share the same element — comfortable and like-minded.")
    else:
        out["day_master"] = None

    pa, pb = chart_a.get("pillars"), chart_b.get("pillars")
    if pa and pb:
        bal_a, bal_b = element_balance(pa), element_balance(pb)
        miss_a, miss_b = missing_elements(bal_a), missing_elements(bal_b)
        covered = [e for e in miss_a if bal_b.get(e, 0) > 0] + \
                  [e for e in miss_b if bal_a.get(e, 0) > 0]
        out["complementarity"] = {
            "a_missing": miss_a, "b_missing": miss_b,
            "gaps_covered": sorted(set(covered)),
        }
        if len(covered) >= 2:
            score += 1
            notes.append("Their charts complement — each supplies elements the other lacks.")
    else:
        out["complementarity"] = None

    out["score"] = _clamp(score)
    out["notes"] = notes
    return out

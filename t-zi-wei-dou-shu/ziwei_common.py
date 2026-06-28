"""Pure 紫微斗數 helpers — 時辰 index, gender normalization, zodiac relationship,
reference. Independent of py-iztro so it can be unit-tested offline."""
import json
import os

# iztro time index: 0 = 早子時 (00:00-00:59) ... 12 = 晚子時 (23:00-23:59).
# (hour + 1) // 2 maps cleanly: 0->0, 1/2->1(丑), ... 21/22->11(亥), 23->12.
def hour_to_time_index(hour):
    if not (0 <= hour <= 23):
        raise ValueError(f"hour must be 0-23, got {hour}")
    return (hour + 1) // 2


_GENDER = {"male": "男", "m": "男", "男": "男", "female": "女", "f": "女", "女": "女"}


def normalize_gender(g):
    if g is None:
        raise ValueError("gender is required (male/female) for 紫微斗數")
    key = str(g).strip().lower()
    # keep CJK as-is (lower() doesn't affect them)
    if key in _GENDER:
        return _GENDER[key]
    if str(g).strip() in _GENDER:
        return _GENDER[str(g).strip()]
    raise ValueError(f"invalid gender: {g!r} (expected male/female/男/女)")


# Earthly-branch zodiac relationships (traditional branches)
_SAN_HE = [{"申", "子", "辰"}, {"寅", "午", "戌"}, {"巳", "酉", "丑"}, {"亥", "卯", "未"}]
_LIU_HE = [{"子", "丑"}, {"寅", "亥"}, {"卯", "戌"}, {"辰", "酉"}, {"巳", "申"}, {"午", "未"}]
_LIU_CHONG = [{"子", "午"}, {"丑", "未"}, {"寅", "申"}, {"卯", "酉"}, {"辰", "戌"}, {"巳", "亥"}]


def zodiac_relationship(branch_a, branch_b):
    pair = {branch_a, branch_b}
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


def load_reference():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "reference.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

"""Offline city -> (lat, lng, timezone) resolution using geonamescache + timezonefinder.
No network, no API key — geonamescache bundles its city database."""
import functools


@functools.lru_cache(maxsize=1)
def _cities():
    import geonamescache
    return geonamescache.GeonamesCache().get_cities()


@functools.lru_cache(maxsize=1)
def _tzfinder():
    from timezonefinder import TimezoneFinder
    return TimezoneFinder()


def resolve_city(name, country=None):
    """Resolve a city name to {city, country, lat, lng, tz}. Picks the most populous
    match. Returns None if no city matches. `country` is an optional ISO-2 code filter."""
    name_l = name.strip().lower()
    matches = []
    for c in _cities().values():
        if c["name"].lower() == name_l:
            matches.append(c)
        elif name_l in [a.lower() for a in c.get("alternatenames", [])]:
            matches.append(c)
    if country:
        matches = [c for c in matches if c["countrycode"].lower() == country.lower()]
    if not matches:
        return None
    best = max(matches, key=lambda c: c.get("population", 0) or 0)
    lat, lng = float(best["latitude"]), float(best["longitude"])
    tz = _tzfinder().timezone_at(lat=lat, lng=lng)
    return {"city": best["name"], "country": best["countrycode"],
            "lat": lat, "lng": lng, "tz": tz}

import math
from typing import Tuple


def haversine_distance_m(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Return great-circle distance in meters between two (lat, lng) points."""
    R = 6371e3
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(h))

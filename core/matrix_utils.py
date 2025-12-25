from typing import List, Tuple, Dict, Any

import numpy as np

from core.haversine import haversine_distance_m

try:
    import googlemaps
except ImportError:  # Optional
    googlemaps = None


Location = Dict[str, Any]


def build_distance_matrix(
    locations: List[Location],
    api_key: str | None = None,
) -> Tuple[np.ndarray, str, str | None]:
    """
    Build distance matrix (meters). Uses Google Distance Matrix if possible;
    otherwise falls back to haversine straight-line distances.
    """
    coords = [(loc["lat"], loc["lng"]) for loc in locations]
    n = len(coords)
    matrix = np.zeros((n, n), dtype=float)

    def fill_haversine() -> np.ndarray:
        for i, a in enumerate(coords):
            for j, b in enumerate(coords):
                matrix[i, j] = haversine_distance_m(a, b)
        return matrix

    if api_key and googlemaps is not None:
        try:
            client = googlemaps.Client(key=api_key)
            response = client.distance_matrix(
                origins=coords,
                destinations=coords,
                mode="driving",
                units="metric",
            )
            for i, row in enumerate(response["rows"]):
                for j, element in enumerate(row["elements"]):
                    if element.get("status") == "OK":
                        matrix[i, j] = element["distance"]["value"]
                    else:
                        matrix[i, j] = haversine_distance_m(coords[i], coords[j])
            return matrix, "google", None
        except Exception as exc:  # noqa: BLE001
            return fill_haversine(), "haversine", str(exc)

    return fill_haversine(), "haversine", None

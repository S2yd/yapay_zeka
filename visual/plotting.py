from typing import List, Dict, Any

import altair as alt
import folium
import numpy as np
import pandas as pd

Location = Dict[str, Any]


def build_route_map(locations: List[Location], order: List[int], tiles: str) -> folium.Map:
    center_lat = np.mean([l["lat"] for l in locations])
    center_lng = np.mean([l["lng"] for l in locations])
    fmap = folium.Map(location=[center_lat, center_lng], zoom_start=14, tiles=tiles)

    for idx, loc in enumerate(locations):
        label = loc.get("id", idx)
        folium.Marker(
            [loc["lat"], loc["lng"]],
            tooltip=f"{label} - {loc['name']}",
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(fmap)

    path = [locations[i] for i in order] + [locations[order[0]]]
    folium.PolyLine(
        locations=[(p["lat"], p["lng"]) for p in path],
        color="#7dd3fc",
        weight=5,
    ).add_to(fmap)
    return fmap


def build_history_chart(history: List[float]) -> alt.Chart:
    df = pd.DataFrame(
        {
            "iter": list(range(1, len(history) + 1)),
            "best_km": [h / 1000 for h in history],
        }
    )
    chart = alt.Chart(df).mark_line().encode(
        x="iter",
        y="best_km",
    )
    return chart

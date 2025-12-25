APP_TITLE = "Isparta Acil Durum Dronu icin Yol Optimizasyonu (ACO)"
APP_SUBTITLE = "Surus mesafeleri Google Distance Matrix API (varsa), yoksa haversine fallback."

MAP_TILES = "cartodbpositron"
START_INDEX = 0

SLIDERS = {
    "iterations": (10, 400, 120, 10),
    "num_ants": (5, 100, 30, 1),
    "alpha": (0.5, 3.0, 1.0, 0.1),
    "beta": (1.0, 6.0, 3.0, 0.1),
    "evaporation": (0.05, 0.9, 0.5, 0.05),
    "q": (0.1, 5.0, 1.0, 0.1),
}

AQI_CATEGORIES = {
    (0, 50): "Good",
    (51, 100): "Satisfactory",
    (101, 200): "Moderate",
    (201, 300): "Poor",
    (301, 400): "Very Poor",
    (401, 500): "Severe"
}


FEATURE_COLUMNS = [
    "aod_550",
    "no2_col",
    "so2_col",
    "co_col",
    "o3_col",
    "hcho_col",
    "t2m",
    "u10",
    "v10",
    "sp",
    "blh",
    "tp",
    "fire_count"
]
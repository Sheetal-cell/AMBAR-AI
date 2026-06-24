from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///./ambar.db"

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS aqi_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pred_date TEXT,
        lat REAL,
        lon REAL,
        aqi_pred REAL,
        aqi_category TEXT,
        model_version TEXT,
        confidence REAL
    )
    """))

    conn.execute(text("""
    INSERT INTO aqi_predictions
    (pred_date, lat, lon, aqi_pred, aqi_category, model_version, confidence)
    VALUES
    ('2025-01-01', 28.6139, 77.2090, 180, 'Moderate', 'v1', 0.92),
    ('2025-01-01', 19.0760, 72.8777, 220, 'Poor', 'v1', 0.88),
    ('2025-01-01', 12.9716, 77.5946, 110, 'Satisfactory', 'v1', 0.95)
    """))

print("Database initialized successfully.")
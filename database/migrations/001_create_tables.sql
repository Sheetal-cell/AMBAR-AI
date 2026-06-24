-- Satellite observations (normalized 0.1° grid)
CREATE TABLE satellite_obs (
  id          BIGSERIAL PRIMARY KEY,
  obs_date    DATE NOT NULL,
  geom        GEOMETRY(POINT, 4326) NOT NULL,
  lat         FLOAT, lon FLOAT,
  no2_col     FLOAT,   -- mol/m²
  so2_col     FLOAT,
  co_col      FLOAT,
  o3_col      FLOAT,
  hcho_col    FLOAT,   -- mol/m²  ← primary hotspot variable
  aod_550     FLOAT,   -- INSAT-3D
  qa_value    FLOAT    -- S5P QA flag, keep ≥ 0.75
);
CREATE INDEX ON satellite_obs USING GIST(geom);
CREATE INDEX ON satellite_obs(obs_date);

-- ERA5 meteorological grid (collocated to same 0.1° grid)
CREATE TABLE era5_meteo (
  id          BIGSERIAL PRIMARY KEY,
  obs_date    DATE NOT NULL,
  geom        GEOMETRY(POINT, 4326) NOT NULL,
  u10         FLOAT,   -- 10m U wind m/s
  v10         FLOAT,   -- 10m V wind m/s
  t2m         FLOAT,   -- 2m temperature K
  sp          FLOAT,   -- surface pressure Pa
  blh         FLOAT,   -- boundary layer height m
  tp          FLOAT    -- total precipitation m
);
CREATE INDEX ON era5_meteo USING GIST(geom);

-- CPCB ground station AQI (training labels)
CREATE TABLE cpcb_aqi (
  id          BIGSERIAL PRIMARY KEY,
  station_id  VARCHAR(32) NOT NULL,
  obs_datetime TIMESTAMPTZ NOT NULL,
  geom        GEOMETRY(POINT, 4326) NOT NULL,
  aqi         FLOAT,
  pm25        FLOAT,
  pm10        FLOAT,
  no2         FLOAT,
  so2         FLOAT,
  co          FLOAT,
  o3          FLOAT
);

-- AQI predictions (model output)
CREATE TABLE aqi_predictions (
  id          BIGSERIAL PRIMARY KEY,
  pred_date   DATE NOT NULL,
  geom        GEOMETRY(POINT, 4326) NOT NULL,
  aqi_pred    FLOAT NOT NULL,
  aqi_category VARCHAR(20),  -- Good/Satisfactory/Moderate/Poor/Very Poor/Severe
  model_version VARCHAR(16),
  confidence  FLOAT
);
CREATE INDEX ON aqi_predictions USING GIST(geom);

-- HCHO hotspot clusters (DBSCAN output)
CREATE TABLE hcho_hotspots (
  id              BIGSERIAL PRIMARY KEY,
  cluster_id      INTEGER NOT NULL,
  detection_date  DATE NOT NULL,
  geom            GEOMETRY(POLYGON, 4326) NOT NULL,  -- convex hull of cluster
  centroid        GEOMETRY(POINT, 4326),
  n_pixels        INTEGER,
  mean_hcho       FLOAT,
  max_hcho        FLOAT,
  persistence_days INTEGER DEFAULT 1,
  state_name      VARCHAR(64)
);
CREATE INDEX ON hcho_hotspots USING GIST(geom);

-- FIRMS fire pixels
CREATE TABLE fire_pixels (
  id          BIGSERIAL PRIMARY KEY,
  acq_date    DATE NOT NULL,
  geom        GEOMETRY(POINT, 4326) NOT NULL,
  source      VARCHAR(8),  -- MODIS or VIIRS
  frp         FLOAT,       -- fire radiative power MW
  confidence  INTEGER,
  brightness  FLOAT
);
CREATE INDEX ON fire_pixels USING GIST(geom);

-- Fire–HCHO lag correlation results
CREATE TABLE fire_hcho_correlation (
  id          BIGSERIAL PRIMARY KEY,
  analysis_date DATE NOT NULL,
  region_geom GEOMETRY(POLYGON, 4326),
  lag_days    INTEGER,
  pearson_r   FLOAT,
  spearman_r  FLOAT,
  p_value     FLOAT,
  n_samples   INTEGER
);
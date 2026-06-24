import geopandas as gpd
from shapely.geometry import Point


def create_point(lat, lon):
    return Point(lon, lat)


def to_geodataframe(df, lat_col="lat", lon_col="lon"):
    geometry = [
        Point(xy)
        for xy in zip(df[lon_col], df[lat_col])
    ]

    return gpd.GeoDataFrame(
        df,
        geometry=geometry,
        crs="EPSG:4326"
    )
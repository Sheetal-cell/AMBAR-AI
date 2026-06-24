import geopandas as gpd

from sqlalchemy import create_engine

from src.config.settings import settings

engine = create_engine(
    settings.DATABASE_URL
)


def load_clusters():

    query = """
    SELECT
        cluster_id,
        geom,
        hcho_col
    FROM hotspot_points
    WHERE cluster_id != -1
    """

    return gpd.read_postgis(
        query,
        engine,
        geom_col="geom"
    )


def generate_polygons(
    gdf
):

    rows = []

    for cluster_id in (
        gdf.cluster_id.unique()
    ):

        subset = gdf[
            gdf.cluster_id
            ==
            cluster_id
        ]

        hull = (
            subset.unary_union
            .convex_hull
        )

        rows.append(
            {
                "cluster_id":
                    cluster_id,
                "geometry":
                    hull,
                "mean_hcho":
                    subset[
                        "hcho_col"
                    ].mean(),
                "max_hcho":
                    subset[
                        "hcho_col"
                    ].max(),
                "n_pixels":
                    len(subset)
            }
        )

    return gpd.GeoDataFrame(
        rows,
        crs="EPSG:4326"
    )


def main():

    clusters = load_clusters()

    polygons = (
        generate_polygons(
            clusters
        )
    )

    polygons.to_file(
        "data/exports/hcho_polygons.geojson",
        driver="GeoJSON"
    )


if __name__ == "__main__":
    main()
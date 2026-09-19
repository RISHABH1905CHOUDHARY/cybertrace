"""Geospatial helper utilities and calculations."""

import math
from typing import Any, Dict, List, Tuple


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) using Haversine formula.
    """
    r = 6371.0  # Earth's radius in kilometers

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2.0) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    distance = r * c
    return round(distance, 3)


def get_bounding_box(latitude: float, longitude: float, radius_km: float) -> Tuple[float, float, float, float]:
    """
    Returns min_lat, max_lat, min_lon, max_lon bounding box for a given radius in km.
    """
    r = 6371.0
    lat_delta = math.degrees(radius_km / r)
    lon_delta = math.degrees(radius_km / (r * math.cos(math.radians(latitude))))
    
    min_lat = latitude - lat_delta
    max_lat = latitude + lat_delta
    min_lon = longitude - lon_delta
    max_lon = longitude + lon_delta
    
    return min_lat, max_lat, min_lon, max_lon


def to_geojson_feature(
    latitude: float,
    longitude: float,
    properties: Dict[str, Any],
) -> Dict[str, Any]:
    """Convert coordinates and properties to a standard GeoJSON Feature."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [longitude, latitude],  # GeoJSON is [lon, lat]
        },
        "properties": properties,
    }


def to_geojson_feature_collection(features: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Wrap a list of GeoJSON features in a FeatureCollection."""
    return {
        "type": "FeatureCollection",
        "features": features,
    }

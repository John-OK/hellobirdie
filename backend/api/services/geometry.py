from math import asin, cos, pi, radians, sin, sqrt

KM_PER_DEGREE_LAT = 111.32


def compute_bounding_box(lat, lon, radius_km):
    delta_lat = radius_km / KM_PER_DEGREE_LAT
    delta_lon = radius_km / (KM_PER_DEGREE_LAT * cos(radians(lat)))
    lat_min = lat - delta_lat
    lon_min = lon - delta_lon
    lat_max = lat + delta_lat
    lon_max = lon + delta_lon

    return lat_min, lon_min, lat_max, lon_max


def haversine_km(lat1, lon1, lat2, lon2):
    EARTH_RADIUS_KM = 6371.0088  # Earth's radius
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = (sin(delta_lat / 2)) ** 2 + cos(lat1_rad) * cos(lat2_rad) * (
        sin(delta_lon / 2)
    ) ** 2
    c = 2 * asin(min(1, sqrt(a)))
    distance_km = EARTH_RADIUS_KM * c
    return distance_km

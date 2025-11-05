KM_PER_DEGREE_LAT = 111.32


def compute_bounding_box(lat, lon, radius_km):
    delta_lat = radius_km / KM_PER_DEGREE_LAT
    lat_min = lat - delta_lat
    lon_min = lon
    lat_max = lat + delta_lat
    lon_max = lon

    return lat_min, lon_min, lat_max, lon_max

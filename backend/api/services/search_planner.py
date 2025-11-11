from api.services.geometry import compute_bounding_box

SEAM_MIN = -179.99
SEAM_MAX = 179.99


def split_box(lat_min, lon_min, lat_max, lon_max):
    if lon_min < -180:
        lon_min += 360
    if lon_max > 180:
        lon_max -= 360

    return [
        (lat_min, lon_min, lat_max, SEAM_MAX),
        (lat_min, SEAM_MIN, lat_max, lon_max),
    ]


def plan_query_boxes(lat, lon, radius_km):
    box = compute_bounding_box(lat, lon, radius_km)
    lat_min = box[0]
    lon_min = box[1]
    lat_max = box[2]
    lon_max = box[3]

    if lon_min < -180 or lon_max > 180:
        return split_box(lat_min, lon_min, lat_max, lon_max)

    return [box]

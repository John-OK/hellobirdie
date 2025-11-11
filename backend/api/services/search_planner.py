from api.services.geometry import compute_bounding_box


def plan_query_boxes(lat, lon, radius_km):
    box = compute_bounding_box(lat, lon, radius_km)

    return [box]

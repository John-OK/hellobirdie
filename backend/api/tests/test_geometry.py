from django.test import TestCase
from api.services.geometry import compute_bounding_box


class ComputeBoundingBoxTestCase(TestCase):

    LAT = 40.0
    LON = 111.0
    KM_PER_DEGREE_LAT = 111.32

    def _km_to_degrees_lat(self, km):
        return km / self.KM_PER_DEGREE_LAT

    def test_returns_expected_latitude_extent_unrounded_at_40deg(self):
        """Test computes unrounded bbox for a mid‑latitude center and 50 km radius;
        latitude extent matches expected within tolerance (0.005°); mins < maxes."""

        radius_km = 50.0
        box = compute_bounding_box(self.LAT, self.LON, radius_km)
        lat_min = box[0]
        lat_max = box[2]
        radius_degrees = self._km_to_degrees_lat(radius_km)

        for coord in box:
            self.assertIsInstance(coord, float)
        self.assertEqual(len(box), 4)
        self.assertLess(lat_min, lat_max)
        self.assertAlmostEqual(lat_min, self.LAT - radius_degrees, delta=0.005)
        self.assertAlmostEqual(lat_max, self.LAT + radius_degrees, delta=0.005)

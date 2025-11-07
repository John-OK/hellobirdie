from django.test import TestCase
from api.services.geometry import compute_bounding_box, haversine_km
from math import cos, pi, radians


class ComputeBoundingBoxTestCase(TestCase):

    LAT = 40.0
    LON = 111.0
    KM_PER_DEGREE_LAT = 111.32

    def _km_to_degrees_lat(self, km):
        return km / self.KM_PER_DEGREE_LAT

    def _km_to_degrees_lon(self, lat, km):
        return km / (self.KM_PER_DEGREE_LAT * cos(lat * (pi / 180)))

    def test_returns_expected_latitude_extent_unrounded_at_40deg(self):
        """Test computes unrounded bbox for a mid‑latitude center and 50 km radius;
        latitude extent matches expected within tolerance (0.005°); mins < maxes."""

        radius_km = 50.0
        box = compute_bounding_box(self.LAT, self.LON, radius_km)
        lat_min = box[0]
        lat_max = box[2]
        radius_degrees_lat = self._km_to_degrees_lat(radius_km)

        for coord in box:
            self.assertIsInstance(coord, float)
        self.assertEqual(len(box), 4)
        self.assertLess(lat_min, lat_max)
        self.assertAlmostEqual(lat_min, self.LAT - radius_degrees_lat, delta=0.005)
        self.assertAlmostEqual(lat_max, self.LAT + radius_degrees_lat, delta=0.005)

    def test_returns_expected_longitude_extent_unrounded_at_40deg_lat(self):
        """Test computes unrounded bbox for a mid‑longitude center at 40° lat and 50 km radius;
        longitude extent matches expected within tolerance (0.005°); mins < maxes."""

        radius_km = 50.0
        box = compute_bounding_box(self.LAT, self.LON, radius_km)
        lon_min = box[1]
        lon_max = box[3]
        radius_degrees_lon = self._km_to_degrees_lon(self.LAT, radius_km)

        for coord in box:
            self.assertIsInstance(coord, float)
        self.assertEqual(len(box), 4)
        self.assertLess(lon_min, lon_max)
        self.assertAlmostEqual(lon_min, self.LON - radius_degrees_lon, delta=0.005)
        self.assertAlmostEqual(lon_max, self.LON + radius_degrees_lon, delta=0.005)

    def test_longitude_degree_span_is_larger_at_60deg_lat_than_40deg_lat(self):
        """At fixed radius, longitudinal span in degrees at 60° lat is larger than at 40° lat."""

        radius_km = 50.0
        lat_60deg = 60.0
        box_60deg = compute_bounding_box(lat_60deg, self.LON, radius_km)
        lon_min_60deg = box_60deg[1]
        lon_max_60deg = box_60deg[3]
        radius_degrees_lon_60deg = self._km_to_degrees_lon(lat_60deg, radius_km)

        box_40deg = compute_bounding_box(self.LAT, self.LON, radius_km)
        lon_min_40deg = box_40deg[1]
        lon_max_40deg = box_40deg[3]
        extent_40deg = lon_max_40deg - lon_min_40deg
        extent_60deg = lon_max_60deg - lon_min_60deg

        for coord in box_60deg:
            self.assertIsInstance(coord, float)
        self.assertEqual(len(box_60deg), 4)
        self.assertLess(lon_min_60deg, lon_max_60deg)
        self.assertAlmostEqual(
            lon_min_60deg, self.LON - radius_degrees_lon_60deg, delta=0.005
        )
        self.assertAlmostEqual(
            lon_max_60deg, self.LON + radius_degrees_lon_60deg, delta=0.005
        )
        self.assertGreater(extent_60deg, extent_40deg)

    def test_haversine_zero_distance_is_zero(self):
        """Test that returns 0.0 km for identical coordinates"""

        haversine_distance = haversine_km(40, 111, 40, 111)

        self.assertEqual(haversine_distance, 0)

    def test_haversine_one_degree_latitude_is_approx_111_32_km(self):
        """Test that 1° latitude ~111.32 km (±0.2 km) from (0°, 0°) to (1°, 0°)"""

        haversine_distance = haversine_km(0, 0, 1, 0)

        self.assertAlmostEqual(haversine_distance, 111.32, delta=0.2)

    def test_haversine_one_degree_longitude_at_40deg_lat_is_approx_111_32_cos40_km(
        self,
    ):
        """Test that 1° longitude is ~(111.32 * cos(rad(40°))) km (±0.2 km) at 40° latitude"""

        haversine_distance = haversine_km(40, 0, 40, 1)

        self.assertAlmostEqual(haversine_distance, 111.32 * cos(radians(40)), delta=0.2)

    def test_haversine_is_commutative(self):
        """Haversine is symmetric: d(A,B) == d(B,A) within a tiny tolerance"""

        haversine_distance1 = haversine_km(10, 20, 15, 25)
        haversine_distance2 = haversine_km(15, 25, 10, 20)

        self.assertAlmostEqual(haversine_distance1, haversine_distance2, delta=0.000001)

    def test_haversine_antimeridian_1deg_longitude_at_equator_is_approx_111_32_km(self):
        """At 0° latitude, (0°, 179.5°) and (0°, −179.5°) are 1° apart across the antimeridian;
        distance ≈ 111.32 km (±0.2 km)"""

        haversine_distance = haversine_km(0.0, 179.5, 0.0, -179.5)

        self.assertAlmostEqual(haversine_distance, 111.32 * cos(radians(0)), delta=0.2)

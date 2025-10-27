from django.test import TestCase
from api.services.query_builder import build_tags


class QueryBuilderTestCase(TestCase):
    LAT_MIN = 10.0
    LON_MIN = -20.0
    LAT_MAX = 11.0
    LON_MAX = 19.0
    GEN = "Corvus"
    SP = "corax"
    EN = "crow"

    def _build_tags_with_default(self):
        return build_tags(
            self.LAT_MIN,
            self.LON_MIN,
            self.LAT_MAX,
            self.LON_MAX,
            self.GEN,
            self.SP,
            self.EN,
        )

    def _extract_box_coordinates_from_tags(self, lat_min, lon_min, lat_max, lon_max):
        return (
            build_tags(
                lat_min,
                lon_min,
                lat_max,
                lon_max,
                self.GEN,
                self.SP,
                self.EN,
            )[1]
            .split(":")[1]
            .split(",")
        )

    def test_returns_list_of_tags(self):
        """Test that query builder returns a list"""
        self.assertIsInstance(self._build_tags_with_default(), list)

    def test_tags_is_list_with_exactly_one_grp_birds(self):
        """Test that exactly one "grp:birds" exists in the tags"""
        self.assertEqual(self._build_tags_with_default().count("grp:birds"), 1)

    def test_tags_in_expected_order(self):
        EXPECTED_PREFIX_ORDER = ["grp:", "box:", "gen:", "sp:", "en:"]
        tags = self._build_tags_with_default()
        prefixes = [tag.split(":")[0] + ":" for tag in tags]
        self.assertEqual(prefixes, EXPECTED_PREFIX_ORDER)
        self.assertEqual(len(tags), len(EXPECTED_PREFIX_ORDER))

    def test_box_rounds_outward_for_positive_coordinates(self):
        """
        Test, for positive coordinates, that box coordinates are exactly 2 decimal places,
        and rounds outward to 0.01°: minimums rounded down; maximums rounded up
        """
        EXPECTED_COORDINATES = ["10.23", "10.23", "20.24", "20.24"]
        rounded_coordinates = self._extract_box_coordinates_from_tags(
            10.231, 10.231, 20.231, 20.231
        )
        self.assertEqual(rounded_coordinates, EXPECTED_COORDINATES)
        for coordinate in rounded_coordinates:
            self.assertEqual(coordinate.count("."), 1)
            self.assertEqual(len(coordinate.split(".")[1]), 2)
        self.assertEqual(len(rounded_coordinates), 4)

    def test_box_rounds_outward_for_negative_coordinates(self):
        """
        Test, for negative coordinates, that box coordinates are exactly 2 decimal places,
        and rounds outward to 0.01°: minimums rounded down; maximums rounded up
        """
        EXPECTED_COORDINATES = ["-20.24", "-20.24", "-10.23", "-10.23"]
        rounded_coordinates = self._extract_box_coordinates_from_tags(
            -20.231, -20.231, -10.231, -10.231
        )
        self.assertEqual(rounded_coordinates, EXPECTED_COORDINATES)
        for coordinate in rounded_coordinates:
            self.assertEqual(coordinate.count("."), 1)
            self.assertEqual(len(coordinate.split(".")[1]), 2)
        self.assertEqual(len(rounded_coordinates), 4)

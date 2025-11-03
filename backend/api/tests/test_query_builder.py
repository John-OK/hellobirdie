from django.test import TestCase
from api.services.query_builder import build_tags


class QueryBuilderTestCase(TestCase):
    LAT_MIN = 10.345
    LON_MIN = -20.991
    LAT_MAX = 11.091
    LON_MAX = -19.039
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
        """Test that returns a list[str] of tags"""

        self.assertIsInstance(self._build_tags_with_default(), list)

    def test_tags_is_list_with_exactly_one_grp_birds(self):
        """Test that exactly one "grp:birds" tag"""

        self.assertEqual(self._build_tags_with_default().count("grp:birds"), 1)

    def test_tags_in_expected_order(self):
        """Test that order of tags is grp -> box -> gen -> sp -> en when present"""

        expected_prefix_order = ["grp:", "box:", "gen:", "sp:", "en:"]
        tags = self._build_tags_with_default()
        prefixes = [tag.split(":")[0] + ":" for tag in tags]
        self.assertEqual(prefixes, expected_prefix_order)
        self.assertEqual(len(tags), len(expected_prefix_order))

    def test_box_rounds_outward_for_positive_coordinates(self):
        """
        Test that coordinates are exactly 2 decimal and rounds outward
        (min floor, max ceil) for positive values
        """

        rounded_coordinates = self._extract_box_coordinates_from_tags(
            10.231, 10.231, 20.231, 20.231
        )
        self.assertEqual(rounded_coordinates, ["10.23", "10.23", "20.24", "20.24"])
        for coordinate in rounded_coordinates:
            self.assertEqual(coordinate.count("."), 1)
            self.assertEqual(len(coordinate.split(".")[1]), 2)
        self.assertEqual(len(rounded_coordinates), 4)

    def test_box_rounds_outward_for_negative_coordinates(self):
        """
        Test that coordinates are exactly 2 decimal and rounds outward
        (min floor, max ceil) for negative values
        """

        rounded_coordinates = self._extract_box_coordinates_from_tags(
            -20.231, -20.231, -10.231, -10.231
        )
        self.assertEqual(rounded_coordinates, ["-20.24", "-20.24", "-10.23", "-10.23"])
        for coordinate in rounded_coordinates:
            self.assertEqual(coordinate.count("."), 1)
            self.assertEqual(len(coordinate.split(".")[1]), 2)
        self.assertEqual(len(rounded_coordinates), 4)

    def test_box_is_correctly_formatted(self):
        """
        Test that box with no spaces, exactly 3 commas,
        four coords in LAT_MIN,LON_MIN,LAT_MAX,LON_MAX order
        """

        coordinates = self._build_tags_with_default()[1].split(":")[1]
        coordinates_list = coordinates.split(",")
        self.assertEqual(coordinates.count(" "), 0)
        self.assertEqual(coordinates.count(","), 3)
        self.assertEqual(coordinates_list, ["10.34", "-21.00", "11.10", "-19.03"])
        self.assertEqual(len(coordinates_list), 4)

    def test_returns_only_grp_and_box_when_no_filters(self):
        """Test that only "grp:" and "box:" tags are present when filters absent"""

        tags = build_tags(self.LAT_MIN, self.LON_MIN, self.LAT_MAX, self.LON_MAX)
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags, ["grp:birds", "box:10.34,-21.00,11.10,-19.03"])

    def test_blank_filters_are_ignored(self):
        """Test that empty/whitespace filters are ignored; mixed cases keep stable order"""

        empty_and_whitespace_tags = build_tags(
            self.LAT_MIN, self.LON_MIN, self.LAT_MAX, self.LON_MAX, "", " ", "    "
        )
        self.assertEqual(len(empty_and_whitespace_tags), 2)
        self.assertEqual(
            empty_and_whitespace_tags, ["grp:birds", "box:10.34,-21.00,11.10,-19.03"]
        )

        mixed_populated_and_empty_and_whitespace_tags = build_tags(
            self.LAT_MIN, self.LON_MIN, self.LAT_MAX, self.LON_MAX, "", " ", "crow"
        )
        self.assertEqual(len(mixed_populated_and_empty_and_whitespace_tags), 3)
        self.assertEqual(
            mixed_populated_and_empty_and_whitespace_tags,
            ["grp:birds", "box:10.34,-21.00,11.10,-19.03", "en:crow"],
        )

    def test_filters_are_trimmed_and_collapsed(self):
        """Test internal whitespace in filter values trimmed and collapsed"""

        tags_with_unnecessary_whitespace_ = build_tags(
            self.LAT_MIN,
            self.LON_MIN,
            self.LAT_MAX,
            self.LON_MAX,
            " Corvus",
            "albus ",
            " Pied  Crow ",
        )
        self.assertEqual(len(tags_with_unnecessary_whitespace_), 5)
        self.assertEqual(
            tags_with_unnecessary_whitespace_,
            [
                "grp:birds",
                "box:10.34,-21.00,11.10,-19.03",
                "gen:Corvus",
                "sp:albus",
                "en:Pied Crow",
            ],
        )

    def test_tags_order_with_only_en(self):
        """Test that stable order kept with provided filters only"""

        tags = build_tags(
            self.LAT_MIN,
            self.LON_MIN,
            self.LAT_MAX,
            self.LON_MAX,
            en="Sharp-shinned Hawk",
        )

        self.assertEqual(
            tags,
            [
                "grp:birds",
                "box:10.34,-21.00,11.10,-19.03",
                "en:Sharp-shinned Hawk",
            ],
        )

    def test_tags_order_with_only_gen(self):
        """Test that stable order kept with provided filters only"""

        tags = build_tags(
            self.LAT_MIN,
            self.LON_MIN,
            self.LAT_MAX,
            self.LON_MAX,
            gen="Buteo",
        )

        self.assertEqual(
            tags,
            [
                "grp:birds",
                "box:10.34,-21.00,11.10,-19.03",
                "gen:Buteo",
            ],
        )

    def test_tags_order_with_only_sp(self):
        """Test that stable order kept with provided filters only"""

        tags = build_tags(
            self.LAT_MIN,
            self.LON_MIN,
            self.LAT_MAX,
            self.LON_MAX,
            sp="corax",
        )

        self.assertEqual(
            tags,
            [
                "grp:birds",
                "box:10.34,-21.00,11.10,-19.03",
                "sp:corax",
            ],
        )

    def test_tags_order_with_gen_and_sp(self):
        """Test that stable order kept with provided filters only"""

        tags = build_tags(
            self.LAT_MIN,
            self.LON_MIN,
            self.LAT_MAX,
            self.LON_MAX,
            gen="Aquila",
            sp="chrysaetos",
        )

        self.assertEqual(
            tags,
            [
                "grp:birds",
                "box:10.34,-21.00,11.10,-19.03",
                "gen:Aquila",
                "sp:chrysaetos",
            ],
        )

    def test_tags_order_with_gen_and_en(self):
        """Test that stable order kept with provided filters only"""

        tags = build_tags(
            self.LAT_MIN,
            self.LON_MIN,
            self.LAT_MAX,
            self.LON_MAX,
            gen="Accipiter",
            en="Cooper's Hawk",
        )

        self.assertEqual(
            tags,
            [
                "grp:birds",
                "box:10.34,-21.00,11.10,-19.03",
                "gen:Accipiter",
                "en:Cooper's Hawk",
            ],
        )

    def test_box_is_idempotent_for_two_decimal_coords(self):
        """Test that leaves box unchanged when inputs already two-decimal and outward rounded"""

        tags = build_tags(27.33, -103.58, 31.49, -87.29)
        self.assertEqual(tags, ["grp:birds", "box:27.33,-103.58,31.49,-87.29"])

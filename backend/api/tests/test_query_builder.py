from django.test import TestCase
from api.services.query_builder import build_tags


class QueryBuilderTestCase(TestCase):
    LAT_MIN = 10.0
    LON_MIN = -20.0
    LAT_MAX = 11.0
    LON_MAX = -19.0
    GEN = "Corvus"
    SP = "corax"
    EN = "crow"

    def test_only_one_grp_birds_exists(self):
        """Test that exactly one "grp:birds" exists in the tags"""
        tags = build_tags(
            self.LAT_MIN,
            self.LON_MIN,
            self.LAT_MAX,
            self.LON_MAX,
            self.GEN,
            self.SP,
            self.EN,
        )
        self.assertEqual(tags.count("grp:birds"), 1)

    # def test_tags_in_expected_order(self):
    #     EXPECTED_PREFIX_ORDER = ["grp:birds", "box:", "gen:", "sp:", "en:"]
    #     pass

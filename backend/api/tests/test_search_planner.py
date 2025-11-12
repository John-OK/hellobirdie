from django.test import TestCase
from api.services.search_planner import plan_query_boxes, SEAM_MIN, SEAM_MAX


class SearchPlannerTestCase(TestCase):
    def test_plan_boxes_non_crossing_returns_single_box(self):
        """Test that single box returned for boxes not crossing antimeridian."""

        boxes = plan_query_boxes(40, 90, 50)
        box = boxes[0]
        lat_min = box[0]
        lon_min = box[1]
        lat_max = box[2]
        lon_max = box[3]

        self.assertIsInstance(boxes, list)
        self.assertEqual(len(boxes), 1)
        self.assertEqual(len(box), 4)
        for coord in box:
            self.assertIsInstance(coord, float)
        self.assertLess(lat_min, lat_max)
        self.assertLess(lon_min, lon_max)

    def test_plan_boxes_pos_lon_crossing_returns_two_boxes(self):
        """Test that two boxes returned for boxes crossing antimeridian with a positive longitude.
        Splits at SEAM_MAX/SEAM_MIN and preserves identical lat bounds."""

        boxes = plan_query_boxes(66.5, 179.8, 50)

        box1 = boxes[0]
        lat_min1 = box1[0]
        lon_min1 = box1[1]
        lat_max1 = box1[2]
        lon_max1 = box1[3]

        box2 = boxes[1]
        lat_min2 = box2[0]
        lon_min2 = box2[1]
        lat_max2 = box2[2]
        lon_max2 = box2[3]

        self.assertEqual(len(boxes), 2)
        self.assertEqual(len(box1), 4)
        self.assertEqual(len(box2), 4)
        self.assertLess(lon_min1, lon_max1)
        self.assertEqual(lon_max1, SEAM_MAX)
        self.assertEqual(lon_min2, SEAM_MIN)
        self.assertEqual(lat_min1, lat_min2)
        self.assertEqual(lat_max1, lat_max2)

    def test_plan_boxes_neg_lon_crossing_returns_two_boxes(self):
        """Test that two boxes returned for boxes crossing antimeridian with a negative longitude.
        Splits at SEAM_MAX/SEAM_MIN and preserves identical lat bounds."""

        boxes = plan_query_boxes(66.5, -179.8, 50)

        box1 = boxes[0]
        lat_min1 = box1[0]
        lon_min1 = box1[1]
        lat_max1 = box1[2]
        lon_max1 = box1[3]

        box2 = boxes[1]
        lat_min2 = box2[0]
        lon_min2 = box2[1]
        lat_max2 = box2[2]
        lon_max2 = box2[3]

        self.assertEqual(len(boxes), 2)
        self.assertEqual(len(box1), 4)
        self.assertEqual(len(box2), 4)
        self.assertLess(lon_min2, lon_max2)
        self.assertEqual(lon_max1, SEAM_MAX)
        self.assertEqual(lon_min2, SEAM_MIN)
        self.assertEqual(lat_min1, lat_min2)
        self.assertEqual(lat_max1, lat_max2)

    def test_plan_boxes_does_not_split_across_prime_meridian(self):
        """Near 0° longitude, planner returns a single box (no split across prime meridian)."""

        boxes = plan_query_boxes(40, 0.2, 50)
        lon_min = boxes[0][1]
        lon_max = boxes[0][3]

        self.assertEqual(len(boxes), 1)
        self.assertNotEqual(lon_min, SEAM_MIN)
        self.assertNotEqual(lon_max, SEAM_MAX)

    def test_plan_boxes_does_not_split_near_equator(self):
        """Near 0° latitude and latitude straddles 0°,
        planner returns a single box (equator crossing does not trigger split)."""

        boxes = plan_query_boxes(0.2, 20, 50)
        lat_min = boxes[0][0]
        lat_max = boxes[0][2]

        self.assertEqual(len(boxes), 1)
        self.assertTrue(lat_min < 0 < lat_max)

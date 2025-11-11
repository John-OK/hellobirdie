from django.test import TestCase
from api.services.search_planner import plan_query_boxes


class SearchPlannerTestCase(TestCase):
    def test_plan_boxes_non_crossing_returns_single_box(self):
        """Test that single box returned for boxes not crossing antimeridian"""

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

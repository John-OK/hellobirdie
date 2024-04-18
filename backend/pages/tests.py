from django.test import TestCase
from django.http import HttpRequest
from pages.views import home_page

class HomePageTest(TestCase):
    def test_can_serve_the_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"bird_name": "A bird to search"})
        self.assertContains(response, "A bird to search")

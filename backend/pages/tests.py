from django.test import TestCase
from django.http import HttpRequest
from pages.views import homepage

class HomePageTest(TestCase):
    def test_uses_home_page_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"bird_name": "A bird to search"})
        self.assertContains(response, "A bird to search")
        self.assertTemplateUsed(response, "home.html")

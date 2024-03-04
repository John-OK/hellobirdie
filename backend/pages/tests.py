from django.test import TestCase
from django.http import HttpRequest
from pages.views import homepage

class HomePageTest(TestCase):
    def test_uses_home_page_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

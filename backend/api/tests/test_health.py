from django.test import TestCase
from django.urls import reverse


class HealthCheckTestCase(TestCase):

    def test_health_check_returns_ok_status(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()
        self.assertEqual(data, {"status": "ok"})

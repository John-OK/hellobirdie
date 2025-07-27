from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Bird


class BirdAdminTestCase(TestCase):
    def setUp(self):
        self.client.force_login(
            User.objects.get_or_create(
                username="admin", is_staff=True, is_superuser=True
            )[0]
        )

        self.bird = Bird.objects.create(
            genus="Falco",
            species="subbuteo",
            english_name="Eurasian Hobby",
        )

    def _get_admin_url(self, query_parameters=None):
        url = reverse("admin:api_bird_changelist")
        if query_parameters:
            url += "?" + query_parameters
        return url

    def _results_table_output(self, content):
        # NOTE: This method relies on Django Admin's HTML structure.
        # It may need updates if Django Admin HTML changes in future versions.
        search_string = 'id="result_list"'
        if search_string in content:
            results = content.split('id="result_list"')[1].split("</table>")[0]
            return results
        else:
            return None

    def test_bird_model_in_admin_interface(self):
        """Test that the Bird model is properly registered in the admin"""
        url = self._get_admin_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_bird_admin_displays_content(self):
        """Test that Bird model content appears in the admin interface's results table"""
        url = self._get_admin_url()
        response = self.client.get(url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Eurasian Hobby", results_table)

        else:
            self.fail("Results table not found in response")

    def test_admin_list_contains_all_configured_fields(self):
        """Test that the admin list contains all fields specified in list_display.

        Verifies that each column header (English Name, Genus, Species, Subspecies)
        appears in the admin interface table.
        """
        url = self._get_admin_url()
        response = self.client.get(url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            expected_headers = ["English Name", "Genus", "Species", "Subspecies"]
            for field in expected_headers:
                self.assertIn(field, results_table)
        else:
            self.fail("Results table not found in response")

    def test_admin_list_displays_fields_in_order(self):
        """Test that the admin list shows fields in the expected order"""
        url = self._get_admin_url()
        response = self.client.get(url)
        content = response.content.decode("utf-8")
        search_string = 'id="result_list"'

        if search_string in content:
            result_table = content.split("<thead>")[1].split("</thead>")[0]

            self.assertIn("English Name", result_table)
            self.assertIn("Genus", result_table)
            self.assertIn("Species", result_table)

            english_name_position = result_table.find("English Name")
            genus_position = result_table.find("Genus")
            species_position = result_table.find("Species")
            subspecies_position = result_table.find("Subspecies")

            self.assertGreater(english_name_position, 0)
            self.assertGreater(genus_position, english_name_position)
            self.assertGreater(species_position, genus_position)
            self.assertGreater(subspecies_position, species_position)

        else:
            self.fail("Results table not found in response")

    def test_search_by_genus(self):
        """Test searching by Genus works"""
        second_bird = Bird.objects.create(
            genus="Menura",
            species="novaehollandiae",
            subspecies="victoriae",
            english_name="Superb Lyrebird",
        )
        search_url = self._get_admin_url("q=Menura")

        response = self.client.get(search_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Superb Lyrebird", results_table)
            self.assertNotIn("Eurasian Hobby", results_table)
        else:
            self.fail("Results table not found in response")

    def test_search_by_species(self):
        """Test searching by Species works"""
        second_bird = Bird.objects.create(
            genus="Alaudala",
            species="heinei",
            subspecies="aharonii",
            english_name="Turkestan Short-toed Lark",
        )
        search_url = self._get_admin_url("q=heinei")

        response = self.client.get(search_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Turkestan Short-toed Lark", results_table)
            self.assertNotIn("subbuteo", results_table)
        else:
            self.fail("Results table not found in response")

    def test_search_by_english_name(self):
        """Test searching by English name works"""
        second_bird = Bird.objects.create(
            genus="Cacomantis",
            species="merulinus",
            subspecies="querulus",
            english_name="Plaintive Cuckoo",
        )
        search_url = self._get_admin_url("q=Eurasian Hobby")

        response = self.client.get(search_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Falco", results_table)
            self.assertNotIn("querulus", results_table)
        else:
            self.fail("Results table not found in response")

    def test_search_by_subspecies(self):
        """Test searching by subspecies (optional field) works"""
        second_bird = Bird.objects.create(
            genus="Lanius",
            species="excubitor",
            subspecies="leucopygos",
            english_name="Great Grey Shrike",
        )
        search_url = self._get_admin_url("q=leucopygos")

        response = self.client.get(search_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Great Grey Shrike", results_table)
            self.assertIn("leucopygos", results_table)
            self.assertNotIn("subbuteo", results_table)
        else:
            self.fail("Results table not found in response")

    def test_bird_without_subspecies_uses_custom_display(self):
        """Test birds without provided subspecies are displayed with "—" rather than "none".

        This ensures the admin interface clearly indicates missing values.
        """
        second_bird = Bird.objects.create(
            genus="Panterpe",
            species="insignis",
            subspecies="eisenmanni",
            english_name="Fiery-throated Hummingbird",
        )
        url = self._get_admin_url()

        response = self.client.get(url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("—", results_table)
            self.assertIn("eisenmanni", results_table)
            self.assertNotIn("none", results_table)
        else:
            self.fail("Results table not found in response")

    def test_search_is_case_insensitive(self):
        """Test that searches are case-insensitive"""
        second_bird = Bird.objects.create(
            genus="Corvus",
            species="meeki",
            english_name="Bougainville Crow",
        )
        search_url = self._get_admin_url("q=cOrVuS")

        response = self.client.get(search_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Bougainville Crow", results_table)
            self.assertNotIn("Hobby", results_table)
        else:
            self.fail("Results table not found in response")

    def test_search_partial_matches(self):
        """Test that partial words are matched"""
        second_bird = Bird.objects.create(
            genus="Glaucidium",
            species="albertinum",
            english_name="Albertine Owlet",
        )
        search_url = self._get_admin_url("q=owl")

        response = self.client.get(search_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Glaucidium", results_table)
            self.assertNotIn("Falco", results_table)
        else:
            self.fail("Results table not found in response")

    def test_empty_search_results(self):
        """Test that searching for non-existent term returns no results"""
        search_url = self._get_admin_url("q=eagle")

        response = self.client.get(search_url)
        self.assertContains(response, "0 birds")

    def test_search_multiple_words(self):
        """Test that multiple word searches use AND logic"""
        second_bird = Bird.objects.create(
            genus="Strix",
            species="nebulosa",
            english_name="Great Grey Owl",
        )
        third_bird = Bird.objects.create(
            genus="Pitangus",
            species="sulphuratus",
            english_name="Great Kiskadee",
        )
        search_url = self._get_admin_url("q=Great Grey")

        response = self.client.get(search_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Strix", results_table)
            self.assertNotIn("Kiskadee", results_table)
            self.assertNotIn("Falco", results_table)
        else:
            self.fail("Results table not found in response")

    def test_list_filter_displays_content(self):
        """Test that list_filter content appears in the admin interface"""
        url = self._get_admin_url()
        response = self.client.get(url)

        self.assertContains(response, "changelist-filter")
        self.assertContains(response, "By genus")
        self.assertContains(response, 'data-filter-title="species"')

    def test_filter_links_present(self):
        """Test filter sidebar contains correct filter options"""
        second_bird = Bird.objects.create(
            genus="Phoeniculus",
            species="purpureus",
            english_name="Green Wood Hoopoe",
        )
        url = self._get_admin_url()
        response = self.client.get(url)

        self.assertContains(response, f'href="?genus=Falco"')
        self.assertContains(response, f'href="?species=purpureus"')

    def test_filter_by_genus(self):
        """Test filtering birds by genus works"""
        second_bird = Bird.objects.create(
            genus="Apteryx",
            species="owenii",
            english_name="Little Spotted Kiwi",
        )
        filter_url = self._get_admin_url("genus=Falco")
        response = self.client.get(filter_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("Falco", results_table)
            self.assertNotIn("Apteryx", results_table)
        else:
            self.fail("Results table not found in response")

    def test_multiple_filters(self):
        """Test applying multiple filters simultaneously"""
        second_bird = Bird.objects.create(
            genus="Falco",
            species="columbarius",
            subspecies="suckleyi",
            english_name="Merlin",
        )
        third_bird = Bird.objects.create(
            genus="Passer",
            species="moabiticus",
            english_name="Dead Sea Sparrow",
        )
        filter_url = self._get_admin_url("genus=Falco&species=columbarius")
        response = self.client.get(filter_url)
        content = response.content.decode("utf-8")
        results_table = self._results_table_output(content)

        if results_table:
            self.assertIn("columbarius", results_table)
            self.assertNotIn("subbuteo", results_table)
            self.assertNotIn("Passer", results_table)
        else:
            self.fail("Results table not found in response")

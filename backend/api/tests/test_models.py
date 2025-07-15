from django.test import TestCase
from django.db import models
from api.models import Bird


class BirdModelTestCase(TestCase):

    def test_required_fields_have_correct_types_and_constraints(self):
        """Verify that all required Bird fields exist with correct types and non-null constraints."""

        genus_field = Bird._meta.get_field("genus")
        self.assertIsInstance(genus_field, models.CharField)
        self.assertEqual(
            genus_field.max_length,
            50,
            "genus field should have max_length=50 to accommodate longest known genus names",
        )
        self.assertFalse(
            genus_field.null, "genus field is required for taxonomic identification"
        )

        species_field = Bird._meta.get_field("species")
        self.assertIsInstance(species_field, models.CharField)
        self.assertEqual(
            species_field.max_length,
            50,
            "species field should have max_length=50 to accommodate longest known species names",
        )
        self.assertFalse(
            species_field.null, "species field is required for taxonomic identification"
        )

        english_name_field = Bird._meta.get_field("english_name")
        self.assertIsInstance(english_name_field, models.CharField)
        self.assertEqual(
            english_name_field.max_length,
            75,
            "english_name field should have max_length=75 to accommodate longer common names",
        )
        self.assertFalse(
            english_name_field.null,
            "english_name field is the common name in English and is required for user friendliness",
        )

    def test_optional_fields_have_correct_types_and_are_nullable(self):

        subspecies_field = Bird._meta.get_field("subspecies")
        self.assertIsInstance(subspecies_field, models.CharField)
        self.assertEqual(
            subspecies_field.max_length,
            50,
            "subspecies field should have max_length=50 to accommodate longest known subspecies names",
        )
        self.assertTrue(
            subspecies_field.null,
            "subspecies field should be nullable as not all birds have subspecies classifications",
        )

        family_field = Bird._meta.get_field("family")
        self.assertIsInstance(family_field, models.CharField)
        self.assertEqual(
            family_field.max_length,
            50,
            "family field should have max_length=50 to accommodate longest known family names",
        )
        self.assertTrue(
            family_field.null,
            "family field should be nullable as it may be populated later via GBIF API",
        )

    def test_string_representation(self):
        """Test that the Bird model string representation shows expected information"""

        # Test case without subspecies
        bird_without_subspecies = Bird.objects.create(
            genus="Accipiter", species="nisus", english_name="Eurasian Sparrowhawk"
        )
        expected_string_without_subspecies = "Eurasian Sparrowhawk (Accipiter nisus)"
        self.assertEqual(
            str(bird_without_subspecies), expected_string_without_subspecies
        )

        # Test case with subspecies
        bird_with_subspecies = Bird.objects.create(
            genus="Charadrius",
            species="nivosus",
            subspecies="occidentalis",
            english_name="Snowy Plover",
        )
        expected_string_with_subspecies = (
            "Snowy Plover (Charadrius nivosus occidentalis)"
        )
        self.assertEqual(str(bird_with_subspecies), expected_string_with_subspecies)

        # Test case with hyphenated english_name
        bird_with_hyphenated_name = Bird.objects.create(
            genus="Pteruthius",
            species="melanotis",
            subspecies="tahanensis",
            english_name="Black-eared Shrike-babbler",
        )
        expected_string_with_hyphen = (
            "Black-eared Shrike-babbler (Pteruthius melanotis tahanensis)"
        )
        self.assertEqual(str(bird_with_hyphenated_name), expected_string_with_hyphen)

        # Test case with multi-hyphenated english_name
        bird_with_multi_hyphenated_name = Bird.objects.create(
            genus="Seleucidis",
            species="melanoleucus",
            english_name="Twelve-wired Bird-of-paradise",
        )
        expected_string_with_multi_hyphens = (
            "Twelve-wired Bird-of-paradise (Seleucidis melanoleucus)"
        )
        self.assertEqual(
            str(bird_with_multi_hyphenated_name), expected_string_with_multi_hyphens
        )

        # Test case with apostrophe in name
        bird_with_apostrophe_in_name = Bird.objects.create(
            genus="Accipiter", species="cooperii", english_name="Cooper's Hawk"
        )
        expected_string_with_apostrophe = "Cooper's Hawk (Accipiter cooperii)"
        self.assertEqual(
            str(bird_with_apostrophe_in_name), expected_string_with_apostrophe
        )

        # Test case with both hyphen and apostrophe
        bird_with_hyphen_and_apostrophe_in_name = Bird.objects.create(
            genus="Diphyllodes",
            species="respublica",
            english_name="Wilson's Bird-of-paradise",
        )
        expected_string_with_hyphen_and_apostrophe = (
            "Wilson's Bird-of-paradise (Diphyllodes respublica)"
        )
        self.assertEqual(
            str(bird_with_hyphen_and_apostrophe_in_name),
            expected_string_with_hyphen_and_apostrophe,
        )

import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_search_for_a_species(self):
        # David sees a bird that he thinks is a white-crowned sparrow,
        # but wants to be sure.
        # He goes to the hellobirdie homepage.
        self.browser.get("http://localhost:8000")

        # He confirms he's at the right webpage from the page title
        self.assertIn("HelloBirdie", self.browser.title)

        # He gets a popup asking if the website can know his location
        # and clicks "allow."
        # The map shifts to his general area and shows a pin at his location.
        self.fail("Finish tests!")

        # A search bar invites him to enter a name.

        # He enters "white-crowned sparrow" and clicks the "Submit" button.
        # Bird-shaped pins of all the white-crowned sparrows within 100-km populate the map
        # and a shaded square (or circle) centered at his location show him the
        # area included in the search.

        # He clicks on one of the bird pins and a pop-up displays some information, including
        # the name of the bird( "White-crowned Sparrow"), the scientific name
        # ("Zonotrichia leucophrys"), a button to play the bird call, and a link to 
        # search for images of the bird.

if __name__ == "__main__":
    unittest.main()
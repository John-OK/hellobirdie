import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_search_for_a_species(self):
        # David sees a bird that he thinks is a white-crowned sparrow,
        # but wants to be sure.
        # He goes to the hellobirdie home page.
        self.browser.get("http://localhost:8000")

        # He confirms he's at the right webpage from the page title and header
        self.assertIn("hellobirdie", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("hellobirdie", header_text)

        # He is invited to enter a bird name
        inputbox = self.browser.find_element(By.ID, "id_bird_to_check")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a bird name")

        # He types "sparrow" into the text box
        inputbox.send_keys("sparrow")

        # When he hits enter, the page updates with the name of the bird he's searching for:
        # "Looking for 'sparrow' in this area..."
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        confirmation_text = self.browser.find_element(By.ID, "id_confirmation_text")
        self.assertEqual(confirmation_text.text, "Looking for 'sparrow' in this area...", )

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
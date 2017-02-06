from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTests(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # The Clumsy Goat visits our page and accidentally selects our inputbox and hits enter.
        # This should not have added a blank item
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys(Keys.ENTER)

        # The home page refreshes and there is an error message saying that you cannot add a blank item

        # He types his real todo item this time and hits enter, which now works
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys('Stop being so clumsy!')
        input_box.send_keys(Keys.ENTER)

        # Because he is a clumsy goat (and apparently not too strict on his TODOs), he accidentally selects the inputbox and hits enter again
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys(Keys.ENTER)

        # He receives a similar warning on the list page

        # And he can correct it by filling some text in
        self.fail('Finish the Clumsy Goat saga!')
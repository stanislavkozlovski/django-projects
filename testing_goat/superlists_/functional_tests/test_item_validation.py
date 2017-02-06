from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTests(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # The Clumsy Goat visits our page and accidentally selects our inputbox and hits enter.
        # This should not have added a blank item
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys(Keys.ENTER)

        # The home page refreshes and there is an error message saying that you cannot add a blank item
        error = self.browser.find_element_by_class_name('has-error')
        self.assertEqual(error.text, "You can't have an empty list item!")

        # He types his real todo item this time and hits enter, which now works
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys('Stop being so clumsy!')
        input_box.send_keys(Keys.ENTER)
        self.assertRowInListTable('1: Stop being so clumsy!')

        # Because he is a clumsy goat (and apparently not too strict on his TODOs), he accidentally selects the inputbox and hits enter again
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys(Keys.ENTER)

        self.assertRowInListTable('1: Stop being so clumsy!')
        # He receives a similar warning on the list page
        error = self.browser.find_element_by_class_name('has-error')
        self.assertEqual(error.text, "You can't have an empty list item!")

        # And he can correct it by filling some text in
        self.browser.find_element_by_id('new_item').send_keys('Stop it!\n')
        self.assertRowInListTable('1: Stop being so clumsy!')
        self.assertRowInListTable('2: Stop it!')


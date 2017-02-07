from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ItemValidationTests(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # The Clumsy Goat visits our page and accidentally selects our inputbox and hits enter.
        # This should not have added a blank item
        self.browser.get(self.live_server_url)
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # The HTML does not even let him enter it in, but the Clumsy Goat is a little hacker and...
        self.browser.execute_script("document.getElementById('id_text').required = false;")
        input_box.send_keys(Keys.ENTER)

        # The home page refreshes and there is an error message saying that you cannot add a blank item
        error = self.browser.find_element_by_class_name('has-error')
        self.assertEqual(error.text, "You can't have an empty list item!")

        # He types his real todo item this time and hits enter, which now works
        input_box = self.get_item_input_box()
        input_box.send_keys('Stop being so clumsy!')
        input_box.send_keys(Keys.ENTER)
        self.assertRowInListTable('1: Stop being so clumsy!')

        # Because he is a clumsy goat (and apparently not too strict on his TODOs), he accidentally selects the inputbox and hits enter again
        input_box = self.get_item_input_box()
        input_box.send_keys(Keys.ENTER)
        # the HTML is no match for him again
        self.browser.execute_script("document.getElementById('id_text').required = false;")
        input_box.send_keys(Keys.ENTER)

        self.assertRowInListTable('1: Stop being so clumsy!')
        # He receives a similar warning on the list page
        error = self.browser.find_element_by_class_name('has-error')
        self.assertEqual(error.text, "You can't have an empty list item!")

        # And he can correct it by filling some text in
        self.get_item_input_box().send_keys('Stop it!\n')
        self.assertRowInListTable('1: Stop being so clumsy!')
        self.assertRowInListTable('2: Stop it!')

    def test_cannot_add_duplicate_items(self):
        # The Goat With Bad Memory opens the site
        goat_todo = 'Buy ginkgo biloba'
        self.browser.get(self.live_server_url)
        # It enters one of it's TODOs
        self.get_item_input_box().send_keys(f'{goat_todo}\n')
        # Some time passes and is adds the same todo, since his memory is pretty Bad
        self.get_item_input_box().send_keys(f'{goat_todo}\n')
        # Luckily, he gets an error message saying that he should not have duplicate items
        error = self.browser.find_element_by_class_name('has-error')
        self.assertEqual(error.text, "You can't have a duplicate list item!")

        self.assertRowInListTable(f'1: {goat_todo}')
        self.assertRowNotInListTable(f'2: {goat_todo}')



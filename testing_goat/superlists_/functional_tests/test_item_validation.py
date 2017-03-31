from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest
from lists.constants import DUPLICATE_ITEM_ERROR_MSG, EMPTY_LIST_ERROR_MSG
from .list_page import ListPage

class ItemValidationTests(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # The Clumsy Goat visits our page and accidentally selects our inputbox and hits enter.
        # This should not have added a blank item
        self.browser.get(self.live_server_url)
        list_page = ListPage(self)
        input_box = list_page.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # The HTML does not even let him enter it in, but the Clumsy Goat is a little hacker and...
        list_page.js_remove_input_box_required_attr()
        input_box.send_keys(Keys.ENTER)

        # The home page refreshes and there is an error message saying that you cannot add a blank item
        error = self.get_error_element()
        self.assertEqual(error.text, EMPTY_LIST_ERROR_MSG)

        # He types his real todo item this time and hits enter, which now works
        list_page.add_list_item('Stop being so clumsy!')
        self.assertRowInListTable('1: Stop being so clumsy!')

        # Because he is a clumsy goat (and apparently not too strict on his TODOs), he accidentally selects the inputbox and hits enter again
        input_box = list_page.get_item_input_box()
        input_box.send_keys(Keys.ENTER)

        # the HTML is no match for him again
        list_page.js_remove_input_box_required_attr()
        input_box.send_keys(Keys.ENTER)

        self.assertRowInListTable('1: Stop being so clumsy!')
        # He receives a similar warning on the list page
        error = self.get_error_element()
        self.assertEqual(error.text, EMPTY_LIST_ERROR_MSG)

        # And he can correct it by filling some text in
        list_page.get_item_input_box().send_keys('Stop it!\n')
        self.assertRowInListTable('1: Stop being so clumsy!')
        self.assertRowInListTable('2: Stop it!')

    def test_cannot_add_duplicate_items(self):
        # The Goat With Bad Memory opens the site
        list_page = ListPage(self)
        goat_todo = 'Buy ginkgo biloba'
        self.browser.get(self.live_server_url)
        # It enters one of it's TODOs
        list_page.add_list_item(goat_todo)
        # Some time passes and is adds the same todo, since his memory is pretty Bad
        list_page.add_list_item(goat_todo, _assert=False)
        # Luckily, he gets an error message saying that he should not have duplicate items
        error = self.get_error_element()
        self.assertEqual(error.text, DUPLICATE_ITEM_ERROR_MSG)

        self.assertRowInListTable(f'1: {goat_todo}')
        self.assertRowNotInListTable(f'2: {goat_todo}')



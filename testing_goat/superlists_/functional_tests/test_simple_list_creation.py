from functional_tests.base import FunctionalTest
from .list_page import ListPage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ListCreationTests(FunctionalTest):
    def test_can_start_todos_and_retrieve_them_later(self):
        # The Testing Goat opens up a popular todo-list website
        list_page = ListPage(self)
        self.browser.get(self.server_url)
        # It sees something about TODOs in the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Start a new To-Do list')
        # It is invited to enter a goat TODO
        input_box = list_page.get_item_input_box()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Add a to-do'
        )
        # It types "Test Coffee"
        list_page.add_list_item('Test Coffee')

        # Gets redirected to a unique URL holding its list
        goat_list_url = self.browser.current_url
        self.assertRegex(goat_list_url, r'/lists/.*')
        self.assertRowInListTable('1: Test Coffee')
        # It types "Buy Coffee" and presses enter again
        list_page.add_list_item('Buy Coffee')

        # His two TODOs are now saved and have a unique URL for the Testing Goat, which is described in the page
        self.assertRowInListTable('2: Buy Coffee')

        # It goes on to test some things
        """ Another Testing Goat comes up and opens the site, he does not see the other one's items """
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.browser.get(self.server_url)

        # the other goat adds a todo item, he is apparently more practical
        list_page.add_list_item('Test things')

        # Gets redirected to his own URL
        other_goat_list_url = self.browser.current_url
        self.assertRegex(goat_list_url, r'/lists/.*')
        self.assertNotEqual(goat_list_url, other_goat_list_url)
        self.assertRowNotInListTable('1: Test Coffee')
        self.assertRowNotInListTable('2: Buy Coffee')
        self.assertRowInListTable('1: Test things')



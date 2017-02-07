from functional_tests.base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ListCreationTests(FunctionalTest):
    def test_can_start_todos_and_retrieve_them_later(self):
        # The Testing Goat opens up a popular todo-list website
        self.browser.get(self.server_url)
        # It sees something about TODOs in the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Start a new To-Do list')
        # It is invited to enter a goat TODO
        input_box = self.get_item_input_box()
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Add a to-do'
        )
        # It types "Test Coffee"
        input_box.send_keys('Test Coffee')

        # When it presses enter, the page reloads and a textbox prompts for another TODO
        input_box.send_keys(Keys.ENTER)
        # Gets redirected to a unique URL holding it's list
        goat_list_url = self.browser.current_url
        self.assertRegex(goat_list_url, r'/lists/.*')
        self.assertRowInListTable('1: Test Coffee')
        # It types "Buy Coffee" and presses enter again
        input_box = self.get_item_input_box()
        input_box.send_keys('Buy Coffee')
        input_box.send_keys(Keys.ENTER)

        # His two TODOs are now saved and have a unique URL for the Testing Goat, which is described in the page
        self.assertRowInListTable('2: Buy Coffee')
        # self.assertIn(, [row.text for row in rows])
        # self.assertIn('2: Buy Coffee', [row.text for row in rows])

        # It goes on to test some things
        """ Another Testing Goat comes up and opens the site, he does not see the other one's items """
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.browser.get(self.server_url)

        # the other goat adds a todo item, he is apparently more practical
        input_box = self.get_item_input_box()
        input_box.send_keys('Test things')
        input_box.send_keys(Keys.ENTER)
        # Gets redirected to his own URL
        other_goat_list_url = self.browser.current_url
        self.assertRegex(goat_list_url, r'/lists/.*')
        self.assertNotEqual(goat_list_url, other_goat_list_url)
        self.assertRowNotInListTable('1: Test Coffee')
        self.assertRowNotInListTable('2: Buy Coffee')
        self.assertRowInListTable('1: Test things')



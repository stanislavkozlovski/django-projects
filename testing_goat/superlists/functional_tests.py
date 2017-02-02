import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def assertRowInTable(self, desired_row):
        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(desired_row, [row.text for row in rows])

    def tearDown(self):
        self.browser.quit()

    def test_can_start_todos_and_retrieve_them_later(self):
        # The Testing Goat opens up a popular todo-list website
        self.browser.get('http://localhost:1337')
        # It sees something about TODOs in the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'To-Do')
        # It is invited to enter a goat TODO
        input_box = self.browser.find_element_by_id('new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Add a to-do'
        )
        # It types "Test Coffee"
        input_box.send_keys('Test Coffee')

        # When it presses enter, the page reloads and a textbox prompts for another TODO
        input_box.send_keys(Keys.ENTER)

        # It types "Buy Coffee" and presses enter again
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys('Buy Coffee')
        input_box.send_keys(Keys.ENTER)

        # His two TODOs are now saved and have a unique URL for the Testing Goat, which is described in the page
        self.assertRowInTable('1: Test Coffee')
        self.assertRowInTable('2: Buy Coffee')
        # self.assertIn(, [row.text for row in rows])
        # self.assertIn('2: Buy Coffee', [row.text for row in rows])

        # It goes on to test some things, as testing goats do, and comes back, opening that URL.

        # He sees that all of his TODOs are still there


if __name__ == '__main__':
    unittest.main()

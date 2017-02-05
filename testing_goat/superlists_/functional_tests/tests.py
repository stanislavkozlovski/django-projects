import sys
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        # Use our own server for tests on staging/production
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return

        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def assertRowInTable(self, desired_row):
        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(desired_row, [row.text for row in rows])

    def assertRowNotInTable(self, desired_row):
        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertNotIn(desired_row, [row.text for row in rows])

    def tearDown(self):
        self.browser.quit()

    def test_can_start_todos_and_retrieve_them_later(self):
        # The Testing Goat opens up a popular todo-list website
        self.browser.get(self.server_url)
        # It sees something about TODOs in the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(header_text, 'Start a new To-Do list')
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
        # Gets redirected to a unique URL holding it's list
        goat_list_url = self.browser.current_url
        self.assertRegex(goat_list_url, r'/lists/.*')
        self.assertRowInTable('1: Test Coffee')
        # It types "Buy Coffee" and presses enter again
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys('Buy Coffee')
        input_box.send_keys(Keys.ENTER)

        # His two TODOs are now saved and have a unique URL for the Testing Goat, which is described in the page
        self.assertRowInTable('2: Buy Coffee')
        # self.assertIn(, [row.text for row in rows])
        # self.assertIn('2: Buy Coffee', [row.text for row in rows])

        # It goes on to test some things
        """ Another Testing Goat comes up and opens the site, he does not see the other one's items """
        self.browser.quit()
        self.browser = webdriver.Chrome()
        self.browser.get(self.server_url)

        # the other goat adds a todo item, he is apparently more practical
        input_box = self.browser.find_element_by_id('new_item')
        input_box.send_keys('Test things')
        input_box.send_keys(Keys.ENTER)
        # Gets redirected to his own URL
        other_goat_list_url = self.browser.current_url
        self.assertRegex(goat_list_url, r'/lists/.*')
        self.assertNotEqual(goat_list_url, other_goat_list_url)
        self.assertRowNotInTable('1: Test Coffee')
        self.assertRowNotInTable('2: Buy Coffee')
        self.assertRowInTable('1: Test things')

    def test_layout_and_styling(self):
        # The Aesthetic Goat visits our page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)
        # It notices that the input box is nicely centered
        input_box = self.browser.find_element_by_id('new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=6
        )

        # It starts a new list and sees that the input box is nicely centered there too
        input_box.send_keys('IsItCentered?\n')
        other_input_box = self.browser.find_element_by_id('new_item')
        self.assertAlmostEqual(
            other_input_box.location['x'] + other_input_box.size['width'] / 2,
            512,
            delta=6
        )

import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_todos_and_retrieve_them_later(self):
        # The Testing Goat opens up a popular todo-list website
        self.browser.get('http://localhost:1337')
        # It sees something about TODOs in the title
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the tests!')
        # It is invited to enter a goat TODO

        # It types "Test Coffee"

        # When it presses enter, the page reloads and a textbox prompts for another TODO

        # It types "Buy Coffee" and presses enter again

        # His two TODOs are now saved and have a unique URL for the Testing Goat, which is described in the page

        # It goes on to test some things, as testing goats do, and comes back, opening that URL.

        # He sees that all of his TODOs are still there


if __name__ == '__main__':
    unittest.main()

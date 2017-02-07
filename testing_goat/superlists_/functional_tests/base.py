import sys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class FunctionalTest(StaticLiveServerTestCase):
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

    def assertRowInListTable(self, desired_row):
        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(desired_row, [row.text for row in rows])

    def assertRowNotInListTable(self, desired_row):
        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertNotIn(desired_row, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def tearDown(self):
        self.browser.quit()



from selenium.webdriver.common.keys import Keys
from .base import wait

class ListPage:

    def __init__(self, test):
        self.test = test

    def get_table_rows(self):
        return self.test.browser.find_elements_by_css_selector('#list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        row_text = f'{item_number}: {item_text}'
        rows = self.get_table_rows()
        self.test.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.test.browser.find_element_by_id('id_text')

    def add_list_item(self, item_text, _assert=True):
        num_rows = len(self.get_table_rows())

        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        if _assert:
            self.wait_for_row_in_list_table(item_text, item_number)

        return self

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector('input[name="shared_with"]')

    def get_shared_with_list(self):
        return self.test.browser.find_element_by_css_selector('shared-with-list')

    def share_list_with(self, email):
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(email, [item.text for item in self.get_shared_with_list()]))

    def js_remove_input_box_required_attr(self):
        self.test.browser.execute_script("document.getElementById('id_text').required = false;")

    def get_list_owner(self):
        return self.test.browser.find_element_by_id('id_list_owner').text
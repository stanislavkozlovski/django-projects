from selenium import webdriver
from .base import FunctionalTest


def quit_if_possible(browser):
    try: browser.quit()
    except: pass

class SharingTest(FunctionalTest):

    def test_can_share_list_with_another_user(self):
        # Carl is a logged-in user
        self.create_pre_authenticated_session('carl@abv.bg')
        carl_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(carl_browser))

        # his friend Lucifer is also hanging out
        luci_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(luci_browser))
        self.browser = luci_browser
        self.create_pre_authenticated_session('luci')

        # carl goes to the home page and starts a list
        self.browser = carl_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Pray')

        # He notices a share this list button
        share_box = self.browser.find_element_by_css_selector('input[name="sharee"]')
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )


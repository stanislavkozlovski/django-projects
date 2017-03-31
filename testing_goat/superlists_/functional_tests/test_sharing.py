from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


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
        list_page = ListPage(self).add_list_item('Pray')

        # He notices a share this list button
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # the page updates to say that the list has been shared wiwth luci
        list_page.share_list_with('luci')

        # Lucifer goes to the list page
        self.browser = luci_browser
        MyListPage(self).go_to_my_lists_page()

        # He sees Carl's list in there! WTF?
        self.browser.find_element_by_link_text('Pray').click()

        # On the list page, Lucifer can see that it's Carl's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'carl@abv.bg'
        ))

        # He adds an item to the list
        list_page.add_list_item('To the devil!')

        # When Carl refreshes the page, he sees Lucifer's message
        self.browser = carl_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('To the devil!', 2)


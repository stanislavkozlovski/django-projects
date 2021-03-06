from django.conf import settings
from .base import FunctionalTest
from .list_page import ListPage

class MyListsTest(FunctionalTest):
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # the list goat is a logged in user
        list_page = ListPage(self)
        self.create_pre_authenticated_session("list_goat@abv.bg")

        # it goes to the home page and starts a list
        self.browser.get(self.live_server_url)
        list_page.add_list_item("Training")
        list_page.add_list_item("Insane")
        first_list_url = self.browser.current_url

        # For the first time it sees a link called My Lists
        self.browser.find_element_by_link_text('My Lists').click()

        # It sees that its list is in there, named according to its first list item
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("1: Training")
        )
        self.browser.find_element_by_link_text("1: Training").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # It decides to start another list
        self.browser.get(self.live_server_url)
        list_page.add_list_item("Woo")
        second_list_url = self.browser.current_url

        # Under "my lists", its new list appears
        self.browser.find_element_by_link_text("My Lists").click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("2: Woo")
        )
        self.browser.find_element_by_link_text("2: Woo").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # It logs out, the My Lists option disappears
        self.browser.find_element_by_link_text("Sign out").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text("My Lists"),
            []
        ))
import re

from selenium.webdriver.common.keys import Keys
from django.core import mail

from functional_tests.base import FunctionalTest


TEST_EMAIL = "Somebody@abv.bg"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # The Log Goat visits our website and sees a form for logging in
        # It prompts it for an email address so he adds his
        self.browser.get(self.server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling it the email has been sent
        self.wait_for(lambda: self.assertIn(
            'Your unique login URL has been sent! Please check your e-mail.',
            self.browser.find_element_by_tag_name('body').text
        ))

        # It opens it's email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # It has an url link to it
        self.assertIn('This is your login link for Superlists', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail("Could not find the login URL in the sent e-mail.")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)  # the base URLs must be identical

        # the goat clicks the URL
        self.browser.get(url)

        # it is logged in!
        self.wait_for(lambda: self.browser.find_element_by_link_text('Sign out'))
        nav_bar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(TEST_EMAIL, nav_bar.text)

        # Now it logs out
        self.browser.find_element_by_link_text('Sign out').click()

        # it is logged out
        self.wait_for(
            lambda: self.browser.find_element_by_name('email')
        )
        nav_bar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(TEST_EMAIL, nav_bar.text)
from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page


class HomePageTests(TestCase):
    def test_root_url_uses_home_page_view(self):
        result = resolve('/')
        # Should be tied to the same function
        self.assertEqual(result.func, home_page)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page


class HomePageTests(TestCase):
    def test_root_url_uses_home_page_view(self):
        result = resolve('/')
        # Should be tied to the same function
        self.assertEqual(result.func, home_page)

    def test_response_page_returns_correct_html(self):
        request = HttpRequest
        response = home_page(request)

        self.assertTrue(response.content.startswith(b"<html>"))
        self.assertContains(response, "<title>To-Do list</title>")
        self.assertTrue(response.content.endswith(b"<html>"))

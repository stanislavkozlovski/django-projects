import re

from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page


class HomePageTests(TestCase):
    def test_root_url_uses_home_page_view(self):
        result = resolve('/')
        # Should be tied to the same function
        self.assertEqual(result.func, home_page)

    def test_response_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html', request=request)
        self.assertEqualExceptCSFR(response.content.decode(), expected_html)

    def test_post_request_home_page(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Coffee'

        response = home_page(request)

        self.assertIn('Coffee', response.content.decode())

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSFR(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )
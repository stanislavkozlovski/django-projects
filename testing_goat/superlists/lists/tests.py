import re

from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from lists.views import home_page
from lists.models import Item


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

    def test_home_page_post_request_saves_item(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'Coffee'
        home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        first_obj = Item.objects.first()
        self.assertEqual(first_obj.text, 'Coffee')

    def test_home_page_displays_multiple_items(self):
        Item.objects.create(text="One")
        Item.objects.create(text="Two")

        request = HttpRequest()
        response: HttpResponse = home_page(request)

        self.assertIn('One', response.content.decode())
        self.assertIn('Two', response.content.decode())

    def test_home_page_redirects_after_post(self):
        request = HttpRequest()
        request.method = 'POST'
        response: HttpResponse = home_page(request)

        self.assertEqual(response.status_code, 302)  # redirected
        self.assertEqual(response['location'], '/')

    def test_item_is_saved_only_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSFR(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        f_item_text = 'First item ever!'
        first_item = Item()
        first_item.text = f_item_text
        first_item.save()

        s_item_text = 'Second!'
        second_item = Item()
        second_item.text = s_item_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, f_item_text)
        self.assertEqual(second_saved_item.text, s_item_text)
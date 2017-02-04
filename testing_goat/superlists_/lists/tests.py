import re

from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from lists.views import home_page, view_list
from lists.models import Item, List


class NewListTests(TestCase):
    def test_new_list_page_post_request_saves_item(self):
        self.client.post('/lists/new', data={'item_text': 'Coffee'})

        self.assertEqual(Item.objects.count(), 1)
        first_obj = Item.objects.first()
        self.assertEqual(first_obj.text, 'Coffee')

    def test_new_list_page_redirects_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'Aa'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world', target_status_code=301)


class ListViewTests(TestCase):
    def test_uses_lists_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_home_page_displays_multiple_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="One", list=list_)
        Item.objects.create(text="Two", list=list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'One')
        self.assertContains(response, 'Two')


class HomePageTests(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_root_url_uses_home_page_view(self):
        result = resolve('/')
        # Should be tied to the same function
        self.assertEqual(result.func, home_page)

    def test_response_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html', request=request)
        self.assertEqualExceptCSFR(response.content.decode(), expected_html)

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSFR(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )


class ItemModelAndListModelTests(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        f_item_text = 'First item ever!'
        first_item = Item()
        first_item.text = f_item_text
        first_item.list = list_
        first_item.save()

        s_item_text = 'Second!'
        second_item = Item()
        second_item.text = s_item_text
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, f_item_text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, s_item_text)
        self.assertEqual(second_saved_item.list, list_)
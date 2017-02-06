import re

from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape
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
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}', target_status_code=301)

    def test_validation_error_are_sent_back_to_home_page(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error_str = "You can't have an empty list item!"
        self.assertContains(response, escape(expected_error_str))

    def test_invalid_list_items_arent_saved(self):
        response = self.client.post('/lists/new', data={'item_text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


class NewItemTests(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'Hello'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Hello')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        lst = List.objects.create()

        response = self.client.post(
            f'/lists/{lst.id}/add_item',
            data={'item_text': 'Hello'}
        )

        self.assertRedirects(response, f'/lists/{lst.id}', target_status_code=301)


class ListViewTests(TestCase):
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response: HttpResponse = self.client.get(f'/lists/{correct_list.id}/', data={'item_text': "AaA"})
        self.assertEqual(response.context['list'], correct_list)

    def test_uses_lists_template(self):
        list_: List = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text="One", list=list_)
        Item.objects.create(text="Two", list=list_)
        useless_list_ = List.objects.create()
        Item.objects.create(text="Three", list=useless_list_)

        response = self.client.get(f'/lists/{list_.id}/')

        self.assertContains(response, 'One')
        self.assertContains(response, 'Two')
        self.assertNotContains(response, 'Three')


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



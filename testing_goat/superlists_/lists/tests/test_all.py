import re
from unittest.mock import patch, Mock
import unittest

from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape
from lists.views import home_page, view_list, new_list2
from lists.models import Item, List
from accounts.models import User
from lists.forms import ItemForm, ExistingListItemForm
from lists.constants import EMPTY_LIST_ERROR_MSG, DUPLICATE_ITEM_ERROR_MSG


@patch('lists.views.NewListForm')
class NewListViewTests(unittest.TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):
        new_list2(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True
        new_list2(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
            self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list2(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_page_if_form_invalid(
            self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list2(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(self.request, 'home.html', {'form': mock_form})

    @patch('lists.views.redirect')
    def test_does_not_save_if_form_invalid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list2(self.request)
        self.assertFalse(mock_form.save.called)


class NewListIntegratedTests(TestCase):
    def test_new_list_page_post_request_saves_item(self):
        self.client.post('/lists/new', data={'text': 'Coffee'})

        self.assertEqual(Item.objects.count(), 1)
        first_obj = Item.objects.first()
        self.assertEqual(first_obj.text, 'Coffee')

    def test_new_list_has_owner(self):
        user = User.objects.create(email="fman@abv.bg")
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'Coffee'})
        first_obj = List.objects.first()
        self.assertEqual(first_obj.owner, user)

    def test_new_list_page_redirects_after_post(self):
        response = self.client.post('/lists/new', data={'text': 'Aa'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_error_are_sent_back_to_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error_str = EMPTY_LIST_ERROR_MSG
        self.assertContains(response, escape(expected_error_str))

    def test_invalid_list_items_arent_saved(self):
        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_home_page(self):
        response = self.client.post(
            '/lists/new',
            data={'text': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_invalid_input_passes_item_form(self):
        response = self.client.post(
            '/lists/new',
            data={'text': ''}
        )

        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_input_shows_error(self):
        response = self.client.post(
            '/lists/new',
            data={'text': ''}
        )

        self.assertContains(response, escape(EMPTY_LIST_ERROR_MSG))


class ListViewTests(TestCase):
    def post_invalid_input(self) -> HttpResponse:
        lst = List.objects.create()
        response: HttpResponse = self.client.post(f'/lists/{lst.id}/', data={'text': ""})

        return response

    def test_displays_item_form(self):
        correct_list = List.objects.create()
        response: HttpResponse = self.client.get(f'/lists/{correct_list.id}/', data={'text': "AaA"})

        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_shows_up_on_page(self):
        lst = List.objects.create()
        item1 = Item.objects.create(text='Text', list=lst)
        response: HttpResponse = self.client.post(f'/lists/{lst.id}/', data={'text': "Text"})

        self.assertContains(response, escape(DUPLICATE_ITEM_ERROR_MSG))
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.count(), 1)

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response: HttpResponse = self.client.get(f'/lists/{correct_list.id}/')
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

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'Hello'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'Hello')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        lst = List.objects.create()

        response = self.client.post(
            f'/lists/{lst.id}/',
            data={'text': 'Hello'}
        )

        self.assertRedirects(response, f'/lists/{lst.id}/')

    def test_invalid_item_POST_shows_error(self):
        response = self.post_invalid_input()

        self.assertContains(response, escape(EMPTY_LIST_ERROR_MSG))

    def test_invalid_item_is_not_saved(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_renders_invalid_input_list_template(self):
        rsp: HttpResponse = self.post_invalid_input()

        self.assertEqual(rsp.status_code, 200)
        self.assertTemplateUsed(rsp, 'list.html')

    def test_invalid_input_uses_item_template(self):
        rsp: HttpResponse = self.post_invalid_input()

        self.assertIsInstance(rsp.context['form'], ExistingListItemForm)

    def test_my_lists_url_renders_my_lists_template(self):
        user = User.objects.create(email='user@abv.bg')
        rsp: HttoResponse = self.client.get(f'/lists/users/{user.email}/')
        self.assertTemplateUsed(rsp, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        wrong_owner = User.objects.create(email='wrong_owner@abv.bg')
        wrong_owner.save()
        correct_user = User.objects.create(email='user@abv.bg')
        correct_user.save()
        response = self.client.get('/lists/users/user@abv.bg/')
        self.assertEqual(response.context['owner'], correct_user)


class HomePageTests(TestCase):
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSFR(self, html_code1, html_code2):
        return self.assertMultiLineEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )



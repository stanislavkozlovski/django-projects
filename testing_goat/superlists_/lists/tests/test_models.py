from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List

from accounts.models import User


class ItemModelTests(TestCase):
    def test_item_str(self):
        item = Item(text='hello')
        self.assertEqual(str(item), 'hello')

    def test_default_value(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List()
        list_.save()
        item = Item()
        item.list = list_
        item.save()

        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_blank_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_cannot_save_duplicate_item(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='dup')
        item.save()
        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='dup')
            item.full_clean()

    def test_can_have_duplicate_items_in_different_lists(self):
        list_ = List.objects.create()
        list2_ = List.objects.create()
        item = Item(list=list_, text='dup')
        item_2 = Item(list=list2_, text='dup')
        item.full_clean()  # should not raise an error


class ListsModelTests(TestCase):
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        expected_url = f'/lists/{list_.id}/'

        self.assertEqual(list_.get_absolute_url(), expected_url)

    def test_list_can_have_owner(self):
        user = User.objects.create(email="guy@abv.bg")
        user.save()
        list = List.objects.create(owner=user)
        list.save()
        self.assertIn(list, user.list_set.all())

    def test_list_owner_is_optional(self):
        List.objects.create()  # should not raise an error

    def test_create_returns_new_list_object(self):
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_text(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='first item')
        Item.objects.create(list=list_, text='second item')
        self.assertEqual(list_.name, 'first item')

    def test_list_name_without_items_is_new_list(self):
        list_ = List.objects.create()
        self.assertEqual(list_.name, 'New List')

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_create_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_try_get_object_pk_returns_list(self):
        ls = List.create_new(first_item_text='whatup')
        ls.save()
        self.assertEqual(ls, List.try_get_object_pk(pk=str(ls.id)))

    def test_try_get_object_pk_invalid_pk_returns_none(self):
        ls = List.create_new(first_item_text='whatup')
        ls.save()
        self.assertIsNone(List.try_get_object_pk(pk='4131'))

    def test_try_get_object_pk_invalid_pk_type_returns_none(self):
        ls = List.create_new(first_item_text='whatup')
        ls.save()
        self.assertIsNone(List.try_get_object_pk(pk='WAA'))

    def test_share_list_shares_list(self):
        ls = List.create_new(first_item_text='whatup')
        ls.save()
        user = User(email='me@abv.bg')
        user.save()
        res = ls.share_with(user.email)
        user.save()
        self.assertTrue(res)
        self.assertIn(user, ls.shared_with.all())
        self.assertIn(ls, user.shared_lists.all())

    def test_share_list_invalid_email_doesnt_throw(self):
        ls = List.create_new(first_item_text='whatup')
        ls.save()
        user = User(email='me@abv.bg')
        user.save()
        res = ls.share_with('nobody')
        user.save()

        self.assertFalse(res)
        self.assertNotIn(user, list(ls.shared_with.all()))
        self.assertEqual(len(ls.shared_with.all()), 0)
        self.assertNotIn(ls, list(user.shared_lists.all()))
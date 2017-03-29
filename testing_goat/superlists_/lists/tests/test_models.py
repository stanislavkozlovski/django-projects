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
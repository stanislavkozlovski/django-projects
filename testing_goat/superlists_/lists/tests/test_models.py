from django.test import TestCase
from lists.models import Item, List


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

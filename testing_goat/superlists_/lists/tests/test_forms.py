from django.test import TestCase

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm
from lists.constants import EMPTY_LIST_ERROR_MSG, DUPLICATE_ITEM_ERROR_MSG


class ExistingListItemFormTests(TestCase):
    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text':"hello"})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Add a to-do"', form.as_p())

    def test_form_validation_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR_MSG])

    def test_form_validation_duplicate_items(self):
        list_ = List.objects.create()
        item = Item.objects.create(text='NoTwins!', list=list_)
        form = ExistingListItemForm(for_list=list_, data={'text': 'NoTwins!'})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR_MSG])


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form: ItemForm = ItemForm()
        self.assertIn('placeholder="Add a to-do"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_LIST_ERROR_MSG])

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'Samurai Jack'})
        new_item: Item = form.save(for_list=list_)

        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.list, list_)
        self.assertEqual(new_item.text, 'Samurai Jack')
        self.assertEqual(Item.objects.count(), 1)

    def test_form_save_handles_creating_a_new_list(self):
        form = ItemForm(data={'text': 'Samurai Jack'})
        new_item: Item = form.save()

        self.assertEqual(new_item, Item.objects.first())
        self.assertIsInstance(new_item.list, List)
        self.assertEqual(new_item.list, List.objects.first())
        self.assertEqual(new_item.text, 'Samurai Jack')
        self.assertEqual(Item.objects.count(), 1)
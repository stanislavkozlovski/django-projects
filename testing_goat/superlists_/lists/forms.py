from django.forms import Form, CharField, fields as dj_fields, models
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.constants import EMPTY_LIST_ERROR_MSG, DUPLICATE_ITEM_ERROR_MSG


class ItemForm(models.ModelForm):
    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': dj_fields.TextInput(attrs={
                'placeholder': 'Add a to-do',
                'class': 'form-control input-lg'
            })
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR_MSG}
        }

    # def save(self, for_list: List=None):
    #     if for_list is None:
    #         for_list = List.objects.create()
    #     self.instance.list = for_list
    #     return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list: List, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR_MSG]}
            self._update_errors(e)

    # def save(self):
    #     return models.ModelForm.save(self)


class NewListForm(ItemForm):
    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data['text'])
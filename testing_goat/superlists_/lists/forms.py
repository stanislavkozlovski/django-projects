from django.forms import Form, CharField, fields as dj_fields, models

from lists.models import Item
from lists.constants import EMPTY_LIST_ERROR_MSG


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

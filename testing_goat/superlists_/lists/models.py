from django.db import models
from django.core.urlresolvers import reverse
from accounts.models import User


class List(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True)

    @property
    def name(self):
        first_item = self.item_set.first()
        if first_item is None:
            return 'New List'
        
        return first_item.text

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    @staticmethod
    def try_get_object_pk(pk: str):
        try:
            pk = int(pk)
        except ValueError:
            return None

        resulting_list = None
        try:
            resulting_list = List.objects.get(pk=pk)
        except List.DoesNotExist as e:
            pass

        return resulting_list

    def share_with(self, email):
        """ Shares the list with a given person"""
        try:
            user = User.objects.get(pk=email)
        except User.DoesNotExist as e:
            return False

        user.shared_lists.add(self)
        return True


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List)

    class Meta:
        ordering = ('id', )
        unique_together = ('list', 'text')

    def __str__(self):
        return str(self.text)

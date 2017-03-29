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


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List)

    class Meta:
        ordering = ('id', )
        unique_together = ('list', 'text')

    def __str__(self):
        return str(self.text)

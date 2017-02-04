
from django.conf.urls import url
from django.contrib import admin
from lists.views import view_list, new_list, add_item

urlpatterns = [
    url(r'^(\d+)/add_item$', add_item, name='add_item'),  # Add item to a list
    url(r'^(\d+)/$', view_list, name='view_list'),  # Specific list view
    url(r'^new$', new_list, name='new_list')
    # url(r'^admin/', admin.site.urls),
]

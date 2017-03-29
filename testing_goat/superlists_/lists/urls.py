from django.conf.urls import url
from django.contrib import admin
from lists.views import view_list, new_list, my_lists

urlpatterns = [
    url(r'^(\d+)/$', view_list, name='view_list'),  # Specific list view
    url(r'^new$', new_list, name='new_list'),
    url(r'^users/(.+@.+)/$', my_lists, name='my_lists')
    # url(r'^admin/', admin.site.urls),
]

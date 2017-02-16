from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout
from accounts.views import send_email_post, login

urlpatterns = [
    url(r'^send_email$', send_email_post, name='send_email'),
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]

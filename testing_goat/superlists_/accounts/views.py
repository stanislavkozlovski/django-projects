from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail as send_email
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

from accounts.models import Token


# Create your views here.
# @accounts/send_email
def send_email_post(request: HttpRequest):
    # Generate the unique Token and the URL
    user_email = request.POST.get('email', '')
    user_token = Token.objects.create(email=user_email)
    unique_url = request.build_absolute_uri(reverse('login') + f'?token={user_token.uid}')

    send_email(recipient_list=[user_email],
               from_email='me',
               subject='Your login link for Superlists',
               message=f'This is your login link for Superlists. Simply click it and you will be logged in!\n{unique_url}')
    messages.success(request, 'Your unique login URL has been sent! Please check your e-mail.')
    return redirect('/')


def login(request: HttpRequest):
    login_token = request.GET.get('token', '')
    return redirect('/')
import uuid
from django.db import models
# from django.contrib.auth import models as auth_models
# from django.contrib import auth

# Hacky way to avoid the lack of 'last_login" field in our user
# auth.signals.user_logged_in.disconnect(auth_models.update_last_login)


# Create your models here.
class User(models.Model):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=60)
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Token

User = get_user_model()


class UserModelTests(TestCase):
    def test_user_is_valid_with_email_only(self):
        user = User(email="me@abv.bg")
        user.full_clean()  # should not raise anything


class TokenModelTests(TestCase):
    def test_links_user_with_auto_generated_token(self):
        token_1 = Token.objects.create(email="me@abv.bg")
        token_2 = Token.objects.create(email="me@abv.bg")
        self.assertNotEqual(token_1.uid, token_2.uid)
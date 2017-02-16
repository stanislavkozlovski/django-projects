from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class AuthenticationTests(TestCase):

    def test_return_none_with_invalid_token(self):
        """ Should return None"""
        result = PasswordlessAuthenticationBackend().authenticate('Invalid_TOKEN')
        self.assertIsNone(result)

    def test_creates_new_user_non_existant_email(self):
        """ Given a valid token with an email that is not associated with a
            user in the DB, it should create a new User"""
        users = User.objects.all()
        self.assertEqual(len(users), 0)
        Token.objects.create(email='valid_email@abv.bg', uid='valid_token')

        new_user = PasswordlessAuthenticationBackend().authenticate('valid_token')

        # should have created a new user
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, 'valid_email@abv.bg')
        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user, users[0])

    def test_does_not_create_new_user_on_existing_user(self):
        User.objects.create(email='valid_email@abv.bg')
        Token.objects.create(email='valid_email@abv.bg', uid='valid_token')

        users = User.objects.all()
        self.assertEqual(len(users), 1)
        orig_user = users[0]

        result = PasswordlessAuthenticationBackend().authenticate('valid_token')

        # Shouldn't have created anything
        users = User.objects.all()
        self.assertEqual(len(users), 1)

        self.assertIsInstance(result, User)
        self.assertEqual(result, orig_user)
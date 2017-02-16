from unittest.mock import patch, call
from django.test import TestCase

from accounts.models import Token

class SendLoginEmailViewTests(TestCase):

    def test_send_email_redirects(self):
        response = self.client.post('/accounts/send_email',
                                    data={'email': "thatguy@abv.bg"})
        self.assertRedirects(response, '/')

    def test_creates_token(self):
        response = self.client.post('/accounts/send_email',
                                    data={'email': "thatguy@abv.bg"})
        created_token = Token.objects.first()

        self.assertEqual(created_token.email, 'thatguy@abv.bg')

    @patch('accounts.views.send_email')
    def test_sends_token_link_to_email(self, mock_send_email):
        response = self.client.post('/accounts/send_email',
                                    data={'email': "thatguy@abv.bg"})
        created_token: Token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={created_token.uid}'
        (), kwargs = mock_send_email.call_args
        self.assertIn(expected_url, kwargs['message'])

    @patch('accounts.views.send_email')
    def test_sends_email_to_address(self, mock_fn):
        """ Monkey patch a fake send_email function """
        response = self.client.post('/accounts/send_email',
                                    data={'email': "thatguy@abv.bg"})

        self.assertTrue(mock_fn.called)
        (), kwargs = mock_fn.call_args
        self.assertEqual(kwargs['subject'], 'Your login link for Superlists')
        self.assertIn('This is your login link for Superlists', kwargs['message'])
        self.assertEqual(kwargs['recipient_list'][0], 'thatguy@abv.bg')

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_email',
                                    data={'email': "thatguy@abv.bg"},
                                    follow=True)

        received_message = list(response.context['messages'])[0]
        self.assertEqual(received_message.message, 'Your unique login URL has been sent! Please check your e-mail.')
        self.assertEqual(received_message.tags, 'success')


@patch('accounts.views.auth')  # mock out the whole authentication module
class LoginTestView(TestCase):

    def test_login_redirects(self, mock_auth):
        response = self.client.get('/accounts/login?token=lala123')
        self.assertRedirects(response, '/')

    def test_login_calls_authenticate_with_token(self, mock_auth):
        self.client.get('/accounts/login?token=lala123')
        self.assertEqual(mock_auth.authenticate.call_args, call(uid='lala123'))

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?token=lala123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_call_auth_login_if_user_doesnt_exist(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=lala123')

        self.assertFalse(mock_auth.login.called)
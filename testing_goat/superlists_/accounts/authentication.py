from accounts.models import Token, User


class PasswordlessAuthenticationBackend:

    def authenticate(self, uid):
        if not Token.objects.filter(uid=uid).exists():
            # Invalid token!
            return None
        token = Token.objects.filter(uid=uid).first()

        return User.objects.get_or_create(email=token.email)[0]

    def get_user(self, email):
        return User.objects.filter(email=email).first()

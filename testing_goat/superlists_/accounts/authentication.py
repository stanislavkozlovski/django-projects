from accounts.models import Token, User


class PasswordlessAuthenticationBackend:

    def authenticate(self, uid):
        if not Token.objects.filter(uid=uid).exists():
            # Invalid token!
            return None
        token = Token.objects.filter(uid=uid).first()

        if not User.objects.filter(email=token.email).exists():
            # Create a new user
            return User.objects.create(email=token.email)

        return User.objects.get(email=token.email)

    def get_user(self, email):
        return User.objects.get(email=email)
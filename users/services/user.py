from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import exceptions

User = get_user_model()


class UserService:
    """User service class"""

    @staticmethod
    def user_login(username: str, password: str) -> Token:
        """Login user, return new token

        :param str username: User username
        :param str password: User password

        :return: Created Token
        """
        user = authenticate(username=username, password=password)
        if not user:
            raise exceptions.AuthenticationFailed()
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        return token

    @staticmethod
    def user_logout(user: User) -> dict:
        """Logout user removing his token

        :param User user: User to logout

        :return: Django deletion result data
        """
        return Token.objects.filter(user=user).delete()

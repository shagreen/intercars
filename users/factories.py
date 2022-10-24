from django.contrib.auth import get_user_model
from factory import Faker, PostGenerationMethodCall
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Django user model factory class"""

    class Meta:
        """DjangoModelFactory meta class"""
        model = User
        django_get_or_create = ('username',)

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    username = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password')
    is_staff = True
    is_superuser = True

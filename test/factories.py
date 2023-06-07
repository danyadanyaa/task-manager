from factory import PostGenerationMethodCall
from factory.django import DjangoModelFactory
from faker import Faker
from main.models import User


class UserFactory(DjangoModelFactory):
    username = Faker("en_US").user_name()
    password = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User

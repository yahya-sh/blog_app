import factory
from factory.django import DjangoModelFactory
from pytest_factoryboy import register
from django.contrib.auth import get_user_model

@register
class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")


from factory.django import DjangoModelFactory
from faker import Factory

faker = Factory.create()


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.CustomUser'
        django_get_or_create = ('username', 'email', 'is_active')

    username = lambda: faker.user_name()
    email = lambda: faker.email()

from factory.django import DjangoModelFactory
from faker import Factory


faker = Factory.create()


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = "tasktime.Projects"
        django_get_or_create = ('name',)

    name = lambda: f"Project {faker.pyint()}"


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = "tasktime.Tasks"
        django_get_or_create = ('name',)

    name = lambda: f"Task {faker.pyint()}"

from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomBaseModelManager(models.Manager):
    def query_active(self) -> QuerySet:
        """
        Queries only active entries
        """
        return self.filter(is_active=True)

    def query_inactive(self) -> QuerySet:
        """
        Queries only the deactivated entries
        """
        return self.filter(is_active=False)


class CustomUserLogBaseModelManager(CustomBaseModelManager):
    def __init__(self):
        super().__init__()
        # Fields to be ignored
        self.IGNORE_FIELDS_CREATE = ["created_by", "modified_by"]

    def create(self, user: User, **extra_fields):
        """
        Overrides the default create method
        it will accept user to be used for
        both created_by and modified_by
        """
        # If any o the following fields are in extra_fields, then
        # it will be removed
        for field in self.IGNORE_FIELDS_CREATE:
            if extra_fields.get(field, None):
                extra_fields.pop(field, None)
        # Creates new entry
        new_entry = self.model(
            created_by=user,
            modified_by=user,
            **extra_fields
        )
        # Save in database
        new_entry.save()
        return new_entry

    def query_by_user_creator(self, user: User) -> QuerySet:
        """
        Queries only the entries created by the given user
        """
        return self.filter(created_by=user)

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers.custom_base_model_manager import (CustomBaseModelManager,
                                                 CustomUserLogBaseModelManager)

Users = get_user_model()


# Create your models here.
class CustomBaseModel(models.Model):
    """
    Base Custom Model containing common properties and
    methods that can be used by other apps
    """
    public_id = models.CharField(
        default=uuid.uuid4,
        unique=True,
        max_length=36
    )
    is_active = models.BooleanField(
        help_text=_("Show whether the entry is active or not"),
        default=True
    )
    created_on = models.DateTimeField(
        help_text=_("Entry creation date"),
        auto_now_add=True,
        editable=False
    )
    modified_on = models.DateTimeField(
        help_text=_("Date of last modification"),
        auto_now=True
    )

    objects = CustomBaseModelManager()

    def activate(self):
        """
        Method to activate entry
        """
        self.is_active = True
        self.save()

    def deactivate(self):
        """
        Method to deactivate entry
        """
        self.is_active = False
        self.save()

    class Meta:
        abstract = True


class CustomUserLogBaseModel(CustomBaseModel):
    """
    Custom Base Model that also logs user information
    regarding who created or modified an entry
    """
    created_by = models.ForeignKey(
        Users,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="%(app_label)s_%(class)s_create",
        related_query_name="%(app_label)s_%(class)s_created",
        help_text=_("Created by this user"),
        editable=False
    )
    modified_by = models.ForeignKey(
        Users,
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="%(app_label)s_%(class)s_modified",
        related_query_name="%(app_label)s_%(class)s_modified",
        help_text=_("Last modified by this user")
    )

    objects = CustomUserLogBaseModelManager()

    def activate(self, user):
        """
        Overrided method to activate an entry
        It will also log which user activated
        """
        self.is_active = True
        self.modified_by = user
        self.save()

    def deactivate(self, user):
        """
        Overrided method to deactivate an entry
        It will also log which user activated
        """
        self.is_active = False
        self.modified_by = user
        self.save()

    class Meta:
        abstract = True

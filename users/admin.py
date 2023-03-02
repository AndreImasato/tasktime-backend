from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active")
    list_filter = ("email", "username", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "groups", "user_permissions")
        }),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )
        }),
    )
    search_fields = ("email", "username")
    ordering = ("email", "username")


admin.site.register(CustomUser, CustomUserAdmin)

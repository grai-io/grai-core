from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.admin import TokenAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User

from .forms import CustomUserChangeForm, CustomUserCreationForm

TokenAdmin.raw_id_fields = ["user"]


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("username", "first_name", "last_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ["username", "first_name", "last_name"]


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)

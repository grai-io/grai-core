from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.admin import TokenAdmin

from users.models import User
from workspaces.models import Membership

from .forms import CustomUserChangeForm, CustomUserCreationForm

TokenAdmin.raw_id_fields = ["user"]


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    fk_name = "user"


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
    list_display = ("username", "first_name", "last_name", "is_staff", "is_superuser", "created_at")
    list_filter = ("is_staff", "is_superuser", ("created_at", DateFieldListFilter))
    search_fields = ["username", "first_name", "last_name"]

    inlines = [
        MembershipInline,
    ]


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)

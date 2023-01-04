from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from users.models import User
from django.contrib.auth.models import Group


from .forms import CustomUserChangeForm, CustomUserCreationForm

TokenAdmin.raw_id_fields = ["user"]


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("username", "first_name", "last_name", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ["username", "first_name", "last_name"]


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from users.models import User

from .forms import CustomUserChangeForm, CustomUserCreationForm

TokenAdmin.raw_id_fields = ["user"]


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["username"]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

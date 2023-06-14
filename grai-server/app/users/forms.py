from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "password1",
            "password2",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "is_staff", "is_superuser")

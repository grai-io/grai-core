from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username",)
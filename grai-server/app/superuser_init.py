from decouple import config
from django.contrib.auth import get_user_model

User = get_user_model()

username = config("DJANGO_SUPERUSER_USERNAME", None)
password = config("DJANGO_SUPERUSER_PASSWORD", None)
email = config("DJANGO_SUPERUSER_EMAIL", None)

if not username and email:
    username = email


if username and password and not User.objects.filter(is_superuser=True).exists():
    print(f"Creating superuser {username}")
    User.objects.create_superuser(username, password)

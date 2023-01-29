import os

from decouple import config
from django.contrib.auth import get_user_model

from workspaces.models import Membership, Organisation, Workspace

## Init Superuser

User = get_user_model()

username = config("DJANGO_SUPERUSER_USERNAME", None)
password = config("DJANGO_SUPERUSER_PASSWORD", None)
email = config("DJANGO_SUPERUSER_EMAIL", None)
organisation_name = config("DJANGO_SUPERUSER_ORGANISATION", "default")
workspace_name = config("DJANGO_SUPERUSER_WORKSPACE", "default")

if not username and email:
    username = email

if username and password and not User.objects.filter(is_superuser=True).exists():
    print(f"Creating superuser {username}")
    user = User.objects.create_superuser(username, password)

    print(f"Get or creating organisation {organisation_name}")
    organisation, created = Organisation.objects.get_or_create(name=organisation_name)

    print(f"Get or creating workspace {workspace_name}")
    workspace, created = Workspace.objects.get_or_create(name=workspace_name, organisation=organisation)

    print(f"Creating membership")
    Membership.objects.create(role="admin", user=user, workspace=workspace)

from django_multitenant.utils import set_current_tenant
from workspaces.models import WorkspaceAPIKey
from django.core.exceptions import PermissionDenied


class MultitenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.headers.get("Authorization")

        if header:
            [type, key] = header.split()
            # TODO: Consider handling Bearer token here
            if type == "Api-Key":
                try:
                    api_key = WorkspaceAPIKey.objects.get_from_key(key)
                except WorkspaceAPIKey.DoesNotExist:
                    raise PermissionDenied()

                workspace = api_key.workspace

                if workspace:
                    set_current_tenant(workspace)

        return self.get_response(request)

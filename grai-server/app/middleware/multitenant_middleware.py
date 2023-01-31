from django_multitenant.utils import set_current_tenant


class MultitenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_tenant(None)

        return self.get_response(request)

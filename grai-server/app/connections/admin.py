from django.contrib import admin
from .models import Connector, Connection, Run


class ConnectorAdmin(admin.ModelAdmin):
    search_fields = ["id", "name"]


class ConnectionAdmin(admin.ModelAdmin):
    search_fields = ["id", "namespace", "name"]
    list_filter = (
        "namespace",
        "is_active",
        ("connector", admin.RelatedOnlyFieldListFilter),
        ("workspace", admin.RelatedOnlyFieldListFilter),
        ("created_by", admin.RelatedOnlyFieldListFilter),
    )


class RunAdmin(admin.ModelAdmin):
    search_fields = ["id"]

    list_filter = (
        "status",
        ("connection", admin.RelatedOnlyFieldListFilter),
    )


admin.site.register(Connector, ConnectorAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Run, RunAdmin)

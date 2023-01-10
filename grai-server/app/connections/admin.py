from django.contrib import admin

from .models import Connection, Connector, Run


class ConnectorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")

    search_fields = ["id", "name"]

    list_filter = ("is_active",)


class ConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "connector",
        "workspace",
        "namespace",
        "is_active",
        "created_by",
    )

    search_fields = ["id", "namespace", "name"]
    list_filter = (
        ("connector", admin.RelatedOnlyFieldListFilter),
        ("workspace", admin.RelatedOnlyFieldListFilter),
        ("created_by", admin.RelatedOnlyFieldListFilter),
        "namespace",
        "is_active",
    )


class RunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "connection",
        "status",
        "workspace",
        "started_at",
        "user",
    )

    search_fields = ["id"]

    list_filter = (
        "status",
        ("connection", admin.RelatedOnlyFieldListFilter),
        "workspace",
    )


admin.site.register(Connector, ConnectorAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Run, RunAdmin)

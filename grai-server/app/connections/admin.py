from common.admin.fields.json_widget import PrettyJSONWidget
from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import JSONField

from .models import Connection, Connector, Run, RunFile


class ConnectorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")

    search_fields = ["id", "name"]

    list_filter = ("is_active",)

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


class RunInline(admin.TabularInline):
    model = Run
    extra = 0
    fields = ["status", "metadata", "created_at", "started_at", "finished_at", "user"]
    readonly_fields = ["status", "metadata", "created_at", "started_at", "finished_at", "user"]

    def has_add_permission(self, request, obj=None):  # pragma: no cover
        return False

    def has_delete_permission(self, request, obj=None):  # pragma: no cover
        return False


class ConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "connector",
        "workspace",
        "namespace",
        "is_active",
        "temp",
        "created_by",
        "created_at",
    )

    search_fields = ["id", "namespace", "name"]
    list_filter = (
        ("workspace", admin.RelatedOnlyFieldListFilter),
        ("created_at", DateFieldListFilter),
        ("connector", admin.RelatedOnlyFieldListFilter),
        ("created_by", admin.RelatedOnlyFieldListFilter),
        "namespace",
        "is_active",
        "temp",
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}

    inlines = [
        RunInline,
    ]


class RunFileInline(admin.TabularInline):
    model = RunFile
    extra = 0
    fields = ["file", "name", "created_at"]
    readonly_fields = ["file", "name", "created_at"]

    def has_add_permission(self, request, obj=None):  # pragma: no cover
        return False

    def has_delete_permission(self, request, obj=None):  # pragma: no cover
        return False


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
        ("started_at", DateFieldListFilter),
        ("connection", admin.RelatedOnlyFieldListFilter),
        "workspace",
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}

    inlines = [
        RunFileInline,
    ]


admin.site.register(Connector, ConnectorAdmin)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(Run, RunAdmin)

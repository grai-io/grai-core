from django.contrib import admin
from common.admin.fields.json_widget import PrettyJSONWidget

from .models import Edge, Node

from django.db.models import JSONField


class NodeAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def final_name(self, obj):
        return obj.display_name if obj.display_name else obj.name

    list_display = (
        "id",
        "namespace",
        "final_name",
        "data_source",
        "workspace",
        "is_active",
    )

    search_fields = ["id", "namespace", "name", "display_name", "data_source"]

    list_filter = (
        "workspace",
        "namespace",
        "is_active",
        "data_source",
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


class EdgeAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def final_name(self, obj):
        return obj.display_name if obj.display_name else obj.name

    list_display = (
        "id",
        "namespace",
        "final_name",
        "data_source",
        "workspace",
        "is_active",
    )

    search_fields = ["id", "namespace", "name", "display_name", "data_source"]

    list_filter = (
        "workspace",
        "namespace",
        "is_active",
        "data_source",
        ("source", admin.RelatedOnlyFieldListFilter),
        ("destination", admin.RelatedOnlyFieldListFilter),
    )

    formfield_overrides = {JSONField: {"widget": PrettyJSONWidget}}


admin.site.register(Node, NodeAdmin)
admin.site.register(Edge, EdgeAdmin)

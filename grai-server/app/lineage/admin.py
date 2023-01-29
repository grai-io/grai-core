from django.contrib import admin

from .models import Edge, Node


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


admin.site.register(Node, NodeAdmin)
admin.site.register(Edge, EdgeAdmin)

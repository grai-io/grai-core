from django.contrib import admin

from .models import Edge, Node


class NodeAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def final_name(self, obj):
        return obj.display_name or obj.name

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
        "namespace",
        "is_active",
        "data_source",
        "workspace",
    )


class EdgeAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def final_name(self, obj):
        return obj.display_name or obj.name

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
        "namespace",
        "is_active",
        "data_source",
        "workspace",
        ("source", admin.RelatedOnlyFieldListFilter),
        ("destination", admin.RelatedOnlyFieldListFilter),
    )


admin.site.register(Node, NodeAdmin)
admin.site.register(Edge, EdgeAdmin)

from django.contrib import admin

from .models import Edge, Node


class NodeAdmin(admin.ModelAdmin):
    search_fields = ["id", "namespace", "name", "display_name", "data_source"]
    list_filter = (
        "namespace",
        "is_active",
        "data_source",
        ("workspace", admin.RelatedOnlyFieldListFilter),
    )


class EdgeAdmin(admin.ModelAdmin):
    search_fields = ["id", "namespace", "name", "display_name", "data_source"]
    list_filter = (
        "namespace",
        "is_active",
        "data_source",
        ("source", admin.RelatedOnlyFieldListFilter),
        ("destination", admin.RelatedOnlyFieldListFilter),
        ("workspace", admin.RelatedOnlyFieldListFilter),
    )


admin.site.register(Node, NodeAdmin)
admin.site.register(Edge, EdgeAdmin)

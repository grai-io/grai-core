from django.contrib import admin
from .models import Connector, Connection, Run


class RunAdmin(admin.ModelAdmin):
    list_filter = (
        "status",
        ("connection", admin.RelatedOnlyFieldListFilter),
    )


admin.site.register(Connector)
admin.site.register(Connection)
admin.site.register(Run, RunAdmin)

from django.contrib import admin

from .models import Connector, Connection, Run

admin.site.register(Connector)
admin.site.register(Connection)
admin.site.register(Run)

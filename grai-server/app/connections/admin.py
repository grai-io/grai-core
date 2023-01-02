from django.contrib import admin

from .models import Connector, Connection

admin.site.register(Connector)
admin.site.register(Connection)

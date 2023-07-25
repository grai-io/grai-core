from django.apps import AppConfig


class LineageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lineage"

    def ready(self):
        import lineage.signals

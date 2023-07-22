from workspaces.sample_data import SampleData
from workspaces.models import Workspace
from asgiref.sync import sync_to_async, async_to_sync
from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create sample data"

    def handle(self, *args, **options):
        workspace = Workspace.objects.get(name="default")
        generator = SampleData(workspace)
        async_to_sync(generator.generate)()
        self.stdout.write(self.style.SUCCESS("Successfully created sample data"))

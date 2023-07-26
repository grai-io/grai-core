from asgiref.sync import async_to_sync, sync_to_async
from django.core.cache import cache
from django.core.management.base import BaseCommand

from workspaces.models import Workspace
from workspaces.sample_data import SampleData


class Command(BaseCommand):
    help = "Create sample data"

    def handle(self, *args, **options):
        workspace = Workspace.objects.get(name="default")
        generator = SampleData(workspace)
        async_to_sync(generator.generate)()
        self.stdout.write(self.style.SUCCESS("Successfully created sample data"))

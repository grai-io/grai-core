from django.core.management.base import BaseCommand, CommandError

from connections.models import Run
from connections.tasks import run_update_server


class Command(BaseCommand):
    help = "Trigger an existing run"

    def add_arguments(self, parser):
        parser.add_argument("run_id", type=str)

    def handle(self, *args, **options):
        run_id = options["run_id"]
        try:
            run = Run.objects.get(pk=run_id)
        except Run.DoesNotExist:
            raise CommandError('run "%s" does not exist' % run_id)

        run_update_server.delay(run_id)

        self.stdout.write(self.style.SUCCESS('Successfully triggered run "%s"' % run_id))

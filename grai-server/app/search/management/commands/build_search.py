from django.core.management.base import BaseCommand

from search.search import SearchClient


class Command(BaseCommand):
    help = "Build the search index"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        search = SearchClient()

        search.build()

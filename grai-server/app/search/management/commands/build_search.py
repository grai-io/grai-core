from typing import List
from django.core.management.base import BaseCommand
from search.search import Search


class Command(BaseCommand):
    help = "Build the search index"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        search = Search()

        search.create()

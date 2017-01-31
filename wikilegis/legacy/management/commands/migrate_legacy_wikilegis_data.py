from django.core.management.base import BaseCommand
from legacy import migration


class Command(BaseCommand):
    def handle(self, *args, **options):
        migration.import_data()

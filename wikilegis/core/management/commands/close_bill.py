from django.core.management.base import BaseCommand
from wikilegis.core.models import Bill
from datetime import date


class Command(BaseCommand):
    def handle(self, *args, **options):
        bills = Bill.objects.filter(status="published", closing_date__lt=date.today())
        for bill in bills:
            bill.status = 'closed'
            bill.save()

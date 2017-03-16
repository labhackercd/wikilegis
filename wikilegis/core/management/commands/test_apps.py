import django.core.management.commands.test
from django.conf import settings


class Command(django.core.management.commands.test.Command):
    args = ''
    help = 'Test all of core apps'

    def handle(self, *args, **options):
        super(Command, self).handle(*(tuple(settings.WIKILEGIS_APPS) + args),
                                    **options)

from django.core.management.base import BaseCommand
from core import plugins
import pkgutil
import click


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help="Plugin name")

    def handle(self, *args, **options):
        availables_plugins = []
        actived = False
        for _, name, _ in pkgutil.iter_modules(['plugins']):
            availables_plugins.append(name)
            if options['name'] == name:
                actived = True
                plugins.add_plugin(name)
                click.secho('Plugin "{}" activated successfully!'.format(
                    options['name']
                ), fg='green')

        if not actived:
            click.secho('Plugin "{}" not found! The availables plugins '
                        'are:'.format(options['name']), fg='red')
            print(availables_plugins)

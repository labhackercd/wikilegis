from django.core.management.base import BaseCommand
from core import plugins
import click


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, help="Plugin name")

    def handle(self, *args, **options):
        plugins_dict = plugins.load_current_plugins()
        available_plugins = []
        deactivated = False
        for name, is_active in plugins_dict.items():
            available_plugins.append(name)
            if options['name'] == name and is_active:
                plugins.remove_plugin(name)
                click.secho('Plugin "{}" deactivated successfully!'.format(
                    options['name']
                ), fg='green')
                deactivated = True
            elif options['name'] == name and not is_active:
                click.secho('Plugin "{}" already deactivated'.format(
                    options['name']
                ), fg='green')
                deactivated = True

        if not deactivated:
            click.secho('Plugin "{}" not found! The availables plugins '
                        'are:'.format(options['name']), fg='red')
            print(available_plugins)

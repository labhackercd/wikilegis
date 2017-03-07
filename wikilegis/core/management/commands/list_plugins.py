from django.core.management.base import BaseCommand
from core import plugins
import pkgutil
import click


class Command(BaseCommand):
    def handle(self, *args, **options):
        click.secho('Availables plugins:', bold=True)
        plugins_dict = plugins.load_current_plugins()
        for _, name, _ in pkgutil.iter_modules(['plugins']):
            if name in plugins_dict.keys():
                is_active = 'x' if plugins_dict[name] else ' '
            else:
                is_active = ' '
            click.secho('[{}] {}'.format(is_active, name))

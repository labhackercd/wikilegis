from django.core.management.base import BaseCommand
from django.db import transaction
from pygov_br.camara_deputados import cd
from plugins.camara_deputados import models
import click


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        click.secho('Fetching data...', bold=True)
        deputies = cd.deputies.all()
        with click.progressbar(deputies, label="Importing deputies") as data:
            for deputy_data in data:
                models.ReportingMember.objects.update_or_create(
                    id=deputy_data['ideCadastro'],
                    name=deputy_data['nomeParlamentar'],
                    party=deputy_data['partido'],
                    region=deputy_data['uf'],
                    email=deputy_data['email'],
                )

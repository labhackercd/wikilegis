from django.core.management.base import BaseCommand
import requests
from wikilegis.core.forms import update_proposition
from wikilegis.core.models import Proposition


class Command(BaseCommand):
    def handle(self, *args, **options):
        propositions = Proposition.objects.all()
        for proposition in propositions:
            params = {'IdProp': proposition.id_proposition}
            site = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID'
            response = requests.get(site, params=params)
            update_proposition(response, proposition.id_proposition)

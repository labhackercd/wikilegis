from django.core.management.base import BaseCommand
import requests
from wikilegis.core.forms import update_proposition
from wikilegis.core.models import Proposition


class Command(BaseCommand):
    def handle(self, *args, **options):
        propositions = Proposition.objects.all()
        for proposition in propositions:
            params = {'IdProp': proposition.id_proposition}
            response = requests.get('http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID'
                                    , params=params)
            update_proposition(response, proposition.id_proposition, proposition.bill.id)

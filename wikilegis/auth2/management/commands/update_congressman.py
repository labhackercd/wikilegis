from django.core.management.base import BaseCommand
import requests
from wikilegis.auth2.models import Congressman
from wikilegis.auth2.admin import update_congressman


class Command(BaseCommand):
    def handle(self, *args, **options):
        congressmen = Congressman.objects.all()
        for congresman in congressmen:
            params = {'ideCadastro': congresman.user.id_congressman, 'numLegislatura': ''}
            response = requests.get('http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDetalhesDeputado',
                                    params=params)
            update_congressman(response, congresman.id)

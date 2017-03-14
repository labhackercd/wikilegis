from autofixture import AutoFixture
from django.test import TestCase
from plugins.camara_deputados import models
from core import models as core_models
import mock


class SignalsTestCase(TestCase):

    def setUp(self):
        self.bill = AutoFixture(core_models.Bill, field_values={
            'title': 'Bill Title'
        }, generate_fk=True).create_one()

    @mock.patch('pygov_br.camara_deputados.cd.proposals.get')
    def test_get_proposal_situation(self, mock_pygov):
        mock_pygov.return_value = {
            'Autor': 'author',
            'ufAutor': 'author region',
            'partidoAutor': 'author party',
            'ideCadastro': 131,
            'Situacao': 'situation'
        }
        proposal_type = AutoFixture(models.ProposalType, field_values={
            'initials': 'PL',
            'description': 'PL'
        }).create_one()
        bill_info = AutoFixture(models.BillInfo, field_values={
            'bill': self.bill,
            'proposal_type': proposal_type,
        }, generate_fk=True).create_one()
        self.assertEquals(bill_info.situation, 'situation')
        self.assertEquals(bill_info.author.name, 'author')

    @mock.patch('pygov_br.camara_deputados.cd.proposals.get')
    def test_get_proposal_situation_keyerror(self, mock_pygov):
        mock_pygov.side_effect = [KeyError()]
        proposal_type = AutoFixture(models.ProposalType, field_values={
            'initials': 'PL',
            'description': 'PL'
        }).create_one()
        with self.assertRaises(Exception):
            AutoFixture(models.BillInfo, field_values={
                'bill': self.bill,
                'proposal_type': proposal_type,
            }, generate_fk=True).create_one()

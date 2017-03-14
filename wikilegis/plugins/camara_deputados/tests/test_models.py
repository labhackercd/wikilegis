from autofixture import AutoFixture
from django.test import TestCase
from core import models as core_models
from plugins.camara_deputados import models
import mock


class ModelsTestCase(TestCase):

    def setUp(self):
        self.bill = AutoFixture(core_models.Bill, field_values={
            'title': 'Bill Title'
        }, generate_fk=True).create_one()

    @mock.patch('pygov_br.camara_deputados.cd.proposals.get')
    def test_bill_info_str(self, mock_pygov):
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
        self.assertEquals(bill_info.__str__(), 'Bill Title')

    def test_proposal_type_str(self):
        proposal_type = AutoFixture(models.ProposalType, field_values={
            'initials': 'PL',
            'description': 'PL'
        }).create_one()
        self.assertEquals(proposal_type.__str__(), 'PL - PL')

    def test_reporting_member_str(self):
        reporting_member = AutoFixture(models.ReportingMember, field_values={
            'name': 'reporting member',
        }).create_one()
        self.assertEquals(reporting_member.__str__(), 'reporting member')

    def test_bill_author_str(self):
        author = AutoFixture(models.BillAuthor, field_values={
            'name': 'author name',
            'region': None,
            'party': None,
            'register_id': None
        }).create_one()
        self.assertEquals(author.__str__(), 'author name')

    def test_bill_author_str_with_register_id(self):
        author = AutoFixture(models.BillAuthor, field_values={
            'name': 'author name',
            'region': 'UF',
            'party': 'TT',
            'register_id': 123
        }).create_one()
        self.assertEquals(author.__str__(), 'author name - TT(UF)')

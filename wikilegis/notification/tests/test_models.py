from autofixture import AutoFixture
from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import Bill, BillTheme
from notification.models import Newsletter


class ModelsTestCase(TestCase):

    def setUp(self):
        self.theme_fixture = AutoFixture(BillTheme)
        self.bill_fixture = AutoFixture(Bill)
        self.newsletter_fixture = AutoFixture(Newsletter)

    def test_newsletter_str(self):
        user = AutoFixture(get_user_model(), field_values={
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@test.com'
        }).create_one()
        self.theme_fixture.create_one()
        bill = self.bill_fixture.create_one()
        bill.title = 'test'
        bill.save()
        newsletter_fixture = AutoFixture(Newsletter, field_values={
            'bill_id': bill.id,
            'user_id': user.id
        })
        newsletter = newsletter_fixture.create_one()
        newsletter.save()
        self.assertEquals(newsletter.__str__(), 'first last - test')

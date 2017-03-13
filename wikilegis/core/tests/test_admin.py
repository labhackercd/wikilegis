from autofixture import AutoFixture
from django.test.client import RequestFactory
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models, admin
from django.contrib import admin as django_admin


class AdminTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.theme_fixture = AutoFixture(models.BillTheme)
        self.bill_fixture = AutoFixture(models.Bill)
        self.segment_fixture = AutoFixture(models.BillSegment)
        self.admin_fixture = AutoFixture(get_user_model(), field_values={
            'is_superuser': True,
            'is_member': True,
            'is_staff': True
        })

    def instance_admin_classes(self, url):
        self.theme_fixture.create_one()
        user_admin = self.admin_fixture.create_one()
        request = self.factory.get(url)
        request.user = user_admin
        bill_inline = admin.BillSegmentInline(models.Bill, django_admin.site)
        formset = bill_inline.get_formset(request)
        pagination_formset = formset()
        self.assertEqual(pagination_formset.per_page, 20)

    def test_bill_segment_inline(self):
        self.instance_admin_classes("/admin/core/bill/add/")

    def test_pagination_formset_value_error(self):
        self.instance_admin_classes("/admin/core/bill/add/?p=a")

    def test_pagination_formset_empty_page(self):
        self.instance_admin_classes("/admin/core/bill/add/?p=-2")

    def test_pagination_formset_change_list_show_all(self):
        self.instance_admin_classes("/admin/core/bill/add/?all")

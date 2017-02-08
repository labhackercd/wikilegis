from autofixture import AutoFixture
from django.test import TestCase
from core import models


class ModelMixinsTestCase(TestCase):

    def setUp(self):
        theme_fixture = AutoFixture(models.BillTheme)
        bill_fixture = AutoFixture(models.Bill)
        theme_fixture.create_one()
        self.bill = bill_fixture.create_one()

        segment_fixture = AutoFixture(models.BillSegment, field_values={
            'bill': self.bill
        })
        self.segment = segment_fixture.create_one()

    def test_vote_count_mixin(self):
        self.bill.upvote_count = None
        self.bill.downvote_count = None
        self.bill.save()
        self.assertEquals(self.bill.upvote_count, 0)
        self.assertEquals(self.bill.downvote_count, 0)

    def test_comment_count_mixin(self):
        self.bill.comments_count = None
        self.bill.save()
        self.assertEquals(self.bill.comments_count, 0)

    def test_participation_count_mixin(self):
        self.segment.participation_count = None
        self.segment.save()
        self.assertEquals(self.segment.participation_count, 0)

    def test_amendment_count_mixin(self):
        segment_fixture = AutoFixture(models.BillSegment)
        segment = segment_fixture.create_one()
        segment.amendments_count = None
        segment.save()
        self.assertEquals(segment.amendments_count, 0)

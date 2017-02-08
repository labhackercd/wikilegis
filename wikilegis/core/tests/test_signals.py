from autofixture import AutoFixture
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from core import models


class ModelMixinsTestCase(TestCase):

    def setUp(self):
        AutoFixture(models.BillTheme).create_one()
        self.bill = AutoFixture(models.Bill).create_one()
        self.segment_fixture = AutoFixture(models.BillSegment, field_values={
            'bill': self.bill
        })
        self.bill_ctype = ContentType.objects.get_for_model(models.Bill)
        self.segment_ctype = ContentType.objects.get_for_model(
            models.BillSegment
        )
        self.user = AutoFixture(get_user_model()).create_one()

    def tearDown(self):
        self.bill.delete()

    def test_update_votes_downvote(self):
        AutoFixture(models.UpDownVote, field_values={
            'user': self.user,
            'content_type': self.bill_ctype,
            'object_id': self.bill.id
        }).create_one()
        bill = models.Bill.objects.get(pk=self.bill.id)
        self.assertEquals(bill.downvote_count, 1)

    def test_update_votes_upvote(self):
        AutoFixture(models.UpDownVote, field_values={
            'user': self.user,
            'content_type': self.bill_ctype,
            'object_id': self.bill.id,
            'vote': True
        }).create_one()
        bill = models.Bill.objects.get(pk=self.bill.id)
        self.assertEquals(bill.upvote_count, 1)

    def test_update_votes_change_upvote(self):
        vote = AutoFixture(models.UpDownVote, field_values={
            'user': self.user,
            'content_type': self.bill_ctype,
            'object_id': self.bill.id,
            'vote': True
        }).create_one()
        vote.vote = False
        vote.save()
        bill = models.Bill.objects.get(pk=self.bill.id)
        self.assertEquals(bill.upvote_count, 0)
        self.assertEquals(bill.downvote_count, 1)

    def test_update_votes_change_downvote(self):
        vote = AutoFixture(models.UpDownVote, field_values={
            'user': self.user,
            'content_type': self.bill_ctype,
            'object_id': self.bill.id,
            'vote': False
        }).create_one()
        vote.vote = True
        vote.save()
        bill = models.Bill.objects.get(pk=self.bill.id)
        self.assertEquals(bill.upvote_count, 1)
        self.assertEquals(bill.downvote_count, 0)

    def test_update_votes_participation_count(self):
        segment = self.segment_fixture.create_one()
        AutoFixture(models.UpDownVote, field_values={
            'user': self.user,
            'content_type': self.segment_ctype,
            'object_id': segment.id,
        }).create_one()
        segment = models.BillSegment.objects.get(pk=segment.id)
        self.assertEquals(segment.participation_count, 1)

    def test_update_comments_count(self):
        AutoFixture(models.Comment, field_values={
            'author': self.user,
            'content_type': self.bill_ctype,
            'object_id': self.bill.id,
        }).create_one()
        bill = models.Bill.objects.get(pk=self.bill.id)
        self.assertEquals(bill.comments_count, 1)

    def test_update_comments_participation_count(self):
        segment = self.segment_fixture.create_one()
        AutoFixture(models.Comment, field_values={
            'author': self.user,
            'content_type': self.segment_ctype,
            'object_id': segment.id,
        }).create_one()
        segment = models.BillSegment.objects.get(pk=segment.id)
        self.assertEquals(segment.participation_count, 1)

    def test_update_additive_amendment_count(self):
        segment = self.segment_fixture.create_one()
        AutoFixture(models.AdditiveAmendment, field_values={
            'reference': segment}
        ).create_one()
        segment = models.BillSegment.objects.get(pk=segment.id)
        self.assertEquals(segment.amendments_count, 1)
        self.assertEquals(segment.participation_count, 1)
        self.assertEquals(segment.additive_amendments_count, 1)

        bill = models.Bill.objects.get(pk=self.bill.id)
        self.assertEquals(bill.amendments_count, 1)

    def test_update_modifier_amendment_count(self):
        segment = self.segment_fixture.create_one()
        AutoFixture(models.ModifierAmendment, field_values={
            'replaced': segment}
        ).create_one()
        segment = models.BillSegment.objects.get(pk=segment.id)
        self.assertEquals(segment.amendments_count, 1)
        self.assertEquals(segment.participation_count, 1)
        self.assertEquals(segment.modifier_amendments_count, 1)

        bill = models.Bill.objects.get(pk=self.bill.id)
        self.assertEquals(bill.amendments_count, 1)

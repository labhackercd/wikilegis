from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)


class TimestampedMixin(models.Model):
    created = models.DateTimeField(_('created'), editable=False,
                                   blank=True, auto_now_add=True)
    modified = models.DateTimeField(_('modified'), editable=False,
                                    blank=True, auto_now=True)

    class Meta:
        abstract = True


class VoteCountMixin(models.Model):
    votes = GenericRelation('UpDownVote', object_id_field="object_id")
    upvote_count = models.IntegerField(verbose_name=_("upvotes count"),
                                       default=0)
    downvote_count = models.IntegerField(verbose_name=_("downvotes count"),
                                         default=0)
    votes_count = models.IntegerField(verbose_name=_("votes count"),
                                      default=0)

    def save(self, *args, **kwargs):
        if self.upvote_count is None:
            self.upvote_count = 0

        if self.downvote_count is None:
            self.downvote_count = 0

        self.votes_count = self.upvote_count + self.downvote_count

        return super(VoteCountMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class CommentCountMixin(models.Model):
    comments = GenericRelation('Comment', object_id_field="object_id")
    comments_count = models.IntegerField(verbose_name=_("comments count"),
                                         default=0)

    def save(self, *args, **kwargs):
        if self.comments_count is None:
            self.comments_count = 0

        return super(CommentCountMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class ParticipationCountMixin(models.Model):
    participation_count = models.IntegerField(
        default=0, verbose_name=_("participations count"))

    def save(self, *args, **kwargs):
        if self.participation_count is None:
            self.participation_count = 0

        return super(ParticipationCountMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class AmendmentCountMixin(models.Model):
    amendments_count = models.IntegerField(verbose_name=_("amendments count"),
                                           default=0)

    def save(self, *args, **kwargs):
        if self.amendments_count is None:
            self.amendments_count = 0

        return super(AmendmentCountMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class GenericRelationMixin(models.Model):

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey('contenttypes.ContentType')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
        unique_together = ('object_id', 'content_type')


class SegmentMixin(TimestampedMixin, VoteCountMixin, CommentCountMixin,
                   ParticipationCountMixin):
    segment_type = models.ForeignKey('core.SegmentType',
                                     verbose_name=_('segment type'),
                                     null=True, blank=True,
                                     on_delete=models.SET_NULL)
    order = models.PositiveIntegerField(_('order'), default=0)
    number = models.IntegerField(_('number'), null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('order', )

    def bill_is_closed(self, segment_reference_field):
        segment = getattr(self, segment_reference_field)
        if segment_reference_field == 'bill':
            return segment.status == 'closed'
        return segment.bill.status == 'closed'

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

    class Meta:
        abstract = True


class CommentCountMixin(models.Model):
    comments = GenericRelation('Comment', object_id_field="object_id")
    comments_count = models.IntegerField(verbose_name=_("comments count"),
                                         default=0)

    class Meta:
        abstract = True


class ParticipationCountMixin(models.Model):
    participation_count = models.IntegerField(
        default=0, verbose_name=_("participations count"))

    class Meta:
        abstract = True


class AmendmentCountMixin(models.Model):
    amendments_count = models.IntegerField(verbose_name=_("amendments count"),
                                           default=0)

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
    number = models.CharField(_('number'), null=True,
                              blank=True, max_length=200)
    parent = models.ForeignKey('self', related_name='children',
                               verbose_name=_('segment parent'),
                               null=True, blank=True)
    content = models.TextField(_('content'))

    class Meta:
        abstract = True
        ordering = ('order', )

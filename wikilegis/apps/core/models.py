from django.contrib.contenttypes.fields import (GenericRelation,
                                                GenericForeignKey)
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

# Create your models here.


class BillStatus(models.Model):

    class Meta:
        verbose_name = _("Bill Status")
        verbose_name_plural = _("Bill Status")

    def __str__(self):
        return self.slug

    description = models.CharField(_('description'), max_length=50)
    slug = models.CharField(_('slug'), max_length=50)


class BillTheme(models.Model):

    class Meta:
        verbose_name = _("Bill Theme")
        verbose_name_plural = _("Bill Themes")

    def __str__(self):
        return self.slug

    description = models.CharField(_('description'), max_length=50)
    slug = models.CharField(_('slug'), max_length=50)


class TimestampedMixin(models.Model):
    created = models.DateTimeField(_('created'), editable=False,
                                   blank=True, auto_now_add=True)
    modified = models.DateTimeField(_('modified'), editable=False,
                                    blank=True, auto_now=True)

    class Meta:
        abstract = True


class Comment(TimestampedMixin):

    class Meta:
        verbose_name = "Segment Comment"
        verbose_name_plural = "Segment Comments"
        unique_together = ('object_id', 'content_type')

    def __str__(self):
        return self.text

    text = models.CharField(_("text"), max_length=500)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('author'), null=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey('contenttypes.ContentType')
    content_object = GenericForeignKey('content_type', 'object_id')


class Bill(TimestampedMixin):
    title = models.CharField(_('subject'), max_length=255)
    epigraph = models.CharField(_('epigraph'), max_length=255, null=True)
    description = models.TextField(_('description'))
    closing_date = models.DateField(_('closing date'))
    status = models.ForeignKey('BillStatus', verbose_name=_('status'))
    theme = models.ForeignKey('BillTheme', verbose_name=_('theme'))
    editors = models.ManyToManyField(
        'auth.Group', verbose_name=_('editors'), blank=True,
        help_text=_('Any users in any of these groups will '
                    'have permission to change this document.'))
    allowed_users = models.ManyToManyField(
        'auth.User', related_name='allowed_bills',
        verbose_name=_('allowed users'), blank=True)
    reporting_member = models.ForeignKey(
        'auth.User', verbose_name=_('reporting member'), null=True, blank=True)
    comments = GenericRelation('Comment', object_id_field="object_id")
    votes = GenericRelation('UpDownVote', object_id_field="object_id")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')


class BillSegment(TimestampedMixin):
    bill = models.ForeignKey('Bill', related_name='segments',
                             verbose_name=_('bill'))
    order = models.PositiveIntegerField(_('order'), default=0)
    segment_type = models.ForeignKey('SegmentType', verbose_name=_('type'),
                                     null=True, blank=True,
                                     on_delete=models.SET_NULL)
    number = models.CharField(_('number'), null=True,
                              blank=True, max_length=200)
    parent = models.ForeignKey('self', related_name='children',
                               verbose_name=_('segment parent'),
                               null=True, blank=True)
    replaced = models.ForeignKey('self', related_name='substitutes',
                                 verbose_name=_('segment replaced'),
                                 null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('author'), null=True)
    original = models.BooleanField(_('original'), default=True)
    content = models.TextField(_('content'))
    comments = GenericRelation('Comment', object_id_field="object_id")
    votes = GenericRelation('UpDownVote', object_id_field="object_id")

    class Meta:
        ordering = ('order',)
        verbose_name = _('segment')
        verbose_name_plural = _('segments')


class SegmentType(models.Model):
    name = models.CharField(_('name'), max_length=200)
    apresentation_name = models.CharField(
        _('apresentation name'), max_length=200, blank=True, null=True)
    editable = models.BooleanField(_('editable'), default='True')

    class Meta:
        verbose_name = _('Segment Type')
        verbose_name_plural = _('Segment Types')

    def __str__(self):
        return self.name


class UpDownVote(TimestampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey('contenttypes.ContentType')
    content_object = GenericForeignKey('content_type', 'object_id')
    vote = models.BooleanField(default=False,
                               choices=((True, _('Up Vote')),
                                        (False, _('Down Vote'))))

    class Meta:
        unique_together = ('user', 'object_id', 'content_type')

    def __unicode__(self):
        return self.user.get_full_name() or self.user.email

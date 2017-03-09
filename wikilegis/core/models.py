from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import slugify
from django.conf import settings
from core.model_mixins import (TimestampedMixin, VoteCountMixin, SegmentMixin,
                               GenericRelationMixin, CommentCountMixin,
                               AmendmentCountMixin)
from core.utils import references_filename, theme_icon_filename


BILL_STATUS_CHOICES = (
    ('draft', _('Draft')),
    ('published', _('Published')),
    ('closed', _('Closed'))
)


class BillTheme(models.Model):

    class Meta:
        verbose_name = _("Bill Theme")
        verbose_name_plural = _("Bill Themes")

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        return super(BillTheme, self).save(*args, **kwargs)

    description = models.CharField(_('description'),
                                   max_length=50, unique=True)
    slug = models.SlugField(_('slug'), max_length=50)
    icon = models.ImageField(upload_to=theme_icon_filename,
                             verbose_name=_('icon'), null=True, blank=True)


class Comment(TimestampedMixin, GenericRelationMixin):

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text

    text = models.CharField(_("text"), max_length=500)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('author'), null=True)


class Bill(TimestampedMixin, AmendmentCountMixin, VoteCountMixin,
           CommentCountMixin):
    title = models.CharField(_('subject'), max_length=255)
    epigraph = models.CharField(_('epigraph'), max_length=255, null=True)
    description = models.TextField(_('description'))
    closing_date = models.DateField(_('closing date'))
    status = models.CharField(_('status'), max_length=20,
                              choices=BILL_STATUS_CHOICES, default='1')
    is_visible = models.BooleanField(default=True, verbose_name=_('visible'))
    theme = models.ForeignKey('BillTheme', verbose_name=_('theme'))
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='allowed_bills',
        verbose_name=_('allowed users'), blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_visible is None:
            self.is_visible = True

        return super(Bill, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')


class BillVideo(models.Model):

    class Meta:
        verbose_name = "Bill Video"
        verbose_name_plural = "Bill Videos"

    def __str__(self):
        return self.url

    url = models.URLField(verbose_name=_('URL'))
    bill = models.ForeignKey('Bill', related_name='videos',
                             verbose_name=_('bill'))


class BillReference(models.Model):

    class Meta:
        verbose_name = "Bill Reference"
        verbose_name_plural = "Bill References"

    def __str__(self):
        return self.title

    title = models.CharField(max_length=50, verbose_name=_('title'))
    reference_file = models.FileField(upload_to=references_filename,
                                      verbose_name=_('reference file'),
                                      null=True)
    url = models.URLField(verbose_name=_('reference url'), null=True)
    bill = models.ForeignKey('Bill', verbose_name=_('bill'),
                             related_name='references')


class BillSegment(SegmentMixin, AmendmentCountMixin):
    bill = models.ForeignKey('core.Bill', related_name='segments',
                             verbose_name=_('bill'))
    parent = models.ForeignKey('self', related_name='children',
                               verbose_name=_('segment parent'),
                               null=True, blank=True)
    content = models.TextField(_('content'))
    additive_amendments_count = models.IntegerField(default=0)
    modifier_amendments_count = models.IntegerField(default=0)
    supress_amendments_count = models.IntegerField(default=0)

    def __str__(self):
        if self.number and self.segment_type:
            return '{kind} {number}'.format(
                kind=self.segment_type.name, number=self.number)
        else:
            return _('segment')

    def save(self, *args, **kwargs):
        if self.additive_amendments_count is None:
            self.additive_amendments_count = 0

        if self.modifier_amendments_count is None:
            self.modifier_amendments_count = 0

        if self.supress_amendments_count is None:
            self.supress_amendments_count = 0

        return super(BillSegment, self).save(*args, **kwargs)

    class Meta:
        ordering = ('order',)
        verbose_name = _('segment')
        verbose_name_plural = _('segments')


class AdditiveAmendment(SegmentMixin):
    content = models.TextField(_('content'))
    reference = models.ForeignKey('BillSegment', verbose_name=_('reference'),
                                  related_name="additive_amendments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('author'))

    class Meta:
        ordering = ('-votes_count',)


class ModifierAmendment(SegmentMixin):
    content = models.TextField(_('content'))
    replaced = models.ForeignKey('BillSegment', verbose_name=_('replaced'),
                                 related_name="modifier_amendments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('author'))

    class Meta:
        ordering = ('-votes_count',)


class SupressAmendment(SegmentMixin):
    content = models.TextField(_('content'))
    supressed = models.ForeignKey('BillSegment', verbose_name=_('supressed'),
                                  related_name="supress_amendments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=_('author'))

    class Meta:
        ordering = ('-votes_count',)


class SegmentType(models.Model):
    name = models.CharField(_('name'), max_length=200)
    presentation_name = models.CharField(_('presentation name'),
                                         max_length=200, blank=True, null=True)
    parents = models.ManyToManyField('self', related_name='children',
                                     verbose_name=_('parent type'),
                                     symmetrical=False)
    editable = models.BooleanField(_('editable'), default='True')

    class Meta:
        verbose_name = _('Segment Type')
        verbose_name_plural = _('Segment Types')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = slugify(self.presentation_name)
        return super(SegmentType, self).save(*args, **kwargs)


class UpDownVote(GenericRelationMixin, TimestampedMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'))
    vote = models.BooleanField(default=False, verbose_name=_('vote'),
                               choices=((True, _('Up Vote')),
                                        (False, _('Down Vote'))))

    class Meta:
        unique_together = ('user', 'object_id', 'content_type')

    def __str__(self):
        return self.user.get_full_name() or self.user.email

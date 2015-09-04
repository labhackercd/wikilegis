# -*- encoding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Bill(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class BillSegment(models.Model):
    bill = models.ForeignKey('core.Bill', related_name='segments')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    content = models.TextField()

    TYPE_CHOICES = (
        ('title', _('Title')),
        ('article', _('Article')),
    )
    type = models.CharField(max_length=64, choices=TYPE_CHOICES)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return '%s: %s' % (self.bill, self.content, )

    def is_editable(self):
        # Currently, only articles are editable.
        return self.type == 'article'


class CitizenAmendment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    segment = models.ForeignKey(BillSegment, related_name='amendments')
    content = models.TextField()
    comment = models.TextField()

    def original_content(self):
        return self.segment.content
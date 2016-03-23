# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wikilegis.core.models import TimestampedMixin


class HistoryNotification(models.Model):
    amendment = models.ForeignKey('core.BillSegment', verbose_name=_('amendment'))
    hour = models.DateTimeField(_('hour'), default=datetime.now)

    class Meta:
        ordering = ('-hour',)
        verbose_name = _('history notification')
        verbose_name_plural = _('history notifications')

    def __unicode__(self):
        return self.amendment.bill.title


class Newsletter(TimestampedMixin):
    PERIODICITY_CHOICES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly'))
    )

    bill = models.ForeignKey('core.Bill', verbose_name=_('bill'))
    user = models.ForeignKey('auth2.User', related_name='newsletters', verbose_name=_('user'))
    periodicity = models.CharField(_('periodicity'), max_length=20, choices=PERIODICITY_CHOICES, default='daily')
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        unique_together = ('user', 'bill')

    def __unicode__(self):
        return '{user} - {bill}'.format(user=self.user, bill=self.bill)

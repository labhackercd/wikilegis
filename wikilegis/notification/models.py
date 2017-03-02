from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from datetime import datetime
from core.model_mixins import TimestampedMixin


class HistoryNotification(models.Model):
    amendment = models.ForeignKey('core.BillSegment',
                                  verbose_name=_('amendment'))
    hour = models.DateTimeField(_('hour'), default=datetime.now)

    class Meta:
        ordering = ('-hour',)
        verbose_name = _('history notification')
        verbose_name_plural = _('history notifications')

    def __str__(self):
        return self.amendment.bill.title


class Newsletter(TimestampedMixin):
    PERIODICITY_CHOICES = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly'))
    )

    bill = models.ForeignKey('core.Bill', verbose_name=_('bill'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='newsletters',
                             verbose_name=_('user'))
    periodicity = models.CharField(_('periodicity'), max_length=20,
                                   choices=PERIODICITY_CHOICES,
                                   default='daily')
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        unique_together = ('user', 'bill')

    def __str__(self):
        return '{user} - {bill}'.format(user=self.user, bill=self.bill)

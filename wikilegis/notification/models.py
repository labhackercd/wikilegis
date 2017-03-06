from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from core.model_mixins import TimestampedMixin


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
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        unique_together = ('user', 'bill')

    def __str__(self):
        return '{user} - {bill}'.format(user=self.user, bill=self.bill)

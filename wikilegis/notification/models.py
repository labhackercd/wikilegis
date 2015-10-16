from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import Truncator


class HistoryNotification(models.Model):
    bill = models.ForeignKey('core.Bill', verbose_name=_('bill'))
    hour = models.DateTimeField(_('hour'), default=datetime.now)

    class Meta:
        ordering = ('-hour',)
        verbose_name = _('history notification')
        verbose_name_plural = _('history notifications')

    def __unicode__(self):
        return '{bill}: {content}'.format(
            bill=self.bill, content=Truncator(self.content).chars(100))
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _


class HistoryNotification(models.Model):
    amendment = models.ForeignKey('core.BillSegment', verbose_name=_('amendment'))
    hour = models.DateTimeField(_('hour'), default=datetime.now)

    class Meta:
        ordering = ('-hour',)
        verbose_name = _('history notification')
        verbose_name_plural = _('history notifications')

    def __unicode__(self):
        return self.amendment.bill.title

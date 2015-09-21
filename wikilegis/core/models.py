# -*- encoding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Bill(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.title


class BillSegment(models.Model):
    bill = models.ForeignKey('core.Bill', related_name='segments', verbose_name="Bill")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    content = models.TextField()

    TYPE_CHOICES = (
        ('title', _(u'Title')),
        ('article', _(u'Article')),
    )
    type = models.CharField(max_length=64, choices=TYPE_CHOICES)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return u'%s: %s' % (self.bill, self.content)

    def is_editable(self):
        # Currently, only articles are editable.
        return self.type == 'article'


class CitizenAmendment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    segment = models.ForeignKey('core.BillSegment', related_name='amendments', verbose_name="BillSegment")
    content = models.TextField()
    comment = models.TextField(null=True, blank=True)

    def original_content(self):
        return self.segment.content


class CitizenComment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    segment = models.ForeignKey('core.BillSegment', related_name='comments', verbose_name="Comment")
    comment = models.TextField()

    def original_content(self):
        return self.segment.content


class UserSegmentChoice(models.Model):
    """
    Modelo que indica a "escolha" de um usuário por uma "vesrão" de um trecho do projeto de lei.

    1. Se `segment is None`, então o usuário votou no texto original.
    2. Se `segment` for algum sement, então o usuário votou naquela versão do texto.
    3. Se não existir um voto tal que `user=user, segment__bill__id=bill.id`, então significa que o usuário não votou ainda.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    segment = models.ForeignKey('core.BillSegment', related_name='choices', verbose_name="choices")
    amendment = models.ForeignKey('core.CitizenAmendment', related_name='choosings', null=True, blank=True, verbose_name="choosings")


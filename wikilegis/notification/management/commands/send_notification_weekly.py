# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, timedelta

from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from wikilegis import settings
from wikilegis.auth2.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain + settings.FORCE_SCRIPT_NAME
        users = User.objects.filter(newsletters__isnull=False, newsletters__periodicity='weekly').distinct()
        bill_proposals = defaultdict(list)
        for user in users:
            for newsletter in user.newsletters.all():
                for segment in newsletter.bill.segments.filter(modified__gte=datetime.now()-timedelta(days=7), original=False):
                    bill_proposals[newsletter.bill].append(segment)
            if bill_proposals:
                html = render_to_string('notification/bill_notification.html',
                                        {'domain': domain,
                                         'proposals': dict(bill_proposals)})
                subject = u'[Wikilegis] Notificação Semanal'
                mail = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [user.email])
                mail.attach_alternative(html, 'text/html')
                mail.send()

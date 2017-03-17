from collections import defaultdict
from datetime import datetime, timedelta
from itertools import chain

from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--periodicity',
            dest='periodicity',
        )

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        if settings.FORCE_SCRIPT_NAME:
            domain += settings.FORCE_SCRIPT_NAME
        users = get_user_model().objects.filter(
            newsletters__isnull=False,
            newsletters__periodicity=options['periodicity']).distinct()
        bill_proposals = defaultdict(list)
        for user in users:
            newsletters = user.newsletters.filter(bill__status='published')
            for newsletter in newsletters:
                for segment in newsletter.bill.segments.all():
                    if options['periodicity'] == 'daily':
                        additives = segment.additive_amendments.filter(
                            modified__gte=datetime.now() - timedelta(days=1))
                        modified = segment.modifier_amendments.filter(
                            modified__gte=datetime.now() - timedelta(days=1))
                        supressed = segment.supress_amendments.filter(
                            modified__gte=datetime.now() - timedelta(days=1))
                    elif options['periodicity'] == 'weekly':
                        additives = segment.additive_amendments.filter(
                            modified__gte=datetime.now() - timedelta(days=7))
                        modified = segment.modifier_amendments.filter(
                            modified__gte=datetime.now() - timedelta(days=7))
                        supressed = segment.supress_amendments.filter(
                            modified__gte=datetime.now() - timedelta(days=7))
                    amendments = list(chain(additives, modified, supressed))
                    if len(amendments) > 0:
                        bill_proposals[newsletter.bill].append(
                            {segment: amendments})

            if bill_proposals:
                html = render_to_string('email/newsletter.html',
                                        {'domain': domain,
                                         'proposals': dict(bill_proposals)})
                subject = u'[Wikilegis] Notificação '
                if options['periodicity'] == 'daily':
                    subject += u'Diária'
                elif options['periodicity'] == 'weekly':
                    subject += u'Semanal'
                mail = EmailMultiAlternatives(subject, '',
                                              settings.EMAIL_HOST_USER,
                                              [user.email])
                mail.attach_alternative(html, 'text/html')
                mail.send()

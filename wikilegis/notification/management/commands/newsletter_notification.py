from collections import defaultdict
from datetime import datetime, timedelta

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
            for newsletter in user.newsletters.filter(bill__status='published'):
                for segment in newsletter.bill.segments.all():
                    additive_amendments = segment.additive_amendments.filter(
                        modified__gte=datetime.now() - timedelta(days=1))
                    modifier_amendments = segment.modifier_amendments.filter(
                        modified__gte=datetime.now() - timedelta(days=1))
                    supress_amendments = segment.supress_amendments.filter(
                        modified__gte=datetime.now() - timedelta(days=1))
                    if (additive_amendments or modifier_amendments or
                            supress_amendments):
                        bill_proposals[newsletter.bill].append(segment)
            # Need html to newsletter
            if bill_proposals:
                html = render_to_string('',  # Add template directory here
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

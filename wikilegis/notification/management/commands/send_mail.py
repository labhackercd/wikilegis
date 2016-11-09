# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_comments.models import Comment
from django.conf import settings
from wikilegis.core.models import Bill, UpDownVote, BillSegment
from wikilegis.notification.models import HistoryNotification


class Command(BaseCommand):
    def handle(self, *args, **options):
        bills = Bill.objects.filter(status='published')
        domain = Site.objects.get_current().domain + settings.FORCE_SCRIPT_NAME
        for bill in bills:
            segment_amendments = defaultdict(list)
            amendment_comments = defaultdict(list)
            top_amendments = []
            segment_ctype = ContentType.objects.get_for_model(BillSegment)
            for segment in bill.segments.filter(original=True):
                up_votes_segment = UpDownVote.objects.filter(content_type=segment_ctype, object_id=segment.id,
                                                             vote=True).count()
                down_votes_segment = UpDownVote.objects.filter(content_type=segment_ctype, object_id=segment.id,
                                                               vote=False).count()
                score_segment = up_votes_segment - down_votes_segment
                for amendment in segment.substitutes.all():
                    votes_amendment = UpDownVote.objects.filter(content_type=segment_ctype, object_id=amendment.pk)
                    try:
                        last_email = HistoryNotification.objects.get(amendment=amendment)
                        if votes_amendment:
                            up_votes_amendment = votes_amendment.filter(vote=True).count()
                            down_votes_amendment = votes_amendment.filter(vote=False).count()
                            score_amendment = up_votes_amendment - down_votes_amendment
                            last_vote = votes_amendment.latest('modified')
                            if last_email.hour < last_vote.modified:
                                if score_amendment > score_segment:
                                    top_amendments.append(amendment.id)
                        comments = Comment.objects.filter(object_pk=amendment.pk,
                                                          content_type=segment_ctype,
                                                          submit_date__gte=last_email.hour)
                        if comments:
                            for comment in comments:
                                amendment_comments[amendment].append(comment)
                            last_email.hour = datetime.now()
                            last_email.save()
                    except HistoryNotification.DoesNotExist:
                        segment_amendments[segment].append(amendment)
                        comments = Comment.objects.filter(object_pk=amendment.pk,
                                                          content_type=segment_ctype)
                        history = HistoryNotification()
                        history.amendment = amendment
                        history.hour = datetime.now()
                        if comments:
                            for comment in comments:
                                amendment_comments[amendment].append(comment)
                                history.hour = datetime.now()
                        history.save()
                        if votes_amendment:
                            up_votes_amendment = votes_amendment.filter(vote=True).count()
                            down_votes_amendment = votes_amendment.filter(vote=False).count()
                            score_amendment = up_votes_amendment - down_votes_amendment
                            if score_amendment > score_segment:
                                top_amendments.append(amendment.id)
            if segment_amendments or amendment_comments or top_amendments:
                try:
                    proposition = bill.proposition_set.all()[0].name_proposition
                except:
                    proposition = ''
                html = render_to_string('notification/notification_email.html',
                                        {'domain': domain, 'bill': bill.title,
                                         'amendments': dict(segment_amendments),
                                         'comments': dict(amendment_comments),
                                         'proposition': proposition,
                                         'top_amendments': BillSegment.objects.filter(id__in=top_amendments)})
                email_list = ['wikilegis@camara.leg.br']
                subject = u'[Wikilegis] Atualizações ao %s %s' % (bill.title, proposition)
                for editor in bill.editors.all():
                    for user in editor.user_set.all():
                        email_list.append(user.email)
                mail = EmailMultiAlternatives(subject, '', '', '', bcc=email_list)
                mail.attach_alternative(html, 'text/html')
                mail.send()

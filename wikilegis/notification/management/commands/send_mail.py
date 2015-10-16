# -*- coding: utf-8 -*-
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from wikilegis.auth2.models import User
from wikilegis.core.models import Bill, BillSegment
from wikilegis.notification.models import HistoryNotification


class Command(BaseCommand):
    def handle(self, *args, **options):
        bills = Bill.objects.all()

        for bill in bills:
            try:
                last_email = HistoryNotification.objects.filter(bill=bill).order_by('-hour')[0]
            except:
                last_email = ''

            if last_email:
                segments = BillSegment.objects.filter(bill=bill, modified__gt=last_email).order_by('-modified')
            else:
                segments = BillSegment.objects.filter(bill=bill).order_by('-modified')

            html = render_to_string('notification/notification_email.html', {'segments': segments})
            superusers = User.objects.filter(is_superuser=True)
            email_list = list()

            for superuser in superusers:
                email_list.append(superuser.email)
            for editor in bill.editors.all():
                for user in editor.user_set.all():
                    email_list.append(user.email)

            mail = EmailMultiAlternatives('Notificações - Wikilegis', '', 'erivanio.vasconcelos@gmail.com', email_list)
            mail.attach_alternative(html, 'text/html')
            sent = mail.send()

            if sent:
                history = HistoryNotification()
                history.bill = bill
                history.hour = datetime.now()
                history.save()
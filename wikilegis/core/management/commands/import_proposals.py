from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from wikilegis.core.models import BillSegment
from django_comments.models import Comment
import csv

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            dest='file',
        )

    def handle(self, *args, **options):
        proposals = csv.DictReader(open(options['file'], 'rt'))
        for i in proposals:
            user = User.objects.get_or_create(email=i['email'])[0]
            segment = BillSegment.objects.get(
                content__startswith=i['artigo'], original=True
            )
            proposal = BillSegment.objects.get_or_create(
                bill=segment.bill, replaced=segment, content=i['sugestao'],
                original=False, type=segment.type, author=user
            )[0]
            segment_ctype = ContentType.objects.get_for_model(BillSegment)
            if i['justificativa']:
                comment = Comment.objects.get_or_create(
                    content_type=segment_ctype, object_pk=proposal.id, user=user,
                    comment=i['justificativa'], site_id=settings.SITE_ID
                )

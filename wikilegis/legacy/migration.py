from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from core import models
from legacy import models as legacy_models
from json import loads
import abc
import click


class BaseMigration(object):

    def __new__(cls):
        for field in cls.model._meta.fields:
            def _method(self, data, legacy_instance):
                return data
            if not hasattr(cls, 'clean_' + field.name):
                setattr(cls, 'clean_' + field.name, _method)
        return super(BaseMigration, cls).__new__(cls)

    @abc.abstractmethod
    def get_data(self):
        return

    def get_label(self):
        return 'Importing data'

    def pre_save(self, obj, legacy_instance):
        pass

    def post_save(self, obj, legacy_instance):
        pass

    @transaction.atomic
    def import_data(self):
        legacy_data = self.get_data()
        with click.progressbar(legacy_data, label=self._get_label()) as data:
            for legacy_instance in data:
                obj = self._get_object(legacy_instance)
                self.pre_save(obj, legacy_instance)
                obj.save()
                self.post_save(obj, legacy_instance)

    def _get_label(self):
        return self.get_label().ljust(50)

    def _get_object(self, legacy_instance):
        obj = self.model()
        for field in self.model._meta.fields:
            try:
                clean_method = getattr(self, 'clean_' + field.name)
                cleaned_field = clean_method(
                    getattr(legacy_instance, field.name, None),
                    legacy_instance=legacy_instance)
                setattr(obj, field.name, cleaned_field)
            except AttributeError:
                continue
        return obj


class UserMigration(BaseMigration):

    model = get_user_model()

    def get_data(self):
        return legacy_models.Auth2User.objects.using('legacy').all()

    def get_label(self):
        return 'Importing users'


class BillMigration(BaseMigration):

    model = models.Bill

    def get_data(self):
        return legacy_models.CoreBill.objects.using('legacy').all()

    def get_label(self):
        return 'Importing bills'

    def clean_theme(self, data, legacy_instance):
        return models.BillTheme.objects.get_or_create(description=data)[0]

    def clean_reporting_member(self, data, legacy_instance):
        if data is not None:
            return get_user_model.objects.get(pk=data.id)
        else:
            return None


class BillReferenceMigration(BaseMigration):
    model = models.BillReference

    def get_data(self):
        return legacy_models.CoreBillreference.objects.using('legacy').all()

    def get_label(self):
        return 'Importing bill references'

    def clean_bill(self, data, legacy_instance):
        return models.Bill.objects.get(pk=data.id)

    def clean_title(self, data, legacy_instance):
        return legacy_instance.name

    def clean_reference_file(self, data, legacy_instance):
        return legacy_instance.file


class BillVideoMigration(BaseMigration):
    model = models.BillVideo

    def get_data(self):
        return legacy_models.CoreGenericdata.objects.using('legacy').filter(
            type='VIDEO'
        )

    def get_label(self):
        return 'Importing bill videos'

    def clean_url(self, data, legacy_instance):
        json = loads(legacy_instance.data)
        return json['url']

    def clean_bill(self, data, legacy_instance):
        return models.Bill.objects.get(pk=legacy_instance.object_id)


class SegmentTypeMigration(BaseMigration):
    model = models.SegmentType

    def get_data(self):
        return legacy_models.CoreTypesegment.objects.using('legacy').all()

    def get_label(self):
        return 'Importing segment types'

    def clean_presentation_name(self, data, legacy_instance):
        return legacy_instance.name


class BillSegmentMigration(BaseMigration):
    model = models.BillSegment

    def get_data(self):
        return legacy_models.CoreBillsegment.objects.using('legacy').filter(
            original=True
        ).order_by('order')

    def get_label(self):
        return 'Importing bill segments'

    def clean_bill(self, data, legacy_instance):
        return models.Bill.objects.get(pk=data.id)

    def clean_segment_type(self, data, legacy_instance):
        return models.SegmentType.objects.get(pk=data.id)

    def clean_parent(self, data, legacy_instance):
        if legacy_instance.parent is not None:
            return models.BillSegment.objects.get(pk=data.id)
        else:
            return None


class ModifierAmendmentMigration(BillSegmentMigration):
    model = models.ModifierAmendment

    def get_data(self):
        return legacy_models.CoreBillsegment.objects.using('legacy').filter(
            original=False
        ).order_by('order')

    def get_label(self):
        return 'Importing modifier amendments'

    def clean_replaced(self, data, legacy_instance):
        return models.BillSegment.objects.get(pk=data.id)

    def clean_author(self, data, legacy_instance):
        return get_user_model().objects.get(pk=data.id)


class CommentMigration(BaseMigration):
    model = models.Comment

    def get_data(self):
        return legacy_models.DjangoComments.objects.using('legacy')

    def get_label(self):
        return 'Importing comments'

    def clean_text(self, data, legacy_instance):
        return legacy_instance.comment

    def clean_author(self, data, legacy_instance):
        return get_user_model().objects.get(pk=legacy_instance.user.id)

    def clean_content_type(self, data, legacy_instance):
        try:
            models.BillSegment.objects.get(pk=legacy_instance.object_pk)
            return ContentType.objects.get(app_label='core',
                                           model='billsegment')
        except models.BillSegment.DoesNotExist:
            models.ModifierAmendment.objects.get(pk=legacy_instance.object_pk)
            return ContentType.objects.get(app_label='core',
                                           model='modifieramendment')

    def clean_object_id(self, data, legacy_instance):
        return legacy_instance.object_pk

    def clean_created(self, data, legacy_instance):
        return legacy_instance.submit_date


class VotesMigration(BaseMigration):
    model = models.UpDownVote

    def get_data(self):
        return legacy_models.CoreUpdownvote.objects.using('legacy').all()

    def get_label(self):
        return 'Importing votes'

    def clean_content_type(self, data, legacy_instance):
        if data.model == 'billsegment':
            try:
                models.BillSegment.objects.get(pk=legacy_instance.object_id)
                ctype = ContentType.objects.get(app_label='core',
                                                model='billsegment')
            except models.BillSegment.DoesNotExist:
                models.ModifierAmendment.objects.get(
                    pk=legacy_instance.object_id
                )
                ctype = ContentType.objects.get(app_label='core',
                                                model='modifieramendment')
        elif data.model == 'bill':
            ctype = ContentType.objects.get(app_label='core',
                                            model='bill')
        return ctype

    def clean_user(self, data, legacy_instance):
        return get_user_model().objects.get(pk=legacy_instance.user.id)


def import_data():
    UserMigration().import_data()
    BillMigration().import_data()
    BillReferenceMigration().import_data()
    BillVideoMigration().import_data()
    SegmentTypeMigration().import_data()
    BillSegmentMigration().import_data()
    ModifierAmendmentMigration().import_data()
    CommentMigration().import_data()
    VotesMigration().import_data()

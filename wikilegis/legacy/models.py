# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create,
#     modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or
# field names.
from __future__ import unicode_literals

from django.db import models


class Auth2Congressman(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    uf = models.CharField(max_length=200, blank=True, null=True)
    party = models.CharField(max_length=200, blank=True, null=True)
    parliamentary_name = models.CharField(max_length=200, blank=True,
                                          null=True)
    user = models.ForeignKey('Auth2User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth2_congressman'


class Auth2User(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    email = models.CharField(unique=True, max_length=254)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    avatar = models.CharField(max_length=100, blank=True, null=True)
    cropping = models.CharField(max_length=255)
    id_congressman = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth2_user'


class Auth2UserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(Auth2User, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth2_user_groups'
        unique_together = (('user', 'group'),)


class Auth2UserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(Auth2User, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth2_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.ForeignKey(Auth2User, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class CoreBill(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    theme = models.CharField(max_length=255)
    epigraph = models.CharField(max_length=255, blank=True, null=True)
    reporting_member = models.ForeignKey(Auth2User, models.DO_NOTHING,
                                         blank=True, null=True)
    closing_date = models.DateField()
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'core_bill'


class CoreBillAllowedUsers(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    bill = models.ForeignKey(CoreBill, models.DO_NOTHING)
    user = models.ForeignKey(Auth2User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_bill_allowed_users'
        unique_together = (('bill', 'user'),)


class CoreBillEditors(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    bill = models.ForeignKey(CoreBill, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_bill_editors'
        unique_together = (('bill', 'group'),)


class CoreBillreference(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    name = models.CharField(max_length=200, blank=True, null=True)
    bill = models.ForeignKey(CoreBill, models.DO_NOTHING)
    file = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'core_billreference'


class CoreBillsegment(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    order = models.PositiveIntegerField()
    content = models.TextField()
    bill = models.ForeignKey(CoreBill, models.DO_NOTHING)
    author = models.ForeignKey(Auth2User, models.DO_NOTHING,
                               blank=True, null=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    original = models.BooleanField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True,
                               related_name='children', null=True)
    replaced = models.ForeignKey('self', models.DO_NOTHING, blank=True,
                                 related_name='substitutes', null=True)
    type = models.ForeignKey('CoreTypesegment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_billsegment'


class CoreGenericdata(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    data = models.TextField()
    type = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'core_genericdata'


class CoreProposition(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    type = models.CharField(max_length=200, blank=True, null=True)
    number = models.CharField(max_length=50, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    name_proposition = models.CharField(max_length=200, blank=True, null=True)
    id_proposition = models.IntegerField(blank=True, null=True)
    id_main_proposition = models.IntegerField(blank=True, null=True)
    name_origin_proposition = models.CharField(max_length=200,
                                               blank=True, null=True)
    theme = models.CharField(max_length=200, blank=True, null=True)
    menu = models.TextField(blank=True, null=True)
    menu_explanation = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    id_register = models.CharField(max_length=200, blank=True, null=True)
    uf_author = models.CharField(max_length=200, blank=True, null=True)
    party_author = models.CharField(max_length=200, blank=True, null=True)
    apresentation_date = models.DateField(blank=True, null=True)
    processing_regime = models.CharField(max_length=200, blank=True, null=True)
    last_dispatch_date = models.DateField(blank=True, null=True)
    last_dispatch = models.TextField(blank=True, null=True)
    appraisal = models.TextField(blank=True, null=True)
    situation = models.CharField(max_length=200, blank=True, null=True)
    content_link = models.CharField(max_length=200, blank=True, null=True)
    bill = models.ForeignKey(CoreBill, models.DO_NOTHING)
    indexing = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'core_proposition'


class CoreTypesegment(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=200)
    editable = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'core_typesegment'


class CoreUpdownvote(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    user = models.ForeignKey(Auth2User, models.DO_NOTHING)
    vote = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'core_updownvote'
        unique_together = (('user', 'object_id', 'content_type'),)


class CorsheadersCorsmodel(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    cors = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'corsheaders_corsmodel'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING,
                                     blank=True, null=True)
    user = models.ForeignKey(Auth2User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCommentFlags(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    flag = models.CharField(max_length=30)
    flag_date = models.DateTimeField()
    comment = models.ForeignKey('DjangoComments', models.DO_NOTHING)
    user = models.ForeignKey(Auth2User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_comment_flags'
        unique_together = (('user', 'comment', 'flag'),)


class DjangoComments(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_pk = models.TextField()
    user_name = models.CharField(max_length=50)
    user_url = models.CharField(max_length=200)
    comment = models.TextField()
    submit_date = models.DateTimeField()
    ip_address = models.CharField(max_length=39, blank=True, null=True)
    is_public = models.BooleanField()
    is_removed = models.BooleanField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    site = models.ForeignKey('DjangoSite', models.DO_NOTHING)
    user = models.ForeignKey(Auth2User, models.DO_NOTHING,
                             blank=True, null=True)
    user_email = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'django_comments'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class EasyThumbnailsSource(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    storage_hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    modified = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_source'
        unique_together = (('storage_hash', 'name'),)


class EasyThumbnailsThumbnail(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    storage_hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    modified = models.DateTimeField()
    source = models.ForeignKey(EasyThumbnailsSource, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_thumbnail'
        unique_together = (('storage_hash', 'name', 'source'),)


class EasyThumbnailsThumbnaildimensions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    thumbnail = models.ForeignKey(EasyThumbnailsThumbnail,
                                  models.DO_NOTHING, unique=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'easy_thumbnails_thumbnaildimensions'


class NotificationHistorynotification(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    hour = models.DateTimeField()
    amendment = models.ForeignKey(CoreBillsegment, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'notification_historynotification'


class NotificationNewsletter(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    created = models.DateTimeField()
    modified = models.DateTimeField()
    periodicity = models.CharField(max_length=20)
    status = models.BooleanField()
    bill = models.ForeignKey(CoreBill, models.DO_NOTHING)
    user = models.ForeignKey(Auth2User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'notification_newsletter'
        unique_together = (('user', 'bill'),)


class RegistrationRegistrationprofile(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    activation_key = models.CharField(max_length=40)
    user = models.ForeignKey(Auth2User, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'registration_registrationprofile'


class SocialAuthAssociation(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'social_auth_association'


class SocialAuthCode(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    code = models.CharField(max_length=32)
    verified = models.BooleanField()
    email = models.CharField(max_length=254)

    class Meta:
        managed = False
        db_table = 'social_auth_code'
        unique_together = (('email', 'code'),)


class SocialAuthNonce(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'social_auth_nonce'
        unique_together = (('server_url', 'timestamp', 'salt'),)


class SocialAuthUsersocialauth(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()
    user = models.ForeignKey(Auth2User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'
        unique_together = (('provider', 'uid'),)

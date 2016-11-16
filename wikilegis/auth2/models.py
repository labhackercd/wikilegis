# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db.models import permalink
from image_cropping import ImageCropField, ImageRatioField
from django import forms


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


def sizeof_fmt(num, suffix='B'):
    """
    Shamelessly copied from StackOverflow:
    http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size

    :param num:
    :param suffix:
    :return:
    """
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def avatar_validation(image):
    if image:
        # 10 MB
        max_file_size = 10 * 1024 * 1024
        if image.size > max_file_size:
            raise forms.ValidationError(
                ugettext('The maximum file size is {0}').format(sizeof_fmt(max_file_size)))


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    avatar = ImageCropField(_('profile picture'), upload_to="avatars/",
                            validators=[avatar_validation], null=True, blank=True)
    cropping = ImageRatioField('avatar', '70x70', help_text=_(
        'Note that the preview above will only be updated after you submit the form.'))

    # XXX This was not supposed to be here.
    # This field and all the logic and subsystems associated with it
    # should belong to a plugin or something. It should be a separate,
    # optional component.
    id_congressman = models.CharField(
        _('Congressman ID'), max_length=30, null=True, blank=True,
        help_text=_("The id of each congressman may be found in the url parameters in the"
                    "congressman profile from the site: http://www2.camara.leg.br/"))

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta(AbstractBaseUser.Meta):
        abstract = False

    def __unicode__(self):
        return self.get_display_name()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return ' '.join([self.first_name, self.last_name]).strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_email_name(self):
        return self.email.split('@')[0]

    def get_display_name(self):
        return self.get_full_name() or self.get_email_name()

    @permalink
    def get_absolute_url(self):
        return 'users_profile', [self.pk], {}


class Congressman(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"))
    uf = models.CharField(_('uf'), max_length=200, null=True, blank=True)
    party = models.CharField(_('party'), max_length=200, null=True, blank=True)
    parliamentary_name = models.CharField(verbose_name=_("parliamentary name"), max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = _('congressman')
        verbose_name_plural = _('congressmen')

    def __unicode__(self):
        return self.user.get_full_name() or self.user.email

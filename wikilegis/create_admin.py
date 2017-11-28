import django
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wikilegis.settings.wikilegis")


def create_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()

    admin_email = os.environ.get('ADMIN_EMAIL', None)
    admin_passwd = os.environ.get('ADMIN_PASSWORD', None)

    if None not in [admin_email, admin_passwd]:
        print('Creating superuser...')
        user = User.objects.get_or_create(email=admin_email)[0]
        user.set_password(admin_passwd)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print('Done!')
    else:
        print('Missing ADMIN_EMAIL or ADMIN_PASSWORD environment variable.')
        sys.exit(1)


def update_sites():
    from django.contrib.sites.models import Site
    import re
    site = Site.objects.get_current()
    site_domain = os.environ.get('SITE_DOMAIN', None)
    site_name = os.environ.get('SITE_NAME', None)

    if None not in [site_domain, site_name]:
        print('Updating site infos...')
        site_domain = re.sub('^(http|https)://', '', site_domain)

        site.domain, site.name = site_domain, site_name
        site.save()
        print('Done!')
    else:
        print('Missing SITE_DOMAIN or SITE_NAME environment variable.')
        sys.exit(2)


if __name__ == '__main__':
    django.setup()
    create_superuser()
    update_sites()

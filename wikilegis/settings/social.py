from django.utils.translation import ugettext_lazy as _


SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

# We just want the *social user*'s email. Not the username.
# This is used by `social.pipeline.user.create_user` to create the user.
# Since our user has no username, we have to remove it from the list.
USER_FIELDS = ('email',)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,first_name,last_name,email'
}

SOCIAL_BACKEND_INFO = {
    'google-oauth2': {
        'title': _('Google'),
        'icon': 'img/sa-google-icon.png',
    },
    'facebook': {
        'title': _('Facebook'),
        'icon': 'img/sa-facebook-icon.png',
    }
}

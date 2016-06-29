import requests
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from image_cropping import ImageCropWidget
from image_cropping.widgets import CropWidget
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from wikilegis.auth2.models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('email',)


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User

    def clean(self):
        if self.data['id_congressman']:
            params = {'ideCadastro': self.data['id_congressman'], 'numLegislatura': ''}
            response = requests.get('http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDetalhesDeputado',
                                    params=params)
            if response.status_code == 500:
                self.add_error('id_congressman', _('ID not found.'))
                raise ValidationError(_('No congressman found with this id.'))
        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('email', 'first_name', 'last_name')


class CustomImageCropWidget(ImageCropWidget):
    """
    Custom ImageCropWidget that doesn't show the initial value of the field.
    We use this trick, and place it right under the CropWidget so that
    it looks like the user is seeing the image and clearing the image.
    """

    template_with_initial = (
        # '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )


class UserProfileEditionForm(BaseUserChangeForm):
    # We don't have a password field
    password = None

    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'cropping')
        widgets = {
            'avatar': CustomImageCropWidget(),
            'cropping': CropWidget(),
        }

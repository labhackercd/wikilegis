from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from django import forms
from django.forms import ModelForm
from image_cropping import ImageCropWidget
from wikilegis.auth2.models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('email',)


class UserChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        model = User


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('email', 'first_name', 'last_name')


class EditProfile(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'cropping']
        widgets = {
            'cropping': ImageCropWidget(),
        }
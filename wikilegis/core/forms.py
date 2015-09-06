from django import forms
from django.contrib.auth.forms import UserCreationForm
from wikilegis.core.models import CitizenAmendment


class CitizenAmendmentCreationForm(forms.ModelForm):

    class Meta:
        model = CitizenAmendment
        fields = ('content', 'comment')


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'username')

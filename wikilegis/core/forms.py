from django import forms
from wikilegis.core.models import CitizenAmendment


class CitizenAmendmentCreationForm(forms.ModelForm):
    class Meta:
        model = CitizenAmendment
        fields = ('content', 'comment')

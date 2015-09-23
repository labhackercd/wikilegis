from django import forms
from wikilegis.core.models import CitizenAmendment


class CitizenAmendmentCreationForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = CitizenAmendment
        fields = ('content',)

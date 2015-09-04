from django.forms import ModelForm
from wikilegis.core.models import CitizenAmendment


class CitizenAmendmentCreationForm(ModelForm):

    class Meta:
        model = CitizenAmendment
        fields = ('content', 'comment')

from django import forms
from wikilegis.core.models import CitizenAmendment, Bill


class BillAdminForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'

    def __init__(self, user, *args, **kwargs):
        super(BillAdminForm, self).__init__(*args, **kwargs)
        self.user = user
        if not self.user.is_superuser:
            groups = self.fields['groups']
            groups.queryset = groups.queryset.filter(pk__in=user.groups.filter())
            if groups.queryset.count() == 1:
                groups.initial = groups.queryset.all()
                groups.required = True

    def save(self, commit=True):
        bill = super(BillAdminForm, self).save(commit=False)
        if not self.user.is_superuser and len(self.user.groups) == 1:
            bill.groups = self.user.groups
        return bill


class CitizenAmendmentCreationForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = CitizenAmendment
        fields = ('content',)


from django.contrib import admin
from plugins.camara_deputados import models, forms
from plugins.camara_deputados.import_file import import_txt


class BillInfoAdmin(admin.ModelAdmin):
    list_display = ('bill', 'proposal_type', 'proposal_number',
                    'proposal_year', 'situation')
    readonly_fields = ('author', 'situation')
    form = forms.BillInfoAdminForm

    def save_form(self, request, form, change):
        bill_info = form.save(commit=False)
        try:
            import_txt(form.files['file_txt'], bill_info.bill.id)
        except:
            pass
        return form.save(commit=False)


class ProposalTypeAdmin(admin.ModelAdmin):
    list_display = ('initials', 'description')
    list_filter = ('initials',)
    search_fields = ('initials',)


admin.site.register(models.ProposalType, ProposalTypeAdmin)
admin.site.register(models.BillInfo, BillInfoAdmin)

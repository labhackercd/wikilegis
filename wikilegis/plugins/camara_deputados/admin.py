from django.contrib import admin
from plugins.camara_deputados import models


class BillInfoAdmin(admin.ModelAdmin):
    list_display = ('bill', 'proposal_type', 'proposal_number',
                    'proposal_year', 'situation')
    readonly_fields = ('author',)


class ProposalTypeAdmin(admin.ModelAdmin):
    list_display = ('initials', 'description')
    list_filter = ('initials',)
    search_fields = ('initials',)


admin.site.register(models.ProposalType, ProposalTypeAdmin)
admin.site.register(models.BillInfo, BillInfoAdmin)

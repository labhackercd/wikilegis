from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from . import models


class BillSegmentInline(SortableInlineAdminMixin, admin.TabularInline):
    model = models.BillSegment


class BillAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = (BillSegmentInline,)


class CitizenAmendmentAdmin(admin.ModelAdmin):
    list_display = ('author', 'segment', 'original_content', 'content')


admin.site.register(models.Bill, BillAdmin)
admin.site.register(models.CitizenAmendment, CitizenAmendmentAdmin)

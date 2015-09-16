from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from . import models


class BillSegmentInline(SortableInlineAdminMixin, admin.TabularInline):
    model = models.BillSegment


class BillAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = (BillSegmentInline,)


class BillSegmentAdmin(admin.ModelAdmin):
    list_display = ('type', 'content')
    list_filter = ('bill',)


class CitizenAmendmentAdmin(admin.ModelAdmin):
    list_display = ('author', 'segment', 'original_content', 'content', 'comment')



admin.site.register(models.Bill, BillAdmin)
admin.site.register(models.BillSegment, BillSegmentAdmin)
admin.site.register(models.CitizenAmendment, CitizenAmendmentAdmin)
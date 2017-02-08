from django.contrib import admin
from core import models


class BillThemeAdmin(admin.ModelAdmin):
    list_display = ('description', 'slug')
    search_fields = ('description', 'slug')
    ordering = ('description',)
    readonly_fields = ('slug',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
    search_fields = ('text', 'author__email', 'author__username')
    ordering = ('created',)


class BillAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'theme', 'reporting_member', 'status', 'upvote_count',
        'downvote_count', 'comments_count')
    list_filter = ('theme', 'is_visible', 'status')
    search_fields = ('title', 'epigraph', 'description')
    ordering = ('created',)


class BillVideoAdmin(admin.ModelAdmin):
    list_display = ('bill', 'url')
    list_filter = ('bill',)
    search_fields = ('url', 'bill__title')


class BillReferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'bill')
    list_filter = ('bill',)
    search_fields = ('title', 'url', 'bill__title')


class BillSegmentAdmin(admin.ModelAdmin):
    list_display = (
        'bill', 'content', 'amendments_count', 'additive_amendments_count',
        'modifier_amendments_count', 'supress_amendments_count')
    list_filter = ('bill',)
    search_fields = ('parent__content', 'content', 'bill__title')


class AdditiveAmendmentAdmin(admin.ModelAdmin):
    list_display = ('content', 'reference', 'author')
    search_fields = ('content', 'reference__content', 'bill__title')


class ModifierAmendmentAdmin(admin.ModelAdmin):
    list_display = ('content', 'replaced', 'author')
    search_fields = ('content', 'replaced__content', 'bill__title')


class SupressAmendmentAdmin(admin.ModelAdmin):
    list_display = ('supressed', 'author')
    search_fields = ('supressed__content', 'bill__title')


class SegmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'presentation_name')
    list_filter = ('editable',)
    search_fields = ('name', 'presentation_name')


admin.site.register(models.BillTheme, BillThemeAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Bill, BillAdmin)
admin.site.register(models.BillVideo, BillVideoAdmin)
admin.site.register(models.BillReference, BillReferenceAdmin)
admin.site.register(models.BillSegment, BillSegmentAdmin)
admin.site.register(models.AdditiveAmendment, AdditiveAmendmentAdmin)
admin.site.register(models.ModifierAmendment, ModifierAmendmentAdmin)
admin.site.register(models.SupressAmendment, SupressAmendmentAdmin)
admin.site.register(models.SegmentType, SegmentTypeAdmin)

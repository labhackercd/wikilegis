from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.admin.views.main import ChangeList
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


class BillReferenceInline(admin.TabularInline):
    model = models.BillReference
    verbose_name = _('reference')
    verbose_name_plural = _('references')
    extra = 1


class BillVideoInline(admin.TabularInline):
    model = models.BillVideo
    verbose_name = _('video')
    verbose_name_plural = _('videos')
    extra = 1


class InlineChangeList(object):
    can_show_all = True
    multi_page = True
    get_query_string = ChangeList.__dict__['get_query_string']

    def __init__(self, request, page_num, paginator):
        self.show_all = 'all' in request.GET
        self.page_num = page_num
        self.paginator = paginator
        self.result_count = paginator.count
        self.opts = {
            'verbose_name': _('segment'), 'verbose_name_plural': _('segments')}
        self.params = dict(request.GET.items())


class BillSegmentInline(admin.TabularInline):
    model = models.BillSegment
    extra = 0
    template = 'admin/segments/edit_inline/tabular.html'
    exclude = [
        'author', 'additive_amendments_count', 'modifier_amendments_count',
        'supress_amendments_count', 'amendments_count', 'upvote_count',
        'downvote_count', 'comments_count', 'participation_count', 'order']
    fields = ['id', 'parent', 'segment_type', 'number', 'content']
    per_page = 20
    readonly_fields = ('id',)
    raw_id_fields = ("parent",)

    def get_formset(self, request, obj=None, **kwargs):
        formset_class = super(BillSegmentInline, self).get_formset(
            request, obj, **kwargs)

        class PaginationFormSet(formset_class):
            def __init__(self, *args, **kwargs):
                super(PaginationFormSet, self).__init__(*args, **kwargs)

                qs = self.queryset
                paginator = Paginator(qs, self.per_page)
                try:
                    page_num = int(request.GET.get('p', '0'))
                except ValueError:
                    page_num = 0

                try:
                    page = paginator.page(page_num + 1)
                except (EmptyPage, InvalidPage):
                    page = paginator.page(paginator.num_pages)

                self.cl = InlineChangeList(request, page_num, paginator)
                self.paginator = paginator

                if self.cl.show_all:
                    self._queryset = qs
                else:
                    self._queryset = page.object_list

        PaginationFormSet.per_page = self.per_page
        return PaginationFormSet


class BillAdmin(admin.ModelAdmin):
    inlines = (BillVideoInline, BillReferenceInline, BillSegmentInline)
    list_display = (
        'title', 'theme', 'reporting_member', 'status', 'upvote_count',
        'downvote_count', 'comments_count')
    list_filter = ('theme', 'is_visible', 'status')
    search_fields = ('title', 'epigraph', 'description')
    ordering = ('created',)
    readonly_fields = (
        'upvote_count', 'downvote_count', 'comments_count', 'amendments_count')
    fieldsets = [
        (None, {'fields': [
            'title', 'epigraph', 'description', 'theme', 'reporting_member',
            'closing_date', 'status', 'is_visible', 'allowed_users']}),
        (_('Counters'), {'fields': [
            'upvote_count', 'downvote_count', 'comments_count',
            'amendments_count']}),
    ]


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
    readonly_fields = (
        'upvote_count', 'downvote_count', 'comments_count', 'amendments_count',
        'additive_amendments_count', 'modifier_amendments_count',
        'supress_amendments_count', 'participation_count', 'order')


class AdditiveAmendmentAdmin(admin.ModelAdmin):
    list_display = ('content', 'reference', 'author')
    search_fields = ('content', 'reference__content', 'bill__title')
    readonly_fields = (
        'upvote_count', 'downvote_count', 'comments_count',
        'participation_count', 'order')


class ModifierAmendmentAdmin(admin.ModelAdmin):
    list_display = ('content', 'replaced', 'author')
    search_fields = ('content', 'replaced__content', 'bill__title')
    readonly_fields = (
        'upvote_count', 'downvote_count', 'comments_count',
        'participation_count', 'order')


class SupressAmendmentAdmin(admin.ModelAdmin):
    list_display = ('supressed', 'author')
    search_fields = ('supressed__content', 'bill__title')
    readonly_fields = (
        'upvote_count', 'downvote_count', 'comments_count',
        'participation_count', 'order')


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

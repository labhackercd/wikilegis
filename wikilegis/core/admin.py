# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from adminsortable2.admin import SortableInlineAdminMixin
from . import models, forms


def get_permission(action, opts):
    codename = get_permission_codename(action, opts)
    return '.'.join([opts.app_label, codename])


class BillSegmentInline(SortableInlineAdminMixin, admin.TabularInline):
    model = models.BillSegment


class BillAuthorDataInline(GenericTabularInline):
    form = forms.MetaAuthorForm
    model = models.GenericData
    verbose_name = _('author')
    verbose_name_plural = _('authors')

    def get_queryset(self, request):
        return super(BillAuthorDataInline, self).get_queryset(request).filter(type=self.form.get_type())


class BillVideoInline(GenericTabularInline):
    form = forms.MetaVideoForm
    model = models.GenericData
    verbose_name = _('video')
    verbose_name_plural = _('videos')

    def get_queryset(self, request):
        return super(BillVideoInline, self).get_queryset(request).filter(type=self.form.get_type())

    def has_add_permission(self, request):
        return (self.has_change_permission(request)
                or super(BillVideoInline, self).has_add_permission(request))

    def has_change_permission(self, request, obj=None):
        # If the user can change the bill, it can also change its videos.
        return (request.user.has_perm('core.change_bill', obj)
                or super(BillVideoInline, self).has_change_permission(request, obj))

    def has_delete_permission(self, request, obj=None):
        return (self.has_change_permission(request, obj)
                or super(BillVideoInline, self).has_delete_permission(request, obj))


class BillChangeList(ChangeList):
    def get_queryset(self, request):
        queryset = super(BillChangeList, self).get_queryset(request)
        user = request.user
        if not getattr(user, 'is_superuser', False):
            queryset = queryset.filter(editors__pk__in=user.groups.values('pk'))
        return queryset


class BillAdmin(admin.ModelAdmin):
    inlines = (BillAuthorDataInline, BillVideoInline, BillSegmentInline)
    list_filter = ['status']
    list_display = ('title', 'description', 'status', 'get_report')

    def get_report(self, obj):
        return u'<a class="default" href="{url}">{title}</a>'.format(
            url=reverse('bill_report', args=[obj.pk]), title=_('Show'))

    get_report.short_description = _('Report')
    get_report.allow_tags = True

    def get_fields(self, request, obj=None):
        fields = super(BillAdmin, self).get_fields(request, obj)
        # XXX This permission can't be granted to anyone but superusers,
        # but we're naming it right now because it could become useful in
        # the future.
        if not request.user.has_perm('core.change_bill_editors', obj):
            fields.remove('editors')
        return fields

    def get_changelist(self, request, **kwargs):
        # XXX We override the ChangeList so we can override *only* the queryset for the changelist view.
        # I don't really remember why we have to do it this way, but I remember this "oh, shit" moment,
        # so I'm pretty sure we're in the right track by trusting myself.
        return BillChangeList
    
    def has_change_permission(self, request, obj=None):
        # XXX We have to override this in order to call `has_perm` with the given object (or None).
        perm = get_permission('change', self.opts)
        return request.user.has_perm(perm, obj)
    
    def has_module_permission(self, request):
        # XXX Again, we override this to rely on our custom permission checking rules.
        # If the user has any `change` permission in this app, it should view this app.
        return self.has_change_permission(request) or super(BillAdmin, self).has_module_permission(request)


class CitizenAmendmentAdmin(admin.ModelAdmin):
    list_display = ('author', 'segment', 'original_content', 'content')


admin.site.register(models.Bill, BillAdmin)
admin.site.register(models.CitizenAmendment, CitizenAmendmentAdmin)

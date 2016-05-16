# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from . import forms
from . import models
import requests
from wikilegis.core.forms import BillAdminForm
from wikilegis.core.forms import BillSegmentAdminForm
from wikilegis.core.forms import update_proposition
from wikilegis.core.models import Bill
from wikilegis.core.models import BillSegment
from wikilegis.core.models import TypeSegment


def get_permission(action, opts):
    codename = get_permission_codename(action, opts)
    return '.'.join([opts.app_label, codename])


def propositions_update(ModelAdmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    bills = Bill.objects.filter(id__in=selected)
    for bill in bills:
        try:
            params = {'IdProp': bill.proposition_set.all()[0].id_proposition}
            response = requests.get(
                'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicaoPorID',
                params=params)
            update_proposition(
                response, bill.proposition_set.all()[0].id_proposition)
        except Exception:
            pass
    ModelAdmin.message_user(request, _("Bills updated successfully."))

propositions_update.short_description = _("Update status of selected bills")


class BillSegmentInline(SortableInlineAdminMixin, admin.TabularInline):
    model = BillSegment
    extra = 1
    exclude = ['original', 'replaced', 'author']

    def get_queryset(self, request):
        return super(
            BillSegmentInline, self).get_queryset(request).filter(original=True)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(BillSegmentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'parent':
            if request._obj_ is not None:
                field.queryset = field.queryset.filter(
                    original=True, bill__exact=request._obj_)
            else:
                field.queryset = field.queryset.none()

        return field


class BillAuthorDataInline(GenericTabularInline):
    form = forms.MetaAuthorForm
    model = models.GenericData
    verbose_name = _('author')
    verbose_name_plural = _('authors')

    def get_queryset(self, request):
        return super(
            BillAuthorDataInline, self).get_queryset(
                request).filter(type=self.form.get_type())


class BillVideoInline(GenericTabularInline):
    form = forms.MetaVideoForm
    model = models.GenericData
    verbose_name = _('video')
    verbose_name_plural = _('videos')

    def get_queryset(self, request):
        return super(
            BillVideoInline, self).get_queryset(
                request).filter(type=self.form.get_type())

    def has_add_permission(self, request):
        return (self.has_change_permission(request) or
                super(BillVideoInline, self).has_add_permission(request))

    def has_change_permission(self, request, obj=None):
        # If the user can change the bill, it can also change its videos.
        return (request.user.has_perm('core.change_bill', obj) or
                super(
                    BillVideoInline, self).has_change_permission(request, obj))

    def has_delete_permission(self, request, obj=None):
        return (self.has_change_permission(request, obj) or
                super(
                    BillVideoInline, self).has_delete_permission(request, obj))


class BillChangeList(ChangeList):
    def get_queryset(self, request):
        queryset = super(BillChangeList, self).get_queryset(request)
        user = request.user
        if not getattr(user, 'is_superuser', False):
            queryset = queryset.filter(
                editors__pk__in=user.groups.values('pk'))
        return queryset


class BillAdmin(admin.ModelAdmin):
    inlines = (BillAuthorDataInline, BillVideoInline, BillSegmentInline)
    list_filter = ['status']
    list_display = (
        'title',
        'description',
        'theme',
        'status',
        'get_situation',
        'get_report')
    actions = [propositions_update]
    form = BillAdminForm
    fieldsets = [
        (None, {'fields': ['title', 'epigraph', 'description', 'theme', 'status', 'editors']}),
        (_('Legislative proposal'), {'fields': ['type', 'number', 'year'],
                                     'description': _("This data will be used to assign the project \
                                                        to a legislative "
                                                      "proposal pending before the House of \
                                                        Representatives. You only "
                                                      "need to inform them if your procedure \
                                                        has been initiated. To "
                                                      "delete , leave the fields blank.")})
    ]
    # 'description': "Esses dados serão usados para associar o
    # projeto a uma proposição legislativa em tramitação na Câmara
    # dos Deputados. Apenas é necessário informá-los se sua
    # tramitação tiver sido iniciada. Para excluir, deixe os campos
    # em branco."})

    class Media(object):
        js = ('js/adminfix.js', )

    def response_add(self, request, obj, post_url_continue=None):
        opts = obj._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)
        if "_newsegment" in request.POST:
            if post_url_continue is None:
                post_url_continue = reverse('admin:%s_%s_change' %
                                            (opts.app_label, opts.model_name),
                                            args=(quote(pk_value),),
                                            current_app=self.admin_site.name)
            post_url_continue = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts},
                post_url_continue
            )
            return HttpResponseRedirect(post_url_continue + '#add_segment')
        return super(
            BillAdmin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        opts = self.model._meta
        preserved_filters = self.get_preserved_filters(request)
        if "_newsegment" in request.POST:
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url + '#add_segment')
        return super(BillAdmin, self).response_change(request, obj)

    def save_formset(self, request, form, formset, change):
        formset.save()
        if formset.model == BillSegment:
            index_parent = 1
            types = TypeSegment.objects.filter(editable=True)
            for type_segment in types:
                segments_parent = formset.queryset.filter(
                    type=type_segment,
                    type__editable=True,
                    parent__isnull=True).order_by('order')
                for segment in segments_parent:
                    if segment.order == 0:
                        segment.order = formset.queryset.all().aggregate(
                            Max('order'))['order__max'] + 1
                        if len(segments_parent) > 1:
                            segment.number = segments_parent.aggregate(
                                Max('number'))['number__max'] + 1
                        else:
                            segment.number = index_parent
                    else:
                        segment.number = index_parent
                        index_parent += 1
                    segment.save()
            segments_child = formset.queryset.filter(
                parent__isnull=False).order_by('order')
            parents = segments_child.values_list('parent_id', flat=True)
            for parent in list(set(parents)):
                segments_child_same_parent = segments_child.filter(
                    parent_id=parent).order_by('order')
                types_child = list(set(
                    segments_child_same_parent.values_list('type', flat=True)))
                if types_child > 1:
                    for each_type in types_child:
                        index_child = 1
                        for child in segments_child_same_parent.filter(type__id=each_type):
                            if child.order == 0:
                                child.order = formset.queryset.all().aggregate(
                                    Max('order'))['order__max'] + 1
                                if len(segments_child_same_parent) > 1:
                                    child.number = segments_child_same_parent.aggregate(
                                        Max('number'))['number__max'] + 1
                                else:
                                    child.number = index_child
                            else:
                                child.number = index_child
                                index_child += 1
                            child.save()
                else:
                    index_child = 1
                    for child in segments_child_same_parent:
                        if child.order == 0:
                            child.order = formset.queryset.all().aggregate(
                                Max('order'))['order__max'] + 1
                            if len(segments_child_same_parent) > 1:
                                child.number = segments_child_same_parent.aggregate(
                                    Max('number'))['number__max'] + 1
                            else:
                                child.number = index_child
                        else:
                            child.number = index_child
                            index_child += 1
                        child.save()

    def get_situation(self, obj):
        try:
            return "%s" % obj.proposition_set.all()[0].situation
        except Exception:
            return ''
    get_situation.short_description = _(u'Situation')

    def get_report(self, obj):
        return u'<a class="default" href="{url}">{title}</a>'.format(
            url=reverse('bill_report', args=[obj.pk]), title=_('Show'))

    get_report.short_description = _('Report')
    get_report.allow_tags = True

    def get_fieldsets(self, request, obj=None):
        excluded = self.get_excluded_fields(request, obj=obj)
        fieldsets = super(BillAdmin, self).get_fieldsets(request, obj=obj)
        for (title, fieldset) in fieldsets:
            fields = fieldset.get('fields', [])
            for e in excluded:
                if e in fields:
                    fields.remove(e)
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        exclude = self.get_excluded_fields(request, obj=obj)
        exclude.extend(kwargs.pop('exclude', []))
        request._obj_ = obj
        return super(BillAdmin, self).get_form(request, obj, exclude=exclude, **kwargs)

    def get_excluded_fields(self, request, obj=None):
        exclude = []
        if not request.user.has_perm('core.change_bill_secret_fields', obj):
            exclude.extend(['editors', 'status'])
        return exclude

    def get_changelist(self, request, **kwargs):
        # XXX We override the ChangeList so we can override *only*
        # the queryset for the changelist view.
        # I don't really remember why we have to do it this way,
        # but I remember this "oh, shit" moment,
        # so I'm pretty sure we're in the right track by trusting myself.
        return BillChangeList

    def has_change_permission(self, request, obj=None):
        # XXX We have to override this in order to call `has_perm`
        # with the given object (or None).
        perm = get_permission('change', self.opts)
        return request.user.has_perm(perm, obj)

    def has_module_permission(self, request):
        # XXX Again, we override this to rely on our custom permission checking rules.
        # If the user has any `change` permission in this app,
        # it should view this app.
        return self.has_change_permission(request) or super(
            BillAdmin, self).has_module_permission(request)


class CitizenAmendmentAdmin(admin.ModelAdmin):
    list_display = ('author', 'segment', 'original_content', 'content')


class TypeSegmentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        perm = get_permission('change', self.opts)
        return request.user.has_perm(perm)

    def has_change_permission(self, request, obj=None):
        perm = get_permission('change', self.opts)
        return request.user.has_perm(perm, obj)


class BillSegmentAdmin(admin.ModelAdmin):
    list_filter = ['original', 'type', 'bill']
    list_display = ('bill', 'order', 'type', 'number', 'author', 'parent', 'original')
    form = BillSegmentAdminForm
    fieldsets = [
        (None, {'fields': ['bill', 'order', 'parent', 'type', 'number', 'content']})
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(BillSegmentAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'order':
            try:
                field.initial = BillSegment.objects.filter(
                    bill_id=Bill.objects.all().last().id).aggregate(Max('order'))['order__max'] + 1
            except Exception:
                field.initial = 1
        return field

admin.site.register(BillSegment, BillSegmentAdmin)
admin.site.register(models.Bill, BillAdmin)
admin.site.register(models.CitizenAmendment, CitizenAmendmentAdmin)
admin.site.register(TypeSegment, TypeSegmentAdmin)

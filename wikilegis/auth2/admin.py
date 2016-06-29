import requests
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from wikilegis.auth2.forms import UserChangeForm, UserCreationForm
from wikilegis.auth2.models import User, Congressman
from image_cropping import ImageCroppingMixin
from xml.etree import ElementTree


def congressman_update(ModelAdmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    congressmen = Congressman.objects.filter(id__in=selected)
    for congresman in congressmen:
        try:
            params = {'ideCadastro': congresman.user.id_congressman, 'numLegislatura': ''}
            response = requests.get('http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDetalhesDeputado',
                                    params=params)
            update_congressman(response, congresman.id)
        except:
            pass
    ModelAdmin.message_user(request, _("Congressmen updated successfully."))

congressman_update.short_description = _("Update selected congressmen")


def update_congressman(response, congresman_id):
    tree = ElementTree.fromstring(response.content)
    congressman = Congressman.objects.get(id=congresman_id)
    congressman.uf = tree[-1].find('ufRepresentacaoAtual').text
    congressman.party = tree[-1].find('partidoAtual').find('sigla').text
    congressman.parliamentary_name = tree[-1].find('nomeParlamentarAtual').text
    congressman.save()


def create_congressman(response, user_id):
    tree = ElementTree.fromstring(response.content)
    congressman = Congressman()
    congressman.user_id = user_id
    congressman.uf = tree[-1].find('ufRepresentacaoAtual').text
    congressman.party = tree[-1].find('partidoAtual').find('sigla').text
    congressman.parliamentary_name = tree[-1].find('nomeParlamentarAtual').text
    congressman.save()


class UserAdmin(BaseUserAdmin, ImageCroppingMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'id_congressman', 'avatar', 'cropping')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        instance.save()
        if instance.id_congressman:
            if instance.congressman_set.all():
                Congressman.objects.get(id=instance.congressman_set.all()[0].id).delete()
            params = {'ideCadastro': instance.id_congressman, 'numLegislatura': ''}
            response = requests.get('http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDetalhesDeputado',
                                    params=params)
            create_congressman(response, instance.id)

        return instance


class CongressmanAdmin(admin.ModelAdmin):
    list_display = ('user', 'party', 'uf', 'parliamentary_name')
    actions = [congressman_update]


admin.site.register(User, UserAdmin)
admin.site.register(Congressman, CongressmanAdmin)

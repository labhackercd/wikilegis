from django.db import models
from django.utils.translation import ugettext as _
from pygov_br.camara_deputados import cd


class BillAuthor(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Author Name'))
    region = models.CharField(max_length=255, blank=True, null=True,
                              verbose_name=_('Region'))
    party = models.CharField(max_length=255, blank=True, null=True,
                             verbose_name=_('Party'))
    register_id = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name=_('Register ID'))

    class Meta:
        verbose_name = "Bill Author"
        verbose_name_plural = "Bill Authors"

    def __str__(self):
        details = ''
        if self.register_id:
            details = ' - {}({})'.format(self.party, self.region)
        return '{}{}'.format(self.name, details)


class BillInfo(models.Model):

    class Meta:
        verbose_name = "Bill Info"
        verbose_name_plural = "Bill Infos"

    def __str__(self):
        return self.bill.title

    def save(self, *args, **kwargs):
        try:
            proposal = cd.proposals.get(
                self.proposal_type.initials,
                self.proposal_number,
                self.proposal_year,
            )
        except KeyError:
            raise Exception('Invalid proposal_type, proposal_number or '
                            'proposal_year')
        author = BillAuthor.objects.update_or_create(
            name=proposal['Autor'],
            region=proposal['ufAutor'],
            party=proposal['partidoAutor'],
            register_id=proposal['ideCadastro'],
        )[0]
        self.situation = proposal['Situacao']
        self.author = author

        return super(BillInfo, self).save(args, kwargs)

    bill = models.OneToOneField('core.Bill', verbose_name=_('Bill'),
                                related_name='infos')
    author = models.ForeignKey('BillAuthor', verbose_name=_('Author'),
                               null=True, blank=True)
    reporting_member = models.ForeignKey('ReportingMember',
                                         verbose_name=_('Reporting Member'))
    proposal_type = models.ForeignKey('ProposalType',
                                      verbose_name=_('Proposal Type'))
    proposal_number = models.IntegerField(verbose_name=_('Proposal Number'))
    proposal_year = models.IntegerField(verbose_name=_('Proposal Year'))
    situation = models.CharField(max_length=400, blank=True, null=True,
                                 verbose_name=_('Situation'))


class ProposalType(models.Model):

    initials = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Proposal Type"
        verbose_name_plural = "Proposal Types"

    def __str__(self):
        return '{} - {}'.format(self.initials, self.description)


class ReportingMember(models.Model):
    id = models.IntegerField(primary_key=True,
                             verbose_name=_('Reporting Member ID'))
    name = models.CharField(max_length=255,
                            verbose_name=_('Parliamentary Name'))
    party = models.CharField(max_length=255,
                             verbose_name=_('Party'))
    region = models.CharField(max_length=2,
                              verbose_name=_('Region'))
    email = models.EmailField(verbose_name=_('Email'))

    class Meta:
        verbose_name = "ReportingMember"
        verbose_name_plural = "ReportingMembers"

    def __str__(self):
        return self.name

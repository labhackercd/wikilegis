from plugins.camara_deputados import models
from pygov_br.camara_deputados import cd


def get_proposal_situation(sender, instance, **kwargs):
    try:
        proposal = cd.proposals.get(
            instance.proposal_type.initials,
            instance.proposal_number,
            instance.proposal_year,
        )
    except KeyError:
        raise Exception('Invalid proposal_type, proposal_number or '
                        'proposal_year')
    author = models.BillAuthor.objects.update_or_create(
        name=proposal['Autor'],
        region=proposal['ufAutor'],
        party=proposal['partidoAutor'],
        register_id=proposal['ideCadastro'],
    )[0]

    instance.situation = proposal['Situacao']
    instance.author = author

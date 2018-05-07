# EDITABLE SETTINGS
CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.ImageField', {}]
}

CONSTANCE_CONFIG = {
    'SUBTITLE': ('Sua ferramenta de edição legislativa', 'Subtítulo da página '
                 'inicial', str),
    'DESCRIPTION_P1': ('Analise os projetos de lei e contribua com sugestões '
                       'de nova redação a artigos ou parágrafos. Os deputados '
                       'relatores das proposições acompanham as participações '
                       'e podem adotar a sua ideia!', 'Primeiro parágrafo da '
                       'descrição na página inicial', str),
    'DESCRIPTION_P2': ('Nessa interação, ganha a sociedade, que participa mais '
                       'ativamente do processo legislativo, e ganha o '
                       'Parlamento, que aprova leis mais aprimoradas e '
                       'conectadas às necessidades dos cidadãos.', 'Segundo '
                       'parágrafo da descrição na página inicial', str),
    'VOTE_TEXT': ('Você apoia esse projeto de lei?', 'Descrição dos botões para'
                  ' apoiar o texto', str),
    'NEWSLETTER_TEXT': ('Assinar este projeto de lei', 'Texto para assinar a '
                        'newsletter', str),
    'SUGGESTION_TEXT': ('Sugestões de emendas', 'Texto para a quantidade de '
                        'sugestões', str),
    'CLOSED_TEXT': ('Este projeto está fechado para participação.', 'Texto '
                    'para exibir quando o texto estiver encerrado.', str),
    'COAT_OF_ARMS_IMAGE': ('brasao.png', 'Brasão do texto', 'image_field'),
    'BILL_VOTES': ('Votos do Projeto', 'Descrição dos votos no texto', str),
    'SEGMENT_VOTES': ('Votos em Dispositivos', 'Descrição dos votos em '
                      'segmentos de texto', str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Página inicial': ('SUBTITLE', 'DESCRIPTION_P1', 'DESCRIPTION_P2'),
    'Página do texto': ('VOTE_TEXT', 'NEWSLETTER_TEXT', 'SUGGESTION_TEXT',
                        'CLOSED_TEXT', 'COAT_OF_ARMS_IMAGE'),
    'Relatório': ('BILL_VOTES', 'SEGMENT_VOTES'),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

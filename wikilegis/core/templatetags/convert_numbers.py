# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import Library
from collections import OrderedDict
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import string

from wikilegis.core.models import BillSegment

register = Library()


def int_to_letter(number):
    num2alpha = dict(zip(range(1, 27), string.ascii_lowercase))
    return num2alpha[number]


def int_to_roman(num):

    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num > 0:
                roman_num(num)
            else:
                break

    return "".join([a for a in roman_num(num)])


@register.simple_tag
def segment_numbering(segment):
    if segment.number:
        type_name = slugify(segment.type.name)
        int_number = int(segment.number)
        if type_name == 'artigo':
            if int_number <= 9:
                return "Art. %dº " % int_number
            else:
                return "Art. %d " % int_number
        elif type_name == 'paragrafo':
            if int_number <= 9:
                if int_number == 1 and BillSegment.objects.filter(type__name=segment.type.name, parent_id=segment.parent_id).count() == 1:
                        return "%s. " % _("Sole paragraph")
                else:
                    return "§ %dº " % int_number
            else:
                return "§ %d " % int_number
        elif type_name == 'alinea':
            return "%s) " % int_to_letter(int_number)
        elif type_name == 'titulo':
            return "%s" % int_to_roman(int_number)
        elif type_name == 'livro':
            return "%s" % int_to_roman(int_number)
        elif type_name == 'capitulo':
            return "%s" % int_to_roman(int_number)
        elif type_name == 'secao':
            return "%s" % int_to_roman(int_number)
        elif type_name == 'subsecao':
            return "%s" % int_to_roman(int_number)

        if type_name == 'articulo':
            if int_number <= 9:
                return "Articulo %dº " % int_number
            else:
                return "Articulo %d " % int_number
        elif type_name == 'seccion':
                return "Seccion %d " % int_number
        elif type_name == 'parte':
            return "%s - " % int_number
        elif type_name == 'inciso':
            return "%s.- " % int_number
        elif type_name == 'titulo':
            return "%s" % int_number
        elif type_name == 'libro':
            return "%s" % int_number
        elif type_name == 'capitulo':
            return "%s" % int_number
        elif type_name == 'letra':
            return "%s" % int_to_letter(int_number)
        elif type_name == 'numero':
            return "%s" % int_number
    else:
        return ''

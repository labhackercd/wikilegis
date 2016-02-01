# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import Library
from collections import OrderedDict
import string


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
def segment_numbering(number, type_segment):
    if type_segment.name == 'Artigo':
        if number <= 9:
            return "Art. %sº " % number
        else:
            return "Art. %s " % number
    elif type_segment.name == 'Parágrafo':
        if number <= 9:
            return "§ %sº " % number
        else:
            return "§ %s " % number
    elif type_segment.name == 'Inciso':
        return "%s - " % int_to_roman(number)
    elif type_segment.name == 'Alínea':
        return "%s) " % int_to_letter(number)
    elif type_segment.name == 'Item':
        return "%s. " % number
    else:
        return ''

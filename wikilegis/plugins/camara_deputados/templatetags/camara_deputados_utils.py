from django.template import Library
from collections import OrderedDict
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
import string

from core.models import BillSegment

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
        type_name = slugify(segment.segment_type.name)
        if type_name == 'artigo':
            if segment.number <= 9:
                return "Art. %dº " % segment.number
            else:
                return "Art. %d " % segment.number
        elif type_name == 'paragrafo':
            if segment.number <= 9:
                siblings_count = BillSegment.objects.filter(
                    segment_type__name=segment.segment_type.name,
                    parent=segment.parent
                ).count()
                if segment.number == 1 and siblings_count == 1:
                        return "%s. " % _("Sole paragraph")
                else:
                    return "§ %dº " % segment.number
            else:
                return "§ %d " % segment.number
        elif type_name == 'inciso':
            return "%s - " % int_to_roman(segment.number)
        elif type_name == 'alinea':
            return "%s) " % int_to_letter(segment.number)
        elif type_name == 'titulo':
            return "%s" % int_to_roman(segment.number)
        elif type_name == 'livro':
            return "%s" % int_to_roman(segment.number)
        elif type_name == 'capitulo':
            return "%s" % int_to_roman(segment.number)
        elif type_name == 'secao':
            return "%s" % int_to_roman(segment.number)
        elif type_name == 'subsecao':
            return "%s" % int_to_roman(segment.number)
    else:
        return ''


@register.filter
def previous_article(segment):
    try:
        if segment.segment_type.name != "artigo":
            article = BillSegment.objects.filter(bill_id=segment.bill_id,
                                                 id__lt=segment.id,
                                                 segment_type__name='artigo'
                                                 ).order_by('-id')[0]
            return article
    except:
        return {}

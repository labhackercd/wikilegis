from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from core.models import BillSegment, SegmentType
import re
import roman
import string


def create_segment(type_id, order, bill_pk, number, content):
    segments = BillSegment.objects.filter(bill_id=bill_pk)
    segment = BillSegment()
    segment.order = order
    segment.bill_id = bill_pk
    segment.segment_type_id = type_id
    if type_id == SegmentType.objects.get(name="paragrafo").id:
        type_parent = SegmentType.objects.get(name="artigo").id
        segment.parent = segments.filter(order__lt=order,
                                         segment_type_id=type_parent).last()
    elif type_id == SegmentType.objects.get(name="inciso").id:
        type_parents = []
        type_parents.append(SegmentType.objects.get(name="artigo").id)
        type_parents.append(SegmentType.objects.get(name="paragrafo").id)
        segment.parent = segments.filter(order__lt=order,
                                         segment_type__in=type_parents).last()
    elif type_id == SegmentType.objects.get(name="alinea").id:
        type_parents = []
        type_parents.append(SegmentType.objects.get(name="inciso").id)
        type_parents.append(SegmentType.objects.get(name="paragrafo").id)
        segment.parent = segments.filter(order__lt=order,
                                         segment_type__in=type_parents).last()
    elif type_id == SegmentType.objects.get(name="item").id:
        type_parent = SegmentType.objects.get(name="alinea").id
        segment.parent = segments.filter(order__lt=order,
                                         segment_type_id=type_parent).last()
    elif type_id == SegmentType.objects.get(name="citacao").id:
        segment.parent = segments.exclude(
            segment_type_id=type_id).filter(order__lt=order).last()
    segment.number = number
    segment.content = content
    segment.save()


def import_txt(bill_txt, bill_pk):
    response = bill_txt.read()
    lines = response.splitlines()
    order = 1
    is_quote = False
    for line in lines:
        type_id = None
        if slugify(line).startswith('livro') and not is_quote:
            type_id = SegmentType.objects.get(name="livro").id
            number = roman.fromRoman(re.sub(b"^Livro ", '', line))
            content = lines[order].decode('utf-8')
        elif slugify(line).startswith('titulo') and not is_quote:
            type_id = SegmentType.objects.get(name="titulo").id
            number = roman.fromRoman(re.sub(b"^T\xc3\xadtulo ", '', line))
            content = lines[order].decode('utf-8')
        elif slugify(line).startswith('capitulo') and not is_quote:
            type_id = SegmentType.objects.get(name="capitulo").id
            number = roman.fromRoman(re.sub(b"^CAP\xc3\x8dTULO ", '', line))
            content = lines[order].decode('utf-8')
        elif slugify(line).startswith('secao') and not is_quote:
            type_id = SegmentType.objects.get(name="secao").id
            number = roman.fromRoman(
                re.sub(b"^Se\xc3\xa7\xc3\xa3o ", '', line))
            content = lines[order].decode('utf-8')
        elif slugify(line).startswith('subsecao') and not is_quote:
            type_id = SegmentType.objects.get(name="subsecao").id
            number = roman.fromRoman(
                re.sub(b"^Subse\xc3\xa7\xc3\xa3o ", '', line))
            content = lines[order].decode('utf-8')
        elif (re.match(b"^Art. \d+ \W+", line) or
              re.match(b"^Art. \d+\.", line) and not is_quote):
            try:
                label = re.match(b"^Art. \d+ \W+", line).group(0)
            except:
                label = re.match(b"^Art. \d+\.", line).group(0)
            type_id = SegmentType.objects.get(name="artigo").id
            number = re.search(b'\d+', label).group(0)
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif re.match(b"^\W+ \d+\W+", line) and not is_quote:
            label = re.match(b"^\W+ \d+\W+", line).group(0)
            type_id = SegmentType.objects.get(name="paragrafo").id
            number = re.search(b'\d+', label).group(0)
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif slugify(line).startswith('paragrafo-unico') and not is_quote:
            segment_type_id = SegmentType.objects.get(name="paragrafo").id
            type_id = segment_type_id
            number = 1
            content = line.decode('utf-8').replace('Parágrafo único. ', '')
        elif re.match(b"^[A-Z\d]+ \W+ ", line) and not is_quote:
            label = re.match(b"^[A-Z\d]+ \W+ ", line).group(0)
            type_id = SegmentType.objects.get(name="inciso").id
            number = roman.fromRoman(re.search(b"^[A-Z\d]+", line).group(0))
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif re.match(b"^[a-z]\W ", line) and not is_quote:
            label = re.match(b"^[a-z]\W ", line).group(0)
            type_id = SegmentType.objects.get(name="alinea").id
            number = string.lowercase.index(
                re.search(b"^[a-z]", line).group(0)) + 1
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif re.match(b"^\d+\. ", line) and not is_quote:
            label = re.match(b"^\d+\. ", line).group(0)
            type_id = SegmentType.objects.get(name="item").id
            number = re.search(b"^\d+", line).group(0)
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif line.decode('utf-8').startswith('Pena') and not is_quote:
            type_id = SegmentType.objects.get(name="citacao").id
            content = line.decode('utf-8')
            number = None
        elif re.match(b"^\"", line) or is_quote:
            type_id = SegmentType.objects.get(name="citacao").id
            content = line.decode('utf-8')
            number = None
            if (line.decode('utf-8').endswith("(NR)") or
               line.decode('utf-8').endswith('"')):
                is_quote = False
            else:
                is_quote = True
        else:
            if not (slugify(lines[order - 2]).startswith('livro') and not
                    slugify(lines[order - 2]).startswith('titulo') and not
                    slugify(lines[order - 2]).startswith('capitulo') and not
                    slugify(lines[order - 2]).startswith('secao') and not
                    slugify(lines[order - 2]).startswith('subsecao')):
                type_id = SegmentType.objects.get(name="citacao").id
                content = line.decode('utf-8')
                number = None
        if type_id:
            create_segment(type_id, order, bill_pk, number, content)

        order += 1

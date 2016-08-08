# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from models import BillSegment, TypeSegment
import re
import roman
import string


def create_segment(type_id, order, bill_pk, number, content):
    segments = BillSegment.objects.filter(bill_id=bill_pk, original=True)
    segment = BillSegment()
    segment.order = order
    segment.bill_id = bill_pk
    segment.type_id = type_id
    if type_id == TypeSegment.objects.get(name="Parágrafo").id:
        type_parent = TypeSegment.objects.get(name="Artigo").id
        segment.parent = segments.filter(order__lt=order, type_id=type_parent).last()
    elif type_id == TypeSegment.objects.get(name="Inciso").id:
        type_parents = []
        type_parents.append(TypeSegment.objects.get(name="Artigo").id)
        type_parents.append(TypeSegment.objects.get(name="Parágrafo").id)
        segment.parent = segments.filter(order__lt=order, type_id__in=type_parents).last()
    elif type_id == TypeSegment.objects.get(name="Alínea").id:
        type_parents = []
        type_parents.append(TypeSegment.objects.get(name="Inciso").id)
        type_parents.append(TypeSegment.objects.get(name="Parágrafo").id)
        segment.parent = segments.filter(order__lt=order, type_id__in=type_parents).last()
    elif type_id == TypeSegment.objects.get(name="Item").id:
        type_parent = TypeSegment.objects.get(name="Alínea").id
        segment.parent = segments.filter(order__lt=order, type_id=type_parent).last()
    elif type_id == TypeSegment.objects.get(name="Citação").id:
        segment.parent = segments.exclude(type_id=type_id).filter(order__lt=order).last()
    segment.number = number
    segment.content = content
    segment.save()


def import_file(bill_txt, bill_pk):
    response = bill_txt.read()
    lines = response.splitlines()
    order = 1
    is_quote = False
    for line in lines:
        type_id = None
        if slugify(line).startswith('livro') and not is_quote:
            type_id = TypeSegment.objects.get(name="Livro").id
            number = roman.fromRoman(re.sub(r"^Livro ", '', line))
            content = lines[order].decode('utf-8')
        elif slugify(line).startswith('titulo') and not is_quote:
            type_id = TypeSegment.objects.get(name="Título").id
            number = roman.fromRoman(re.sub(r"^T\xc3\xadtulo ", '', line))
            content = lines[order].decode('utf-8')
        elif slugify(line).startswith('capitulo') and not is_quote:
            type_id = TypeSegment.objects.get(name="Capítulo").id
            number = roman.fromRoman(re.sub(r"^CAP\xc3\x8dTULO ", '', line))
            content = lines[order].decode('utf-8')
        elif slugify(line).startswith('secao') and not is_quote:
            type_id = TypeSegment.objects.get(name="Seção").id
            number = roman.fromRoman(re.sub(r"^Se\xc3\xa7\xc3\xa3o ", '', line))
            content = lines[order].decode('utf-8')
        elif slugify(line).startswith('subsecao') and not is_quote:
            type_id = TypeSegment.objects.get(name="Subseção").id
            number = roman.fromRoman(re.sub(r"^Subse\xc3\xa7\xc3\xa3o ", '', line))
            content = lines[order].decode('utf-8')
        elif re.match(r"^Art. \d+ \W+", line) or re.match(r"^Art. \d+\.", line) and not is_quote:
            try:
                label = re.match(r"^Art. \d+ \W+", line).group(0)
            except:
                label = re.match(r"^Art. \d+\.", line).group(0)
            type_id = TypeSegment.objects.get(name="Artigo").id
            number = re.search(r'\d+', label).group(0)
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif re.match(r"^\W+ \d+\W+", line) and not is_quote:
            label = re.match(r"^\W+ \d+\W+", line).group(0)
            type_id = TypeSegment.objects.get(name="Parágrafo").id
            number = re.search(r'\d+', label).group(0)
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif slugify(line).startswith('paragrafo-unico') and not is_quote:
            segment_type_id = TypeSegment.objects.get(name="Parágrafo").id
            type_id = segment_type_id
            number = 1
            content = line.decode('utf-8').replace('Parágrafo único. ', '')
        elif re.match(r"^[A-Z\d]+ \W+ ", line) and not is_quote:
            label = re.match(r"^[A-Z\d]+ \W+ ", line).group(0)
            type_id = TypeSegment.objects.get(name="Inciso").id
            number = roman.fromRoman(re.search(r"^[A-Z\d]+", line).group(0))
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif re.match(r"^[a-z]\W ", line) and not is_quote:
            label = re.match(r"^[a-z]\W ", line).group(0)
            type_id = TypeSegment.objects.get(name="Alínea").id
            number = string.lowercase.index(re.search(r"^[a-z]", line).group(0)) + 1
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif re.match(r"^\d+\. ", line) and not is_quote:
            label = re.match(r"^\d+\. ", line).group(0)
            type_id = TypeSegment.objects.get(name="Item").id
            number = re.search(r"^\d+", line).group(0)
            content = line.decode('utf-8').replace(label.decode('utf-8'), '')
        elif line.decode('utf-8').startswith('Pena') and not is_quote:
            type_id = TypeSegment.objects.get(name="Citação").id
            content = line.decode('utf-8')
            number = None
        elif re.match(r"^\"", line) or is_quote:
            type_id = TypeSegment.objects.get(name="Citação").id
            content = line.decode('utf-8')
            number = None
            if line.decode('utf-8').endswith("(NR)") or line.decode('utf-8').endswith('"'):
                is_quote = False
            else:
                is_quote = True
        else:
            if not slugify(lines[order - 2]).startswith('livro') and not slugify(lines[order - 2]).startswith('titulo') and not slugify(lines[order - 2]).startswith('capitulo') and not slugify(lines[order - 2]).startswith('secao') and not slugify(lines[order - 2]).startswith('subsecao'):
                type_id = TypeSegment.objects.get(name="Citação").id
                content = line.decode('utf-8')
                number = None
        if type_id:
            create_segment(type_id, order, bill_pk, number, content)

        order += 1

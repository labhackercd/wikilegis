# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from haystack import indexes
from wikilegis.core.models import Bill


class BillIndex(indexes.SearchIndex, indexes.Indexable):
    """
    Index a Bill, by concatenating it's title, description and all of it's segments.
    """
    text = indexes.CharField(document=True)

    def get_model(self):
        return Bill

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_text(self, obj):
        return '\n\n'.join([
            obj.title, obj.description, obj.content
        ])

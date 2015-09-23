import datetime
from haystack import indexes
from wikilegis.core.models import BillSegment


class BillSegmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return BillSegment

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
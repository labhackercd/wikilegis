import datetime
from haystack import indexes
from wikilegis.core.models import Bill


class BillIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True)


	def get_model(self):
		return Bill

	def index_queryset(self, using=None):
		return self.get_model().objects.all()

	def prepare_text(self, obj):
		content = obj.title + '\n\n'
		content += obj.description + '\n\n'
		content += obj.content
		return content
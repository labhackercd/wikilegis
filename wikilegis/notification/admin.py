from django.contrib import admin
from wikilegis.notification.models import HistoryNotification


class HistoryNotificationAdmin(admin.ModelAdmin):
    list_display = ('related_segment', 'hour')
    list_filter = ['amendment__segment__bill', 'amendment__segment', 'hour']
    search_fields = ['amendment__segment', 'amendment__segment__bill']

    def related_segment(self, obj):
        return obj.amendment.segment
    related_segment.short_description = 'Segment'

admin.site.register(HistoryNotification, HistoryNotificationAdmin)

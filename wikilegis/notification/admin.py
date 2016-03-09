from django.contrib import admin
from wikilegis.notification.models import HistoryNotification, Newsletter


class HistoryNotificationAdmin(admin.ModelAdmin):
    list_display = ('related_bill', 'related_segment', 'hour')
    list_filter = ['hour']

    def related_segment(self, obj):
        return obj.amendment.replaced
    related_segment.short_description = 'Segment'

    def related_bill(self, obj):
        return obj.amendment.bill
    related_bill.short_description = 'Bill'

admin.site.register(HistoryNotification, HistoryNotificationAdmin)
admin.site.register(Newsletter)

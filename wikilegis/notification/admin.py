from django.contrib import admin
from wikilegis.notification.models import HistoryNotification


class HistoryNotificationAdmin(admin.ModelAdmin):
    list_display = ('bill', 'hour')
    list_filter = ['bill', 'hour']
    search_fields = ['bill']

admin.site.register(HistoryNotification, HistoryNotificationAdmin)

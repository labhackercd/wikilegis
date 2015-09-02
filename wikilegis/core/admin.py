from django.contrib import admin
from . import models

admin.site.register(models.Bill)
admin.site.register(models.BillSegment)
admin.site.register(models.CitizenAmendment)

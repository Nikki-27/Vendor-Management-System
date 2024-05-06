from django.contrib import admin
from .models import vendor, PurchaseOrder, HistoricalPerformance

# Register your models here.
admin.site.register(vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)

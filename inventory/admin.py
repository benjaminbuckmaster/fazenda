from django.contrib import admin
from .models import Bean, StockAdjustment, StockEntry, StockTotal

admin.site.register(Bean)
admin.site.register(StockAdjustment)
admin.site.register(StockEntry)
admin.site.register(StockTotal)
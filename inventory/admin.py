from django.contrib import admin
from .models import Bean, StockEntry, StockOffset, StockTotal

admin.site.register(Bean)
admin.site.register(StockEntry)
admin.site.register(StockOffset)
admin.site.register(StockTotal)
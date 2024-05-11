from django.contrib import admin
from .models import Bean, ProductLabel, Shipping, StockAdjustment, StockEntry, StockTotal, Product, Packaging, ProductBean, ProductPackaging, ProductShipping

admin.site.register(Bean)
admin.site.register(ProductLabel)
admin.site.register(Shipping)
admin.site.register(Product)
admin.site.register(Packaging)
admin.site.register(ProductBean)
admin.site.register(ProductPackaging)
admin.site.register(ProductShipping)

admin.site.register(StockAdjustment)
admin.site.register(StockEntry)
admin.site.register(StockTotal)
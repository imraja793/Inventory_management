from django.contrib import admin

# Register your models here.
from product_app.models import Location, Product, WarehouseProductDescription

admin.site.register(Location)
admin.site.register(Product)
admin.site.register(WarehouseProductDescription)

from django.contrib import admin

from .models import Products, ProductCategory, Users, Orders, OrderItems, Payments, Customers, Inventory, Shipments


admin.site.register(Products)
admin.site.register(ProductCategory)
admin.site.register(Users)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(Payments)
admin.site.register(Customers)
admin.site.register(Inventory)
admin.site.register(Shipments)
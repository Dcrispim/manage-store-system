from django.contrib import admin

from .models import Client, Product, Stock, CartItem, SalesOrBuy, Service, Operation, Config

admin.site.register(Client)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Stock)
admin.site.register(SalesOrBuy)
admin.site.register(Service)
admin.site.register(Operation)
admin.site.register(Config)
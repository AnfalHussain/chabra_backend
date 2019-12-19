from django.contrib import admin
from .models import Product, Profile, Order, Basket, Address, Origin


admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Basket)
admin.site.register(Origin)




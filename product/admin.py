from django.contrib import admin
from .models import category,Product,contact, Basket, BasketProduct,Address, Doller,Color

admin.site.register(Product)
admin.site.register(category)
admin.site.register(contact)
admin.site.register(BasketProduct)
admin.site.register(Basket)
admin.site.register(Address)
admin.site.register(Doller)
admin.site.register(Color)
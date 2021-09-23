from django.urls import path
from .views import index 
from .views import (
                index,product_single,delete_product,
                categories,about,all_products,contact_us,
                search, cart,add_to_basket,product_special,
                update_basket,remove_basket,pay,address
)

app_name = 'product'

urlpatterns = [
    path('', index, name='index'),
    path('product/single/<str:slug>/',product_single,name='product_single'),
    path('product/special/',product_special,name='product_special'),
    path('about/',about,name='about'),
    path('all/products/',all_products,name="all_products"),
    path('category/<str:name>/',categories,name='category'),
    path('contact/',contact_us,name='contact'),
    path('search/',search,name='search'),
    path('cart',cart ,name='cart'),
    path('add_to_basket/<int:pk>/',add_to_basket ,name='add_to_basket'),
    path('delete_product/', delete_product, name='delete_product'),
    path('update_basket/', update_basket, name='update_basket'),
    path('remove_basket/', remove_basket, name='remove_basket'),
    path('pay/', pay, name='pay'),
    path('address/<int:pk>/', address, name='address'),
]

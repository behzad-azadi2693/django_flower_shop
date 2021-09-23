from django import template
from django.http import request
from product.models import Basket, category, Product, BasketProduct

register = template.Library()

@register.inclusion_tag('nav/category.html')
def navbar(request):
    product_promo = Product.objects.filter(status='promo').order_by('?')[:3]
    categories = category.objects.all()
    user_count = 0
    total_rial = 0
    total_doller = 0
    if request.user.is_authenticated:
        basket = Basket.objects.filter(is_paid = False, user = request.user).first()
        if basket is not None:
            user_count = basket.basketproduct_user.count()
            total_doller = 0
            total_rial = 0

            for pro in basket.basketproduct_user.all():
                total_doller = total_doller + pro.product.price_end_doller() * int(pro.qty)
                total_rial = total_rial + pro.product.price_end_rial() * int(pro.qty)
        

    context = {
        'product_promo':product_promo,
        'categories':categories,
        'user_count':user_count,
        'total_doller':total_doller,
        'total_rial':total_rial
    }

    return context
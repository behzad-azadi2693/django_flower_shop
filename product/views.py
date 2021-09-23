from django.http import request
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doller, Product,category,contact, Basket, BasketProduct, Address
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ContactForm, AddresForm
from django.utils.translation import gettext_lazy as _


def index(request):
    product_null = Product.objects.all()[:3]
    product_new = Product.objects.filter(status='new').order_by('-id')[:6]

    context = {
        'product_null':product_null,
        'product_new':product_new
    }
    return render(request, 'index.html', context)


def product_single(request, slug):
    product = get_object_or_404(Product, slug=slug)
    products = Product.objects.filter(categoryto=product.categoryto).order_by('-date')[:6]

    context = {
        'product':product,
        'products':products
    }
    return render(request, 'details.html', context)

def product_special(request):
    products = Product.objects.filter(status = 'special')

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 5)

    try:
        searchs = paginator.page(page)
    except PageNotAnInteger:
        searchs = paginator.page(1)
    except EmptyPage:
        searchs = paginator.page(paginator.num_pages)
    context = {
        'products':products,
        'searchs':searchs,
    }
    return render(request, 'specials.html', context)


def search(request):
    products = Product.objects.all()

    if request.GET.get('name'):
        name = request.GET.get('name')
        products = products.filter(name = name)

    if request.GET.get('category'):
        cat = request.GET.get('category')
        products = products.filter(category__name = cat)

    if request.GET.get('price_up'):
        up = request.GET.get('price_up')
        products = products.filter(price__gte = up)

    if request.GET.get('price_down'):
        down = request.GET.get('price_down')
        products = products.filter(price__lte = down)

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 12)

    try:
        searchs = paginator.page(page)
    except PageNotAnInteger:
        searchs = paginator.page(1)
    except EmptyPage:
        searchs = paginator.page(paginator.num_pages)

    context = {
        'categories':category.objects.all(),
        'name': request.GET.get('name'),
        'category':request.GET.get('category'),
        'price_up':request.GET.get('price_up'),
        'price_down':request.GET.get('price_down'),
        'products':products,
        'searchs':searchs
    }
    return render(request, 'category.html', context)

def contact_us(request):
    categoryes = category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('your messages successfully'), 'success')
            return redirect('product:contact_us')
        else:
            form = ContactForm(request.POST)
            return render(request, 'contact.html', {'form':form})
    else:
        form = ContactForm()
        return render(request,'contact.html',{'form':form})



def categories(request, name):
    cat = get_object_or_404(category, name_en=name)
    products = Product.objects.filter(categoryto = cat)

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 12)

    try:
        searchs = paginator.page(page)
    except PageNotAnInteger:
        searchs = paginator.page(1)
    except EmptyPage:
        searchs = paginator.page(paginator.num_pages)

    context = {
        'products':products,
        'searchs':searchs
    }
    return render(request, 'category.html', context)


def all_products(request):
    products = Product.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(products, 12)

    try:
        searchs = paginator.page(page)
    except PageNotAnInteger:
        searchs = paginator.page(1)
    except EmptyPage:
        searchs = paginator.page(paginator.num_pages)
    context = {
        'products':products,
        'searchs':searchs,
        'categories':category.objects.all(),
    }
    return render(request, 'category.html', context)


def about(request):
    return render(request, 'about.html')

@login_required
def cart(request):
    basket = Basket.objects.filter(user = request.user, is_paid = False).first()
    print(basket)
    if basket:
        basket_is = False
        basket_pk= basket.pk
        products = basket.basketproduct_user.all()
        if products:
            basket_is = True
        print(products)
        total_doller = 0
        total_rial = 0

        for pro in products:
            total_doller = total_doller + int(pro.product.price_end_doller()) * int(pro.qty)
            total_rial = total_rial + int(pro.product.price_end_rial()) * int(pro.qty)

        
    else:
        products = None
        total_doller = 0
        total_rial = 0
        basket_pk = 0
        basket_is = False

    context = {
        'products':products,
        'total_doller':total_doller,
        'total_rial':total_rial,
        'basket_pk':basket_pk,
        'basket':basket_is,
        'basket_old': Basket.objects.filter(user = request.user, is_paid=True),
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_basket(request, pk):
    basket = Basket.objects.filter(user = request.user, is_paid = False).first()
    pro = get_object_or_404(Product, pk=pk)
    if pro.count > 0:
        if basket:
            bas = basket.basketproduct_user.filter(product__pk=pk)
            if bas:
                return redirect('product:product_single', pro.slug)
            else:
                BasketProduct.objects.create(user = request.user, basket=basket, product=pro)
                return redirect('product:product_single', pro.slug)
        else:
            basket = Basket.objects.create(user=request.user)
            BasketProduct.objects.create(user = request.user, basket=basket, product=pro)        
            return redirect('product:product_single',pro.slug)
    else:
        return redirect('product:product_single',pro.slug)

@login_required
def delete_product(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        product = BasketProduct.objects.get(pk=pk)
        if product.user == request.user:
            product.delete()
            return redirect('product:cart')
        else:
            return redirect('product:cart')
    return redirect('product:cart')


@login_required
def update_basket(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        obj = get_object_or_404(BasketProduct, user = request.user, pk=pk)
        
        if obj.user == request.user:
            if int(request.POST.get('number')) > obj.product.count:
                return redirect('product:cart')
            obj.qty = request.POST.get('number')
            obj.save()
            return redirect('product:cart')
        else:
            return redirect('product:cart')
    return redirect('product:cart')


@login_required
def pay(requst):
    basket = Basket.objects.get(user = requst.user, is_paid=False)
    address = basket.basket_address.all().first()
    if address:
        products = basket.basketproduct_user.all()
        total = int(0)

        for pro in products:
            obj = Product.objects.select_for_update().get(pk = pro.product.pk)
            total = total + int(pro.product.price) * int(pro.qty)
            pro.price_unit_doller = pro.product.price
            unit = Doller.objects.all().first()
            pro.price_unit_rial = int(pro.product.price) * unit.price
            pro.save()
            
            
            objs = BasketProduct.objects.filter(product=pro)
            if pro.qty >= pro.product.count:
                objs.delete()
            else:
                for pro in objs:
                    pro.qty = 1
                    pro.save()

            obj.count = obj.count - pro.qty
            obj.save()

        basket.money_paid = int(total)
        basket.is_paid = True
        basket.save()
        return redirect('product:cart')
    else:
        return redirect('product:cart')

@login_required
def remove_basket(request):
    basket = Basket.objects.filter(user = request.user, is_paid = False)
    basket.delete()
    return redirect('product:cart')


@login_required
def address(request, pk):
    bas = get_object_or_404(Basket, user=request.user, pk=pk, is_paid = False)

    if bas.basket_address.filter(basket = bas):
        return redirect('product:pay')

    if request.method == 'POST':
        form = AddresForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.basket = bas
            obj.save()
            messages.success(request, _("your address successful"), 'succecc')
            return redirect('product:pay')
        else:
            messages.warning(request, _('wrong for submit your address'), 'error')
            return redirect('product:cart')
    
    else:
        form = AddresForm()
        return render(request, 'contact.html',{'form':form})
        

@login_required
def is_sending(request):
    if not request.user.is_admin:
        return redirect('product:index')
    
    order = Basket.objects.filter(is_paid=True, is_send_to_user=False)
    context = {
        'order':order,
        'send':True    
    }
    return render(request, 'send.html', context)


@login_required
def show_order(request, pk):
    if not request.user.is_admin:
        return redirect('product:index')
    
    basket = get_object_or_404(Basket, pk=pk, is_paid=True, is_send_to_user=False)

    products = basket.basketproduct_user.all()
    address = get_object_or_404(Address,basket = basket)
    context={
        'products':products,
        'address':address,
        'basket':basket,
        'show':True
    }
    return render(request, 'send.html', context)


@login_required
def is_send(request, pk):
    if not request.user.is_admin:
        return redirect('product:index')
    
    obj = get_object_or_404(Basket, pk=pk, is_paid=True, is_send_to_user=False)
    obj.is_send_to_user = True
    obj.save()
    return redirect('product:is_sending')
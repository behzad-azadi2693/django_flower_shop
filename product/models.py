from django.db import models
from accounts.models import User
from django.db.models.fields import BooleanField, PositiveIntegerField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import format_html

class category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('category name persian'))
    name_en = models.CharField(max_length=100, verbose_name=_('category name english'))
    title = models.CharField(max_length=250, verbose_name=_('category title persian'))
    title_en = models.CharField(max_length=250, verbose_name=_('category title english'))

    class Meta:
        verbose_name=_('Category Model')
        verbose_name_plural=_('Categories Model')
        
    def __str__(self):
        return self.name

        
class contact(models.Model):
    name =models.CharField(max_length=200, verbose_name=_('your name'))
    email=models.EmailField(verbose_name=_('your email'))
    phone=models.PositiveIntegerField(help_text='+989210000000',verbose_name=_('your phone'))
    company=models.CharField(max_length=200, verbose_name=_('your company'))
    messages=models.TextField(verbose_name=_('your message'))

    class Meta:
        ordering = ['name']
        verbose_name = _('Contact Us Model')
        verbose_name_plural = _('Contacts Us Model')

    def __str__(self) -> str:
        return self.name


class Color(models.Model):
    name_color = models.CharField(max_length=100, verbose_name=_('Color Name English'))
    class Meta:
        verbose_name = _('Color Model')
        verbose_name_plural = _('Colors Model')

    def __str__(self):
        return self.name_color

class Doller(models.Model):
    price = PositiveIntegerField(verbose_name=_('price Doller'))

    def __str__(self):
        return f'{self.price}'


def path_save_course(instance, filename):
    name = '{0}/{1}/{2}'.format(instance.categoryto.name_en, instance.name_en, filename)
    return name

class Product(models.Model):
    CHOICE_STATE = (
        ('null','null'),
        ('special','special'),
        ('new','new'),
        ('promo','promo'),
    )

    name = models.CharField(max_length=100, verbose_name=_('product name persian'))
    name_en = models.CharField(max_length=100, verbose_name=_('product name english'))
    slug = models.SlugField(allow_unicode=True, verbose_name=_("product slug"), unique=True)
    title = models.CharField(max_length=500, verbose_name=_('product title persiian'))
    title_en = models.CharField(max_length=500, verbose_name=_('product title english'))
    description = models.TextField(verbose_name=_('product description persian'))
    description_en = models.TextField(verbose_name=_('product description english'))
    date = models.DateTimeField(verbose_name=_('product date publish'))
    categoryto = models.ForeignKey(category,on_delete=models.CASCADE, verbose_name=_('category for product'))
    price = models.PositiveIntegerField(verbose_name=_('product price to dollers'))
    price_doller = models.ForeignKey(Doller, on_delete=models.DO_NOTHING, verbose_name=_('product price to dollers'))
    image = models.ImageField(upload_to ='flower', verbose_name=_('product image'))
    color = models.ManyToManyField(Color, verbose_name=_('colors use in product'))
    count = models.PositiveIntegerField(verbose_name=_('count product exists'))
    status = models.CharField(choices=CHOICE_STATE, max_length=7, verbose_name=_('product status'))

    class Meta:
        ordering = ['-id']
        verbose_name = _('Prouct Model')
        verbose_name_plural = _('Products Model')

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('product:product_single', args=(self.slug,))

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.translate.delete()
        super(Product, self).delete()

    def save(self, *args, **kwargs):
        slti = self.title_en.replace(' ','-')
        slna = self.name_en.replace(' ','-')
        self.slug = f'{slti}-{slna}'
        try:
            this = Product.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except: 
            pass
        super(Product, self).save(*args, **kwargs)

    def price_end_doller(self):
        if self.status == 'promo':
            product_price = self.price * (1 - float('0.10'))
            if 0 <= product_price <= self.price:
                return product_price
        else:
            return self.price
    
    def price_end_rial(self):
        if self.status == 'promo':
            product_price = (self.price * (1 - float('0.10'))) * self.price_doller.price
            if 0 <= product_price <= self.price:
                return product_price
        else:
            return self.price * self.price_doller.price

    def image_tag(self):
        return format_html("<img alt='' class='thumb'' border='0' src='{}' />".format(self.image.url))

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_baske', verbose_name=_('basket for witch user'))
    is_paid = models.BooleanField(default=False, verbose_name=_('basket paied'))
    is_send_to_user = BooleanField(default=False, verbose_name=_('order sending'))
    money_paid = models.PositiveBigIntegerField(null=True, blank=True, verbose_name=_('money paied'))


class BasketProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='baske_user', verbose_name=_('for witch user'))
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basketproduct_user', verbose_name=_('for witch basket'))
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='basket_product', verbose_name=_('for witch basket'))
    qty = models.PositiveIntegerField(default=1, verbose_name=_('product quaity'))
    price_unit_doller = models.PositiveIntegerField(null=True, blank=True)
    price_unit_rial = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _('Basket Product Model')
        verbose_name_plural = _('Baskets Products Model')
        ordering = ('-id',)

    def total_doller(self):
        return int(self.product.price_end_doller()) * self.qty

    def total_rial(self):
        return int(self.product.price_end_rial()) * self.qty

    def total_doller_paid(self):
        return int(self.price_unit_doller) * self.qty

    def total_rial_paid(self):
        return int(self.price_unit_rial) * self.qty


class Address(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_address', verbose_name=_('for witch basket'))
    number = models.PositiveIntegerField(verbose_name=_('user phone number'))
    address = models.TextField(verbose_name=_('user addresses'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Adresses')

    def __str__(self) -> str:
        return f'{self.number}'
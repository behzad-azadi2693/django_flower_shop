from django.db.models import fields
from django.forms import ModelForm
from django import forms
from .models import Product, contact, Address
from django.utils.translation import gettext_lazy as _

messages = {
    'required':_("this field is required"),
    'invalid':_("It is not correct"),
    'max_length':_("The size of the characters is large of 15 character"),
    'min_length':_("The size of the characters is small of 9 character"),
}

class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'contact_input'
            self.fields[field].error_messages = messages

    class Meta:
        model = contact
        fields = ('name','email','phone','company','messages')


class AddresForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddresForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'contact_input'
            self.fields[field].error_messages = messages
    
    class Meta:
        model = Address
        fields = ('number','address')

class CreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'contact_input'
            self.fields[field].error_messages = messages
    
    class Meta:
        model = Product
        fields = '__all__'
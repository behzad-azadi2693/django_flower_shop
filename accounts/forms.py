from django import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms.forms import Form
from django.forms.models import ModelForm
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField


messages = {
    'required':_("this field is required"),
    'invalid':_("It is not correct"),
    'max_length':_("The size of the characters is large of 15 character"),
    'min_length':_("The size of the characters is small of 4 character"),
    'max_value':_("out of range maximum size"),
    'min_value':_("out of range minimum size"),
    'invalid':_('this field is invalid')
}

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    password_confierm = forms.CharField(label=_('password_confierm'), widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ('username', 'email', 'password', 'password_confierm', 'count', 'date_for_wait')

    def clean_password_confierm(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_confierm'] and cd['password'] != cd['password_confierm']:
            raise forms.ValidationError(_("password and confirm password must be match "))

        return cd['password_confierm']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        models = User
        fields = ('username', 'email', 'password', 'count', 'date_for_wait')

    def clean_password(self):
        return self.initial['password']
    

class RegisterForm(forms.Form):
    username = forms.CharField(label=_('username'), widget=forms.TextInput,min_length=4)
    email = forms.EmailField(label=_('email'), widget=forms.EmailInput,)
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput,min_length=4)
    password_confierm = forms.CharField(label=_('password_confierm'), widget=forms.PasswordInput, min_length=4)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'contact_input'
            self.fields[field].error_messages = messages

    
    def clean_username(self):
        cd = self.cleaned_data['username']
        user = User.objects.filter(username = cd).first()
        if user:
            raise forms.ValidationError(_('this username is exits'))
        return cd

    def clean_email(self):
        cd = self.cleaned_data['email']
        user = User.objects.filter(email = cd).first()
        if user:
            raise forms.ValidationError(_('this email is exists'))
        return cd

    def clean_password_confierm(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_confierm'] and cd['password'] != cd['password_confierm']:
            raise forms.ValidationError(_("password and confirm password must be match "))
        
        return cd['password_confierm']


class LoginForm(forms.Form):
    username = forms.CharField(label=_('username'), widget=forms.TextInput,required=False,min_length=4)
    email = forms.EmailField(label=_('email'), widget=forms.EmailInput,required=False)
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput,min_length=4)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'contact_input'
            self.fields[field].error_messages = messages

    def clean_email(self):
        cd = self.cleaned_data
        username = cd['username']
        email = cd['email']

        if username == '' and email == '':
            raise forms.ValidationError(_('please enter email or username'))
        return email


class EmailForm(forms.Form):
    email = forms.EmailField(label=_('email'), widget=forms.EmailInput,required=False)
    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'contact_input'
            self.fields[field].error_messages = messages

    def clean_email(self):
        cd = self.cleaned_data['email']
        user = User.objects.filter(email = cd).first()
        if not user:
            raise forms.ValidationError(_('this email is not exists'))
        return cd


class UpdatePasswordForm(forms.Form): 
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput,min_length=4)
    password_confierm = forms.CharField(label=_('password_confierm'), widget=forms.PasswordInput, min_length=4)

    def clean_password_confierm(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_confierm'] and cd['password'] != cd['password_confierm']:
            raise forms.ValidationError(_("password and confirm password must be match "))
        
        return cd['password_confierm']
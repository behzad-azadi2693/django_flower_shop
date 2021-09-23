from django.contrib.auth import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.api import error, success
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from .forms import RegisterForm, LoginForm, UpdatePasswordForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate

def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:signout')

    if request.method == 'POST':
        form_create = RegisterForm(request.POST)
        if form_create.is_valid():
            cd = form_create.cleaned_data
            get_user_model().objects.create_user(username = cd['username'], email=cd['email'], password = cd['password'])
            messages.success(request,_('your submited is successfully'),success)
            return redirect('acounts:sigin')
        else:
            form_create = RegisterForm(request.POST)
            return render(request, 'register.html',{'form_create':form_create})
    else:
        form_create = RegisterForm()
        return render(request, 'register.html', {'form_create':form_create})

def signin(request):
    if request.user.is_authenticated:
        return redirect('accounts:logout')

    if request.method == 'POST':
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            cd = form_login.cleaned_data
            if cd['username']:
                user = get_user_model().objects.filter(username = cd['username']).first()
                if not user:
                    messages.warning(request, _('please check username or email'), error)
                    return redirect('accounts:signin')

            elif cd['email']:
                user = get_user_model().objects.filter(email = cd['email']).first()
                if not user:
                    messages.warning(request, _('please check username or email'), error)
                    return redirect('accounts:signin')

            user_auth = authenticate(username = user.username, password = cd['password'])
            login(request,user_auth)
            return redirect('product:index')

        else:
            form_login = LoginForm(request.POST)
            return render(request, 'register.html', {'form_login':form_login})
    else:
        form_login = LoginForm()
        return render(request, 'register.html', {'form_login':form_login})


@login_required
def profile(request):
    if request.method == "POST":
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj = get_object_or_404(get_user_model(), username=request.user.username)
            obj.set_password(cd['password'])
            return redirect('accounts:profile')
        else:
            form = UpdatePasswordForm(request.POST)
            return render(request, 'myaccount.html',{'form':form})
    else:
        form = UpdatePasswordForm()
        return render(request, 'myaccount.html',{'form':form})


@login_required
def signout(request):
    logout(request)
    return redirect('accounts:signin')
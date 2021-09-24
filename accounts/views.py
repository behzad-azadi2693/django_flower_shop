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
from django.utils import translation


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:signout')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            get_user_model().objects.create_user(username = cd['username'], email=cd['email'], password = cd['password'])
            messages.success(request,_('your submited is successfully'),success)
            return redirect('acounts:sigin')
        else:
            form = RegisterForm(request.POST)
            messages.warning(request, _('please check fields'),'warning')
            return render(request, 'register.html',{'form':form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('accounts:logout')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
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
            messages.success(request, _('your login to site successfull'),'success')
            return redirect('product:index')

        else:
            form = LoginForm(request.POST)
            messages.warning(request, _('please check fields'),'warning')
            return render(request, 'register.html', {'form':form})
    else:
        form = LoginForm()
        return render(request, 'register.html', {'form':form})


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
    messages.success(request,_('your logout successfull'), 'success')
    return redirect('accounts:signin')


from django.utils.translation import LANGUAGE_SESSION_KEY
from django.conf import settings
from django.http import HttpResponse
from django.utils import translation

def change_language(request, name):
                   
    user_language = name
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    response = HttpResponse(...)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
    return redirect('product:index')

from django import urls
from django.urls import path
from .views import signin, signup, profile,signout

app_name = 'accounts'

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('profile/', profile, name='profile'),
]
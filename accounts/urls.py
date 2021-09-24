from django import urls
from django.urls import path
from .views import signin, signup, profile,signout, change_language, recovery

app_name = 'accounts'

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('profile/', profile, name='profile'),
    path('recovery/', recovery, name='recovery'),
    path('change_language/<str:name>/',change_language, name='change_language'),
]
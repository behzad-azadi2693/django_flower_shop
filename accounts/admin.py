from django.contrib import admin
from .models import User
from .forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



@admin.register(User)
class AdminUser(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_admin', 'is_active')
    list_filter = ('is_admin', )

    fieldsets = ( #this is for form
        (_('Information Personal'),{'fields':('username','email','password')}),
        (_('access info'),{'fields':('is_active','is_admin')}),
        (_('information try'),{'fields':('count','date_for_wait')}),
        (_('permission'),{'fields':('groups', 'user_permissions')}),
    )
    add_fieldsets = (#this is for add_form 
        (_('Information personal'),{'fields':('username', 'email', 'password','password_confierm')}),
        (_('information try'),{'fields':('count', 'date_for_wait')}),
        (_('Access'),{'fields':('is_active','is_admin', 'groups', 'user_permissions')})
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    actions = ('make_admin',)

    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)

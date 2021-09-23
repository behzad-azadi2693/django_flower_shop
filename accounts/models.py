from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not username:
            raise ValueError(_('please insert username'))

        if not email:
            raise ValueError(_('please insert email'))

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, unique=True, verbose_name=_('user_name'))
    email = models.EmailField(unique=True, verbose_name=_('your email'))
    count = models.IntegerField(default=0, verbose_name=_('count password insert'))
    date_for_count = models.DateTimeField(null=True, blank=True, verbose_name=_('set time for wait'))

    is_active = models.BooleanField(default=True, verbose_name=_('user is active?'))
    is_admin = models.BooleanField(default=False, verbose_name=_('user is admin?'))

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = _('User Model')
        verbose_name_plural = _('Users Model')

    def __str__(self):
        return f'{self.username}-{self.email}'
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        
    @property
    def is_staff(self):
        return self.is_admin

   
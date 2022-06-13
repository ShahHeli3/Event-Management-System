from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField

from .manager import UserManager
from .validations import validate_username, validate_name


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    username = models.CharField(verbose_name='Username', max_length=200, unique=True, validators=[validate_username])
    first_name = models.CharField(verbose_name='First Name', max_length=200, validators=[validate_name])
    last_name = models.CharField(verbose_name='Last Name', max_length=200, validators=[validate_name])
    contact_number = PhoneNumberField(verbose_name='Contact Number', unique=True)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics/', null=True, blank=True)
    is_event_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'contact_number']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_event_manager

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_event_manager

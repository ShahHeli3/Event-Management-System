from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, username, f_name, l_name, contact_num, password=None, password2=None):
        """
        Creates and saves a User with the given email, username, f_name, l_name, contact_num and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            f_name=f_name,
            l_name=l_name,
            contact_num=contact_num,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, f_name, l_name, contact_num, password=None):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            f_name=f_name,
            l_name=l_name,
            contact_num=contact_num,
        )
        user.is_event_manager = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    username = models.CharField(verbose_name='Username', max_length=200, unique=True)
    f_name = models.CharField(verbose_name='First Name', max_length=200)
    l_name = models.CharField(verbose_name='Last Name', max_length=200)
    contact_num = PhoneNumberField()
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    is_event_manager = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'f_name', 'l_name', 'contact_num']

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

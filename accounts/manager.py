from django.contrib.auth.models import BaseUserManager

from constants import USER_MANAGER


class UserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        """
        Creates and saves a User with the given email, username, first_name, last_name, contact_number, profile_image and password
        """
        if not kwargs.get('email'):
            raise ValueError(USER_MANAGER)

        kwargs.pop("password2", None)
        user = self.model(**kwargs)

        user.set_password(kwargs.get('password'))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, contact_number, password=None):
        """
        Creates and saves a superuser with the given email, username, first_name, last_name, contact_number, profile_image and
        password
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
        )
        user.is_event_manager = True
        user.save(using=self._db)
        return user

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.save(self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    objects = UserManager()
    USERNAME_FIELD = "email"

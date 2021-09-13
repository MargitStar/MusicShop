from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from genre.models import Genre
from user.managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    ADMIN = "admin"
    STAFF = "staff"
    STATUS = [(ADMIN, "Admin User"), (STAFF, "Staff User")]
    username = models.CharField("username", max_length=100, unique=True)
    email = models.EmailField("email", unique=True, blank=True, null=True)
    group = models.CharField(max_length=100, default="User")
    favourite_genre = models.ManyToManyField(Genre, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    def __str__(self):
        return self.username

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(_('nickname'), max_length=255, unique=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
    objects = CustomUserManager()

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'user'


class Post(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.TextField(blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['author_id', 'post_text']

    class Meta:
        db_table = "post"

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager

from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    nickname = models.CharField(_('nickname'), max_length=255, unique=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")

    is_staff = True
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']
    objects = CustomUserManager()

    def __str__(self):
        return self.nickname

    def get_photo_url(self):
        return settings.MEDIA_URL + str(self.photo)

    @classmethod
    def get_by_nickname(cls, pk, nickname):
        try:
            return cls.objects.exclude(pk=pk).get(nickname=nickname)
        except cls.DoesNotExist:
            return False

    @classmethod
    def get_by_email(cls, pk, email):
        try:
            return cls.objects.exclude(pk=pk).get(email=email)
        except cls.DoesNotExist:
            return False

    class Meta:
        db_table = 'user'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post_text = models.TextField(blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['author_id', 'post_text']

    class Meta:
        db_table = "post"

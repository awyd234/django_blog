# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from config import settings
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from userena.models import UserenaLanguageBaseProfile, UserenaBaseProfile

# Create your models here.


class User(AbstractUser):
    last_login_ip = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    ip_joined = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)

    last_login_time = models.DateTimeField('上次登录时间', auto_now_add=True)
    last_update_time = models.DateTimeField('上次修改时间', auto_now=True)

    def __str__(self):
        return self.username

    # def save(self, *args, **kwargs):
    #     if not self.nickname:
    #         self.nickname = self.username


class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='user_profile')
    register_time = models.DateTimeField('注册时间', auto_now_add=True)
    last_login_time = models.DateTimeField('上次登录时间', auto_now_add=True)
    last_update_time = models.DateTimeField('上次修改时间', auto_now=True)
    phone_number = models.CharField('手机号', max_length=11)
    language = models.CharField('语言', default='en', max_length=10)

    # def __str__(self):
    #     return self.user

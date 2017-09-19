# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.contrib.auth.models import User
import os
# Create your models here.


class BookInfo(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    imgurl = models.CharField(max_length=2048)
    score = models.IntegerField()
    path = models.CharField(max_length=150)
    file = models.FileField(upload_to='./upload/', default='./upload/aaa')

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        ordering = ('-score',)

class UserProfile(models.Model):
    user = models.OneToOneField(User) # 关联自带的User结构
    score = models.IntegerField(default=1)
    userType = models.IntegerField(default=0)

class UserForm(forms.Form):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)
    email = forms.EmailField()

class UserFormLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class UploadFileForm(forms.Form):
    file = forms.FileField()
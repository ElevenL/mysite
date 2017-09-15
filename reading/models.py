# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
# Create your models here.


class BookInfo(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    imgurl = models.CharField(max_length=2048)
    score = models.IntegerField()
    path = models.CharField(max_length=150)
    file = models.FileField(upload_to='./upload/', default='./upload/aaa')
    class Meta:
        ordering = ('-score',)

class User(AbstractUser, models.Model):
    Points = models.IntegerField(default=0)
    accountType = models.IntegerField(default=0)

    class Meta(AbstractUser.Meta):
        pass


class UserForm(forms.Form):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)
    email = forms.EmailField()

class UserFormLogin(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField()
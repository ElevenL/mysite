# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django import forms

class BookInfo(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    imgurl = models.CharField(max_length=2048)
    score = models.IntegerField()
    path = models.CharField(max_length=150)
    file = models.FileField(upload_to='./upload/', default='./upload/aaa')
    class Meta:
        ordering = ('-score',)

class UserInfo(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)



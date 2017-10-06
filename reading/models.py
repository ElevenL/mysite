# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
import django.utils.timezone as timezone
from django.contrib.auth.models import User
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class BookInfo(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    imgurl = models.CharField(max_length=2048, blank=True, default='http://readfree.me/static/img/kindle-boy.png')
    score = models.IntegerField()
    path = models.CharField(max_length=150)
    file = models.FileField(upload_to='./upload/', default='./upload/aaa')

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        ordering = ('-score',)

class BookInfoForm(forms.ModelForm):
    class Meta:
        model = BookInfo
        exclude = ('path',)

class DownloadRecord(models.Model):
    username = models.CharField(max_length=50)
    bookname = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    downtime = models.DateTimeField(default = timezone.now)
    filename = models.CharField(max_length=150, blank=True, default='')

class UploadRecord(models.Model):
    username = models.CharField(max_length=50)
    bookname = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    downtime = models.DateTimeField(default = timezone.now)
    filename = models.CharField(max_length=150, blank=True, default='')

class SearchRecord(models.Model):
    username = models.CharField(max_length=50)
    keyword = models.CharField(max_length=150)
    searchtime = models.DateTimeField(default = timezone.now)

class TaskRecode(models.Model):
    askuser = models.CharField(max_length=50)
    bookname = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    asktime = models.DateTimeField(default=timezone.now)
    score = models.IntegerField()
    format = models.CharField(max_length=50, default='any')
    status = models.IntegerField(default=0)
    solutionuser = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ('-asktime',)

class TaskForm(forms.Form):
    bookname = forms.CharField(max_length=150)
    author = forms.CharField(max_length=150)
    imgurl = forms.CharField(max_length=2048,required=False)
    score = forms.IntegerField()
    format = forms.CharField(max_length=50)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # 关联自带的User结构
    score = models.IntegerField(default=5)
    userType = models.IntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

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

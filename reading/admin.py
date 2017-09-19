# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from reading.models import *

# Register your models here.

class BookInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author')

class ProfileInline(admin.StackInline):
    model = UserProfile
    verbose_name = 'profile'

class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

admin.site.register(BookInfo, BookInfoAdmin)
admin.site.unregister(User) # User是已经注册过的，所以首先需要解绑注册
admin.site.register(User, UserAdmin)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from reading.models import *

# Register your models here.

class BookInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'imgurl')
    search_fields = ('name', 'author')
    admin_order_field = 'name'

class DownloadRecordAdmin(admin.ModelAdmin):
    list_display = ('bookname', 'author', 'downtime', 'username')
    search_fields = ('bookname', 'author', 'downtime', 'username')

class UploadRecordAdmin(admin.ModelAdmin):
    list_display = ('bookname', 'author', 'downtime', 'username')
    search_fields = ('bookname', 'author', 'downtime', 'username')

class TaskRecodeAdmin(admin.ModelAdmin):
    list_display = ('bookname', 'author', 'asktime')
    search_fields = ('bookname', 'author', 'asktime')

class ProfileInline(admin.StackedInline):
    model = UserProfile
    verbose_name = 'profile'

class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)

admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(DownloadRecord, DownloadRecordAdmin)
admin.site.register(UploadRecord, UploadRecordAdmin)
admin.site.register(TaskRecode, TaskRecodeAdmin)
admin.site.unregister(User) # User是已经注册过的，所以首先需要解绑注册
admin.site.register(User, UserAdmin)

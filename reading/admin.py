# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from reading import models

# Register your models here.

class BookInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('name', 'author')

admin.site.register(models.BookInfo, BookInfoAdmin)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog import models

# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp')

admin.site.register(models.BlogPost, BlogPostAdmin)

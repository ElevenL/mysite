# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from blog.models import BlogPost

# Create your views here.

def archive(request):
    posts = BlogPost.objects.all()
    return render_to_response('archive.html', {'posts':posts})

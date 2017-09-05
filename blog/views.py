# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from blog.models import BlogPost, BlogPostForm
from datetime import datetime
from django.http import HttpResponseRedirect

# Create your views here.

def archive(request):
    posts = BlogPost.objects.all()[:10]
    return render(request, 'archive.html', {'posts':posts, 'form':BlogPostForm()})

def create_blogpost(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.timestamp = datetime.now()
            post.save()
    return HttpResponseRedirect('/blog/')
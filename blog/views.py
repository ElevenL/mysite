# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from blog.models import BlogPost, BlogPostForm
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

# Create your views here.

@csrf_protect
def archive(request):
    posts = BlogPost.objects.all()[:10]
    return render(request, 'index.html', {'posts':posts, 'form':BlogPostForm()})

def create_blogpost(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.timestamp = timezone.now()
            post.save()
    return HttpResponseRedirect('/blog/')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from reading.models import BookInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

# Create your views here.

@csrf_protect
def index(request):
    books = BookInfo.objects.all()[:2]
    return render(request, 'index.html', {'books':books})

def get_page(request):
    cus_list = BookInfo.objects.all()
    paginator = Paginator(cus_list, 2, 2)
    page = int(request.GET.get('page'))
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'books': books})
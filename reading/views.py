# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from reading.models import BookInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

# Create your views here.

# @csrf_protect
def index(request):
    books = BookInfo.objects.all()[:2]
    return render(request, 'index.html', {'books':books})

def get_page(request):
    page_pernum = 2
    page = int(request.GET.get('page', '2'))
    allBookCounts = BookInfo.objects.count()
    max_page = allBookCounts / page_pernum
    start_id = (page - 1) * page_pernum
    end_id = start_id + page_pernum
    page = 100
    books = BookInfo.objects.all()[start_id:end_id]
    return render(request, 'index.html', {'books': books, 'cpage':page})
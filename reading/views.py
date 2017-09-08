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
    page = int(request.GET.get('page', '1'))
    start_id = (page - 1) * 2
    end_id = start_id + 2
    books = BookInfo.objects.all()[start_id:end_id]
    return render(request, 'index.html', {'books': books})
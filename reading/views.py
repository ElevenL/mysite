# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from reading.models import BookInfo
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect

# Create your views here.

@csrf_protect
def index(request):
    books = BookInfo.objects.all()[:2]
    return render(request, 'index.html', {'books':books})

def get_page(request):
    page = int(request.GET.get('page'))
    print page
    print type(page)
    start_id = (page - 1) * 2 + 1
    end_id = start_id + 2
    books = BookInfo.objects.filter(id__range=(start_id,end_id))
    return render(request, 'index.html', {'books': books})
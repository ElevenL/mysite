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
    books = BookInfo.objects.all()
    return render(request, 'index.html', {'books':books})
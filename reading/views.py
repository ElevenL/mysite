# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from reading.models import BookInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def make_pages():
    pass


# @csrf_protect
def index(request):
    page_pernum = 2
    allBookCounts = BookInfo.objects.count()
    max_page = int(allBookCounts / page_pernum)
    # if max_page < 5:
    #     max_page = 5
    page = int(request.GET.get('page', '1'))
    if page > max_page:
        page = max_page
    elif page < 1:
        page = 1
    start_id = (page - 1) * page_pernum
    end_id = start_id + page_pernum
    books = BookInfo.objects.all()[start_id:end_id]
    last_page = 5
    if page <= 3:
        last_page =5
    elif page >= (max_page - 2):
        last_page = max_page
    else:
        last_page = page + 2
    if last_page > max_page:
        last_page = max_page
    if last_page >= 5:
        page_list = range(last_page - 4, last_page + 1)
    else:
        page_list = range(1, last_page + 1)
    if page_list[0] == 1:
        p_page = 1
    else:
        p_page = page_list[0] - 1
    if page_list[-1] == max_page:
        n_page = max_page
    else:
        n_page = page_list[-1] + 1
    return render(request, 'index.html',
                  {'books': books,
                   'cur_page': page,
                   'page_list': page_list,
                   'p_page': str(p_page),
                   'n_page': str(n_page)})

def search(request):
    page_pernum = 2
    name_kw = int(request.GET.get('q', 'all'))
    if name_kw == 'all':
        return index(request)
    else:
        search_content = BookInfo.objects.filter(name__icontains=name_kw)
    allBookCounts = len(search_content)
    max_page = int(allBookCounts / page_pernum)
    start_id = (page - 1) * page_pernum
    end_id = start_id + page_pernum
    page = 100
    books = BookInfo.objects.all()[start_id:end_id]
    return render(request, 'index.html', {'books': books, 'cur_page':page, 'max_page':max_page})
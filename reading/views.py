# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from reading.models import BookInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect
import urllib

# Create your views here.
def make_pages(cpage, allcount):
    '''

    :param cpage: 当前页数
    :param allcount: 数据总数
    :return:
    '''
    page_pernum = 2
    page = cpage
    max_page = int(allcount / page_pernum)
    if page > max_page:
        page = max_page
    elif page < 1:
        page = 1
    start_id = (page - 1) * page_pernum
    end_id = start_id + page_pernum
    last_page = 5
    if page <= 3:
        last_page = 5
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
    if len(page_list) == 0:
        p_page = ''
        n_page = ''
        start_id = 0
        end_id = 0
    else:
        if page_list[0] == 1:
            p_page = 1
        else:
            p_page = page_list[0] - 1
        if page_list[-1] == max_page:
            n_page = max_page
        else:
            n_page = page_list[-1] + 1
    return start_id,end_id,page_list,p_page,n_page

# @csrf_protect
def index(request):
    page = int(request.GET.get('page', '1'))
    allBookCounts = BookInfo.objects.count()
    start_id, end_id, page_list, p_page, n_page = make_pages(page, allBookCounts)
    books = BookInfo.objects.all()[start_id:end_id]
    return render(request, 'index.html',
                  {'books': books,
                   'cur_page': page,
                   'page_list': page_list,
                   'p_page': str(p_page),
                   'n_page': str(n_page)})

def search(request):
    name_kw = request.GET.get('q', 'all')
    page = int(request.GET.get('page', '1'))
    if name_kw == 'all':
        return index(request)
    else:
        search_content = BookInfo.objects.filter(name__icontains=name_kw)
    allBookCounts = len(search_content)
    start_id, end_id, page_list, p_page, n_page = make_pages(page, allBookCounts)
    books = search_content[start_id:end_id]
    return render(request, 'search.html',
                  {'books': books,
                   'cur_page': page,
                   'page_list': page_list,
                   'p_page': str(p_page),
                   'n_page': str(n_page),
                    'name_kw': urllib.unquote(name_kw)})
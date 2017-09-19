# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.shortcuts import render, render_to_response
from django import forms
import pdb
from django.http import StreamingHttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from reading.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect
import urllib
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def make_pages(cpage, allcount):
    '''
    处理分页
    :param cpage: 当前页数
    :param allcount: 数据总数
    :return:
    '''
    page_pernum = 20
    page = cpage
    if allcount == 0:
        max_page = 0
    elif (allcount % page_pernum) != 0:
        max_page = int(allcount / page_pernum) + 1
    else:
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

@login_required
def index(request):
    '''
    浏览书库
    :param request:
    :return:
    '''
    logging.debug(request.user)
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

@login_required
def search(request):
    '''
    书库搜索
    :param request:
    :return:
    '''
    page = int(request.GET.get('page', '1'))
    name_kw = request.GET.get('q', 'all')
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

@login_required
def download(request):
    '''
    下载图书
    :param request:
    :return:
    '''
    # do something...
    file_name = urllib.unquote(str(request.get_full_path().split('/')[-1]))
    file_path = ('/root/book/upload/' + file_name.decode('utf-8'))
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name.decode('utf-8'))

    return response

@login_required
def upload(request):
    if request.method == 'POST':
        form = BookInfo(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.path = '/download/' + post.file.name.spit('/')[-1]
            post.save()
    return HttpResponseRedirect('/')

@login_required
def uploadfile(request):
    if request.method == 'POST':
        uff = UploadFileForm(request.POST, request.FILES)
        logging.debug(uff.is_valid())
        if uff.is_valid():
            bookName = urllib.unquote(str(request.get_full_path().split('/')[-1])).decode('utf-8')
            bookInfo = BookInfo.objects.filter(name=bookName)[0]
            uploadfile = uff.cleaned_data['file']
            bookInfo.file = uploadfile
            logging.debug(bookInfo.file.filename)
            bookInfo.path = '/download/' + bookInfo.file.filename
            logging.debug(bookInfo.path)
            bookInfo.save()
    else:
        bookName = urllib.unquote(str(request.get_full_path().split('/')[-1])).decode('utf-8')
        bookInfo = BookInfo.objects.filter(name=bookName)[0]
        book = {}
        book['name'] = bookInfo.name
        book['author'] = bookInfo.author
        book['score'] = bookInfo.score
        return render(request, 'uploadfile.html', {'book':book})
    return HttpResponseRedirect('/')


def register(request):
    # curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());

    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            filterResult = User.objects.filter(username = username)
            if len(filterResult)>0:
                return render(request, 'register.html', {"errors":"用户名已存在"})
            else:
                password1 = uf.cleaned_data['password1']
                password2 = uf.cleaned_data['password2']
                errors = []
                if (password2 != password1):
                    errors.append("两次输入的密码不一致!")
                    return render(request, 'register.html',{'errors':errors[0]})
                email = uf.cleaned_data['email']
                user = User.objects.create_user(username=username,password=password1, email=email)
                # #返回注册成功页面
                return render(request, 'register_success.html')
        else:
            return render(request, 'register.html', {"errors": "表单不正确"})

    else:
        uf = UserForm()
    return render(request, 'register.html')

def userlogin(request):
    if request.method == "POST":
        ulf = UserFormLogin(request.POST)
        if ulf.is_valid():
            #获取表单信息
            logging.debug('uf is avlid!!!!!')
            username = ulf.cleaned_data['username']
            password = ulf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            logging.debug(username)
            logging.debug(password)
            logging.debug(user)
            if user is not None:
                login(request,user)
                request.session.set_expiry(12 * 3600)
                return HttpResponseRedirect('/')
            else:
                return render(request, "login.html", {'errors': "用户名密码不正确"})
    else:
        ulf = UserFormLogin()
    return render(request, "login.html")

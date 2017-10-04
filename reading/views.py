# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.shortcuts import render, render_to_response
from django import forms
import pdb
from django.core.mail import send_mail
from django.http import StreamingHttpResponse
from django.db.models import Q
from datetime import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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
    page_pernum = 24
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
    username = request.user.username
    nouwuser = User.objects.get(username=username)
    score = nouwuser.userprofile.score
    page = int(request.GET.get('page', '1'))
    allBookCounts = BookInfo.objects.count()
    start_id, end_id, page_list, p_page, n_page = make_pages(page, allBookCounts)
    books = BookInfo.objects.all()[start_id:end_id]
    return render(request, 'index.html',
                  {'books': books,
                   'username': username,
                   'score': score,
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
        search_content = BookInfo.objects.filter(Q(name__icontains=name_kw)|Q(author__icontains=name_kw))
    allBookCounts = len(search_content)
    start_id, end_id, page_list, p_page, n_page = make_pages(page, allBookCounts)
    books = search_content[start_id:end_id]
    username = request.user.username
    nouwuser = User.objects.get(username=username)
    score = nouwuser.userprofile.score
    return render(request, 'search.html',
                  {'books': books,
                   'username': username,
                   'score': score,
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
    username = request.user.username
    nouwuser = User.objects.get(username=username)
    nouwuser.userprofile.score = nouwuser.userprofile.score - 1
    if nouwuser.userprofile.score < 0:
        return HttpResponseRedirect('/')
    file_name = urllib.unquote(str(request.get_full_path().split('/')[-1]))
    file_path = ('/root/book/upload/' + file_name.decode('utf-8'))
    path = ('/download/' + file_name.decode('utf-8'))
    bookinfo = BookInfo.objects.filter(path=path)[0]
    dr = DownloadRecord(
        username=username,
        bookname=bookinfo.name,
        author=bookinfo.author,
        filename=bookinfo.file.name
    )
    logging.debug(username)
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
    dr.save()
    nouwuser.save()
    return response

@login_required
def upload(request):
    if request.method == 'POST':
        bif = BookInfoForm(request.POST, request.FILES)
        if bif.is_valid():
            filterresult = BookInfo.objects.filter(name=bif.cleaned_data['name'],author=bif.cleaned_data['author'])
            if len(filterresult) > 0:
                return render(request, 'upload.html', {'errors':'已经存在该书籍'})
            username = request.user.username
            logging.debug(username)
            nouwuser = User.objects.get(username=username)
            nouwuser.userprofile.score = nouwuser.userprofile.score + 1
            bookinfo = BookInfo(
                name = bif.cleaned_data['name'],
                author = bif.cleaned_data['author'],
                # imgurl = bif.cleaned_data['imgurl'],
                score = int(bif.cleaned_data['score']),
                file = bif.cleaned_data['file'],
                path = '/'
            )
            if bif.cleaned_data['imgurl'] != '':
                bookinfo.imgurl = bif.cleaned_data['imgurl']
            logging.debug(bif.cleaned_data['imgurl'])
            bookinfo.save()
            bookinfo.path = ('/download/' + bookinfo.file.name.split('/')[-1])
            bookinfo.save()
            nouwuser.save()
            ur = UploadRecord(
                username=username,
                bookname=bookinfo.name,
                author=bookinfo.author,
                filename=bookinfo.file.name
            )
            ur.save()
            return HttpResponseRedirect('/')
    else:
        username = request.user.username
        nouwuser = User.objects.get(username=username)
        score = nouwuser.userprofile.score
    return render(request, 'upload.html', {'username': username, 'score':score})

@login_required
def uploadfile(request):
    if request.method == 'POST':
        uff = UploadFileForm(request.POST, request.FILES)
        if uff.is_valid():
            username = request.user.username
            logging.debug(username)
            nouwuser = User.objects.get(username=username)
            nouwuser.userprofile.score = nouwuser.userprofile.score + 1
            bookName = urllib.unquote(str(request.get_full_path().split('/')[-1])).decode('utf-8')
            uploadfile = uff.cleaned_data['file']
            bookInfos = BookInfo.objects.filter(name=bookName)
            for bookInfo in bookInfos:
                if bookInfo.path == '/':
                    bookInfo.file = uploadfile
                    bookInfo.save()
                    bookInfo.path = ('/download/' + bookInfo.file.name.split('/')[-1])
                    bookInfo.save()
                    nouwuser.save()
                    ur = UploadRecord(
                        username=username,
                        bookname=bookInfo.name,
                        author=bookInfo.author,
                        filename=bookInfo.file.name
                    )
                    ur.save()
                    break
        return HttpResponseRedirect('/')
    else:
        bookName = urllib.unquote(str(request.get_full_path().split('/')[-1])).decode('utf-8')
        bookInfo = BookInfo.objects.filter(name=bookName)[0]
        book = {}
        book['name'] = bookInfo.name
        book['author'] = bookInfo.author
        book['score'] = bookInfo.score

        username = request.user.username
        nouwuser = User.objects.get(username=username)
        score = nouwuser.userprofile.score
        return render(request, 'uploadfile.html', {'book':book, 'username':username, 'score':score})

@login_required
def dotask(request):
    if request.method == 'POST':
        uff = UploadFileForm(request.POST, request.FILES)
        if uff.is_valid():
            username = request.user.username
            logging.debug(username)
            nouwuser = User.objects.get(username=username)
            nouwuser.userprofile.score = nouwuser.userprofile.score + 2
            bookName = urllib.unquote(str(request.get_full_path().split('/')[-1])).decode('utf-8')
            uploadfile = uff.cleaned_data['file']
            bookInfos = BookInfo.objects.filter(name=bookName)
            for bookInfo in bookInfos:
                if bookInfo.path == '/':
                    bookInfo.file = uploadfile
                    bookInfo.save()
                    bookInfo.path = ('/download/' + bookInfo.file.name.split('/')[-1])
                    bookInfo.save()
                    nouwuser.save()
                    ur = UploadRecord(
                        username=username,
                        bookname=bookInfo.name,
                        author=bookInfo.author,
                        filename=bookInfo.file.name
                    )
                    ur.save()
                    trs = TaskRecode.objects.filter(bookname=bookInfo.name, author=bookInfo.author)
                    for tr in trs:
                        if tr.status == 0:
                            tr.status =1
                            tr.solutionuser = username
                            tr.save()
                            break
                    break
        return HttpResponseRedirect('/task/')
    else:
        bookName = urllib.unquote(str(request.get_full_path().split('/')[-1])).decode('utf-8')
        bookInfo = BookInfo.objects.filter(name=bookName)[0]
        book = {}
        book['name'] = bookInfo.name
        book['author'] = bookInfo.author
        book['score'] = bookInfo.score

        username = request.user.username
        nouwuser = User.objects.get(username=username)
        score = nouwuser.userprofile.score
        return render(request, 'uploadfile.html', {'book':book, 'username':username, 'score':score})


@login_required
def task(request):
    username = request.user.username
    nouwuser = User.objects.get(username=username)
    score = nouwuser.userprofile.score
    tasks = TaskRecode.objects.all()
    return render(request, 'task.html',
                  {'tasks': tasks,
                   'username': username,
                   'score':score,
                   'errors':None})

@login_required
def createtask(request):
    username = request.user.username
    nouwuser = User.objects.get(username=username)
    score = nouwuser.userprofile.score
    if request.method == 'POST':
        tf = TaskForm(request.POST)
        logging.debug(tf)
        if tf.is_valid():
            filterresult = BookInfo.objects.filter(name=tf.cleaned_data['bookname'], author=tf.cleaned_data['author'])
            if len(filterresult) == 0:
                bookinfo = BookInfo(
                    name=tf.cleaned_data['bookname'],
                    author=tf.cleaned_data['author'],
                    score=int(tf.cleaned_data['score']),
                    path='/'

                )
                if tf.cleaned_data['imgurl'] != '':
                    bookinfo.imgurl = tf.cleaned_data['imgurl']
                bookinfo.save()
            taskrecord = TaskRecode(
                askuser = username,
                bookname = tf.cleaned_data['bookname'],
                author = tf.cleaned_data['author'],
                score = int(tf.cleaned_data['score']),
                format = tf.cleaned_data['format'],
            )
            taskrecord.save()
            return HttpResponseRedirect('/task/')
    else:
        pass
    return render(request, 'createtask.html',
                  {'username': username,
                   'score':score,
                   'errors':None})


@login_required
def contact(request):
    username = request.user.username
    nouwuser = User.objects.get(username=username)
    score = nouwuser.userprofile.score
    if request.method == 'POST':
        email = request.POST['email']
        content = request.POST['content']
        logging.debug(email)
        logging.debug(content)
        send_mail('From Reading contact', 'user:%s\r\nmail:%s\r\n%s' % (username, email, content), '554824553@qq.com', ['lhq2818@163.com'], fail_silently=False)
        return HttpResponseRedirect('/')
    else:
        pass
    return render(request, 'contact.html', {'username':username, 'score':score})


def register(request):
    errors = ''
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            logging.debug(username)
            filterResult = User.objects.filter(username = username.encode('utf-8'))
            if len(filterResult)>0:
                errors = "用户名已存在！"
                return render(request, 'register.html', {"errors":errors})
            else:
                password1 = uf.cleaned_data['password1']
                password2 = uf.cleaned_data['password2']
                email = uf.cleaned_data['email']
                user = User.objects.create_user(username=username,password=password1, email=email)
                login(request, user)
                request.session.set_expiry(12 * 3600)
                return render(request, 'register_success.html')
        else:
            errors = "提交的信息不正确！"
            return render(request, 'register.html', {"errors": errors})

    else:
        uf = UserForm()
    return render(request, 'register.html', {"errors": errors})

def userlogin(request):
    errors = ''
    if request.method == "POST":
        ulf = UserFormLogin(request.POST)
        if ulf.is_valid():
            #获取表单信息
            username = ulf.cleaned_data['username']
            password = ulf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if (user.last_login.date() != datetime.today().date()):
                    user.userprofile.score = user.userprofile.score + 1
                    user.save()
                login(request,user)
                request.session.set_expiry(12 * 3600)
                return HttpResponseRedirect('/')
            else:
                errors = "用户名密码不正确!"
                return render(request, "login.html", {'errors':errors})
    else:
        ulf = UserFormLogin()
    return render(request, "login.html", {'errors':errors})

@login_required
def changepassword(request):
    errors = ''
    username = request.user.username
    nouwuser = User.objects.get(username=username)
    score = nouwuser.userprofile.score
    if request.method == "POST":
        oldpassword = request.POST['password']
        user = authenticate(username=username, password=oldpassword)
        if user is not None and user.is_active:
            newpassword = request.POST['password1']
            user.set_password(newpassword)
            user.save()
            return HttpResponseRedirect('/')
        else:
            errors = "原密码不正确！"
    else:
        pass
    return render(request, "changepassword.html", {'username': username, 'score':score, 'errors':errors})



@login_required
def userlogout(request):
    logout(request)
    return HttpResponseRedirect("/login/")
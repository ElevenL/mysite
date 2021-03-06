"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import *
from django.contrib import admin
from django.views.generic import RedirectView
from reading import views
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^blog/', include('blog.urls')),
    url(r'^search/', views.search),
    url(r'^download/', views.download),
    url(r'^register/', views.register),
    url(r'^login/', views.userlogin),
    url(r'^logout/', views.userlogout),
    url(r'^changepassword/', views.changepassword),
    url(r'^uploadfile/', views.uploadfile),
    url(r'^upload/', views.upload),
    url(r'^dotask/', views.dotask),
    url(r'^contact/', views.contact),
    url(r'^createtask/', views.createtask),
    url(r'^task/', views.task),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

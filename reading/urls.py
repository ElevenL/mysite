from django.conf.urls import *
from reading.views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^reading/(?P<page>[0-9]+)/$', get_page)
]
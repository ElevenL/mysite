from django.conf.urls import *
from reading.views import *

urlpatterns = [
    url(r'^reading/\?page', get_page),
    url(r'^$', index),
]
from django.conf.urls import *
from reading.views import *

urlpatterns = [
    url(r'^$', index),
    # url(r'^reading/\?page', get_page),
]
from django.conf.urls import *
from reading.views import *

urlpatterns = [
    url(r'^look/', get_page),
    url(r'^$', index),
]
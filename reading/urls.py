from django.conf.urls import *
from reading.views import *

urlpatterns = [
    url(r'^$', index),
]
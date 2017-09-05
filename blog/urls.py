from django.conf.urls import *
from blog.views import *

urlpatterns = [
    url(r'^$', archive),
]

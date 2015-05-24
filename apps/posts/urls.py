from django.conf.urls import patterns
from django.conf.urls import url
from apps.posts.views import *

urlpatterns = patterns("apps.posts.views",
                       url(r'^$', Homepage.as_view(), name='home'),
                       url(r'posts/add-post/$', 'addpost', name='add-post')
                       )
from django.conf.urls import patterns
from django.conf.urls import url
from apps.posts.views import *

urlpatterns = patterns("apps.posts.views",
                       url(r'^$', Homepage.as_view(), name='home'),
                       url(r'^posts/add-post/$', 'addpost', name='add-post'),
                       url(r'^posts/preview/(?P<id>\d+)/$', Preview.as_view(), name='preview'),
                       url(r'^post-edit/(?P<id>\d+)/$', PostEdit.as_view(), name='edit-post'),
                       url(r'^category/(?P<category>\w+)/type/(?P<type>\w+)/$', CategoryList.as_view(), name='category-post'),
                       url(r'^post-detail/(?P<id>\d+)/$', PostDetail.as_view(), name='post-detail')
                       )
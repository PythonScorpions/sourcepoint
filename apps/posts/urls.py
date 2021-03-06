from django.conf.urls import patterns
from django.conf.urls import url
from apps.posts.views import *

urlpatterns = patterns("apps.posts.views",
                       url(r'^$', Homepage.as_view(), name='home'),
                       url(r'^posts/add-post/$', 'addpost', name='add-post'),
                       url(r'^posts/preview/(?P<id>\d+)/$', Preview.as_view(), name='preview'),
                       url(r'^post-edit/(?P<id>\d+)/$', PostEdit.as_view(), name='edit-post'),
                       url(r'^category/(?P<category>[\w-]+)/type/(?P<type>\w+)/$', CategoryList.as_view(), name='category-post'),
                       url(r'^post-detail/(?P<slug>[\w-]+)/$', PostDetail.as_view(), name='post-detail'),
                       url(r'^my-posting/$',MyPosting.as_view(), name='my-posting'),
                       url(r'^posting-details/(?P<id>\d+)/$', MyPostDetail.as_view(), name='posting-detail'),
                       url(r'^post-delete/(?P<id>\d+)/$','postdelete', name='delete-post'),
                       url(r'^job-detail-contact/(?P<slug>[\w-]+)/$', PostContact.as_view(), name='post-contact'),
                       url(r'^send-contact/(?P<slug>[\w-]+)/$', SendContact.as_view(), name='send-contact'),
                       url(r'^my-interests/$', MyInterests.as_view(), name='my-interests'),
                       url(r'^my-interest-detail/(?P<slug>[\w-]+)/$', MyInterestDetail.as_view(), name='interest-detail'),
                       url(r'^delete-interest/(?P<slug>[\w-]+)/$', 'delete_interest',name='delete-interest'),
                       url(r'^search/$', SearchResults.as_view(), name='search'),
                       url(r'^posts/buy/$', PostsBuy.as_view(), name='posts-buy'),
                       )
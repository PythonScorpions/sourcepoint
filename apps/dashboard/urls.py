from django.conf.urls import patterns
from django.conf.urls import url
from apps.dashboard.views import *

urlpatterns = patterns("apps.dashboard.views",
                       url(r'^$', AdminLoginpage.as_view(), name='admin_login'),
                       url(r'^home/$', HomePage.as_view(), name='home'),
                       url(r'^user-profiles/$', UserLists.as_view(), name='user-lists'),
                       url(r'^user-details/(?P<pk>\d+)/$', UserDetails.as_view(), name='user-details'),
                       url(r'^deactivate-user/(?P<pk>\d+)/$', 'deactivate_user', name='deactivate-user'),
                       url(r'^subscription-lists/$', UserSubscriptionList.as_view(), name='subscriptions'),
                       url(r'^subscription-detail/(?P<pk>\d+)/$', SubscriptionDetails.as_view(), name='subscription-detail'),
                       url(r'^plan-lists/$', PlanLists.as_view(), name='plan-lists'),
                       url(r'add-plan/$', AddPlan.as_view(), name='add-plan'),
                       url(r'edit-plan/(?P<id>\d+)/$', EditPlan.as_view(), name='edit-plan'),
                       url(r'^delete-plan/(?P<id>\d+)/$', 'delete_plan', name='delete-plan'),
                       url(r'^category-lists/$', CategoryLists.as_view(), name='category-list'),
                       url(r'^category-add/$', CategoryAdd.as_view(), name='add-category'),
                       url(r'edit-category/(?P<id>\d+)/$', EditCategory.as_view(), name='edit-category'),
                       url(r'^delete-category/(?P<id>\d+)/$', 'delete_view', name='delete-view'),
                       url(r'^technology-tags/$', TechnologyTagsList.as_view(), name='tags-list'),
                       url(r'^edit-tags/(?P<id>\d+)/$', EditTags.as_view(), name='edit-tags'),
                       url(r'^delete-tags/(?P<id>\d+)/$', 'delete_tag', name='delete-tags'),
                       url(r'^add-tag/$', AddTag.as_view(), name='add-tag'),
                       url(r'^post-list/$', PostLists.as_view(), name='post-list'),
                       url(r'^user-post-details/(?P<slug>[\w-]+)/$', PostDetail.as_view(), name='user-post-detail'),
                       url(r'admin-logout/$', 'admin_logout', name='admin-logout'),
                       url(r'^payment-details/$', PaymentLists.as_view(), name='paypal-lists'),
                       url(r'^add-about/$', About.as_view(), name='about-us'),
                       url(r'^status-plan/(?P<id>\d+)/$', 'plan_status', name='plan-status')
                       )
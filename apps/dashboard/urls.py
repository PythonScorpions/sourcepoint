from django.conf.urls import patterns
from django.conf.urls import url
from apps.dashboard.views import *

urlpatterns = patterns("apps.dashboard.views",
                       url(r'^$', AdminLoginpage.as_view(), name='admin_login'),
                       url(r'^home/$', HomePage.as_view(), name='home'),
                       url(r'^user-profiles/$', UserLists.as_view(), name='user-lists'),
                       url(r'subscription-lists/$', UserSubscriptionList.as_view(), name='subscriptions'),
                       url(r'plan-lists/$', PlanLists.as_view(), name='plan-lists'),
                       url(r'add-plan/$', AddPlan.as_view(), name='add-plan'),
                       url(r'delete-plan/(?P<id>\d+)//$', 'delete_plan', name='delete-plan')
                       )
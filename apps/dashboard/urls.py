from django.conf.urls import patterns
from django.conf.urls import url
from apps.dashboard.views import *

urlpatterns = patterns("",
                       url(r'^$', AdminLoginpage.as_view(), name='admin_login'),
                       url(r'^home/$', HomePage.as_view(), name='home'),
                       url(r'^user-profiles/$', UserLists.as_view(), name='user-lists'),
                       url(r'subscription-lists/$', UserSubscriptionList.as_view(), name='subscriptions'),
                       url(r'plan-lists/$', PlanLists.as_view(), name='plan-lists')
                       )
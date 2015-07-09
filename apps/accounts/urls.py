from django.conf.urls import patterns
from django.conf.urls import url
from apps.accounts.views import *

urlpatterns = patterns("apps.accounts.views",
                       url(r'^login/$', Loginpage.as_view(), name='login'),
                       url(r'^register/$', 'register', name='register'),
                       url(r'subscribe/$', 'subscribe', name='subscribe'),
                       url(r'^verification/(?P<key>\w+)/$', Verification.as_view(), name='verification'),
                       url(r'send-email/$', 'mail_sent', name='send-email'),
                       url(r'email-verification/(?P<key>\w+)/$', 'email_verification', name='email-verification'),
                       url(r'^thanku/$', Thankyou.as_view(), name='thankyou'),
                       url(r'^foreget-password/$', ForegetPassword.as_view(), name='foreget-password'),
                       url(r'^reset-password/(?P<key>\w+)/$', ResetPassword.as_view(), name='reset-password'),
                       url(r'^update-profile/$', UpdateProfile.as_view(), name='update-profile'),
                       url(r'^myplan/$', MyPlan.as_view(), name='my-plan'),
                       url(r'^settings/$', Settings.as_view(), name='settings'),
                       url(r'^save-setings', 'save_settings', name='save-settings'),
                       url(r'^logout/$','user_logout', name='user_logout'),
                       url(r'^change-plan/$', ChangePlan.as_view(), name='change-plan'),
                       url(r'^change-password/$', ChangePassword.as_view(), name='change-password'),
                       url(r'^aboutus/$', About.as_view(), name='aboutus'),
                       url(r'^contact/$', Contact.as_view(), name='contact'),
                       url(r'^payment/$', 'checkout', name='payment'),
                       url(r'^card-pay/$', CardPayment.as_view(), name='card-pay'),
                       url(r'^custom_ipn/','custom_ipn', name = 'custom_ipn'),
                       )
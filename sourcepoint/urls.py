"""sourcepoint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from billing import get_integration

stripe_obj = get_integration("stripe",)
braintree = get_integration("braintree_payments")

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('apps.posts.urls')),
    url(r'^accounts/',include('apps.accounts.urls')),
    url(r'dashboard/',include('apps.dashboard.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^stripe/', include(stripe_obj.urls)),
    url(r'^braintree/', include(braintree.urls)),
]
urlpatterns += patterns('',
        (r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT,'show_indexes': False}),
    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


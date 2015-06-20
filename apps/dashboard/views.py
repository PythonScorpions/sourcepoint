
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView
from django.views.generic import View
import json
from django.template import RequestContext, Context
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from apps.accounts.models import *


class AdminLoginpage(TemplateView):

    template_name = 'dashboard/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active and user.is_superuser:
                login(request, user)
                return redirect('/dashboard/home/')
            else:
                messages.success(request, "You Don't Have Enough Permission to View this Page")
        else:
            messages.success(request, "Invalid Username or Password")
        return render_to_response(self.template_name, context_instance=RequestContext(request),)

class HomePage(TemplateView):

    template_name = 'dashboard/adminindex.html'


class UserLists(TemplateView):

    template_name = 'dashboard/users.html'

    def get_context_data(self, **kwargs):
        context = super(UserLists, self).get_context_data(**kwargs)
        context['users'] = UserProfiles.objects.all()
        return context

class UserSubscriptionList(TemplateView):
    template_name = 'dashboard/user-subscriptions.html'

    def get_context_data(self, **kwargs):
        context = super(UserSubscriptionList, self).get_context_data(**kwargs)
        context['subscriptions'] = UserSubscriptions.objects.all()
        return context

class PlanLists(TemplateView):
    template_name = 'dashboard/plan-list.html'

    def get_context_data(self, **kwargs):
        context = super(PlanLists, self).get_context_data(**kwargs)
        context['plans'] = SubscriptionPlan.objects.all()
        return context


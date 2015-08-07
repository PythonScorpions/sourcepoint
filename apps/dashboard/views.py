
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, DetailView, ListView
from django.views.generic import View
import json
from django.template import RequestContext, Context
from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from paypal.standard.ipn.models import PayPalIPN
from apps.accounts.models import *
from apps.dashboard.forms import PlanForm, CategoryForm, TagForm


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



def deactivate_user(request, pk):
    template_name = 'dashboard/users.html'
    user = User.objects.get(id=pk)
    if user.is_active == True:
        user.is_active = False
        user.save()
    elif user.is_active == False:
        print "sdvsfsffsdfs", user.is_active
        user.is_active = True
        user.save()
    else:
        pass
    return redirect('/dashboard/user-profiles/')
    return render_to_response(self.template_name, content_instance=RequestContext(request),)

# class DeactivateUser(TemplateView):
#     template_name = 'dashboard/users.html'
#
#     def post(self, request, *args, **kwargs):
#         user = User.objects.get(id=kwargs['id'])
#         if user.is_active == True:
#             user.is_active == False
#             user.save()
#             return redirect('/user-profiles/')
#         elif user.is_active == False:
#             user.is_active == True
#             user.save()
#             return redirect('/user-profiles/')
#         else:
#             pass
#             return redirect('/user-profiles/')

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


class AddPlan(TemplateView):
    template_name = 'dashboard/add-plan.html'
    form_class = PlanForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/plan-lists/')
        else:
            print "errors",form.errors
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

class EditPlan(TemplateView):
    template_name = 'dashboard/edit-plan.html'
    form_class = PlanForm

    def get(self, request, *args, **kwargs):
        plan = SubscriptionPlan.objects.get(id=kwargs['id'])
        form = self.form_class(instance=plan)
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        plan = SubscriptionPlan.objects.get(id=kwargs['id'])
        form = self.form_class(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/plan-lists/')
        else:
            print "errors",form.errors
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


def delete_plan(request, id):
    template_name = 'dashboard/plan-list.html'
    if SubscriptionPlan.objects.filter(id=id).exists():
        SubscriptionPlan.objects.get(id=id).delete()
        return redirect('/dashboard/plan-lists/')
    return render_to_response(template_name, context_instance=RequestContext(request))


class SubscriptionDetails(DetailView):
    template_name = 'dashboard/subscription-detail.html'
    model = UserSubscriptions

    def get_context_data(self, **kwargs):
        context = super(SubscriptionDetails, self).get_context_data(**kwargs)
        return context


class UserDetails(DetailView):
    template_name = 'dashboard/user-detail.html'
    model = UserProfiles


class CategoryLists(ListView):
    template_name = 'dashboard/category-list.html'
    model = Category


class CategoryAdd(TemplateView):
    template_name = 'dashboard/category-add.html'
    form_class = CategoryForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/category-lists/')
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


class EditCategory(TemplateView):
    template_name = 'dashboard/edit-category.html'
    form_class = CategoryForm

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(id=kwargs['id'])
        form = self.form_class(instance=category)
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(id=kwargs['id'])
        form = self.form_class(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/category-lists/')
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


def delete_view(request, id):
    template_name = 'dashboard/category-list.html'
    if Category.objects.filter(id=id).exists():
        Category.objects.get(id=id).delete()
        return redirect('/dashboard/category-lists/')
    return render_to_response(template_name, context_instance=RequestContext(request))


class TechnologyTagsList(ListView):
    template_name = 'dashboard/tech-tags-list.html'
    model = TechnologyTags


def delete_tag(request, id):
    template_name = 'dashboard/tech-tags-list.html'
    if TechnologyTags.objects.filter(id=id).exists():
        TechnologyTags.objects.get(id=id).delete()
        return redirect('/dashboard/technology-tags/')
    return render_to_response(template_name, context_instance=RequestContext(request))


class AddTag(TemplateView):
    template_name = 'dashboard/add-tag.html'
    form_class = TagForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/technology-tags/')
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

class EditTags(TemplateView):
    template_name = 'dashboard/edit-tags.html'
    form_class = TagForm

    def get(self, request, *args, **kwargs):
        tag = TechnologyTags.objects.get(id=kwargs['id'])
        form = self.form_class(instance=tag)
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        tag = TechnologyTags.objects.get(id=kwargs['id'])
        form = self.form_class(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/technology-tags/')
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


class PostLists(ListView):
    template_name = 'dashboard/post-lists.html'
    model = Posts


class PostDetail(DetailView):
    template_name = 'dashboard/post-detail.html'
    model = Posts


def admin_logout(request):
    logout(request)
    return redirect('/dashboard/')

class PaymentLists(ListView):
    template_name = 'dashboard/paypal-lists.html'
    model = PayPalIPN










from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
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
from apps.dashboard.forms import PlanForm, CategoryForm, TagForm, AboutForm, OurTemaForm, WebSiteContentsForm, \
    ContactForm
from django.template import loader
from django.conf import settings
from apps.payment.models import Payment


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

class About(TemplateView):
    template_name = 'dashboard/aboutus.html'
    form_class = AboutForm

    def get(self, request, *args, **kwargs):
        site = Site.objects.get(pk=1)
        if AboutUs.objects.filter(site=site).exists():
            about = AboutUs.objects.get(site=site)
            form = self.form_class(instance=about)
        else:
            form = self.form_class
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        site = Site.objects.get(pk=1)
        if AboutUs.objects.filter(site=site).exists():
            about = AboutUs.objects.get(site=site)
            form = self.form_class(request.POST, request.FILES, instance=about)
            if form.is_valid():
                form.save()
            else:
                print "error", form.errors
        else:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


def plan_status(request, id):
    template_name = 'dashboard/plan-list.html'
    plan = SubscriptionPlan.objects.get(id=id)
    if plan.active == True:
        plan.active = False
        plan.save()
        return redirect('/dashboard/plan-lists/')
    elif plan.active == False:
        plan.active = True
        plan.save()
        return redirect('/dashboard/plan-lists/')
    else:
        pass
    return render_to_response(template_name, context_instance=RequestContext(request))


def post_status(request, id):
    template_name = 'dashboard/post-lists.html'
    post = Posts.objects.get(id=id)
    if post.publish == True:
        post.publish = False
        post.save()
        return redirect('/dashboard/post-list/')
    elif post.publish == False:
        post.publish = True
        post.save()
        return redirect('/dashboard/post-list/')
    else:
        pass
    return render_to_response(template_name, context_instance=RequestContext(request))

class TeamLists(ListView):
    template_name = 'dashboard/team-lists.html'
    model = OurTema

class TeamMember(TemplateView):
    template_name = 'dashboard/add-team-member.html'
    form_class = OurTemaForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/team-lists/')
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


class MemberDetail(TemplateView):
    template_name = 'dashboard/member-detail.html'
    form_class = OurTemaForm

    def get(self, request, *args, **kwargs):
        member = OurTema.objects.get(id=kwargs['id'])
        form = self.form_class(instance=member)
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        member = OurTema.objects.get(id=kwargs['id'])
        form = self.form_class(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/team-lists/')
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


class WebContent(TemplateView):
    template_name = 'dashboard/web-content.html'
    form_class = WebSiteContentsForm

    def get(self, request, *args, **kwargs):
        site = Site.objects.get(pk=1)
        if WebSiteContents.objects.filter(site=site).exists():
            content = WebSiteContents.objects.get(site=site)
            form = self.form_class(instance=content)
        else:
            form = self.form_class()
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        site = Site.objects.get(pk=1)
        if WebSiteContents.objects.filter(site=site).exists():
            content = WebSiteContents.objects.get(site=site)
            form = self.form_class(request.POST, instance=content)
            if form.is_valid():
                form.save()
                return redirect('/dashboard/web-contents/')
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/dashboard/web-contents/')
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


class ContactData(TemplateView):
    template_name = 'dashboard/contact.html'
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        site = Site.objects.get(pk=1)
        if Contact.objects.filter(site=site).exists():
            content = Contact.objects.get(site=site)
            form = self.form_class(instance=content)
        else:
            form = self.form_class()
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))

    def post(self, request, *args, **kwargs):
        site = Site.objects.get(pk=1)
        if Contact.objects.filter(site=site).exists():
            content = Contact.objects.get(site=site)
            form = self.form_class(request.POST, instance=content)
            if form.is_valid():
                form.save()
                return redirect('/dashboard/contactus/')
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/dashboard/contactus/')
        return render_to_response(self.template_name, {'form': form}, context_instance=RequestContext(request))


class StatusChange(TemplateView):
    template_name = 'dashboard/status-change.html'

    def get(self, request, *args, **kwargs):
        request.session['type'] = request.GET.get('type')
        # if request.GET['type'] == 'user':
        #     user = User.objects.get(id=kwargs['id'])
        #     if user.is_active == True:
        #         user.is_active = False
        #         user.save()
        #         return redirect('/dashboard/user-profiles/')
        #     elif user.is_active == False:
        #         user.is_active = True
        #         user.save()
        #         return redirect('/dashboard/user-profiles/')
        #     else:
        #         pass
        # elif request.GET['type'] == 'post':
        #     post = Posts.objects.get(id=kwargs['id'])
        #     if post.publish == True:
        #         post.publish = False
        #         post.save()
        #         return redirect('/dashboard/post-list/')
        #     elif post.publish == False:
        #         post.publish = True
        #         post.save()
        #         return redirect('/dashboard/post-list/')
        #     else:
        #         pass
        # else:
        #     pass
        return render_to_response(self.template_name, context_instance=RequestContext(request))


    def post(self, request, *args, **kwargs):
        print "request", request.session['type']
        if request.session['type'] == 'user':
            user = User.objects.get(id=kwargs['id'])
            if user.is_active == True:
                user.is_active = False
                user.save()
                type = 'disabled'
                t = loader.get_template('accounts/deactivate')
                user = UserProfiles.objects.get(user=user)
                site = Site.objects.get(pk=1)
                reason = request.POST.get('reason')
                c = Context({'name': user.user.first_name, 'email': user.user.email, 'site': site.name,
                             'token': user.token, 'type': type, 'reason': reason})
                send_mail('[%s] %s' % (site.name, 'Account Disabled'), t.render(c), settings.DEFAULT_FROM_EMAIL,
                          [user.user.email], fail_silently=False)
                return redirect('/dashboard/user-profiles/')
            elif user.is_active == False:
                user.is_active = True
                user.save()
                type = 'enabled'
                reason = request.POST.get('reason')
                t = loader.get_template('accounts/deactivate')
                user = UserProfiles.objects.get(user=user)
                site = Site.objects.get(pk=1)
                c = Context({'name': user.user.first_name, 'email': user.user.email, 'site': site.name,
                             'token': user.token, 'type': type, 'reason': reason})
                send_mail('[%s] %s' % (site.name, 'Account Enabled'), t.render(c), settings.DEFAULT_FROM_EMAIL,
                          [user.user.email], fail_silently=False)
                return redirect('/dashboard/user-profiles/')
            else:
                pass
        elif request.session['type'] == 'post':
            post = Posts.objects.get(id=kwargs['id'])
            if post.publish == True:
                post.publish = False
                post.save()
                type = 'deactivated'
                t = loader.get_template('accounts/post_status')
                site = Site.objects.get(pk=1)
                reason = request.POST.get('reason')
                c = Context({'name': post.user.first_name, 'email': post.user.email, 'site': site.name,
                             'type': type, 'reason': reason})
                send_mail('[%s] %s' % (site.name, 'Post disabled'), t.render(c), settings.DEFAULT_FROM_EMAIL,
                          [post.user.email], fail_silently=False)
                return redirect('/dashboard/post-list/')
            elif post.publish == False:
                post.publish = True
                post.save()
                t = loader.get_template('accounts/post_status')
                type = 'activated'
                reason = request.POST.get('reason')
                site = Site.objects.get(pk=1)
                c = Context({'name': post.user.first_name, 'email': post.user.email, 'site': site.name,
                             'type': type, 'reason': reason})
                send_mail('[%s] %s' % (site.name, 'Post Enabled'), t.render(c), settings.DEFAULT_FROM_EMAIL,
                          [post.user.email], fail_silently=False)
                return redirect('/dashboard/post-list/')
            else:
                pass
        else:
            pass
        return render_to_response(self.template_name, context_instance=RequestContext(request))


import csv
class GenerateReport(TemplateView):
    template_name = 'dashboard/adminindex.html'

    def get(self, request):
        if request.GET.get('type') == 'daily':
            with open('DailyReport.csv', 'w') as csvfile:
                payments = Payment.objects.filter(date=datetime.date.today())
                fieldnames = ["User", "Plan", "Payment Type", "Amount", "Date"]
                doc = csv.DictWriter(csvfile, fieldnames=fieldnames)
                doc.writeheader()
                for pay in payments:
                    doc.writerow({'User': pay.user, 'Plan': pay.plan, "Payment Type": pay.get_payment_type_display(),
                                  'Amount': pay.amount, 'Date': pay.date})
            return redirect('/dashboard/home/')
        elif request.GET.get('type') == 'monthly':
            payments = Payment.objects.filter(date__month=datetime.datetime.now().month)
            with open('MonthlyReport.csv', 'w') as csvfile:
                payments = Payment.objects.filter(date=datetime.date.today())
                fieldnames = ["User", "Plan", "Payment Type", "Amount", "Date"]
                doc = csv.DictWriter(csvfile, fieldnames=fieldnames)
                doc.writeheader()
                for pay in payments:
                    doc.writerow({'User': pay.user, 'Plan': pay.plan, "Payment Type": pay.get_payment_type_display(),
                                  'Amount': pay.amount, 'Date': pay.date})
            return redirect('/dashboard/home/')
        else:
            pass
        return render_to_response(self.template_name, context_instance=RequestContext(request))









